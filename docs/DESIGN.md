# practical-meteorology-course — design account

The decisions behind the material, the trade-offs each one carries, what
was rejected, and who decided what. The README's *How it was built* table
gives the CRediT summary; this file is the reasoning behind it. "Fabio" is
the lecturer, author and maintainer; "Claude" is the AI coding agent
(Claude Code) that wrote the material under his direction. Every design
decision below was made or ratified by Fabio; the agent proposed mechanisms
and implemented them.

## 1. The problem

Stull's *Practical Meteorology* is a complete, rigorous, algebra-based
textbook that is free and openly licensed (CC BY-NC-SA 4.0). What a lecturer
in a Portuguese-speaking department still has to build is everything around
it: a blackboard script per chapter, slides, exercises with solutions, a
two-semester schedule — and the numerical side a book cannot carry on paper.
The course was built once, checked mechanically, and shared under the
book's own licence so that anyone can adapt it.

Two consequences shaped everything:

- **The chapter is the unit.** Each of the book's 22 chapters, plus a module
  on climate change that the book does not have, gets the same five pieces:
  notes, slides, a teacher's-guide section, a student notebook and a
  solutions notebook. A course that is complete for every chapter can be
  taught from the first week; a deeper treatment of some chapters and none
  of others cannot.
- **Nothing is trusted, everything is read back.** Every notebook ships
  executed; every PDF is opened by the suite and checked for page count,
  text and attribution; every figure cited on a slide must exist; every
  exercise list is generated from one source. The material was produced by
  an AI agent at a pace no lecturer could review line by line, so the
  checks had to be mechanical before the chapter-by-chapter human review.

*Framed by Fabio; the five-pieces-per-chapter shape and the mechanical-check
contract were his requirements from the first session.*

## 2. Decisions and trade-offs

### 2.1 Portuguese material, English tooling

The notes, slides, guide, exercise lists and notebook text are Portuguese
(pt-BR), decimal comma included. The README, the manual, `AGENTS.md` and the
licences are English.

- *Gain:* the material serves the audience it was written for — Brazilian
  undergraduate courses — without a translation layer between the student
  and the physics; the tooling and licence conditions stay readable to
  anyone.
- *Cost:* an English-speaking lecturer gets the notebooks (code and figures
  read across languages) but not the prose.
- *Rejected:* writing the material in English and translating. It would have
  doubled the review load for a course whose first users are Portuguese
  speakers.

*Decided by Fabio.*

### 2.2 Both mathematical forms, side by side

Every chapter's notes state the book's algebraic form and the differential
form of each relation next to each other.

- *Gain:* the algebra-based book stays the reference for the exam; the
  differential form is what the numerical experiment integrates and what a
  physics or engineering student will meet next.
- *Cost:* longer notes; a lecturer teaching a strictly algebra-based course
  skips half of each derivation.

