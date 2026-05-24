# replicating-neural-computers - Work Queue

**This file is a queue of concrete, executable steps, not a state snapshot.**
Finished work lives in `devlog.md` (dated entries) and `git log`;
longer-horizon items live in `todo.md`. **When an item is done, delete it
from this file AND append a dated entry to `devlog.md` in the same commit,
then push.** No checkmarks, no status indicators in place.

**Why this file exists:** the replication plan is written here BEFORE
execution so an interrupted session resumes from the queue, not from chat.
The canonical methodology is `SKILL.md`; this queue is its executable form.

---

## Active — Publish & finish

The replication itself is done (see `devlog.md` 2026-05-24 and `FINDINGS.md`):
source read, repo live, no recipe found, Experiment 1 (Wan2.1 VAE terminal
reconstruction) reproduced, all other claims catalogued as not-reproducible,
references checked. Remaining steps are the publish/verify tail.

1. **Enable GitHub Pages** so the findings site deploys. In the repo:
   **Settings → Pages → Source: "GitHub Actions"** (one-time, manual; the
   `pages.yml` workflow is already committed). Confirm the `pages` workflow run
   goes green and the site renders `FINDINGS.md` (including the two comparison
   PNGs copied from `results/`).

2. **Confirm CI is green.** Check the `pages` and `package` workflow runs in the
   Actions tab (`gh run list`). The `package` workflow builds the downloadable
   ZIP on `workflow_dispatch`/release; trigger it once to confirm it builds.

3. **(Optional) Cut a release** (`v0.1.0`) so `package.yml` attaches the ZIP
   replication package as a release asset. Note the tag in `devlog.md`.

4. **(Optional) Tighten the PSNR match.** The reproduced 13px PSNR (37.2 dB)
   sits below the paper's 40.77 dB because our rendered terminals are denser /
   lower-res than theirs. If desired, add a `--very-sparse` profile (few lines,
   720p) and a brief OCR-on-recon check to substantiate the 6px text-blur claim
   quantitatively (not just visually). Update `FINDINGS.md` if pursued.

---

## Pointers

- Methodology / definition of done: `SKILL.md`.
- Long-horizon items: `todo.md`.
- Completed work + replication milestones (chronological): `devlog.md`.
- Recipe-search + claims inventory: `notes/sources.md`, `notes/claims.md`.
- Narrative history: `git log`.
