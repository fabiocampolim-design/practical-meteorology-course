# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""render_qa.py — renderiza páginas de amostra dos PDFs compilados (slides,
notas, guia) em PNG para QA visual. ``--fase 1`` é o plano dos caps. 1-11,
``--fase 2`` o dos caps. 12-14 + notas + guia (era o antigo render_qa2.py),
``--fase all`` os dois. Requer PyMuPDF.

    python ferramentas/render_qa.py                      # qa/render/, fase all
    python ferramentas/render_qa.py --fase 2 --dpi 90 --outdir qa/f2
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402

PLANOS = {
    "1": [("slides/cap01_slides.pdf", [3]), ("slides/cap02_slides.pdf", [4, 6]),
          ("slides/cap03_slides.pdf", [4]), ("slides/cap05_slides.pdf", [2, 9]),
          ("slides/cap07_slides.pdf", [6]), ("slides/cap08_slides.pdf", [3]),
          ("slides/cap09_slides.pdf", [4]), ("slides/cap10_slides.pdf", [5, 10]),
          ("slides/cap11_slides.pdf", [3, 5])],
    "2": [("slides/cap12_slides.pdf", [4, 7]), ("slides/cap13_slides.pdf", [2, 8]),
          ("slides/cap14_slides.pdf", [3, 9]), ("notas/cap12_notas.pdf", [0]),
          ("notas/cap16_notas.pdf", [1]), ("guia_do_professor/guia.pdf", [30])],
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Renderiza páginas de amostra dos PDFs para QA visual.")
    p.add_argument("--root", default=registro.ROOT, metavar="PASTA",
                   help="raiz do material (padrão: a raiz deste repositório)")
    p.add_argument("--outdir", default=os.path.join(registro.ROOT, "qa", "render"), metavar="PASTA",
                   help="pasta dos PNG (padrão: qa/render/)")
    p.add_argument("--fase", choices=("1", "2", "all"), default="all",
                   help="qual plano de amostras renderizar (padrão: all)")
    p.add_argument("--dpi", type=int, default=60, help="resolução das amostras (padrão: 60)")
    return registro.adicionar_comuns(p)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    log = registro.iniciar("render_qa", args, args.outdir)
    try:
        import pymupdf
    except ImportError:
        return registro.concluir(log, False, "PyMuPDF não instalado (pip install pymupdf)")
    log.debug("pymupdf %s", pymupdf.__version__)
    fases = ["1", "2"] if args.fase == "all" else [args.fase]
    k, faltando = 0, []
    for fase in fases:
        for rel, pages in PLANOS[fase]:
            caminho = os.path.join(args.root, rel)
            if not os.path.isfile(caminho):
                faltando.append(rel)
                log.warning("PDF ausente: %s", rel)
                continue
            d = pymupdf.open(caminho)
            tag = os.path.splitext(os.path.basename(rel))[0]
            for p in pages:
                if p >= d.page_count:
                    log.warning("%s: página %d fora do PDF (%d páginas)", rel, p, d.page_count)
                    continue
                dest = os.path.join(args.outdir, f"qa_f{fase}_{tag}_p{p}.png")
                d[p].get_pixmap(dpi=args.dpi).save(dest)
                k += 1
                log.debug("%s", dest)
    log.info("ok %d página(s) em %s", k, args.outdir)
    return registro.concluir(log, not faltando, f"({k} páginas, {len(faltando)} PDF ausentes)")


if __name__ == "__main__":
    sys.exit(main())
