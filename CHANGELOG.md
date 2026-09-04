# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [1.0.2] — 2026-09-04

Independent review of the public repository (every tool read line by line)
and the publishing playbook's community-files rule.

### Added
- `CONTRIBUTING.md` (what is welcome, the ground rules, how the material is
  checked), `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1) and
  `docs/DESIGN.md` (the design decisions and their trade-offs, with who
  decided what); the README links to them. A suite check keeps them present.

### Fixed
- `ferramentas/audita.py`: a missing `guia_do_professor/guia.tex` is a listed
  problem, not a traceback; the chapter number is read from the file name,
  never from the path (a folder named `cap99` anywhere above the material
  renumbered every chapter).

### Changed
- Vendored publication-conformance checker 1.6.1 (was 1.4.1): rules 25–27
  and the citation-version check; the byte-identity test is green again.
- Suite: 25 checks (was 22): missing guide, chapter numbering, community files.

## [1.0.1] — 2026-09-02

Post-release independent code review of 1.0.0 (two defects, both in the
manual builder's fallback path).

### Fixed
- `docs/build_manual.py`: the built-in Markdown converter left a list open
  when a table or heading followed it without a blank line (malformed HTML);
  a pandoc failure now falls back to the built-in converter instead of
  aborting with a traceback, as the docstring promised.
- `ferramentas/audita.py`: error cells counted once per notebook, not twice.
- `ferramentas/map_figs.py`: help text says why the chapter range is 1–22.

### Added
- Suite check for the fallback converter (22 checks).

## [1.0.0] — 2026-09-02

First public release. The course itself has been complete since 2026-08-28
(22 chapters of Stull's *Practical Meteorology* plus an extra module on
climate change, each with lecture notes, Beamer slides, a teacher's-guide
section, a student notebook and a solutions notebook; printable exercise
lists; a two-semester schedule; a course index).

### Added
- `LICENSE` (Apache-2.0, code) + `NOTICE`, `LICENSES/CC-BY-NC-SA-4.0.txt`
  (teaching content), README licence section with disclaimer and
  non-affiliation note; SPDX headers on every code file.
- `VERSION`, `CITATION.cff`, `AGENTS.md`, `docs/USER_MANUAL.md` (built to
  HTML and PDF by `docs/build_manual.py`).
- `tests/`: 21 checks (licence guards, notebook QA, figure policy, docs
  guard, PDF read-back, run logs) plus the vendored publication-conformance
  checker; GitHub Actions on Linux, Windows and macOS with `pyflakes`
  before the suite.
- `ferramentas/registro.py`: every maintenance script now has `--help`,
  `--verbose` / `--quiet` and writes a run log under `<outdir>/logs/`.
- `\figlivroref` macro (`comum/temameteo.sty`): a boxed "see the book"
  note for figures that are not redistributed.

### Changed
- Maintenance scripts take every input and output from the command line
  (`--outdir`, `--notebooks`, `--book`, …); no hard-coded paths.
- `render_qa2.py` folded into `render_qa.py --fase 2`.
- `comum/estilo_meteo.py` no longer imports what it does not use.
- The working handoff `CONTINUAR.md` moved to `docs/DEVLOG.md`.

### Removed
- 24 figure crops the book credits to third parties (EUMETSAT, SSEC/CIMSS,
  Environment Canada, Gene Rhoden, Gene Moore, NCAR, ECMWF): figs. 8.11,
  8.16a/d, 9.20, 14.1, 14.3, 14.5, 15.3, 15.18, 16.19, 17.6, 20.15, 20.19.
  The six slides that used them now carry the note above; fig. 7.13
  (K. Libbrecht) was never included. A test keeps them out.
- The source book, its page slices and the extractor output are not part of
  the repository (download the book from UBC).
