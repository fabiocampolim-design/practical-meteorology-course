# Renderiza páginas de amostra dos slides para QA visual
import os, sys
import pymupdf

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
outdir = sys.argv[1]
plan = [('01', [3]), ('02', [4, 6]), ('03', [4]), ('05', [2, 9]),
        ('07', [6]), ('08', [3]), ('09', [4]), ('10', [5, 10]),
        ('11', [3, 5])]
for cap, pages in plan:
    d = pymupdf.open(os.path.join(root, 'slides', f'cap{cap}_slides.pdf'))
    for p in pages:
        d[p].get_pixmap(dpi=60).save(os.path.join(outdir, f'qa_c{cap}_p{p}.png'))
print('ok', sum(len(p) for _, p in plan), 'pages')
