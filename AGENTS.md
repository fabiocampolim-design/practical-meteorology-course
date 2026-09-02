# AGENTS.md — instructions for AI agents working in this repository

Complete, machine-oriented description of `practical-meteorology-course`.
Humans: read `README.md` and `docs/USER_MANUAL.md`; hand this file to your
agent. Keep the three in sync when anything changes.

## What the repository is

Portuguese (pt-BR) teaching material for a two-semester undergraduate course
on R. Stull, *Practical Meteorology* (v1.02b, UBC, CC BY-NC-SA 4.0):
23 chapters (22 of the book + module 23 "Mudança Climática", which is ours),
each with `notas/capNN_notas.tex`, `slides/capNN_slides.tex`,
`guia_do_professor/capNN_guia.tex`, `notebooks/capNN_<tema>.ipynb` (student)
and `notebooks/capNN_solucoes.ipynb` (teacher); plus `listas/` (generated),
`guia_do_professor/cronograma.tex`, `indice.tex`, `figuras/capNN/`,
`comum/` (LaTeX preamble, Beamer theme, plotting style module).
Version in `VERSION`; history in `CHANGELOG.md`.

## Hard rules

1. **Language of the material is Portuguese.** Notes, slides, guide, lists,
   notebook text: pt-BR, decimal comma in plot annotations
   (`.replace('.', ',')`). English only in README, manual, AGENTS, licences,
   code comments may be either.
2. **Never edit `listas/listas_exercicios.tex` by hand.** Edit the exercise
   section of `notas/capNN_notas.tex` and run
   `python ferramentas/gera_listas.py --pdf`.
3. **Figure policy.** A figure the book credits to a third party is never
   added to `figuras/` nor referenced from a `.tex`. The banned list is
   `BANNED_FIGURES` in `tests/test_course.py` (figs. 7.13, 8.11, 8.16a/d,
   9.20, 14.1, 14.3, 14.5, 15.3, 15.18, 16.19, 17.6, 20.15, 20.19). Use
   `\figlivroref{Fig.~N.M}{caption}{holder}` on the slide instead. When
   mapping a new chapter, read the extracted text for "courtesy of",
   "used with permission", "©" before keeping a crop; US-government images
   (NOAA, NWS, NASA) are fine, credit them in the caption.
4. **The book, its page slices and the extraction never enter git**
   (`book/`, `extracted/`, `ferramentas/capNN*.pdf` are gitignored). Do not
   quote long passages of the book in tracked files.
5. **Chapter 22 is atmospheric optics; climate change is chapter 23.**
   `audita.py` check 7 exists because this was once wrong.
6. **Notebook QA is a JSON scan, not an exit code.** After
   `jupyter nbconvert --execute --to notebook --inplace notebooks/capNN_x.ipynb`
   (one notebook per command, never chained with `;`), assert no
   `output_type == "error"` and no `stderr` stream, then run the suite.
7. **Notebook size cap 1.5 MB** (target 1 MB): lower figure dpi before
   splitting anything.
8. **LaTeX**: no raw Unicode symbols (Γ ≈ ✓ φ) in `.tex`, use commands;
   compile from the document's own folder; two passes when there is a TOC;
   a PDF open in a viewer blocks `pdflatex` on Windows.
9. **Licence split**: code Apache-2.0 with an SPDX header in every `.py`
   and `.sty` (first 5 lines); content CC BY-NC-SA 4.0. Never relicense the
   content; never strip the disclaimer from README or LICENSE.
10. **Version discipline**: any behaviour change bumps `VERSION`, adds a
    `CHANGELOG.md` entry and updates `CITATION.cff`; the suite checks the
    three agree.

## Commands

```
python -m pyflakes ferramentas comum docs tests        # static check, first
python -m unittest discover -s tests -v                # the suite (needs pymupdf for PDF read-back)
python ferramentas/audita.py                           # course consistency audit (exit 1 = new problem)
python ferramentas/gera_listas.py --pdf                # regenerate + compile the exercise lists
python ferramentas/extract_plots.py --notebooks cap06_nuvens --outdir qa/plots
python ferramentas/contact_sheet.py 6 --out qa/c6.png
python ferramentas/render_qa.py --fase all --outdir qa/render
python ferramentas/slice.py 17 42 cap01 --book book/Practical_Meteorology-v1.02b-WholeBookColor.pdf
python ferramentas/map_figs.py 1 --extracted extracted --figuras figuras
python docs/build_manual.py                            # docs/USER_MANUAL.html + .pdf
conda env create -f environment.yml && conda activate meteo
```

