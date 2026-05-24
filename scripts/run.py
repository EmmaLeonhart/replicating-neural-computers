"""Replication entry point: Wan2.1 VAE terminal-reconstruction (Experiment 1).

Reproduces the one headline number from "Neural Computers" (arXiv:2604.06425)
that needs only public, pretrained components — Table tab:cli-vae-recon:

    "At 13 px, reconstruction quality is high (40.77 dB PSNR, 0.989 SSIM).
     At 6 px, text exhibits noticeable blurring even when global PSNR/SSIM
     remain strong, because background regions dominate these metrics."

Everything else in the paper requires the unreleased CLIGen/GUIWorld corpora and
tens of thousands of H100 GPU-hours; see FINDINGS.md / notes/claims.md.

Usage:
    python scripts/run.py                      # defaults: 13px & 6px, GPU if present
    python scripts/run.py --num-samples 16
    python scripts/run.py --device cpu --num-samples 2
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import torch
from PIL import Image

# Make src/ importable whether run from repo root or elsewhere.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from terminal_frames import RenderConfig, build_corpus              # noqa: E402
from wan_vae_recon import (DEFAULT_MODEL, load_vae, reconstruct_clip,  # noqa: E402
                           frame_metrics)

# Paper's reported values (Table tab:cli-vae-recon), keyed by font size in px.
PAPER_REF = {13: {"psnr": 40.77, "ssim": 0.989}}


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--font-sizes", default="13,6",
                    help="comma-separated font sizes in px (default: 13,6)")
    ap.add_argument("--densities", default="1.0,0.5,0.25",
                    help="comma-separated content densities, fraction of rows "
                         "filled with text (default: 1.0,0.5,0.25)")
    ap.add_argument("--num-samples", type=int, default=8,
                    help="terminal clips rendered per (font,density) (default: 8)")
    ap.add_argument("--frames", type=int, default=5,
                    help="frames per clip (default: 5)")
    ap.add_argument("--width", type=int, default=832)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "vae_recon.json"))
    ap.add_argument("--save-compare", action="store_true", default=True,
                    help="save an original-vs-recon strip per font size")
    return ap.parse_args()


def pick_device(choice: str) -> str:
    if choice == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return choice


def save_compare(path, orig01, recon01):
    """Save a vertical original/reconstruction strip of the first frame."""
    o = (orig01[0] * 255).round().astype(np.uint8)
    r = (recon01[0] * 255).round().astype(np.uint8)
    gap = np.full((8, o.shape[1], 3), 32, dtype=np.uint8)
    strip = np.concatenate([o, gap, r], axis=0)
    Image.fromarray(strip).save(path)


def main():
    args = parse_args()
    device = pick_device(args.device)
    dtype = torch.float32
    font_sizes = [int(s) for s in args.font_sizes.split(",") if s.strip()]
    densities = [float(s) for s in args.densities.split(",") if s.strip()]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    print(f"[run] model={args.model}")
    print(f"[run] device={device} dtype={dtype} font_sizes={font_sizes} "
          f"densities={densities} num_samples={args.num_samples} "
          f"frames={args.frames} res={args.width}x{args.height}")

    t_load = time.time()
    vae = load_vae(args.model, device=device, dtype=dtype)
    print(f"[run] VAE loaded in {time.time() - t_load:.1f}s")

    sweep = []
    saved = set()  # (fp) -> only save one comparison image per font size
    print(f"[run] {'font':>4} {'dens':>5} {'PSNR(dB)':>9} {'SSIM':>8}  frames")
    for fp in font_sizes:
        for dens in densities:
            cfg = RenderConfig(width=args.width, height=args.height, font_px=fp,
                               frames=args.frames, seed=0, density=dens)
            clips = build_corpus(args.num_samples, cfg)
            psnrs, ssims = [], []
            first = None
            t0 = time.time()
            for clip in clips:
                orig01, recon01 = reconstruct_clip(vae, clip, device, dtype)
                p, s = frame_metrics(orig01, recon01)
                psnrs.extend(p)
                ssims.extend(s)
                if first is None:
                    first = (orig01, recon01)
            dt = time.time() - t0
            entry = {
                "font_px": fp,
                "density": dens,
                "n_frames": len(psnrs),
                "psnr_mean": float(np.mean(psnrs)),
                "psnr_std": float(np.std(psnrs)),
                "ssim_mean": float(np.mean(ssims)),
                "ssim_std": float(np.std(ssims)),
                "seconds": round(dt, 1),
            }
            sweep.append(entry)
            print(f"[run] {fp:>3}px {dens:>5.2f} {entry['psnr_mean']:8.2f}  "
                  f"{entry['ssim_mean']:7.4f}  [{len(psnrs)}f {dt:.0f}s]")
            # Save one orig-vs-recon strip per font size (at the sparsest density,
            # the realistic case) so the report can show 13px sharp vs 6px blur.
            if args.save_compare and first is not None and \
                    fp not in saved and dens == min(densities):
                cmp_path = os.path.join(os.path.dirname(args.out),
                                        f"compare_{fp}px.png")
                save_compare(cmp_path, *first)
                saved.add(fp)

    out = {
        "experiment": "Wan2.1 VAE terminal-frame reconstruction (Exp. 1)",
        "paper": "arXiv:2604.06425, Table tab:cli-vae-recon",
        "model": args.model,
        "device": device,
        "dtype": str(dtype),
        "config": {
            "font_sizes": font_sizes,
            "densities": densities,
            "num_samples": args.num_samples,
            "frames": args.frames,
            "width": args.width,
            "height": args.height,
        },
        "paper_reference": PAPER_REF,
        "sweep": sweep,
        "torch": torch.__version__,
        "cuda_device": (torch.cuda.get_device_name(0)
                        if torch.cuda.is_available() else None),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"[run] wrote {args.out}")


if __name__ == "__main__":
    main()
