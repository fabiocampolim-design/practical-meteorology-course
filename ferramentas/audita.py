# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""audita.py — auditoria de consistência do material do curso.

Verifica: figuras citadas nos slides existem; nenhum placeholder sobrou;
``\\javimos``/``\\veremos`` apontam para capítulos válidos e na direção
certa; casos citados nas notas existem nos notebooks; pares aluno/soluções
completos, 4 casos e 4 enunciados N por notebook do aluno, 5 T + 4 N nas
soluções, nenhuma célula com erro; 5 T + 4 N nas notas; sobras da antiga
confusão cap. 22 = clima; guia com os 23 capítulos.

    python ferramentas/audita.py            # lista os problemas, sai 1 se houver
    python ferramentas/audita.py --json relatorio.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro  # noqa: E402

# Falsos positivos conhecidos e aceitos (template do cap. 1 aprovado em
# 2026-08-22: 5 casos, e os enunciados N ficam nas notas, não no notebook).
# A suíte compara o resultado com esta lista.
EXCECOES = (
    "cap01_fundamentos.ipynb: 5 casos (esperado 4)",
    "cap01_fundamentos.ipynb: 0 enunciados N (esperado 4)",
)


def _ler(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _cap(f: str) -> str:
    """Número do capítulo lido do NOME do arquivo, nunca do caminho: uma pasta
    chamada cap99 no caminho renumerava todos os capítulos (1.0.1)."""
    return re.search(r"cap(\d+)", os.path.basename(f)).group(1)


def auditar(root: str) -> list[str]:
    """Devolve a lista de problemas encontrados (vazia = tudo certo)."""
    problemas: list[str] = []
    P = problemas.append

    # 1. figuras citadas nos slides existem?
    for f in sorted(glob.glob(os.path.join(root, "slides", "cap*_slides.tex"))):
        nn = _cap(f)
        src = _ler(f)
        figdir = os.path.join(root, "figuras", f"cap{nn}")
        usados = re.findall(r"\\figlivroslide\{([^}]+)\}", src)
        usados += re.findall(r"\\includegraphics\[[^]]*\]\{([^}]+)\}", src)
        for u in usados:
            if not os.path.exists(os.path.join(figdir, u)):
                P(f"slides cap{nn}: figura ausente: {u}")

    # 2. placeholders remanescentes
    for f in glob.glob(os.path.join(root, "slides", "*.tex")) + \
            glob.glob(os.path.join(root, "notas", "*.tex")):
        if "figplaceholder" in _ler(f):
            P(f"placeholder remanescente em {os.path.basename(f)}")

    # 3. \javimos/\veremos: alvo 1..23 e direção certa
    for f in sorted(glob.glob(os.path.join(root, "notas", "cap*_notas.tex"))):
        nn = int(_cap(f))
        src = _ler(f)
        for m in re.finditer(r"\\(javimos|veremos)\{(\d+)\}", src):
            alvo = int(m.group(2))
            if not 1 <= alvo <= 23:
                P(f"notas cap{nn:02d}: \\{m.group(1)}{{{alvo}}} fora de 1..23")
            if m.group(1) == "veremos" and alvo < nn:
                P(f"notas cap{nn:02d}: \\veremos{{{alvo}}} aponta para tras")
            if m.group(1) == "javimos" and alvo > nn:
                P(f"notas cap{nn:02d}: \\javimos{{{alvo}}} aponta para frente")

    # 4. "Caso N" citado nas notas: notebooks têm 4 casos
    for f in sorted(glob.glob(os.path.join(root, "notas", "cap*_notas.tex"))):
        nn = int(_cap(f))
        for m in re.finditer(r"Caso~(\d+)", _ler(f)):
            if int(m.group(1)) > 4:
                P(f"notas cap{nn:02d}: cita Caso~{m.group(1)} (>4)")

    # 5. notebooks: pares aluno/soluções, casos e exercícios, erros
    nbs = sorted(glob.glob(os.path.join(root, "notebooks", "cap*.ipynb")))
    temas, sols = {}, {}
    for f in nbs:
        base = os.path.basename(f)
        nn = re.search(r"cap(\d+)", base).group(1)
        (sols if "_solucoes" in base else temas)[nn] = f
    for nn in sorted(set(temas) | set(sols)):
        if nn not in temas:
            P(f"cap{nn}: falta notebook do aluno")
        if nn not in sols:
            P(f"cap{nn}: falta notebook de soluções")

    def _erros(nb):
        return sum(1 for c in nb["cells"] for o in c.get("outputs", [])
                   if o.get("output_type") == "error")

    for nn, f in sorted(temas.items()):
        nb = json.loads(_ler(f))
        txt = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
        ncasos = len(re.findall(r"## Caso \d", txt))
        n_ex = len(re.findall(r"\*\*N\d\*\*", txt))
        if ncasos != 4:
            P(f"{os.path.basename(f)}: {ncasos} casos (esperado 4)")
        if n_ex != 4:
            P(f"{os.path.basename(f)}: {n_ex} enunciados N (esperado 4)")
        n_err = _erros(nb)
        if n_err:
            P(f"{os.path.basename(f)}: {n_err} celulas com ERRO")
    for nn, f in sorted(sols.items()):
        nb = json.loads(_ler(f))
        txt = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
        nT = len(re.findall(r"## T\d", txt))
        nN = len(re.findall(r"## N\d", txt))
        if nT != 5 or nN != 4:
            P(f"{os.path.basename(f)}: {nT} solucoes T (esp. 5), {nN} N (esp. 4)")
        n_err = _erros(nb)
        if n_err:
            P(f"{os.path.basename(f)}: {n_err} celulas com ERRO")

    # 6. exercícios nas notas: 5 T e 4 N por capítulo
    for f in sorted(glob.glob(os.path.join(root, "notas", "cap*_notas.tex"))):
        nn = int(_cap(f))
        src = _ler(f)
        m = re.search(r"\\subsection\*\{Te[óo]ricos\}(.*?)\\subsection\*\{Num", src, re.DOTALL)
        m2 = re.search(r"\\subsection\*\{Num[ée]ricos[^}]*\}(.*?)\\vspace\{1em\}", src, re.DOTALL)
        nT = len(re.findall(r"\\item", m.group(1))) if m else 0
        nN = len(re.findall(r"\\item", m2.group(1))) if m2 else 0
        if nT != 5 or nN != 4:
            P(f"notas cap{nn:02d}: {nT} exercicios T (esp. 5), {nN} N (esp. 4)")

    # 7. sobras de referências erradas (cap. 22 é óptica, não clima)
    for f in glob.glob(os.path.join(root, "notas", "*.tex")) + \
            glob.glob(os.path.join(root, "guia_do_professor", "*.tex")) + \
            glob.glob(os.path.join(root, "slides", "*.tex")):
        src = _ler(f)
        if re.search(r"Cap\.?~?\s*22[^0-9]{0,40}(clim|carbono|CO)", src):
            P(f"{os.path.basename(f)}: possivel referencia cap22=clima")
        if "cap22_mudanca" in src or "cap22\\_mudanca" in src:
            P(f"{os.path.basename(f)}: cita cap22_mudanca (renomeado p/ 23)")

    # 8. guia: todos os capítulos incluídos (guia ausente é um problema
    # listado, não um traceback -- 1.0.1)
    guia = os.path.join(root, "guia_do_professor", "guia.tex")
    if not os.path.isfile(guia):
        P("guia.tex: ausente em guia_do_professor/")
    else:
        gsrc = _ler(guia)
        for nn in range(1, 24):
            if f"cap{nn:02d}_guia" not in gsrc:
                P(f"guia.tex: falta \\input de cap{nn:02d}_guia")
    return problemas


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Auditoria de consistência do material do curso.")
    p.add_argument("--root", default=registro.ROOT, metavar="PASTA",
                   help="raiz do material (padrão: a raiz deste repositório)")
    p.add_argument("--json", default=None, metavar="ARQUIVO",
                   help="grava a lista de problemas em JSON")
    return registro.adicionar_comuns(p)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    log = registro.iniciar("audita", args, args.root)
    problemas = auditar(args.root)
    novos = [p for p in problemas if p not in EXCECOES]
    log.info("%d problema(s) encontrado(s), %d conhecido(s) e aceito(s):",
             len(problemas), len(problemas) - len(novos))
    for p in problemas:
        log.info(" - %s%s", p, "  [aceito]" if p in EXCECOES else "")
    if not problemas:
        log.info(" (nenhum)")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"problemas": problemas, "aceitos": list(EXCECOES)}, fh,
                      ensure_ascii=False, indent=2)
        log.info("relatório: %s", args.json)
    return registro.concluir(log, not novos, f"({len(novos)} problema(s) novo(s))")


if __name__ == "__main__":
    sys.exit(main())
