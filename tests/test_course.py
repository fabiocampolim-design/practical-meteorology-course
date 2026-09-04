# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""The course suite: licence guards, figure policy, notebook QA, docs guard,
PDF read-back and tool run logs. Standard library only; PyMuPDF enables the
PDF read-back (skipped cleanly when absent).

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import glob
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "ferramentas"))
sys.path.insert(0, os.path.join(ROOT, "docs"))

# Figures the book credits to third parties: never in figuras/, never in a .tex.
# (fig 7.13 K. Libbrecht; 8.11 EUMETSAT; 8.16a/d SSEC; 9.20 Environment Canada;
# 14.1/14.3/14.5 Gene Rhoden; 15.3 Gene Moore; 15.18 NCAR; 16.19 CIMSS/SSEC;
# 17.6 Shane Mayor/NCAR; 20.15, 20.19 ECMWF.)
BANNED_FIGURES = (
    "fig_07_13", "fig_08_11", "fig_08_16a", "fig_08_16d", "fig_09_20",
    "fig_14_1", "fig_14_3", "fig_14_5", "fig_15_3", "fig_15_18",
    "fig_16_19", "fig_17_6", "fig_20_15", "fig_20_19",
)
# a stem matches itself and its panels (a-h), never a longer figure number
BANNED_RE = re.compile(r"^(?:%s)[a-h]?\.(?:jpg|png)$" % "|".join(BANNED_FIGURES))
TOOLS = ("audita", "gera_listas", "extract_plots", "contact_sheet",
         "render_qa", "slice", "map_figs")
MAX_NOTEBOOK_BYTES = 1_500_000


def _read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _notebooks():
    return sorted(glob.glob(os.path.join(ROOT, "notebooks", "cap*.ipynb")))


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _banned(name):
    return bool(BANNED_RE.match(os.path.basename(name)))


class Licence(unittest.TestCase):
    def test_license_is_apache_with_disclaimers(self):
        text = _read("LICENSE")
        self.assertIn("Apache License", text)
        self.assertIn("WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND", text)
        self.assertIn("Limitation of Liability", text)

    def test_cc_licence_text_present(self):
        text = _read("LICENSES", "CC-BY-NC-SA-4.0.txt")
        self.assertIn("Attribution-NonCommercial-ShareAlike 4.0 International", text)
        self.assertIn("Disclaimer of Warranties and Limitation of Liability", text)

    def test_notice_names_both_licences(self):
        text = _read("NOTICE")
        self.assertIn("practical-meteorology-course", text)
        self.assertIn("Apache License, Version 2.0", text)
        self.assertIn("CC BY-NC-SA 4.0", text)
        self.assertIn("Stull", text)

    def test_readme_licence_disclaimer_non_affiliation(self):
        text = _read("README.md")
        self.assertIn("## Licence", text)
        self.assertIn("### Disclaimer", text)
        self.assertLess(text.index("## Licence"), text.index("### Disclaimer"))
        low = text.lower()
        self.assertIn("without warrant", low)
        self.assertIn("liable", low)
        self.assertIn("not affiliated", low)
        self.assertIn("CC BY-NC-SA 4.0", text)
        self.assertIn("Apache", text)

    def test_citation_mentions_both_licences(self):
        text = _read("CITATION.cff")
        self.assertIn("Apache-2.0", text)
        self.assertIn("CC-BY-NC-SA-4.0", text)
        self.assertIn("Stull", text)

    def test_version_consistent_across_files(self):
        version = _read("VERSION").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn(f'version: "{version}"', _read("CITATION.cff"))
        first = re.search(r"^## \[(\d+\.\d+\.\d+)\]", _read("CHANGELOG.md"), re.M)
        self.assertIsNotNone(first, "CHANGELOG.md needs a '## [x.y.z]' heading")
        self.assertEqual(first.group(1), version)
        self.assertIn(f"Version {version}", _read("docs", "USER_MANUAL.md"))

    def test_spdx_headers_on_code(self):
        files = [f for pat in ("ferramentas/*.py", "comum/*.py", "comum/*.sty",
                               "docs/*.py", "tests/*.py")
                 for f in glob.glob(os.path.join(ROOT, pat))]
        self.assertGreaterEqual(len(files), 12)
        missing = [os.path.relpath(f, ROOT) for f in files
                   if "SPDX-License-Identifier: Apache-2.0"
                   not in "\n".join(_read(f).splitlines()[:5])]
        self.assertEqual(missing, [])


