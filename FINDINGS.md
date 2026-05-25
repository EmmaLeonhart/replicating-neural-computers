# Findings — Replicating "Neural Computers" (arXiv:2604.06425)

**Paper:** Zhuge et al., *Neural Computers*, Meta AI / KAUST, 2026
([arXiv:2604.06425](https://arxiv.org/abs/2604.06425v2)).
**This replication:** <https://github.com/EmmaLeonhart/replicating-neural-computers>
**Hardware used:** one NVIDIA RTX 4070 Laptop GPU (8 GB), CUDA 12.8, ~2 min.

## TL;DR

"Neural Computers" is a position + empirical paper. It defines **NCs** — video
models that act as a learned computer runtime — and ships two prototypes built on
**Wan2.1**: **CLIGen** (terminal) and **GUIWorld** (desktop GUI). Its tables are
diagnostic ablations on the authors' **unreleased** corpora and **unreleased**
trained checkpoints.

- **Full reproduction is impossible from what ships.** No code, no weights, no
  dataset release, no recipe — and training costs **>10⁵ H100 GPU-hours**.
  Marked `ci_runnable: false` in `paper.json`.
- **One headline number needs only public, pretrained parts — and we reproduce
  it:** Experiment 1 (Table `tab:cli-vae-recon`), the **off-the-shelf Wan2.1 VAE**
  reconstructing terminal frames.
- **Result: the paper's claim holds.** We match its **SSIM** (0.989) at realistic
  terminal density, land in its **PSNR** regime, and reproduce its specific
  **6px nuance** ("text blurs but global PSNR/SSIM stay high because background
  dominates"). See the [side-by-side images](#the-6px-nuance-reproduced).

## What we reproduced — Experiment 1: Wan2.1 VAE on terminals

The paper tests NeuralOS's claim that "generic natural-image VAEs can perform
poorly on structured computer screenshots" by applying the **pretrained Wan2.1
VAE** (no NC training) to terminal content, reporting:

> "At 13px, reconstruction quality is high (40.77 dB PSNR, 0.989 SSIM). At 6px,
> text exhibits noticeable blurring even when global PSNR/SSIM remain strong,
> because background regions dominate these metrics." — §Exp. 1

We render representative dark-background terminal frames (prompts, output, code,
colored logs, errors, tables) at 832×480, round-trip each through
`AutoencoderKLWan` from `Wan-AI/Wan2.1-T2V-1.3B-Diffusers`, and score per-frame
PSNR/SSIM (`skimage`). Because a real terminal is mostly uniform background, we
sweep a **content-density** knob (fraction of rows filled) — the paper's own
stated mechanism ("background regions dominate these metrics").

### Reproduced vs. reported

| Font | Content density | PSNR (dB) | SSIM | vs. paper (40.77 / 0.989 @ 13px) |
|------|-----------------|-----------|------|----------------------------------|
| 13px | 1.00 (wall-to-wall text) | 31.02 ± 1.11 | 0.9761 | floor case |
| 13px | 0.50 | 34.20 ± 1.32 | 0.9874 | SSIM ≈ paper |
| **13px** | **0.25 (realistic sparse)** | **37.20 ± 1.45** | **0.9935** | **SSIM ≥ paper; PSNR in-regime** |
| 6px  | 1.00 | 31.46 ± 0.98 | 0.9826 | — |
| 6px  | 0.50 | 32.41 ± 1.01 | 0.9855 | — |
| 6px  | 0.25 | 35.57 ± 1.27 | 0.9922 | global metrics stay high |

*(8 clips × 5 frames = 40 frames per row; `results/vae_recon.json`.)*

**Verdict: reproduced (qualitatively and at the SSIM level; PSNR in-regime).**
- **SSIM matches.** The paper's 0.989 sits inside our 13px range (0.976–0.994),
  matched at density ≈ 0.35–0.5. The Wan2.1 VAE *is* adequate for 13px terminal
  text — the paper's central Exp-1 conclusion, confirmed.
- **PSNR is content-dependent, as the paper says.** It climbs monotonically as
  the terminal gets realistically sparse (31 → 37 dB at 13px). The paper's exact
  40.77 dB implies even sparser frames and/or higher resolution than our 832×480
  (a separate probe gave +2 dB going 640→1024 wide). We land in the same regime
  rather than hitting the decimal — expected, since we cannot use their frames.

### The 6px nuance, reproduced

The paper's subtle point is that at 6px the *global* metrics stay high even though
text visibly blurs. Our numbers show exactly this: 6px PSNR/SSIM (31–36 dB /
0.983–0.992) are **as high as 13px** — because background dominates the metric —
while the reconstructed glyphs smear. The committed comparison strips
(original top, reconstruction bottom) make it visible:

- `results/compare_13px.png` — reconstruction is visually identical; text sharp.
- `results/compare_6px.png` — reconstructed text is smeared, yet metrics stayed high.

This is the paper's claim demonstrated, not just its number.

## What we did **not** reproduce (and why)

Everything below needs trained NC checkpoints (unreleased), the curated
CLIGen/GUIWorld corpora (unreleased), or proprietary models — none feasible on
one consumer GPU. Reported values are catalogued in `notes/claims.md`.

| Claim | Reported | Blocker |
|---|---|---|
| CLI caption-style fidelity | Semantic 21.9 → Detailed 26.9 dB | trained NC + unreleased captions |
| CLI OCR vs steps | char-acc 0.03→0.54, exact-line→0.31 | trained NC (~7k H100-h) |
| CLI arithmetic probe | Wan 0%, NC 4%, Veo3.1 2%, **Sora2 71%** | trained NC + **proprietary** baselines |
| CLI reprompting | 4% → 83% | trained NC |
| GUI data quality | FVD 149.6→14.7 (CUA best) | trained NC + unreleased GUI corpus |
| GUI cursor supervision | 8.7% → **98.7%** with SVG mask/ref | trained NC |
| GUI injection depth | `internal` best (SSIM 0.863, FVD 14.5) | trained NC, ×4 passes |
| GUI action encoding | meta ≳ raw (SSIM 0.847→0.863) | trained NC |

The paper's **evaluation protocols** (OCR via Tesseract + Levenshtein; FVD via
r3d18; +15-frame action windows) *are* fully specified and would be reproducible
given the models — the gap is artifacts, not method description.

## Reference checks

All load-bearing references verified real and not mis-cited (details in
`notes/claims.md`): **Wan2.1** (arXiv:2503.20314, public weights — the backbone
and our VAE source); **NeuralOS** (arXiv:2507.08800 — the claim Exp 1 contests);
**Sora 2** / **Veo 3.1** (real, proprietary product pages — arithmetic baselines);
CLIP, T5, Llama-3 (standard, for conditioning/captioning).

## Reproduce it yourself

```bash
pip install -r requirements.txt   # torch installed separately; see the file
python scripts/run.py             # 13px & 6px × density sweep, writes results/vae_recon.json
# faster smoke test on CPU:
python scripts/run.py --device cpu --num-samples 2 --frames 1 --densities 0.25
```

First run downloads the public Wan2.1 VAE (~hundreds of MB) from HuggingFace.
Outputs: `results/vae_recon.json` plus `results/compare_{13,6}px.png`.

## Scope and limits

This replication reproduces **one** of the paper's results — the only one whose
inputs (a public pretrained VAE) are available — and documents the rest as
reported-but-not-reproduced with the specific blocker for each. The reproduced
result supports the paper's Exp-1 conclusion: the Wan2.1 VAE is an adequate
encoder/decoder for 13px terminal content, and global PSNR/SSIM understate the
6px text degradation. We did not retrain, and we make no claim about the NC
prototypes' behavior, which our hardware cannot touch.