*Decided by Fabio (the physicist's reason for the course).*

### 2.3 A numerical experiment in every chapter, framed as NWP in miniature

Each student notebook carries four cases and a small numerical model — a
parcel, a column, a slab, a grid — presented as a miniature of the numerical
weather prediction of chapter 20. Soundings use MetPy, radiative equilibrium
climlab, cloud microphysics pyrcel and ambiance, hurricane potential
intensity tcpyPI, radar and satellite data Py-ART and Satpy.

- *Gain:* the student meets the discretised equation twenty-two times before
  chapter 20 names it; the chosen libraries are the ones a working
  meteorologist uses.
- *Cost:* the `meteo` environment is heavy (Py-ART, Satpy, climlab); it does
  not fit hosted CI runners, so notebook execution is local and CI checks the
  committed outputs. The roadmap has a slimmer environment.
- *Rejected:* pure NumPy re-implementations of what the libraries do. They
  would execute anywhere but teach the wrong tool.

*Conceptualization — the Python stack and the framing — led by Fabio (CRediT
table in the README).*

### 2.4 Exercises have one source: the notes

Every chapter's notes end with five theory (T) and four numerical (N)
exercises. `ferramentas/gera_listas.py` extracts them into the printable
lists; the solutions notebook verifies the T exercises with SymPy and solves
the N ones. The audit counts 5 T + 4 N in the notes, 4 N in the student
notebook and 5 T + 4 N in the solutions.

- *Gain:* a change to an exercise cannot leave the list, the notes and the
  solutions disagreeing; the count is a guarantee, not a hope.
- *Cost:* the generated `listas/listas_exercicios.tex` must never be edited
  by hand, which every contributor has to learn once (`AGENTS.md` rule 2).
- *Rejected:* a separate exercise file per chapter, which invites exactly the
  drift the generator exists to prevent.

*Exercise scheme: methodology, led jointly (CRediT table); the "never by
hand" rule is `AGENTS.md` rule 2.*

### 2.5 Figure policy and the licence split

The book's figures are CC BY-NC-SA 4.0, except thirteen it credits to third
parties. Those are never added to `figuras/` nor referenced from a `.tex`;
the slide carries a boxed pointer to the book's figure instead, and a test
keeps the banned list out of the tree. Code (`ferramentas/`, `comum/*.py`,
`comum/*.sty`, `docs/*.py`, `tests/`) is Apache-2.0; everything derived from
the book inherits CC BY-NC-SA 4.0.

- *Gain:* the repository can be public without a permission the maintainer
  does not hold; the code can be reused in a course on any other book.
- *Cost:* six slides show a pointer where an image belonged, until
  permissions are obtained (roadmap).
- *Rejected:* redistributing the figures under the book's licence, which
  does not cover them; and a single licence for the whole tree, which would
  either relicense the book's material (impossible) or put NC-SA on the
  tools (needless).

*Decided by Fabio at publication (2026-09-01); the banned list assembled by
Claude from the book's credits.*

### 2.6 Notebook QA is a JSON scan, not an exit code

After execution, a notebook is checked by reading its JSON: no error output,
no stderr stream, no unexecuted code cell, under 1.5 MB. The suite repeats
the scan on every committed notebook.

- *Gain:* `nbconvert` exits 0 on a notebook that printed a traceback into a
  cell; the scan does not.
- *Cost:* the size cap forces figure dpi choices; a chapter with many plots
  is tuned rather than split.

*The QA-by-JSON rule: methodology, led jointly (CRediT table); it is
`AGENTS.md` rule 6.*

### 2.7 Every tool is a CLI with a log

The maintenance scripts share `ferramentas/registro.py`: `-v/-q`,
`--log-dir`, `--version` from `VERSION`, a run log with the exact command,
versions and outcome, exit 1 on failure. The audit tool lists every problem
and keeps a short list of accepted findings that the suite compares against.

- *Gain:* a lecturer regenerating the lists a year later gets the same
  behaviour and a record of what ran.
- *Cost:* small tools carry more scaffolding than they would as one-off
  scripts.

*Playbook rule applied at publication; accepted by Fabio.*

## 3. What was left out, and why

- **Notebook execution in CI** — the environment is too heavy for hosted
  runners; the committed outputs are checked instead (roadmap).
- **Dates in the schedule** — the course has not yet run in a real
  semester; `cronograma.pdf` gives weeks, not dates.
- **Four deliberate omissions** from the book (manual §5.4, §9.2, §20.5,
  crepuscular rays in chapter 22), listed in the manual's known
  limitations rather than papered over.

## 4. How the work was divided

Chapter 1 was written as a template and approved; chapters 2–22 followed in
batches of three or four, each `.tex` compiled and each notebook executed
and scanned before the next batch; chapter 22 was rewritten when a slip
(climate change instead of atmospheric optics) was caught; module 23 was
added with figures from its own notebook; a scope audit against the book's
tables of contents filled the gaps it found. Fabio reviewed every chapter
and made every licence and publication decision; Claude wrote, executed,
compiled and tested. The CRediT table in the README is the summary of this
account.