class FigurePolicy(unittest.TestCase):
    def test_banned_figures_absent_from_figuras(self):
        present = [os.path.relpath(f, ROOT)
                   for f in glob.glob(os.path.join(ROOT, "figuras", "cap*", "*"))
                   if _banned(f)]
        self.assertEqual(present, [])

    def test_banned_figures_not_referenced_in_tex(self):
        hits = []
        for tex in glob.glob(os.path.join(ROOT, "**", "*.tex"), recursive=True):
            src = _read(tex)
            for name in re.findall(r"fig_\d\d_\d+[a-h]?\.(?:jpg|png)", src):
                if _banned(name):
                    hits.append((os.path.relpath(tex, ROOT), name))
        self.assertEqual(hits, [])

    def test_audita_reports_only_accepted_findings(self):
        audita = importlib.import_module("audita")
        problemas = audita.auditar(ROOT)
        self.assertEqual(sorted(set(problemas) - set(audita.EXCECOES)), [])
        # the accepted list is not stale either
        self.assertEqual(sorted(set(audita.EXCECOES) - set(problemas)), [])

    def test_book_material_not_tracked(self):
        if not os.path.isdir(os.path.join(ROOT, ".git")):
            self.skipTest("not a git checkout")
        try:
            out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                                 text=True, timeout=120)
        except OSError:
            self.skipTest("git not available")
        if out.returncode != 0:
            self.skipTest("git ls-files failed")
        tracked = out.stdout.splitlines()
        bad = [t for t in tracked if t.startswith(("book/", "extracted/"))
               or re.match(r"ferramentas/cap\d\d.*\.pdf$", t)
               or t.endswith((".aux", ".log", ".out", ".nav", ".snm", ".toc"))]
        self.assertEqual(bad, [])


class Notebooks(unittest.TestCase):
    def test_notebooks_form_23_pairs(self):
        nbs = [os.path.basename(p) for p in _notebooks()]
        self.assertEqual(len(nbs), 46)
        chapters = {re.match(r"cap(\d\d)", n).group(1) for n in nbs}
        self.assertEqual(sorted(chapters), [f"{i:02d}" for i in range(1, 24)])
        for c in chapters:
            self.assertIn(f"cap{c}_solucoes.ipynb", nbs)
            self.assertEqual(sum(1 for n in nbs if n.startswith(f"cap{c}_")), 2, c)

    def test_notebooks_have_no_error_or_stderr_outputs(self):
        bad = {}
        for p in _notebooks():
            nb = _load(p)
            err = sum(1 for c in nb["cells"] for o in c.get("outputs", [])
                      if o.get("output_type") == "error")
            se = sum(1 for c in nb["cells"] for o in c.get("outputs", [])
                     if o.get("output_type") == "stream" and o.get("name") == "stderr")
            if err or se:
                bad[os.path.basename(p)] = (err, se)
        self.assertEqual(bad, {})

    def test_notebooks_fully_executed(self):
        bad = {}
        for p in _notebooks():
            nb = _load(p)
            n = sum(1 for c in nb["cells"] if c["cell_type"] == "code"
                    and "".join(c["source"]).strip() and c.get("execution_count") is None)
            if n:
                bad[os.path.basename(p)] = n
        self.assertEqual(bad, {})

    def test_notebooks_under_size_cap(self):
        big = {os.path.basename(p): os.path.getsize(p) for p in _notebooks()
               if os.path.getsize(p) > MAX_NOTEBOOK_BYTES}
        self.assertEqual(big, {})


