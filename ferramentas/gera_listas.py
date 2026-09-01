# Gera listas/listas_exercicios.tex extraindo os enunciados T1-T5 e N1-N4
# de cada notas/capNN_notas.tex (fonte única: as notas). Cada capítulo
# começa em página nova — imprimível por capítulo.
import os, re, glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(root, 'listas')
os.makedirs(out_dir, exist_ok=True)

cabeca = r"""% Listas de exercícios — geradas de notas/capNN_notas.tex por
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

rodape = r"""
\vspace{1em}
\noindent\rule{\linewidth}{0.4pt}\\
{\scriptsize Material derivado de R.~Stull, \emph{Practical Meteorology}
(CC BY-NC-SA 4.0); este documento herda a mesma licença.}
\end{document}
"""

blocos = []
for f in sorted(glob.glob(os.path.join(root, 'notas', 'cap*_notas.tex'))):
    src = open(f, encoding='utf-8').read()
    m_tit = re.search(r'\\title\{(Cap[íi]tulo[^\\]+?)\\\\', src)
    titulo = m_tit.group(1).strip() if m_tit else os.path.basename(f)
    m_ex = re.search(r'(\\subsection\*\{Te[óo]ricos\}.*?)\\vspace\{1em\}',
                     src, re.DOTALL)
    if not m_ex:
        print('SEM EXERCICIOS:', f)
        continue
    corpo = m_ex.group(1).rstrip()
    num = re.search(r'cap(\d+)', os.path.basename(f)).group(1)
    corpo = corpo.replace('Numéricos (no notebook)',
                          'Numéricos (no notebook do capítulo)')
    blocos.append(
        '\\clearpage\n'
        f'\\section*{{Lista {int(num)} --- {titulo}}}\n'
        '\\instrucoes\n\n' + corpo + '\n')
    print(f'ok cap{num}: {titulo}')

with open(os.path.join(out_dir, 'listas_exercicios.tex'), 'w',
          encoding='utf-8') as fh:
    fh.write(cabeca + '\n'.join(blocos) + rodape)
print(f'\n{len(blocos)} listas -> listas/listas_exercicios.tex')
