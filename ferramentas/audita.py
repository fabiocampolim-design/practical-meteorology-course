# Auditoria de consistência do material do curso
import os, re, glob, json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problemas = []

def P(msg):
    problemas.append(msg)

# ---------- 1. figuras citadas nos slides existem? ----------
for f in sorted(glob.glob(os.path.join(root, 'slides', 'cap*_slides.tex'))):
    nn = re.search(r'cap(\d+)', f).group(1)
    src = open(f, encoding='utf-8').read()
    figdir = os.path.join(root, 'figuras', f'cap{nn}')
    usados = re.findall(r'\\figlivroslide\{([^}]+)\}', src)
    usados += re.findall(r'\\includegraphics\[[^]]*\]\{([^}]+)\}', src)
    for u in usados:
        if not os.path.exists(os.path.join(figdir, u)):
            P(f'slides cap{nn}: figura ausente: {u}')

# ---------- 2. placeholders remanescentes ----------
for f in glob.glob(os.path.join(root, 'slides', '*.tex')) + \
         glob.glob(os.path.join(root, 'notas', '*.tex')):
    src = open(f, encoding='utf-8').read()
    if 'figplaceholder' in src:
        P(f'placeholder remanescente em {os.path.basename(f)}')

# ---------- 3. \javimos/\veremos: alvo 1..23 e != capítulo próprio ----------
for f in sorted(glob.glob(os.path.join(root, 'notas', 'cap*_notas.tex'))):
    nn = int(re.search(r'cap(\d+)', f).group(1))
    src = open(f, encoding='utf-8').read()
    for m in re.finditer(r'\\(javimos|veremos)\{(\d+)\}', src):
        alvo = int(m.group(2))
        if not (1 <= alvo <= 23):
            P(f'notas cap{nn:02d}: \\{m.group(1)}{{{alvo}}} fora de 1..23')
        if m.group(1) == 'veremos' and alvo < nn:
            P(f'notas cap{nn:02d}: \\veremos{{{alvo}}} aponta para tras')
        if m.group(1) == 'javimos' and alvo > nn:
            P(f'notas cap{nn:02d}: \\javimos{{{alvo}}} aponta para frente')

# ---------- 4. "Caso N" citado nas notas: notebooks têm 4 casos ----------
for f in sorted(glob.glob(os.path.join(root, 'notas', 'cap*_notas.tex'))):
    nn = int(re.search(r'cap(\d+)', f).group(1))
    src = open(f, encoding='utf-8').read()
    for m in re.finditer(r'Caso~(\d+)', src):
        if int(m.group(1)) > 4:
            P(f'notas cap{nn:02d}: cita Caso~{m.group(1)} (>4)')

# ---------- 5. notebooks: pares aluno/solucoes, casos e exercícios ----------
nbs = sorted(glob.glob(os.path.join(root, 'notebooks', 'cap*.ipynb')))
temas, sols = {}, {}
for f in nbs:
    base = os.path.basename(f)
    nn = re.search(r'cap(\d+)', base).group(1)
    if '_solucoes' in base:
        sols[nn] = f
    else:
        temas[nn] = f
for nn in sorted(set(temas) | set(sols)):
    if nn not in temas:
        P(f'cap{nn}: falta notebook do aluno')
    if nn not in sols:
        P(f'cap{nn}: falta notebook de soluções')
for nn, f in sorted(temas.items()):
    nb = json.load(open(f, encoding='utf-8'))
    txt = '\n'.join(''.join(c.get('source', [])) for c in nb['cells'])
    ncasos = len(re.findall(r'## Caso \d', txt))
    n_ex = len(re.findall(r'\*\*N\d\*\*', txt))
    if ncasos != 4:
        P(f'{os.path.basename(f)}: {ncasos} casos (esperado 4)')
    if n_ex != 4:
        P(f'{os.path.basename(f)}: {n_ex} enunciados N (esperado 4)')
    errs = sum(1 for c in nb['cells'] for o in c.get('outputs', [])
               if o.get('output_type') == 'error')
    if errs:
        P(f'{os.path.basename(f)}: {errs} celulas com ERRO')
for nn, f in sorted(sols.items()):
    nb = json.load(open(f, encoding='utf-8'))
    txt = '\n'.join(''.join(c.get('source', [])) for c in nb['cells'])
    nT = len(re.findall(r'## T\d', txt))
    nN = len(re.findall(r'## N\d', txt))
    if nT != 5 or nN != 4:
        P(f'{os.path.basename(f)}: {nT} solucoes T (esp. 5), {nN} N (esp. 4)')
    errs = sum(1 for c in nb['cells'] for o in c.get('outputs', [])
               if o.get('output_type') == 'error')
    if errs:
        P(f'{os.path.basename(f)}: {errs} celulas com ERRO')

# ---------- 6. exercícios nas notas: 5 T e 4 N por capítulo ----------
for f in sorted(glob.glob(os.path.join(root, 'notas', 'cap*_notas.tex'))):
    nn = int(re.search(r'cap(\d+)', f).group(1))
    src = open(f, encoding='utf-8').read()
    m = re.search(r'\\subsection\*\{Te[óo]ricos\}(.*?)\\subsection\*\{Num',
                  src, re.DOTALL)
    m2 = re.search(r'\\subsection\*\{Num[ée]ricos[^}]*\}(.*?)\\vspace\{1em\}',
                   src, re.DOTALL)
    nT = len(re.findall(r'\\item', m.group(1))) if m else 0
    nN = len(re.findall(r'\\item', m2.group(1))) if m2 else 0
    if nT != 5 or nN != 4:
        P(f'notas cap{nn:02d}: {nT} exercicios T (esp. 5), {nN} N (esp. 4)')

# ---------- 7. sobras de referencias erradas ----------
for f in glob.glob(os.path.join(root, 'notas', '*.tex')) + \
         glob.glob(os.path.join(root, 'guia_do_professor', '*.tex')) + \
         glob.glob(os.path.join(root, 'slides', '*.tex')):
    src = open(f, encoding='utf-8').read()
    if re.search(r'Cap\.?~?\s*22[^0-9]{0,40}(clim|carbono|CO)', src):
        P(f'{os.path.basename(f)}: possivel referencia cap22=clima')
    if 'cap22_mudanca' in src or 'cap22\\_mudanca' in src:
        P(f'{os.path.basename(f)}: cita cap22_mudanca (renomeado p/ 23)')

# ---------- 8. guia: todos os capítulos incluídos ----------
gsrc = open(os.path.join(root, 'guia_do_professor', 'guia.tex'),
            encoding='utf-8').read()
for nn in range(1, 24):
    if f'cap{nn:02d}_guia' not in gsrc:
        P(f'guia.tex: falta \\input de cap{nn:02d}_guia')

print(f'{len(problemas)} problema(s) encontrados:')
for p in problemas:
    print(' -', p)
if not problemas:
    print(' (nenhum)')
