# Meteorologia Prática — material de curso

Material didático completo (notas de aula, slides, guia do professor,
notebooks de simulação, listas de exercícios e cronograma) para um curso de
graduação em Meteorologia Prática — 22 capítulos + 1 módulo extra, em dois
semestres — baseado em:

> Roland Stull, **Practical Meteorology: An Algebra-based Survey of
> Atmospheric Science**, versão 1.02b, University of British Columbia.
> Disponível em: https://www.eoas.ubc.ca/books/Practical_Meteorology/

**Comece por `indice.pdf`** — o índice geral do curso, com o mapa de todos
os materiais.

## Licença

O livro de Stull é licenciado sob **Creative Commons
Attribution–NonCommercial–ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.
As figuras extraídas do livro (pasta `figuras/`) e todo o material derivado
neste repositório **herdam a mesma licença**: uso não comercial, com
atribuição, e compartilhamento sob os mesmos termos.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `book/` | PDF original do livro |
| `extracted/` | texto extraído por capítulo (material de trabalho) |
| `figuras/capNN/` | figuras do livro, por capítulo |
| `notas/` | notas de aula em LaTeX (roteiro de quadro-negro), uma por capítulo |
| `slides/` | apresentações Beamer, uma por capítulo |
| `guia_do_professor/` | guia do professor (uma seção por capítulo) e `cronograma.pdf` |
| `notebooks/` | notebooks Jupyter: `capNN_<tema>.ipynb` (aluno) e `capNN_solucoes.ipynb` (professor) |
| `listas/` | listas de exercícios imprimíveis (uma página por capítulo) |
| `ferramentas/` | scripts de manutenção (extração de figuras, geração das listas, QA) |
| `comum/` | preâmbulo LaTeX, tema Beamer e `estilo_meteo.py` compartilhados |

## Ambiente Python

```
conda env create -f environment.yml
conda activate meteo
jupyter lab
```

Pacotes principais: MetPy, climlab, ambiance, pyrcel, tcpyPI, Py-ART, Satpy.

## Compilação do LaTeX

Cada documento compila com `pdflatex` (TeX Live), a partir da pasta do
próprio arquivo; o preâmbulo comum está em `comum/` e é localizado via
caminho relativo.
