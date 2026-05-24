# replicating-neural-computers — Devlog

**This file is where "done" lives.** `queue.md` is delete-only: when a queue
item is finished, the item is **deleted from `queue.md`** and a dated entry
is **appended here**, in the same commit as the work, then pushed. Never
tick a box in place — a checked box left in `queue.md` is the failure mode
this file exists to prevent.

Also record releases (tag + a one-line note), notable milestones, and
anything else worth a chronological trail. Newest entries at the bottom.

This is the **same convention as the cleanvibe repo's own `devlog.md`** —
every cleanvibe-scaffolded project gets one for the same reason.

See `CLAUDE.md` § "Workflow Rules" and `queue.md`'s preamble.

---

## 2026-05-24 — Project scaffolded

Scaffolded with `cleanvibe new` (cleanvibe v1.9.1). Future entries
land here as queue items get deleted.

## 2026-05-24 — Source read; no recipe; repo live (queue 1–4)

- Got explicit user consent to run third-party code (the pretrained Wan2.1 VAE),
  to target the "VAE slice + full analysis" scope, and to go public now.
- Read the e-print source (`replication_target/source/`). It is **paper LaTeX
  only** — no authors' code. Searched the whole `.tex` tree for recipe markers
  (`reproduc`/`replicat`/`github.com`/`huggingface`/`SKILL`/zip/weights):
  **no reproduction recipe, no code repo, no released weights/data, no zip.**
  Only a blogpost URL and unlinked "released configs." Recorded in
  `notes/sources.md`.
- **Went live:** created the PUBLIC repo and pushed →
  <https://github.com/EmmaLeonhart/replicating-neural-computers>.

## 2026-05-24 — Claims audit + references; marked not CI-runnable (queue 6–7)

- Catalogued every headline number (6 CLI + 4 GUI tables) in `notes/claims.md`
  with the blocker for each. Compute envelope is **>10⁵ H100 GPU-hours**
  (CLIGen ~15k+7k, GUIWorld ~23k/pass × ablations), datasets and checkpoints
  unreleased, arithmetic baselines (Sora2/Veo3.1) proprietary.
- Verified all load-bearing references (Wan2.1, NeuralOS, Sora2, Veo3.1, CLIP,
  T5, Llama-3) are real and not mis-cited.
- Marked `ci_runnable: false` in `paper.json` with reason + the reproducible
  slice (per the `SKILL.md` ~4 GPU-hour guardrail).

## 2026-05-24 — Reproduced Experiment 1: Wan2.1 VAE terminal reconstruction (queue 5,8,9,10)

- **First reproduced number.** Built `src/terminal_frames.py` (renders dark
  terminal frames at a chosen font size + content density),
  `src/wan_vae_recon.py` (round-trips clips through public `AutoencoderKLWan`
  and scores PSNR/SSIM), and `scripts/run.py` (CI entry point; sweeps font ×
  density). Pinned env in `requirements.txt`.
- Ran on an RTX 4070 (8 GB) in ~2 min. **Result matches the paper's Exp-1
  claim:** SSIM hits the paper's 0.989 at realistic terminal density (13px:
  0.976→0.994 over density 1.0→0.25), PSNR lands in-regime (31→37 dB; paper
  40.77), and the **6px nuance reproduces** — global PSNR/SSIM stay as high as
  13px while reconstructed text visibly blurs (`results/compare_{13,6}px.png`).
  Metrics in `results/vae_recon.json`.
- Wrote `FINDINGS.md` (reproduced-vs-reported table, the not-reproduced
  catalogue with blockers, reproduce-it-yourself steps). Updated `README.md`
  status and taught `pages.yml` to copy result PNGs into the published site.
