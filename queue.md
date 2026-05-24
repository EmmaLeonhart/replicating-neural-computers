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

## Done — replication complete and published

The replication is finished and live (see `devlog.md` 2026-05-24 and
`FINDINGS.md`): source read, public repo pushed, no recipe found, Experiment 1
(Wan2.1 VAE terminal reconstruction) reproduced, all other claims catalogued as
not-reproducible, references checked. **Pages is enabled and the `pages` (site +
PDF) and `package` (ZIP) workflows both build green.**
Site: <https://emmaleonhart.github.io/replicating-neural-computers/>

The `SKILL.md` definition of done is fully met. Only optional polish remains.

## Optional — polish (no longer blocking)

1. **Cut a release** (`v0.1.0`) so `package.yml` attaches the ZIP replication
   package as a release asset. Note the tag in `devlog.md`.

2. **Tighten the PSNR match.** The reproduced 13px PSNR (37.2 dB) sits below the
   paper's 40.77 dB because our rendered terminals are denser / lower-res than
   theirs. If desired, add a `--very-sparse` profile (few lines, 720p) and a
   brief OCR-on-recon check to substantiate the 6px text-blur claim
   quantitatively (not just visually). Update `FINDINGS.md` if pursued.

3. **Modernize workflow actions** before 2026-06-02: bump `actions/checkout`,
   `actions/upload-artifact`, `actions/deploy-pages` off Node.js 20 (currently
   only deprecation warnings, not failures).

---

## Pointers

- Methodology / definition of done: `SKILL.md`.
- Long-horizon items: `todo.md`.
- Completed work + replication milestones (chronological): `devlog.md`.
- Recipe-search + claims inventory: `notes/sources.md`, `notes/claims.md`.
- Narrative history: `git log`.