## Tool flags (every one must appear here and in the manual — the suite checks)

Common to all `ferramentas/*.py`: `--verbose`/`-v`, `--quiet`/`-q`,
`--log-dir PASTA`, `--version`, `--help`. Each run writes
`<outdir>/logs/<script>-<UTC>.log` (command line, versions, `RESULTADO`).

| Script | Flags |
|---|---|
| `audita.py` | `--root PASTA`, `--json ARQUIVO` |
| `gera_listas.py` | `--notas PASTA`, `--outdir PASTA`, `--pdf` |
| `extract_plots.py` | `--notebooks NOME...`, `--pasta-notebooks PASTA`, `--outdir PASTA` |
| `contact_sheet.py NN` | `--figuras PASTA`, `--out PNG`, `--cols N`, `--dpi N` |
| `render_qa.py` | `--root PASTA`, `--outdir PASTA`, `--fase {1,2,all}`, `--dpi N` |
| `slice.py PRIMEIRA ULTIMA NOME` | `--book PDF`, `--outdir PASTA` |
| `map_figs.py NN` | `--extracted PASTA`, `--figuras PASTA` |
| `docs/build_manual.py` | `--outdir PASTA`, `--no-pdf`, `--verbose` |

Every script exposes `build_parser()` and `main(argv) -> int`.

## File schemas

- Student notebook: markdown `## Caso 1..4` sections, each with executed
  code; at the end four `**N1**`..`**N4**` statements followed by empty
  cells for the student. First code cell: `sys.path.append('../comum')` +
  `from estilo_meteo import aplicar_estilo, CORES` + `aplicar_estilo()`.
- Solutions notebook: `## T1`..`## T5` (SymPy verification) and
  `## N1`..`## N4` (full numerical solution).
- Notes: `\title{Capítulo N --- Título\\ ...}`; boxes `noquadro`; cross-refs
  `\javimos{N}` (backwards only) / `\veremos{N}` (forwards only); final
  section `Exercícios complementares` with `\subsection*{Teóricos}` (5
  `\item`) and `\subsection*{Numéricos (no notebook)}` (4 `\item`) ending
  with `\vspace{1em}` — `gera_listas.py` parses exactly this.
- Slides: `\figlivroslide{fig_NN_X.jpg}{height}{short caption}` for book
  figures (macro adds the CC attribution); `\figlivroref{...}` for
  non-redistributed ones; `\includegraphics` for notebook PNGs in
  `figuras/capNN/notebook_*.png`.
- Figures: `figuras/capNN/fig_NN_M[a-h].jpg` — book figure M of chapter NN,
  panels a, b, ...; `notebook_<slug>.png` — generated by our notebooks.
- Run logs: `logs/<script>-<YYYYmmddTHHMMSSZ>.log`, lines
  `comando: ...`, versions, then the script's messages, then
  `RESULTADO: ok|FALHA <summary>`.

## Workflows

- **Change an exercise**: edit the notes → `gera_listas.py --pdf` →
  recompile the chapter's notes → if it is an N exercise, update both
  notebooks and re-execute → `audita.py` → suite.
- **Add/replace a book figure**: check the credit in the extracted text →
  `map_figs.py NN` (or copy the crop by hand with the naming above) →
  `contact_sheet.py NN` to verify → reference it in the slide → recompile →
  `audita.py`.
- **Release**: bump `VERSION`, `CHANGELOG.md`, `CITATION.cff` (version +
  date) → `python docs/build_manual.py` → pyflakes → suite green → commit →
  `git tag -a vX.Y.Z` → push with tags → GitHub release from the changelog
  section.

## What the suite guards (`tests/test_course.py`, 21 checks)

Licence texts and README disclaimer; SPDX headers; VERSION = CITATION =
CHANGELOG; banned figures absent from `figuras/` and from every `.tex`;
`audita.py` reports only its accepted findings; book material untracked;
46 notebooks in 23 pairs, no error/stderr outputs, every code cell executed,
≤ 1.5 MB; every tool flag documented in `AGENTS.md` and the manual; README
and manual counts match the tree; no personal paths or codenames in sources;
every committed PDF opens, has the expected page count and text
(PyMuPDF, skipped if absent); `gera_listas.py` and `extract_plots.py` run
and write their logs; the vendored conformance checker runs.
