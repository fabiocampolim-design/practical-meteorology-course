# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""slice.py — recorta um intervalo de páginas do PDF do livro (que você baixa
da UBC; não é distribuído aqui) para alimentar o extrator, uma fatia por vez.
Requer PyMuPDF.

    python ferramentas/slice.py 17 42 cap01           # ferramentas/cap01.pdf
    python ferramentas/slice.py 17 42 cap01 --book /caminho/Practical_Meteorology.pdf --outdir fatias
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402

LIVRO_PADRAO = os.path.join(registro.ROOT, "book", "Practical_Meteorology-v1.02b-WholeBookColor.pdf")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Recorta páginas do PDF do livro para o extrator.")
    p.add_argument("primeira", type=int, help="primeira página do PDF (1 = capa)")
    p.add_argument("ultima", type=int, help="última página do PDF, inclusive")
    p.add_argument("nome", help="nome da fatia (sem extensão), ex. cap05b")
    p.add_argument("--book", default=LIVRO_PADRAO, metavar="PDF",
                   help="PDF do livro (padrão: book/Practical_Meteorology-v1.02b-WholeBookColor.pdf)")
    p.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)), metavar="PASTA",
                   help="pasta da fatia (padrão: ferramentas/)")
    return registro.adicionar_comuns(p)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    log = registro.iniciar("slice", args, args.outdir)
    try:
        import pymupdf
    except ImportError:
        return registro.concluir(log, False, "PyMuPDF não instalado (pip install pymupdf)")
    if not os.path.isfile(args.book):
        return registro.concluir(log, False, f"livro não encontrado: {args.book} "
                                            "(baixe-o de eoas.ubc.ca/books/Practical_Meteorology/)")
    if not 1 <= args.primeira <= args.ultima:
        return registro.concluir(log, False, "intervalo inválido: 1 <= primeira <= ultima")
    doc = pymupdf.open(args.book)
    if args.ultima > doc.page_count:
        return registro.concluir(log, False, f"o livro tem {doc.page_count} páginas")
    out = pymupdf.open()
    out.insert_pdf(doc, from_page=args.primeira - 1, to_page=args.ultima - 1)
    dest = os.path.join(args.outdir, args.nome + ".pdf")
    out.save(dest)
    log.info("saved %s (%d páginas)", dest, out.page_count)
    return registro.concluir(log, True, f"({out.page_count} páginas -> {dest})")


if __name__ == "__main__":
    sys.exit(main())
