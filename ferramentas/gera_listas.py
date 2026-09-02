# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""gera_listas.py — gera ``listas/listas_exercicios.tex`` extraindo os
enunciados T1-T5 e N1-N4 de cada ``notas/capNN_notas.tex`` (fonte única: as
notas — nunca editar a lista à mão). Cada capítulo começa em página nova,
imprimível em separado.

    python ferramentas/gera_listas.py             # listas/listas_exercicios.tex
    python ferramentas/gera_listas.py --pdf       # ... e compila com pdflatex (2 passadas)
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402

CABECA = r"""% Listas de exercícios — geradas de notas/capNN_notas.tex por
% ferramentas/gera_listas.py — NÃO editar à mão; editar as notas e regerar.
\documentclass[11pt]{article}
\usepackage{../comum/preambulo}

\title{Listas de Exercícios Complementares\\
{\large Meteorologia Prática --- curso baseado em R.~Stull,
\emph{Practical Meteorology}}}
\author{}
\date{}

\newtcolorbox{caixalista}{colback=corquadro!6,colframe=corquadro,
  title={Instruções},fonttitle=\bfseries\small,
  before skip=8pt,after skip=8pt}
\newcommand{\instrucoes}{%
\begin{caixalista}
\textbf{Teóricos (T):} resolução escrita, individual, para entrega.\\
\textbf{Numéricos (N):} resolver nas células reservadas no notebook do
capítulo (\texttt{notebooks/capNN\_*.ipynb}) e entregar o
\texttt{.ipynb} executado.\\
Estas listas complementam os exercícios do próprio livro indicados no
guia do professor.
\end{caixalista}}

\begin{document}
\maketitle
\thispagestyle{fancy}

\noindent Uma lista por capítulo; cada uma começa em página nova para
impressão avulsa. Numeração: T$n$ (teóricos), N$n$ (numéricos, no
notebook do capítulo).

"""

RODAPE = r"""
\vspace{1em}
\noindent\rule{\linewidth}{0.4pt}\\
{\scriptsize Material derivado de R.~Stull, \emph{Practical Meteorology}
(CC BY-NC-SA 4.0); este documento herda a mesma licença.}
\end{document}
"""


def gerar(pasta_notas: str) -> tuple[str, list[str], list[str]]:
    """Devolve (tex completo, capítulos incluídos, notas sem exercícios)."""
    blocos, incluidos, sem = [], [], []
    for f in sorted(glob.glob(os.path.join(pasta_notas, "cap*_notas.tex"))):
        with open(f, encoding="utf-8") as fh:
            src = fh.read()
        m_tit = re.search(r"\\title\{(Cap[íi]tulo[^\\]+?)\\\\", src)
        titulo = m_tit.group(1).strip() if m_tit else os.path.basename(f)
        m_ex = re.search(r"(\\subsection\*\{Te[óo]ricos\}.*?)\\vspace\{1em\}", src, re.DOTALL)
        if not m_ex:
            sem.append(os.path.basename(f))
            continue
        corpo = m_ex.group(1).rstrip()
        num = re.search(r"cap(\d+)", os.path.basename(f)).group(1)
        corpo = corpo.replace("Numéricos (no notebook)", "Numéricos (no notebook do capítulo)")
        blocos.append("\\clearpage\n"
                      f"\\section*{{Lista {int(num)} --- {titulo}}}\n"
                      "\\instrucoes\n\n" + corpo + "\n")
        incluidos.append(f"cap{num}: {titulo}")
    return CABECA + "\n".join(blocos) + RODAPE, incluidos, sem


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Gera as listas de exercícios a partir das notas.")
    p.add_argument("--notas", default=os.path.join(registro.ROOT, "notas"), metavar="PASTA",
                   help="pasta das notas capNN_notas.tex (padrão: notas/)")
    p.add_argument("--outdir", default=os.path.join(registro.ROOT, "listas"), metavar="PASTA",
                   help="pasta de saída do .tex (padrão: listas/)")
    p.add_argument("--pdf", action="store_true",
                   help="compila o .tex com pdflatex (duas passadas) na pasta de saída")
    return registro.adicionar_comuns(p)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    log = registro.iniciar("gera_listas", args, args.outdir)
    tex, incluidos, sem = gerar(args.notas)
    for s in sem:
        log.warning("SEM EXERCICIOS: %s", s)
    for i in incluidos:
        log.info("ok %s", i)
    destino = os.path.join(args.outdir, "listas_exercicios.tex")
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(tex)
    log.info("%d listas -> %s", len(incluidos), destino)
    ok = bool(incluidos) and not sem
    if args.pdf and ok:
        pdflatex = shutil.which("pdflatex")
        if not pdflatex:
            return registro.concluir(log, False, "pdflatex não encontrado no PATH")
        for passada in (1, 2):
            proc = subprocess.run([pdflatex, "-interaction=nonstopmode", "-halt-on-error",
                                   os.path.basename(destino)],
                                  cwd=args.outdir, capture_output=True, text=True)
            log.debug("pdflatex passada %d rc=%d", passada, proc.returncode)
            if proc.returncode != 0:
                log.error("%s", proc.stdout[-1500:])
                return registro.concluir(log, False, f"pdflatex falhou na passada {passada}")
        log.info("pdf: %s", destino[:-4] + ".pdf")
    return registro.concluir(log, ok, f"({len(incluidos)} listas)")


if __name__ == "__main__":
    sys.exit(main())
