"""Round-trip terminal frames through the pretrained Wan2.1 VAE and score them.

Reproduces Experiment 1 (Table tab:cli-vae-recon, arXiv:2604.06425): the paper
applies the *off-the-shelf* Wan2.1 VAE to terminal content and reports
PSNR/SSIM, finding ~40.77 dB / 0.989 at 13 px and degradation at 6 px. No
NC-specific training is involved, so the public Wan2.1 VAE is the exact model.

We encode each clip with the VAE, decode it back, and compute per-frame PSNR/SSIM
against the input. The encode->decode round trip uses the raw posterior mode; the
diffusion-space latents_mean/std normalisation is *not* applied (that scaling is
for the denoiser, and cancels in a plain reconstruction).
"""
from __future__ import annotations

import numpy as np
import torch
from diffusers import AutoencoderKLWan
from skimage.metrics import peak_signal_noise_ratio as sk_psnr
from skimage.metrics import structural_similarity as sk_ssim

# Public Wan2.1 weights on HuggingFace. The VAE is shared across the T2V family;
# the 1.3B repo is the smallest download that carries the same VAE subfolder.
DEFAULT_MODEL = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"


def load_vae(model: str = DEFAULT_MODEL, device: str = "cuda",
             dtype: torch.dtype = torch.float32) -> AutoencoderKLWan:
    vae = AutoencoderKLWan.from_pretrained(model, subfolder="vae", torch_dtype=dtype)
    vae.to(device).eval()
    # Tiling/slicing keep peak VRAM low enough for an 8 GB card.
    for fn in ("enable_tiling", "enable_slicing"):
        try:
            getattr(vae, fn)()
        except Exception:
            pass
    return vae


@torch.no_grad()
def reconstruct_clip(vae: AutoencoderKLWan, frames_uint8: list[np.ndarray],
                     device: str, dtype: torch.dtype):
    """frames_uint8: list of HxWx3 uint8. Returns (orig01, recon01) as T,H,W,3."""
    arr = np.stack(frames_uint8).astype(np.float32) / 255.0      # T,H,W,3 in [0,1]
    x = torch.from_numpy(arr).permute(3, 0, 1, 2).unsqueeze(0)   # 1,3,T,H,W
    x = (x * 2.0 - 1.0).to(device=device, dtype=dtype)           # -> [-1,1]

    posterior = vae.encode(x).latent_dist
    z = posterior.mode()
    dec = vae.decode(z).sample                                   # 1,3,T,H,W in [-1,1]

    rec = ((dec.float().clamp(-1, 1) + 1.0) / 2.0).cpu().numpy()[0]  # 3,T,H,W
    rec = np.transpose(rec, (1, 2, 3, 0))                            # T,H,W,3
    # Causal VAE should preserve T; guard against any off-by-one anyway.
    t = min(arr.shape[0], rec.shape[0])
    return arr[:t], rec[:t]


def frame_metrics(orig01: np.ndarray, recon01: np.ndarray):
    """Per-frame PSNR (dB) and SSIM for matched T,H,W,3 arrays in [0,1]."""
    psnrs, ssims = [], []
    for o, r in zip(orig01, recon01):
        psnrs.append(float(sk_psnr(o, r, data_range=1.0)))
        ssims.append(float(sk_ssim(o, r, data_range=1.0, channel_axis=-1)))
    return psnrs, ssims
