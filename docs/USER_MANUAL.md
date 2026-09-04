# practical-meteorology-course — User Manual

Version 1.0.2 (2026-09-04). Source of truth: this Markdown file; the HTML and
PDF beside it are built by `python docs/build_manual.py`. Machine-oriented
instructions for AI agents are in [`AGENTS.md`](../AGENTS.md).

The material itself is in **Portuguese (pt-BR)**; this manual is in English
so that the tooling and the licence conditions are clear to everyone.

## 1. What this is

Complete teaching material for a two-semester undergraduate course on
Roland Stull's open textbook *Practical Meteorology: An Algebra-based Survey
of Atmospheric Science* (v1.02b, UBC, CC BY-NC-SA 4.0). For each of the
book's 22 chapters, plus an extra module 23 on climate change (which is not
a chapter of the book), it ships five pieces:

| Piece | Where | Form |
|---|---|---|
| Lecture notes — a blackboard script with `noquadro` boxes, cross-references `\javimos`/`\veremos`, and the chapter's complementary exercises (T1–T5 theory, N1–N4 numerical) | `notas/capNN_notas.tex` + `.pdf` | LaTeX article |
| Slides — one deck per chapter, every book figure that may be redistributed, plus notebook figures | `slides/capNN_slides.tex` + `.pdf` | Beamer |
| Teacher's guide — one section per chapter (`guia.pdf`, 47 pages) and the two-semester schedule (`cronograma.pdf`) | `guia_do_professor/` | LaTeX |
| Student notebook — four worked cases and the N1–N4 exercise cells, executed | `notebooks/capNN_<tema>.ipynb` | Jupyter |
| Solutions notebook — T1–T5 checked with SymPy, N1–N4 solved in full, executed | `notebooks/capNN_solucoes.ipynb` | Jupyter |

Across the course: `listas/listas_exercicios.pdf` (24 pages, one printable
list per chapter, generated from the notes), `indice.pdf` (the course map:
overview, the five pieces, chapter table, quick start, licence), and
`figuras/capNN/` (the book's figures as JPEG crops plus the PNGs the
notebooks generate for the slides).

**Start with `indice.pdf`.**

## 2. Setup

### 2.1 Reading and teaching (no tooling)

Every deliverable is committed as a PDF or an executed notebook: clone (or
download the release archive) and open them. Nothing to install.

### 2.2 Running the notebooks

```
conda env create -f environment.yml
conda activate meteo
jupyter lab
```

The `meteo` environment (Python 3.11) carries NumPy, SciPy, SymPy, pandas,
xarray, MetPy, Py-ART, Satpy, Cartopy, pint, ipywidgets and, from pip,
ambiance, pyrcel, tcpyPI and climlab ≥ 0.9.2. `environment.yml` explains
the two pins that matter (matplotlib < 3.11 for MetPy's `StationPlot`;
climlab from pip because the conda-forge build breaks with NumPy 2).

Each notebook begins with

```python
import sys; sys.path.append('../comum')
from estilo_meteo import aplicar_estilo, CORES
aplicar_estilo()
```

so run it from `notebooks/` (Jupyter does this when you open the file there).

### 2.3 Compiling the LaTeX

TeX Live (2026 used here) with `pdflatex`. Every document compiles from its
own folder; the shared preamble and Beamer theme live in `comum/` and are
found by relative path:

```
cd slides && pdflatex cap05_slides.tex && pdflatex cap05_slides.tex
cd notas  && pdflatex cap05_notas.tex
cd guia_do_professor && pdflatex guia.tex && pdflatex guia.tex
```

Two passes for anything with a table of contents or cross-references.

### 2.4 Rebuilding figures from the book (maintainers only)

The book is **not** in the repository. Download the whole-book PDF from
<https://www.eoas.ubc.ca/books/Practical_Meteorology/> into `book/`
(gitignored), then slice → extract → map (section 4). The extractor used
was a local MinerU-based pipeline; any extractor that writes
`capNN.md` + `capNN_assets/images/<hash>.jpg` works with `map_figs.py`.

## 3. Using the material

- **A chapter in class**: notes as the lecturer's script, slides projected,
  the student notebook opened live for the four cases; the guide section
  lists the book exercises to assign and the timing.
- **Exercises**: the printable list (`listas/`) states T1–T5 and N1–N4; the
  students solve T on paper and N in the empty cells at the end of their
  notebook; the solutions notebook is for the teacher.
