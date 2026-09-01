# QA visual dos materiais dos caps. 12-14 (fase 2)
import os, sys
import pymupdf

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
outdir = sys.argv[1]
alvos = [('slides/cap12_slides.pdf', [4, 7]), ('slides/cap13_slides.pdf', [2, 8]),
         ('slides/cap14_slides.pdf', [3, 9]), ('notas/cap12_notas.pdf', [0]),
         ('notas/cap16_notas.pdf', [1]), ('guia_do_professor/guia.pdf', [30])]
k = 0
for rel, pages in alvos:
    d = pymupdf.open(os.path.join(root, rel))
    for p in pages:
        d[p].get_pixmap(dpi=60).save(os.path.join(outdir, f'qa2_{k:02d}.png'))
        k += 1
print('ok', k)
