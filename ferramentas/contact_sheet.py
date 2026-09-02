# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""contact_sheet.py — folha de contato (grade de miniaturas rotuladas) das
figuras de um capítulo, para conferir o mapeamento fig_NN_X a olho.

    python ferramentas/contact_sheet.py 5                 # qa/contato_cap05.png
    python ferramentas/contact_sheet.py 5 --out c5.png --cols 8 --dpi 100
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Folha de contato das figuras de um capítulo.")
    p.add_argument("capitulo", help="número do capítulo (1-23)")
    p.add_argument("--figuras", default=os.path.join(registro.ROOT, "figuras"), metavar="PASTA",
                   help="pasta com as subpastas capNN/ (padrão: figuras/)")
    p.add_argument("--out", default=None, metavar="PNG",
                   help="arquivo de saída (padrão: qa/contato_capNN.png)")
    p.add_argument("--cols", type=int, default=6, help="colunas da grade (padrão: 6)")
    p.add_argument("--dpi", type=int, default=80, help="resolução da folha (padrão: 80)")
    return registro.adicionar_comuns(p)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    nn = args.capitulo.zfill(2)
    out = args.out or os.path.join(registro.ROOT, "qa", f"contato_cap{nn}.png")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    log = registro.iniciar("contact_sheet", args, os.path.dirname(os.path.abspath(out)))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    log.debug("matplotlib %s", matplotlib.__version__)

    d = os.path.join(args.figuras, f"cap{nn}")
    if not os.path.isdir(d):
        return registro.concluir(log, False, f"pasta inexistente: {d}")
    files = sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".png")))
    n = len(files)
    if n == 0:
        return registro.concluir(log, False, f"nenhuma figura em {d}")
    cols = max(1, args.cols)
    rows = math.ceil(n / cols)
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2.6, rows * 2.4), squeeze=False)
    axs = axs.ravel()
    for ax in axs[n:]:
        ax.axis("off")
    for ax, f in zip(axs, files):
        ax.imshow(mpimg.imread(os.path.join(d, f)))
        ax.set_title(f, fontsize=7)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=args.dpi)
    plt.close(fig)
    log.info("ok %s (%d figuras)", out, n)
    return registro.concluir(log, True, f"{n} figuras -> {out}")


if __name__ == "__main__":
    sys.exit(main())
