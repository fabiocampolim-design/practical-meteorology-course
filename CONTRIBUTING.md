# Contributing to practical-meteorology-course

Thank you for considering a contribution. This file says what is welcome,
how the material is checked, and the few rules that keep it consistent. The
design and its trade-offs are written up in [`docs/DESIGN.md`](docs/DESIGN.md);
the complete machine-oriented description of the repository is
[`AGENTS.md`](AGENTS.md); the human reference is
[`docs/USER_MANUAL.md`](docs/USER_MANUAL.md).

## What is most welcome

- **Corrections to the material** — a wrong sign in a chapter's notes, a
  slide that contradicts the book, an exercise whose solution does not
  match its statement, a notebook case that mis-states a physical quantity.
  Say the chapter, the file and the book page (v1.02b) the correct value
  comes from.
- **Classroom experience.** The course was reviewed chapter by chapter by
  the lecturer but has not yet run in class; how long a chapter actually
  took, which numerical case students found hardest, which slide needed a
  second board explanation — this is what the roadmap needs most.
- **Figure permissions.** Thirteen of the book's figures are credited to
  third parties and are not redistributed here (the slides carry a boxed
  pointer to the book instead). If you hold or obtain permission for one,
  open an issue with the holder's written consent.
- **Translations of the notes and slides** to another language, as a
  separate directory, once there is demand. The English documentation
  (README, manual, `AGENTS.md`) is maintained here; the material itself is
  Portuguese and stays so.
- **Notebook cases with a lighter dependency**, so that notebook execution
  can move into CI (the `meteo` environment is too heavy for hosted runners
  today).

## Ground rules

1. **The material is in Portuguese (pt-BR).** Notes, slides, teacher's
   guide, exercise lists and notebook text; decimal comma in plot
   annotations. English is for the README, the manual, `AGENTS.md`, the
   licences and, optionally, code comments.
2. **The exercise lists are generated, never edited.** Edit the exercise
   section of `notas/capNN_notas.tex` and run
   `python ferramentas/gera_listas.py --pdf`; the audit refuses a hand edit.
3. **Figure policy is a licence matter, not a preference.** A figure the
   book credits to a third party is never added to `figuras/` nor
   referenced from a `.tex`; the banned list is `BANNED_FIGURES` in
   `tests/test_course.py`. US-government images (NOAA, NWS, NASA) are fine
   with a credit in the caption. Read the extracted text for "courtesy of",
   "used with permission" and "©" before keeping any crop.
4. **The book itself never enters git.** `book/`, `extracted/` and the page
   slices `ferramentas/capNN*.pdf` are gitignored; do not quote long
   passages of the book in tracked files. Download it from the author's
   site (see the README).
5. **Notebooks are executed, then scanned.** After
   `jupyter nbconvert --execute --to notebook --inplace notebooks/capNN_x.ipynb`
   (one notebook per command), the suite must find no error output, no
   stderr stream, no unexecuted code cell and no notebook over 1.5 MB.
   Lower the figure dpi before splitting anything.
6. **Every change to the tools ships with a test that failed first**
   (`python -m unittest discover -s tests -v`), and `pyflakes` must be clean
   over `ferramentas comum docs tests`. Every tool flag must appear in
   `AGENTS.md` and in the manual; the suite checks.
7. **LaTeX conventions**: no raw Unicode symbols in `.tex` (use commands),
   compile from the document's own folder, two passes when there is a table
   of contents. Chapter 22 is atmospheric optics; climate change is chapter
   23 (`audita.py` check 7 exists because this was once wrong).
8. **Two licences, by origin.** Code (`ferramentas/`, `comum/*.py`,
   `comum/*.sty`, `docs/*.py`, `tests/`) is Apache-2.0 with an SPDX header;
   content derived from the book (notes, slides, guide, lists, notebook
   text, figures) is CC BY-NC-SA 4.0 and cannot be relicensed. Never strip
   the disclaimer from the README or `LICENSE`.
9. **Nothing personal in the tree.** No absolute paths, no e-mail addresses,
   no institutional identifiers in code, docs or notebook outputs; the suite
   scans for them.

## Pull requests

- One change per pull request, with the `CHANGELOG.md` line you would want
  to read six months later.
- Code contributions are accepted under the Apache License 2.0 (its
  section 5); content contributions under CC BY-NC-SA 4.0, the licence the
  material inherits from the book.
- CI runs `pyflakes` and the suite on Linux, Windows and macOS; all of it
  must be green. Notebooks are executed locally (see rule 5), not in CI.
- Releases are the maintainer's: a `VERSION` bump, a changelog entry,
  `CITATION.cff`, the rebuilt manual, an annotated tag and a GitHub
  Release, followed by an independent code review.

## Where to talk

Open an [issue](https://github.com/fabiocampolim-design/practical-meteorology-course/issues).
There is no mailing list and no e-mail contact; the maintainer's GitHub
profile is the other door. Please read the [Code of Conduct](CODE_OF_CONDUCT.md)
first.