class DocsGuard(unittest.TestCase):
    def test_tool_flags_documented_in_agents_and_manual(self):
        agents, manual = _read("AGENTS.md"), _read("docs", "USER_MANUAL.md")
        for name in TOOLS + ("build_manual",):
            mod = importlib.import_module(name)
            parser = mod.build_parser()
            flags = {s for a in parser._actions for s in a.option_strings
                     if s.startswith("--") and s != "--help"}
            for f in sorted(flags):
                self.assertIn(f, agents, f"{name}: {f} missing from AGENTS.md")
                self.assertIn(f, manual, f"{name}: {f} missing from docs/USER_MANUAL.md")
            self.assertTrue(callable(getattr(mod, "main")), name)

    def test_readme_and_manual_counts_match_tree(self):
        readme, manual = _read("README.md"), _read("docs", "USER_MANUAL.md")
        n_nb = len(_notebooks())
        n_ch = len(glob.glob(os.path.join(ROOT, "notas", "cap*_notas.tex")))
        self.assertEqual((n_nb, n_ch), (46, 23))
        loader = unittest.TestLoader()
        n_checks = loader.loadTestsFromModule(sys.modules[__name__]).countTestCases()
        for doc, label in ((readme, "README.md"), (manual, "USER_MANUAL.md")):
            self.assertIn(f"{n_nb} notebooks", doc, label)
            self.assertIn(f"{n_ch} chapters", doc, label)
            self.assertIn(f"{n_checks}-check", doc, f"{label} must state the {n_checks}-check suite")
        self.assertIn("## 6. Every feature and every known limitation", manual)
        self.assertIn("Known limitations", manual)
        self.assertIn("USER_MANUAL.md", readme)
        self.assertIn("AGENTS.md", readme)

    def test_no_personal_paths_or_codenames(self):
        # needles assembled from fragments so this file does not trip itself
        needles = ["Users" + "/fabio", "Users" + "\\fabio", "g" + "mail.com",
                   "CLAUDE" + "_", "Desktop" + "\\", "/c/" + "Users/"]
        hits = []
        for pat in ("*.md", "*.py", "*.tex", "*.sty", "*.yml", "*.cff",
                    "ferramentas/*.py", "comum/*", "docs/*.md", "docs/*.py", "tests/*.py",
                    "notas/*.tex", "slides/*.tex", "guia_do_professor/*.tex", "listas/*.tex"):
            for f in glob.glob(os.path.join(ROOT, pat)):
                if not os.path.isfile(f):
                    continue
                src = _read(f)
                for n in needles:
                    if n in src:
                        hits.append((os.path.relpath(f, ROOT), n))
        for p in _notebooks():
            src = "\n".join("".join(c["source"]) for c in _load(p)["cells"])
            for n in needles:
                if n in src:
                    hits.append((os.path.relpath(p, ROOT), n))
        self.assertEqual(hits, [])


class ReadBack(unittest.TestCase):
    def test_committed_pdfs_read_back(self):
        try:
            import pymupdf
        except ImportError:
            self.skipTest("PyMuPDF not installed")
        expected_min = {"guia_do_professor/guia.pdf": 40, "listas/listas_exercicios.pdf": 23,
                        "indice.pdf": 2, "guia_do_professor/cronograma.pdf": 2,
                        "docs/USER_MANUAL.pdf": 3}
        pdfs = [os.path.relpath(p, ROOT).replace("\\", "/") for pat in
                ("slides/*.pdf", "notas/*.pdf", "guia_do_professor/*.pdf", "listas/*.pdf",
                 "indice.pdf", "docs/USER_MANUAL.pdf")
                for p in glob.glob(os.path.join(ROOT, pat))]
        self.assertGreaterEqual(len(pdfs), 49)
        for rel in pdfs:
            with self.subTest(pdf=rel):
                doc = pymupdf.open(os.path.join(ROOT, rel))
                self.assertGreaterEqual(doc.page_count, expected_min.get(rel, 2), rel)
                text = "".join(page.get_text() for page in doc)
                self.assertGreater(len(text.strip()), 200, f"{rel}: no extractable text")
                if rel.startswith(("slides/", "notas/")):
                    self.assertIn("Stull", text, f"{rel}: attribution missing")
        for rel in expected_min:
            self.assertIn(rel, pdfs, f"{rel} must be committed")


