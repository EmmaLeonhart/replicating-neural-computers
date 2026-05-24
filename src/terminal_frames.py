"""Render synthetic terminal frames for the Wan2.1 VAE reconstruction test.

This reproduces the *input* side of Experiment 1 (Table tab:cli-vae-recon in
arXiv:2604.06425): terminal screenshots at a chosen monospace font size. The
paper's claim is a property of the pretrained Wan2.1 VAE on terminal content, so
we only need representative terminal frames — not the (unreleased) CLIGen corpus.

Frames are dark-background terminals with ANSI-style coloured spans (prompts,
commands, output, logs, code, errors, tables), rendered at a fixed font size on a
fixed canvas whose dimensions are multiples of 8 (the Wan VAE spatial stride).
Each "clip" is a few frames of an otherwise-static screen with a blinking cursor,
matching how a near-idle terminal looks in a short video window.

Deterministic: a fixed seed makes the rendered corpus reproducible across runs.
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Terminal palette (Windows Terminal "Campbell"-ish on a near-black background).
BG = (12, 12, 12)
FG = (204, 204, 204)
COLORS = {
    "fg": FG,
    "green": (35, 209, 139),
    "red": (231, 72, 86),
    "yellow": (229, 229, 16),
    "blue": (59, 142, 234),
    "cyan": (41, 184, 219),
    "magenta": (180, 0, 158),
    "gray": (118, 118, 118),
    "white": (242, 242, 242),
}

def _mpl_mono() -> str | None:
    """Path to matplotlib's bundled DejaVu Sans Mono, if matplotlib is present."""
    try:
        import matplotlib
        return os.path.join(
            os.path.dirname(matplotlib.__file__),
            "mpl-data", "fonts", "ttf", "DejaVuSansMono.ttf",
        )
    except Exception:
        return None


def font_candidates() -> list[str]:
    # Portable first (bundled with matplotlib), Consolas as a Windows fallback.
    return [
        p for p in (
            _mpl_mono(),
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\cour.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ) if p
    ]


def find_font(size: int) -> ImageFont.FreeTypeFont:
    for path in font_candidates():
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError("No monospace TTF found (DejaVuSansMono / Consolas).")


# ---- A pool of representative terminal lines: list of (text, color) spans. ----
def _line(*spans):
    return list(spans)


def line_pool():
    p = "root@NeuralComputer"
    return [
        _line((f"{p}:~# ", "green"), ("ls -l --color=auto", "fg")),
        _line(("total 48", "gray")),
        _line(("drwxr-xr-x 2 root root 4096 Apr 16 13:48 ", "fg"), ("assets", "blue")),
        _line(("-rw-r--r-- 1 root root 7578 Apr 16 13:48 NC.tex", "fg")),
        _line(("-rwxr-xr-x 1 root root 1102 Apr 16 13:48 ", "fg"), ("run.sh", "green")),
        _line((f"{p}:~# ", "green"), ("python", "fg")),
        _line(("Python 3.13.3 (main) [GCC 13.2.0] on linux", "gray")),
        _line((">>> ", "yellow"), ("values = [n*n for n in range(1, 10)]", "fg")),
        _line((">>> ", "yellow"), ("print(values)", "fg")),
        _line(("[1, 4, 9, 16, 25, 36, 49, 64, 81]", "cyan")),
        _line((f"{p}:~# ", "green"), ("apt-get install -y ffmpeg", "fg")),
        _line(("Reading package lists... ", "fg"), ("Done", "green")),
        _line(("Building dependency tree... ", "fg"), ("Done", "green")),
        _line(("Get:1 http://deb.debian.org bookworm/main amd64 ffmpeg [1,492 kB]", "fg")),
        _line(("Fetched 1,492 kB in 1s (1,403 kB/s)", "gray")),
        _line(("Setting up ffmpeg (7:5.1.6-0) ", "fg"), ("...", "gray")),
        _line((f"{p}:~# ", "green"), ("git status", "fg")),
        _line(("On branch ", "fg"), ("main", "green")),
        _line(("Changes not staged for commit:", "fg")),
        _line(("  modified:   ", "red"), ("src/wan_vae_recon.py", "red")),
        _line(("  modified:   ", "red"), ("scripts/run.py", "red")),
        _line((f"{p}:~# ", "green"), ("pytest -q", "fg")),
        _line(("....F..                                       [100%]", "fg")),
        _line(("FAILED test_recon.py::test_psnr - AssertionError", "red")),
        _line(("Traceback (most recent call last):", "red")),
        _line(('  File "run.py", line 42, in <module>', "fg")),
        _line(("    raise ValueError(\"bad shape\")", "yellow")),
        _line(("ValueError: bad shape", "red")),
        _line((f"{p}:~# ", "green"), ("nvidia-smi --query-gpu=name --format=csv", "fg")),
        _line(("name", "gray")),
        _line(("NVIDIA GeForce RTX 4070 Laptop GPU", "white")),
        _line(("Progress |", "fg"), ("############------", "green"), ("| 67% 1.2GB/s", "fg")),
    ]


