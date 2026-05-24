# Sources & reproduction-recipe search

Queue item 4: find the authors' reproduction recipe in the e-print source.
**Result: no recipe, no code, no released artifacts.** This is a from-scratch
(scope-limited) replication, not a recipe-run.

## What was searched

The extracted e-print source (`replication_target/source/`) is the LaTeX of the
paper only — `NC.tex`, `section/*.tex`, `paper.bib`, `assets/` (figures + class
files). Searched the full `.tex` tree for: `reproduc`, `replicat`, `github.com`,
`huggingface`, `SKILL`, `AGENTS`, `run.sh`, `Makefile`, `.zip`, `download`,
`release`, `checkpoint`, `weights`.

## What exists (none of it is a runnable recipe)

- **Blogpost only:** `\metadata[Blogpost]{https://metauto.ai/neuralcomputer}`
  (NC.tex:138). Marketing page, not a recipe.
- **"Released configs" — referenced, never linked.** `appendix_pipeline.tex:32,36`
  say window sizes/strides and preprocessing live "in the released configs" so
  "external users can rebuild the corpus." No URL is given anywhere in the source.
- **Tool links (third-party, not the authors' code):**
  - asciinema `agg` — https://github.com/asciinema/agg (GIF rendering)
  - FFmpeg — https://github.com/FFmpeg/FFmpeg
  - charmbracelet `vhs` — https://github.com/charmbracelet/vhs (Clean-set capture)
  These are generic terminal-recording tools the data pipeline used, not a
  reproduction package.
- **No authors' code repo, no model weights, no dataset release, no zip.**

## Backbone & datasets (for the record)

- **Backbone:** Wan2.1 (`wan2025wan`), image-to-video (I2V) variant. The Wan2.1
  weights *are* public (HuggingFace: `Wan-AI/Wan2.1-*`), but the NC-adapted
  checkpoints (CLIGen / GUIWorld) are not released.
- **Datasets:** CLIGen (General) from public asciinema `.cast` archives
  (~824k clips, ~1,100 h); CLIGen (Clean) from authored `vhs` scripts
  (~250k scripts, 51.21% retained → ~78k regular + ~50k math); GUIWorld from a
  NeuralOS-style XFCE capture rig (~1,400 h random + ~110 h Claude-CUA).
  None are published as a downloadable corpus.

## Consequence for this replication

Full reproduction is impossible from what is shipped: tens of thousands of H100
GPU-hours (see `claims.md`), no released curated data, no released NC weights,
and proprietary baselines (Sora2, Veo3.1). Per the `SKILL.md` budget guardrail
(>~4 GPU-hours on one consumer GPU → not CI-runnable), this replication is marked
**not CI-runnable** in `paper.json`, and we reproduce the single slice that needs
only public, pretrained components: the **Wan2.1 VAE terminal-reconstruction**
test (Experiment 1, Table `tab:cli-vae-recon`). Everything else is documented as
reported-but-not-reproduced in `FINDINGS.md`.