class Tools(unittest.TestCase):
    def test_manual_fallback_converter_closes_lists_before_tables_and_headings(self):
        # 1.0.1: a table or heading right after a list landed inside an unclosed <ul>
        bm = importlib.import_module("build_manual")
        out = bm.md_to_html_minimal("- item\n| a | b |\n|---|---|\n| 1 | 2 |\n- x\n## H\n")
        self.assertLess(out.index("</ul>"), out.index("<table>"))
        self.assertEqual(out.count("<ul>"), out.count("</ul>"))
        self.assertLess(out.rindex("</ul>"), out.index("<h2>"))
        self.assertNotIn("<ul>\n<li>x</li>\n<h2>", out)

    def test_gera_listas_runs_and_logs(self):
        gera = importlib.import_module("gera_listas")
        with tempfile.TemporaryDirectory() as tmp:
            rc = gera.main(["--outdir", tmp, "-q"])
            self.assertEqual(rc, 0)
            tex = _read(os.path.join(tmp, "listas_exercicios.tex"))
            self.assertEqual(tex.count("\\section*{Lista "), 23)
            self.assertIn("CC BY-NC-SA 4.0", tex)
            logs = glob.glob(os.path.join(tmp, "logs", "gera_listas-*.log"))
            self.assertEqual(len(logs), 1)
            body = _read(logs[0])
            self.assertIn("comando:", body)
            self.assertIn("RESULTADO: ok", body)

    def test_extract_plots_runs_and_logs(self):
        ep = importlib.import_module("extract_plots")
        with tempfile.TemporaryDirectory() as tmp:
            rc = ep.main(["--notebooks", "cap08_sensoriamento", "--outdir", tmp, "-q"])
            self.assertEqual(rc, 0)
            pngs = glob.glob(os.path.join(tmp, "cap08_sensoriamento_plot*.png"))
            self.assertGreaterEqual(len(pngs), 1)
            with open(pngs[0], "rb") as fh:
                self.assertEqual(fh.read(8), b"\x89PNG\r\n\x1a\n")
            self.assertTrue(glob.glob(os.path.join(tmp, "logs", "extract_plots-*.log")))
            # a missing notebook is reported, not silently skipped
            self.assertEqual(ep.main(["--notebooks", "nao_existe", "--outdir", tmp, "-q"]), 1)

    def test_audita_reports_a_missing_guide_instead_of_raising(self):
        # 1.0.2: check 8 opened guia.tex directly, so a tree without it was a
        # traceback rather than a listed problem
        audita = importlib.import_module("audita")
        with tempfile.TemporaryDirectory() as tmp:
            for d in ("notas", "slides", "notebooks", "guia_do_professor", "figuras"):
                os.makedirs(os.path.join(tmp, d))
            problemas = audita.auditar(tmp)
        self.assertTrue(any("guia.tex" in p and "ausente" in p for p in problemas), problemas)

    def test_audita_numbers_chapters_from_the_file_name_not_the_path(self):
        # 1.0.2: the chapter number was taken from the first "capNN" in the
        # full path, so a root folder named cap99 renumbered every chapter
        audita = importlib.import_module("audita")
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "cap99")
            for d in ("notas", "slides", "notebooks", "guia_do_professor", "figuras"):
                os.makedirs(os.path.join(root, d))
            with open(os.path.join(root, "notas", "cap01_notas.tex"), "w", encoding="utf-8") as fh:
                fh.write("\\veremos{0}\n")
            with open(os.path.join(root, "slides", "cap01_slides.tex"), "w", encoding="utf-8") as fh:
                fh.write("\\figlivroslide{fig_01_1.jpg}\n")
            problemas = audita.auditar(root)
        self.assertIn("notas cap01: \\veremos{0} fora de 1..23", problemas)
        self.assertIn("slides cap01: figura ausente: fig_01_1.jpg", problemas)
        self.assertFalse([p for p in problemas if "cap99" in p], problemas)

    def test_audita_lists_a_chapter_file_without_a_number_instead_of_raising(self):
        # 1.0.3 (post-review): capitulo_notas.tex matches the glob cap*_notas.tex
        # but carries no chapter number; that is a listed problem, not a traceback
        audita = importlib.import_module("audita")
        with tempfile.TemporaryDirectory() as tmp:
            for d in ("notas", "slides", "notebooks", "guia_do_professor", "figuras"):
                os.makedirs(os.path.join(tmp, d))
            for rel in (("notas", "capitulo_notas.tex"), ("slides", "capitulo_slides.tex")):
                with open(os.path.join(tmp, *rel), "w", encoding="utf-8") as fh:
                    fh.write("\\veremos{1}\n")
            with open(os.path.join(tmp, "notebooks", "capitulo_x.ipynb"), "w", encoding="utf-8") as fh:
                fh.write('{"cells": []}')
            problemas = audita.auditar(tmp)
        sem_numero = [p for p in problemas if "sem numero de capitulo" in p]
        self.assertEqual(len(sem_numero), 3, problemas)


class Community(unittest.TestCase):
    def test_community_files_present_and_linked(self):
        # publishing playbook rule 26: a public repository carries its
        # contribution guide, code of conduct and design account, and the
        # README points at the first two
        for rel in ("CONTRIBUTING.md", "CODE_OF_CONDUCT.md", os.path.join("docs", "DESIGN.md")):
            self.assertTrue(os.path.isfile(os.path.join(ROOT, rel)), rel)
        self.assertGreater(os.path.getsize(os.path.join(ROOT, "docs", "DESIGN.md")), 400)
        self.assertIn("Contributor Covenant", _read("CODE_OF_CONDUCT.md"))
        readme = _read("README.md")
        self.assertIn("CONTRIBUTING.md", readme)
        self.assertIn("CODE_OF_CONDUCT.md", readme)


if __name__ == "__main__":
    unittest.main()