- **Schedule**: `guia_do_professor/cronograma.pdf` — semester I chapters 1–11,
  semester II chapters 12–23, 15 weeks each, 2 × 2 h per week, lists due the
  following week, two exams per semester, and a compact one-semester track.
- **Editing exercises**: edit the notes (`notas/capNN_notas.tex`, section
  "Exercícios complementares") and regenerate the list with
  `gera_listas.py` — never edit `listas/listas_exercicios.tex` by hand.
- **Adding a figure to a slide**: `\figlivroslide{fig_NN_X.jpg}{height}{caption}`
  for a book figure (adds the CC attribution line);
  `\figlivroref{Fig.~N.M}{caption}{holder}` for a figure that is *not*
  redistributed (a boxed pointer to the book).

## 4. Tools reference (`ferramentas/`)

Every script has `--help`, `--version`, and the common options
`-v`/`--verbose`, `-q`/`--quiet`, `--log-dir PASTA`. Each run writes a log
under `<output folder>/logs/<script>-<UTC>.log` with the command line, the
versions and the outcome (`RESULTADO: ok|FALHA`). Exit code 0 = success.
Run them from anywhere; paths default to this repository.

| Script | What | Options |
|---|---|---|
| `audita.py` | Consistency audit of the whole course (figures cited exist, no placeholders, cross-references, notebook pairs, 4 cases + 4 N per student notebook, 5 T + 4 N in solutions and notes, no error cells, guide complete). Exit 1 on any problem not in its accepted list. | `--root PASTA`, `--json ARQUIVO` |
| `gera_listas.py` | Generate `listas/listas_exercicios.tex` from the notes; `--pdf` also compiles it (two `pdflatex` passes). | `--notas PASTA`, `--outdir PASTA`, `--pdf` |
| `extract_plots.py` | Dump the `image/png` outputs of executed notebooks as PNG files (`<notebook>_plotNN.png`). | `--notebooks NOME ...`, `--pasta-notebooks PASTA`, `--outdir PASTA` |
| `contact_sheet.py NN` | Labelled thumbnail grid of `figuras/capNN/` to check the figure mapping by eye. | `--figuras PASTA`, `--out PNG`, `--cols N`, `--dpi N` |
| `render_qa.py` | Render sample pages of the compiled PDFs to PNG for visual QA (`--fase 1`: chapters 1–11 decks; `2`: chapters 12–14, notes, guide; `all`). Needs PyMuPDF. | `--root PASTA`, `--outdir PASTA`, `--fase {1,2,all}`, `--dpi N` |
| `slice.py PRIMEIRA ULTIMA NOME` | Cut a page range of the book PDF into `NOME.pdf` for the extractor (PDF page = book page + 16). Needs PyMuPDF and the book. | `--book PDF`, `--outdir PASTA` |
| `map_figs.py NN` | Map the extractor's crops for chapter NN to `figuras/capNN/fig_NN_X.jpg` (one caption, one figure; several images → suffixes a, b, c). Needs the extraction. | `--extracted PASTA`, `--figuras PASTA` |

`docs/build_manual.py` builds this manual (`--outdir PASTA`, `--no-pdf`,
`--verbose`); it uses pandoc + xelatex/lualatex when present and a built-in
converter otherwise.

## 5. Quality checks

- `python ferramentas/audita.py` — the course-level audit above.
- `python -m unittest discover -s tests -v` — the 25-check suite: licence and
  disclaimer guards, SPDX headers, version consistency, the figure policy
  (section 7), notebook QA (46 notebooks, 23 pairs, no error or stderr
  output, every code cell executed, ≤ 1.5 MB each), the docs guard (every
  script flag appears in this manual and in `AGENTS.md`, README counts match
  the tree), read-back of every committed PDF with PyMuPDF (page counts and
  text), run logs, and the vendored publication-conformance checker.
- `python -m pyflakes ferramentas comum docs tests` — static check, also the
  first CI step. CI runs both on Linux, Windows and macOS (Python 3.11 and
  3.13). CI has no TeX: it reads the committed PDFs, it does not rebuild them.
- After executing a notebook, scan its JSON for `output_type: error` **and**
  `stderr` streams — a clean exit code is not enough (the suite does this).

## 6. Every feature and every known limitation

Features (each one is verified by the suite or by the audit):

1. 23 chapters × 5 pieces, all present, all compiled/executed (46 notebooks).
2. Every book figure used on a slide exists in `figuras/` and carries the
   CC BY-NC-SA attribution line; non-redistributable figures are replaced by
   a boxed pointer to the book.
