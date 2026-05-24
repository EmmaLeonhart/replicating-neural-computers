# Replicating: Neural Computers

**arXiv:** [2604.06425](https://arxiv.org/pdf/2604.06425v2) - **HTML:** [2604.06425](https://arxiv.org/html/2604.06425v2)
**Authors:** Mingchen Zhuge, Changsheng Zhao, Haozhe Liu, Zijian Zhou, Shuming Liu, Wenyi Wang, Ernie Chang, Gael Le Lan, Junjie Fei, Wenxuan Zhang, Yasheng Sun, Zhipeng Cai, Zechun Liu, Yunyang Xiong, Yining Yang, Yuandong Tian, Yangyang Shi, Vikas Chandra, Jürgen Schmidhuber
**Published:** 2026-04-07T20:01:05Z

## Abstract

We propose a new frontier: Neural Computers (NCs) that unify computation, memory, and I/O of traditional computers in a learned runtime state. Our long-term goal is the Completely Neural Computer (CNC): the mature, general-purpose realization of this emerging machine form, with stable execution, explicit reprogramming, and durable capability reuse. As an initial step, we study whether elementary NC primitives can be learned solely from collected I/O traces, without instrumented program state. Concretely, we instantiate NCs as video models that roll out screen frames from instructions, pixels, and user actions (when available) in CLI and GUI settings. We show that NCs can acquire elementary interface primitives, especially I/O alignment and short-horizon control, while routine reuse, controlled updates, and symbolic stability remain challenging. We outline a roadmap toward CNCs, to establish a new computing paradigm beyond today's agents and conventional computers.

## Replication status

**Done, scope-limited.** See [`FINDINGS.md`](./FINDINGS.md) for the full report.

No reproduction recipe, code, weights, or dataset ships with the paper, and full
reproduction needs **>10⁵ H100 GPU-hours** — so it is marked **not CI-runnable**
(`paper.json`). We reproduce the one headline number whose inputs are public: the
**pretrained Wan2.1 VAE reconstructing terminal frames** (Experiment 1, Table
`tab:cli-vae-recon`). Result: the paper's claim holds — SSIM matches its 0.989 at
realistic terminal density, PSNR lands in its regime, and the "6px text blurs but
global metrics stay high" nuance is reproduced. Run it with `python scripts/run.py`
(~2 min on a consumer GPU). The remaining tables (trained-NC ablations, proprietary
baselines) are catalogued as reported-but-not-reproduced in
[`notes/claims.md`](./notes/claims.md).

The agent-executable methodology is in [`SKILL.md`](./SKILL.md); recipe-search
findings in [`notes/sources.md`](./notes/sources.md).

## What this repo produces

Three compounding artifacts:

1. **The replication** — runnable code under `src/` + `scripts/run.py`.
2. **The legibility layer** — `FINDINGS.md`, published as a GitHub Pages
   site with a transportable PDF report (built by GitHub Actions).
3. **`SKILL.md`** — a reusable, agent-executable replication methodology.

## Layout

- `replication_target/` — the paper and everything pulled about it:
  - `source/` — extracted arXiv LaTeX/e-print source (committed; the primary,
    token-efficient text — read the `.tex` directly). Fetched by
    `python download_paper.py`; the raw archive is gitignored.
  - `paper.pdf` — downloaded PDF (gitignored; fallback / complete record).
  - the authors' code, if any, as a git **submodule**.
- `replication_skill.md` — the authors' recipe, if one is shipped (run first).
- `data_lake/` — other downloaded/supplied material (NOT the paper).
- `src/` — your reimplementation. `scripts/run.py` — CI entry point.
- `results/` — metrics JSON (gitignored). `FINDINGS.md` — the report.
- `paper.json` — frozen metadata pulled from the arXiv API.
- `.github/workflows/` — `pages.yml` (site + PDF), `package.yml` (ZIP).

## Deliverables (GitHub Actions)

To publish, **make this repo public** and set **Settings -> Pages -> Source:
GitHub Actions**. Then `pages.yml` deploys the findings site + PDF report and
`package.yml` builds a downloadable ZIP replication package. Site shape
inspiration: http://sutra.emmaleonhart.com/
