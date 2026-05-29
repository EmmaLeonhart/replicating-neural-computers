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

## 2026-05-24 — Published: Pages live, both workflows green (queue 11)

- Enabled GitHub Pages (Source: GitHub Actions) via the API. **Site live:**
  <https://emmaleonhart.github.io/replicating-neural-computers/> (HTTP 200;
  renders `FINDINGS.md` with the comparison images).
- Fixed the PDF step: it was hitting its skip fallback (no PDF engine), so
  `pages.yml` now installs weasyprint and renders `report.pdf` (serves HTTP 200,
  application/pdf) — handles the report's unicode and local result images.
- `package` workflow (downloadable ZIP) triggered and builds green.
- **Definition of done met:** FINDINGS reports a reproduced headline number,
  `scripts/run.py` runs end-to-end (downloads the public VAE), repo is public,
  and Pages + ZIP build green. **Replication complete.** Remaining queue items
  are optional polish (release tag, PSNR tightening, action version bumps).

## 2026-05-28 — Windowed launcher for the runnable demo; sources note updated

- User wanted a double-click, windowed way to run "the paper's programmes."
  Reality check first: the trained NCs (NCCLIGen / NCGUIWorld) were never
  released, so only the public-weights slice (Experiment 1, Wan2.1 VAE recon)
  can run. Built a launcher around exactly that, nothing it can't deliver:
  - `scripts/gui.py` — Tkinter front-end over `scripts/run.py` (device / clips /
    frames / font-sizes / densities; live output; view compare PNGs). No new
    deps (Tkinter ships with Python). Drives the verified entry point as a
    subprocess so it can't drift from the reproduced result.
  - `Run Neural Computers Demo.bat` — repo-root launcher; honours `NC_PYTHON`
    for picking a package-complete interpreter.
- **Verified:** `py_compile` clean; tkinter 8.6 + torch 2.10.0+cu128 present;
  GUI window opens and closes cleanly; CPU smoke run (`--device cpu
  --num-samples 2 --frames 1 --densities 0.25`) completed and wrote
  `results/vae_recon.json` (13px 35.10 dB / 0.991, 6px 33.56 dB / 0.989).
- Fixed a stale note: `notes/sources.md` recorded "no authors' code repo," but
  `github.com/metauto-ai/NeuralComputer` (a **data-engine** repo — trajectory
  generation only, still no weights/inference) now exists. Added a dated update;
  conclusions unchanged.
