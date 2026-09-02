# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""extract_plots.py — extrai as figuras (image/png) das saídas dos notebooks
executados para arquivos PNG, para reaproveitar em slides ou conferir.

    python ferramentas/extract_plots.py                       # todos os notebooks do aluno
    python ferramentas/extract_plots.py --notebooks cap04_vapor cap06_nuvens --outdir qa/plots
"""

from __future__ import annotations

import argparse
import base64
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Extrai as figuras PNG das saídas dos notebooks.")
    p.add_argument("--notebooks", nargs="*", default=None, metavar="NOME",
                   help="nomes sem extensão (padrão: todos os notebooks do aluno)")
    p.add_argument("--pasta-notebooks", default=os.path.join(registro.ROOT, "notebooks"),
                   metavar="PASTA", help="onde estão os .ipynb (padrão: notebooks/)")
    p.add_argument("--outdir", default=os.path.join(registro.ROOT, "qa", "plots"), metavar="PASTA",
                   help="pasta dos PNG (padrão: qa/plots/)")
    return registro.adicionar_comuns(p)


def extrair(caminho: str, outdir: str, prefixo: str) -> list[str]:
    """Grava cada image/png das saídas de ``caminho`` como ``<prefixo>_plotNN.png``."""
    with open(caminho, encoding="utf-8") as fh:
        nb = json.load(fh)
    escritos = []
    for cell in nb["cells"]:
        for out in cell.get("outputs", []):
            data = out.get("data", {})
            if "image/png" in data:
                dest = os.path.join(outdir, f"{prefixo}_plot{len(escritos) + 1:02d}.png")
                with open(dest, "wb") as fh:
                    fh.write(base64.b64decode(data["image/png"]))
                escritos.append(dest)
    return escritos


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    log = registro.iniciar("extract_plots", args, args.outdir)
    if args.notebooks:
        nomes = list(args.notebooks)
    else:
        nomes = sorted(os.path.splitext(os.path.basename(f))[0]
                       for f in glob.glob(os.path.join(args.pasta_notebooks, "cap*.ipynb"))
                       if "_solucoes" not in f)
    total, faltando = 0, []
    for nome in nomes:
        caminho = os.path.join(args.pasta_notebooks, nome + ".ipynb")
        if not os.path.isfile(caminho):
            faltando.append(nome)
            log.warning("notebook inexistente: %s", caminho)
            continue
        escritos = extrair(caminho, args.outdir, nome)
        total += len(escritos)
        log.info("%s: %d figura(s)", nome, len(escritos))
    return registro.concluir(log, not faltando, f"({total} PNG em {args.outdir})")


if __name__ == "__main__":
    sys.exit(main())