3. Exercise lists are generated from the notes, never hand-edited.
4. Both math forms side by side: the book's algebraic form and the
   differential form, in every chapter's notes.
5. Every chapter has at least one small numerical simulation ("previsão
   numérica em miniatura") and four worked cases with the full Python stack.
6. Solutions notebooks verify the theory exercises with SymPy.
7. Consistent plotting style (`comum/estilo_meteo.py`): course palette,
   shaded atmospheric layers, decimal commas in annotations.
8. Maintenance tools with complete command-line parameters and run logs.

Known limitations:

1. **Language**: everything a student sees is in Portuguese; only this
   manual, `AGENTS.md`, the README and the licence files are in English.
2. **Non-commercial only** for the teaching content (CC BY-NC-SA 4.0,
   inherited from the book); the code is Apache-2.0. See section 7.
3. **13 book figures are not included** (24 crops: figs. 8.11, 8.16a/d,
   9.20, 14.1, 14.3, 14.5, 15.3, 15.18, 16.19, 17.6, 20.15, 20.19, and 7.13
   was never included) because the book credits them to third parties;
   six slides show the boxed pointer instead of the image.
4. **The book is not redistributed**; rebuilding figures needs your own
   download and an extractor. The shipped crops are as good as the extractor
   made them (vector figures rasterised at page resolution).
5. **Chapter 23 (climate change) is not a chapter of Stull's book**: its
   slides use notebook figures only; its content follows the notes.
6. **Schedule dates are placeholders** until the academic calendar is known.
7. **Deliberate omissions** at curiosity level (recorded in the audit of
   2026-08-28): the diagram-identification quick guide (§5.4), SYNOP codes in
   detail (§9.2), MOS (§20.5), crepuscular rays (§22).
8. **`audita.py` has two accepted findings**: chapter 1 has five cases and
   states its N exercises in the notes rather than in the notebook (the
   approved template) — both are listed in the script's `EXCECOES`.
9. **Notebook execution is not part of CI** (the `meteo` environment is
   heavy); the committed notebooks are executed locally and the suite checks
   the committed outputs.
10. **Windows LaTeX trap**: a PDF open in a viewer locks `pdflatex`'s output;
    close the viewer or compile with `-jobname`.
11. **Unicode in LaTeX**: Greek letters, the approximately-equal sign or a
    check mark typed directly break `pdflatex`; use the LaTeX commands.
12. **Third-party cross-checks are numerical, not refereed**: values in the
    notebooks follow the book and standard references; teachers remain
    responsible for what they teach.

## 7. Licence and figure policy

- **Code** (`ferramentas/`, `comum/*.py`, `comum/*.sty`, `docs/*.py`,
  `tests/`, the code cells of the notebooks): Apache License 2.0
  (`LICENSE`, `NOTICE`).
- **Teaching content** (notes, slides, guide, lists, index, figures, the
  text cells of the notebooks): derived from Stull's CC BY-NC-SA 4.0 book,
  therefore CC BY-NC-SA 4.0 (`LICENSES/CC-BY-NC-SA-4.0.txt`): credit the
  book and this project, no commercial use, share adaptations under the same
  licence.
- **Figures**: a figure the book credits to a third party ("courtesy of",
  "used with permission", a copyright line) is covered by *that* holder's
  permission to the book, not by the book's licence, and is not
  redistributed here. `tests/test_course.py` carries the banned list and
  fails if any of them reappears in `figuras/` or in a `.tex` file.
  US-government images (NOAA, NWS, NASA) are public domain and stay, with
  their credit in the slide caption.
- The warranty disclaimer and limitation of liability are in `LICENSE`
  (Apache §7–8), in the CC text (section 5) and in the README.

## 8. Layout

```
indice.tex/.pdf          course map — start here
notas/                   capNN_notas.tex/.pdf
slides/                  capNN_slides.tex/.pdf
guia_do_professor/       guia.tex (+ capNN_guia.tex), guia.pdf, cronograma.tex/.pdf
notebooks/               capNN_<tema>.ipynb, capNN_solucoes.ipynb
listas/                  listas_exercicios.tex/.pdf (generated)
figuras/capNN/           fig_NN_X.jpg (book), notebook_*.png (ours)
comum/                   preambulo.sty, temameteo.sty, estilo_meteo.py
ferramentas/             the tools of section 4 (+ registro.py, shared logging)
docs/                    this manual (+ html/pdf), build_manual.py, DEVLOG.md, AUDIT-*.md
tests/                   the suite + vendored conformance checker
book/, extracted/        your local copy of the book and its extraction (gitignored)
```
