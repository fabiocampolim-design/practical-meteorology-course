# Estado do projeto — CURSO COMPLETO (2026-08-27)

Curso *Meteorologia Prática* (Stull, CC BY-NC-SA 4.0). **Todos os 22
capítulos do livro + 1 módulo extra estão prontos**, cada um com:
notas LaTeX (roteiro de quadro com caixas `noquadro` + refs cruzadas
`\javimos`/`\veremos`), slides Beamer (todas as figuras do livro),
seção no guia do professor, notebook do aluno (4 casos + células N
vazias) e notebook de soluções (T1–T5 com sympy + N1–N4), todos
executados e com QA (sem erros/stderr no JSON).

## Estrutura final

- Caps. 1–22 = os capítulos do livro do Stull. **ATENÇÃO: o cap. 22
  do livro é ÓPTICA ATMOSFÉRICA** (arco-íris, halos, Rayleigh,
  miragens) — corrigido em 27/08 (originalmente havia sido escrito
  como "mudança climática" por engano).
- **Cap. 23 = módulo extra "Mudança Climática"** (não é capítulo do
  Stull; a base natural do clima é o cap. 21 do livro). Slides do 23
  usam figuras dos próprios notebooks (não há figuras de livro).
- Guia do professor: `guia.pdf` com 47 pp, caps. 1–23.
- Notebooks: 46 arquivos (23 pares aluno/soluções).
- Figuras: `figuras/capNN/fig_NN_X.jpg` mapeadas automaticamente das
  extrações MinerU (`ferramentas/map_figs.py`); conferidas via
  `contact_sheet.py`. Fig 7.13 (© Libbrecht) **não redistribuir**.

## Ferramentas (`ferramentas/`)

`slice.py` (fatia o PDF do livro), `map_figs.py NN` (auto-mapeia
crops→fig_NN_X.jpg), `contact_sheet.py NN out.png` (grade de conferência),
`render_qa.py`/`render_qa2.py` (QA visual dos PDFs).
Extração: `conda run -n pdfextract python <pdf-extract checkout>/extract.py <fatia> --out extracted --fallback`
(~4–11 min/fatia; RODAR EM FOREGROUND — background era morto com
frequência nesta máquina).

## Ambiente

- conda `meteo` (py 3.11): MetPy 1.7.1, climlab 0.9.2 (pip! conda-forge
  0.8.2 quebra com numpy 2), ambiance, pyrcel, tcpypi, sympy,
  ipywidgets, matplotlib<3.11 (pinado), numpy 2.4 (pip).
- conda `pdfextract`: MinerU + pymupdf. TeX Live 2026.

## Materiais de apoio (28/08)

- `listas/listas_exercicios.pdf` (24 pp): uma lista por capítulo
  (T1–T5 + N1–N4, sem soluções), cada uma em página própria para
  impressão avulsa. GERADA de notas/capNN_notas.tex por
  `ferramentas/gera_listas.py` — editar as NOTAS e regerar, nunca
  editar a lista à mão.
- `guia_do_professor/cronograma.pdf` (3 pp): sequência de DOIS
  semestres (I: caps. 1–11; II: caps. 12–23), 15 semanas cada,
  2×2h/semana, com listas entregues na semana seguinte, P1/P2 por
  semestre, avaliação sugerida (provas 50% / listas+notebooks 30% /
  projeto final 20%) e uma trilha compacta opcional de 1 semestre.

## Auditoria de escopo (28/08)

`ferramentas/audita.py` roda as checagens automáticas (figuras citadas
existem, sem placeholders, \javimos/\veremos coerentes, 4 casos + 9
exercícios por capítulo, notebooks sem erro, guia completo). Cobertura
conferida seção a seção contra os TOCs de `extracted/capNN.md`; lacunas
preenchidas em 28/08: actinômetros (2.5), wind chill + sensores
(3.7-3.8), medida de precipitação (7.8), perfilador de vento (8.3),
antitríptico + anemômetros + cinemática (10.5/10.9/10.10), tipos de
vorticidade/PV + monções (11.9/11.7), sting jet (12.7), PV + ciclogênese
de sotavento (13.3), índices operacionais (14.7), Weibull/Betz + jato
costeiro + canopy (17.1-2/17.6/17.11), tectônica + GCMs + Köppen
(21.3/21.6/21.7, com slide novo fig_21_25). Corrigido: limiares da
escala EF no cap15_solucoes (agora oficiais: 29/38/50/61/74/89 m/s).
Omissões conscientes (nível curiosidade): guia rápido de identificação
de diagramas (5.4), códigos SYNOP em detalhe (9.2), MOS (20.5), raios
crepusculares (22). Falsos positivos conhecidos do audita.py: cap01 tem
5 casos e enunciados N nas notas (template aprovado).

## Pendências / próximos passos possíveis

- `indice.pdf` na raiz (28/08): índice geral do curso — visão geral,
  as cinco peças por capítulo, tabela dos 23 capítulos com temas dos
  notebooks, materiais transversais, quickstart e licença. README.md
  aponta para ele.
- Datas reais no cronograma quando o calendário acadêmico sair.
- Os .md mesclados em `extracted/capNN.md` servem de referência
  textual completa do livro por capítulo.

## Armadilhas conhecidas (poupam horas)

- Unicode (Γ, ≈, ✓, φ) quebra o pdflatex — usar comandos LaTeX.
- numpy 2: `np.trapezoid`; nada de `float()` em array len-1.
- pint/MetPy: converter `.to('K')` antes de somar; Skew-T: labels
  manuais.
- `conda run python -c` multilinha engole saída → usar arquivo .py.
- nbconvert: executar UM notebook por comando; QA via scan do JSON
  (exit 0 não basta).
- PDF aberto no leitor trava o pdflatex (usar -jobname e renomear).
- Vírgula decimal nas anotações de plots: `.replace('.', ',')`.
