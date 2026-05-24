# Claims inventory — "Neural Computers" (arXiv:2604.06425)

Queue items 6 & 7. Scope: every headline number, the compute envelope (decides
CI-runnability), datasets, and reference checks. What we actually reproduced is
in `FINDINGS.md`; this is the full map of what the paper claims.

The paper is a **position + empirical** paper. It defines "Neural Computers"
(NCs) — video models that act as a learned computer runtime — and ships two
prototypes built on **Wan2.1** (I2V): **CLIGen** (terminal) and **GUIWorld**
(desktop GUI). All numbers below are *ablation/diagnostic* results on the
authors' unreleased corpora; there is no single accuracy "headline."

## Compute envelope → NOT CI-runnable

| Component | Reported compute |
|---|---|
| CLIGen (General) training | ~15,000 H100 GPU-hours, batch size 1 (`impl_cli.tex:140`) |
| CLIGen (Clean) training (both subsets) | ~7,000 H100 GPU-hours (`impl_cli.tex:141`) |
| GUIWorld, per full pass | ~23,000 GPU-hours = 64 GPUs × ~15 days (`impl_gui.tex:163`) |
| GUIWorld ablations | one model **per** injection mode (×4) + encoders → many passes |

Total is well into the **10⁵ H100-GPU-hour** range. The `SKILL.md` guardrail
trips at ~4 GPU-hours on one consumer GPU, so this is marked
`ci_runnable: false` / `not_runnable` in `paper.json`. None of the *trained-model*
numbers are reproducible here.

## CLI (CLIGen) claims

| # | Table/Fig | Claim (reported value) | Reproducible here? |
|---|---|---|---|
| 1 | `tab:cli-vae-recon` | **Pretrained Wan2.1 VAE** reconstructs 13px terminal frames at **40.77 dB PSNR / 0.989 SSIM**; degrades at 6px (text blurs, global metrics stay high) | **YES** — public VAE, no training. **This is what we reproduce.** |
| 2 | `fig:cligen-long-train` | PSNR/SSIM plateau ~25k steps (up to 460k); can slightly degrade later | No — needs NC training (~7k H100-h) |
| 3 | `tab:cligen-captions` | Caption specificity ↑ fidelity: Semantic 21.90/0.813 → Regular 23.63/0.843 → Detailed 26.89/0.867 | No — trained NC + unreleased captioned data |
| 4 | `tab:cligen-ocr` | OCR char-acc 0.03→0.54 and exact-line 0.01→0.31 over 0–60k steps (Tesseract) | No — needs trained NC; protocol is reproducible (`appendix_pipeline.tex:75`) |
| 5 | `tab:cligen-arith` | Arithmetic probe: Wan2.1 0%, NC 4%, Veo3.1 2%, **Sora2 71%** (100 of 1,000 held-out) | No — trained NC + **proprietary** Sora2/Veo3.1 |
| 6 | `fig:cligen-exp6` | Reprompting lifts arithmetic 4%→83% (no backbone change / RL) | No — trained NC |

## GUI (GUIWorld) claims

| # | Table | Claim (reported value) | Reproducible here? |
|---|---|---|---|
| 7 | `tab:gui-data-quality` | Data quality > size: Claude-CUA (110h) beats Random Slow/Fast (~1,400h). FVD 149.6→14.7, SSIM 0.496→0.885 | No — trained NC + unreleased GUI corpus |
| 8 | `tab:cursor-loss` | Cursor accuracy: coords 8.7% → +Fourier 13.5% → **+SVG mask/ref 98.7%** | No — trained NC |
| 9 | `tab:gui-action-ssim` | Injection depth: `external` SSIM₊₁₅ 0.746 → `contextual` 0.813 → `residual` 0.857 → `internal` 0.863; FVD₊₁₅ 33.4→14.5 | No — trained NC (×4 passes) |
| 10 | `tab:gui-encoding-ablation` | meta-action ≳ raw-action under `internal` (SSIM 0.847→0.863) | No — trained NC |

Metric definitions (FVD via r3d18, SSIM/LPIPS via torchmetrics/AlexNet, +15-frame
action windows) are fully specified in `appendix_pipeline.tex:122-159` — so the
*evaluation suite* is reproducible even though the *models* are not.

## Datasets (none released as a downloadable corpus)

- **CLIGen (General):** public asciinema `.cast` archives → replay → frames.
  ~823,989 streams (~1,100h), 15 FPS, captions by Llama-3.1-70B in 3 tiers.
- **CLIGen (Clean):** authored `vhs` scripts, Dockerized. ~250k scripts, 51.21%
  retained → ~78k regular + ~50k Python-math traces.
- **GUIWorld:** NeuralOS-style XFCE capture rig (Ubuntu 22.04, 1024×768, 15 FPS).
  ~1,000h Random Slow + ~400h Random Fast + ~110h Claude-CUA supervised.

Raw *tools* are public (asciinema/agg, vhs, ffmpeg); the *curated corpora* and
"released configs" are referenced but **not linked anywhere** in the source.

## Reference checks (queue item 6 — all verified real)

- **Wan2.1** `wan2025wan` = "Wan: Open and advanced large-scale video generative
  models," arXiv:2503.20314. Real; weights public on HuggingFace
  (`Wan-AI/Wan2.1-*`). The **backbone**, and the source of the VAE we run. ✓
- **NeuralOS** `rivard2025neuralos` = arXiv:2507.08800. The load-bearing claim
  Experiment 1 tests against: "generic natural-image VAEs can perform poorly on
  structured computer screenshots." The paper *pushes back* — finding the Wan2.1
  VAE adequate at 13px. Our run supports the paper's side (high SSIM). ✓
- **Sora 2** `openai_sora2_2025` (OpenAI, 2025-09-30) and **Veo 3.1**
  `google_veo3_1_2025` (Google, 2025-11) = real, **proprietary/gated** product
  pages — used as arithmetic-probe baselines, not reproducible. ✓
- CLIP `radford2021learning`, T5 `raffel2020exploring`, Llama-3 `dubey2024llama`
  = real, standard, used for conditioning/captioning. ✓

No reference appears mis-cited or to overstate what the cited work says.