@dataclass
class RenderConfig:
    width: int = 832          # multiple of 8 (Wan VAE spatial stride); 480p landscape
    height: int = 480         # multiple of 8
    font_px: int = 13
    frames: int = 5           # T = 4k+1 not required at T<=5; min(T) handled downstream
    margin: int = 6
    seed: int = 0
    density: float = 0.5      # fraction of available rows filled with text (rest BG)
    # A real terminal screenshot is mostly uniform background with a handful of
    # text rows; density controls that. The VAE reconstructs background near-
    # perfectly, so PSNR/SSIM rise as density falls (see FINDINGS.md sweep).


def render_clip(cfg: RenderConfig, screen_lines) -> list[np.ndarray]:
    """Render one clip (list of HxWx3 uint8 frames) with a blinking cursor.

    Only the first `density` fraction of available rows is filled with text
    (top-aligned), leaving the rest as background — mimicking a real session.
    """
    font = find_font(cfg.font_px)
    # Monospace cell metrics.
    cell_w = font.getlength("M")
    ascent, descent = font.getmetrics()
    line_h = ascent + descent + max(1, cfg.font_px // 6)

    avail_rows = max(1, (cfg.height - 2 * cfg.margin) // line_h)
    n_lines = max(1, min(len(screen_lines), round(avail_rows * cfg.density)))

    frames = []
    for t in range(cfg.frames):
        img = Image.new("RGB", (cfg.width, cfg.height), BG)
        draw = ImageDraw.Draw(img)
        y = cfg.margin
        last_x = cfg.margin
        for spans in screen_lines[:n_lines]:
            if y + line_h > cfg.height - cfg.margin:
                break
            x = cfg.margin
            for text, color in spans:
                draw.text((x, y), text, font=font, fill=COLORS[color])
                x += int(round(cell_w * len(text)))
            last_x = x
            y += line_h
        # Blinking block cursor at the end of the last drawn prompt line.
        if t % 2 == 0:
            cy = y - line_h
            draw.rectangle(
                [last_x, cy, last_x + int(cell_w), cy + ascent + descent],
                fill=FG,
            )
        frames.append(np.asarray(img, dtype=np.uint8))
    return frames


def build_corpus(num_samples: int, cfg: RenderConfig):
    """Build `num_samples` distinct terminal clips, deterministically.

    Each clip uses a rotated/shuffled window of the line pool so screens differ
    while staying representative of real terminal content.
    """
    rng = random.Random(cfg.seed)
    pool = line_pool()
    clips = []
    for i in range(num_samples):
        lines = pool[:]
        rng.shuffle(lines)
        offset = (i * 5) % len(lines)
        screen = lines[offset:] + lines[:offset]
        clips.append(render_clip(cfg, screen))
    return clips


if __name__ == "__main__":
    # Quick visual smoke test: dump one frame per font size.
    os.makedirs("results", exist_ok=True)
    for fp in (13, 6):
        cfg = RenderConfig(font_px=fp)
        clip = build_corpus(1, cfg)[0]
        Image.fromarray(clip[0]).save(f"results/_smoke_term_{fp}px.png")
        print(f"wrote results/_smoke_term_{fp}px.png  ({clip[0].shape})")
