# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""registro.py — logging comum das ferramentas do curso.

Toda ferramenta em ``ferramentas/`` usa este módulo: ``adicionar_comuns``
dá ao parser as opções ``-v/--verbose``, ``-q/--quiet`` e ``--log-dir``;
``iniciar`` liga o console e um arquivo de log por execução
(``<pasta de saída>/logs/<nome>-<UTC>.log``) registrando a linha de comando,
as versões e, ao final, o resultado (``concluir``).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import os
import platform
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def versao() -> str:
    """Versão do material (arquivo VERSION na raiz)."""
    try:
        with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return "desconhecida"


def adicionar_comuns(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Acrescenta as opções comuns a um parser."""
    g = parser.add_argument_group("registro")
    g.add_argument("-v", "--verbose", action="store_true",
                   help="mostra mensagens de depuração no console")
    g.add_argument("-q", "--quiet", action="store_true",
                   help="só avisos e erros no console (o arquivo de log é completo)")
    g.add_argument("--log-dir", default=None, metavar="PASTA",
                   help="pasta dos arquivos de log (padrão: <pasta de saída>/logs)")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s (practical-meteorology-course {versao()})")
    return parser


def iniciar(nome: str, args: argparse.Namespace, pasta_saida: str) -> logging.Logger:
    """Configura o logger ``nome``: console + arquivo em ``pasta_saida/logs``."""
    log = logging.getLogger(nome)
    log.setLevel(logging.DEBUG)
    log.propagate = False
    for h in list(log.handlers):
        log.removeHandler(h)
        h.close()
    console = logging.StreamHandler(sys.stdout)
    nivel = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    if getattr(args, "quiet", False):
        nivel = logging.WARNING
    console.setLevel(nivel)
    console.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(console)

    pasta_log = getattr(args, "log_dir", None) or os.path.join(pasta_saida, "logs")
    os.makedirs(pasta_log, exist_ok=True)
    carimbo = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    arquivo = os.path.join(pasta_log, f"{nome}-{carimbo}.log")
    fh = logging.FileHandler(arquivo, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(fh)

    log.debug("comando: %s", " ".join(sys.argv) if sys.argv else nome)
    log.debug("practical-meteorology-course %s | python %s | %s",
              versao(), platform.python_version(), platform.platform())
    log.debug("log: %s", arquivo)
    return log


def concluir(log: logging.Logger, ok: bool, resumo: str = "") -> int:
    """Registra o resultado, fecha o arquivo e devolve o código de saída."""
    if ok:
        log.info("RESULTADO: ok %s", resumo)
    else:
        log.error("RESULTADO: FALHA %s", resumo)
    for h in list(log.handlers):
        h.flush()
        if isinstance(h, logging.FileHandler):
            log.removeHandler(h)
            h.close()
    return 0 if ok else 1
