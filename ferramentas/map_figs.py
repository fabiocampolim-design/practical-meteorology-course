# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""map_figs.py — mapeia os recortes de figura do extrator (MinerU, em
``extracted/capNN*.md`` + ``capNN*_assets/``) para ``figuras/capNN/fig_NN_X.jpg``.
Regra: cada legenda "Figure N.M" recebe as imagens acumuladas desde a legenda
anterior; mais de uma imagem => sufixos a, b, c...

Requer a extração local do livro (não distribuída): ver docs/USER_MANUAL.md.

    python ferramentas/map_figs.py 5
    python ferramentas/map_figs.py 5 --extracted extracted --figuras figuras
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402

IMG_RE = re.compile(r"!\[\]\(images/([0-9a-f]+\.jpg)\)")
FIG_RE = re.compile(r"^#*\s*Figure\s+(\d+)\.(\d+[a-z]?)", re.IGNORECASE)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Mapeia recortes do extrator para figuras/capNN/.")
    p.add_argument("capitulo", help="número do capítulo (1-22)")
    p.add_argument("--extracted", default=os.path.join(registro.ROOT, "extracted"), metavar="PASTA",
                   help="saída do extrator: capNN*.md + capNN*_assets/ (padrão: extracted/)")
    p.add_argument("--figuras", default=os.path.join(registro.ROOT, "figuras"), metavar="PASTA",
                   help="destino: <PASTA>/capNN/fig_NN_X.jpg (padrão: figuras/)")
    return registro.adicionar_comuns(p)


def mapear(nn: str, ext: str, dest: str):
    """Copia os recortes; devolve (mapeadas, faltando)."""
    mds = sorted(glob.glob(os.path.join(ext, f"cap{nn}[a-z]*.md")))
    merged = os.path.join(ext, f"cap{nn}.md")
    if os.path.exists(merged):
        mds = [merged]
    if not mds:
        raise FileNotFoundError(f"nenhum .md para cap{nn} em {ext}")
    assets = {}
    for d in glob.glob(os.path.join(ext, f"cap{nn}*_assets")):
        for f in os.listdir(d):
            assets[f] = os.path.join(d, f)
    os.makedirs(dest, exist_ok=True)
    mapped, missing, pend = [], [], []
    for md in mds:
        with open(md, encoding="utf-8") as fh:
            for line in fh:
                m = IMG_RE.search(line)
                if m:
                    pend.append(m.group(1))
                    continue
                f = FIG_RE.match(line.strip())
                if f and pend:
                    cap, num = f.group(1), f.group(2)
                    sufs = [""] if len(pend) == 1 else list("abcdefgh"[:len(pend)])
                    for img, suf in zip(pend, sufs):
                        name = f"fig_{int(cap):02d}_{num}{suf}.jpg"
                        if img in assets:
                            shutil.copyfile(assets[img], os.path.join(dest, name))
                            mapped.append(name)
                        else:
                            missing.append((name, img))
                    pend = []
                elif f:
                    missing.append((f"fig_{int(f.group(1)):02d}_{f.group(2)}", "SEM IMAGEM"))
    return mapped, missing


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    nn = args.capitulo.zfill(2)
    dest = os.path.join(args.figuras, f"cap{nn}")
    os.makedirs(dest, exist_ok=True)
    log = registro.iniciar("map_figs", args, args.figuras)
    try:
        mapped, missing = mapear(nn, args.extracted, dest)
    except FileNotFoundError as e:
        return registro.concluir(log, False, str(e))
    log.info("cap%s: %d mapeadas -> %s", nn, len(mapped), dest)
    log.info("%s", " ".join(mapped))
    if missing:
        log.warning("FALTANDO: %s", missing)
    return registro.concluir(log, True, f"({len(mapped)} mapeadas, {len(missing)} faltando)")


if __name__ == "__main__":
    sys.exit(main())
