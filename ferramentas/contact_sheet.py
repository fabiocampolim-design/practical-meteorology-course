# Gera uma folha de contato (grade de miniaturas rotuladas) de figuras/capNN
# Uso: python contact_sheet.py NN saida.png
import os, sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

NN = sys.argv[1].zfill(2)
out = sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(root, 'figuras', f'cap{NN}')
files = sorted(f for f in os.listdir(d) if f.endswith(('.jpg', '.png')))
n = len(files)
cols = 6
rows = math.ceil(n/cols)
fig, axs = plt.subplots(rows, cols, figsize=(cols*2.6, rows*2.4))
axs = axs.ravel() if n > 1 else [axs]
for ax in axs[n:]:
    ax.axis('off')
for ax, f in zip(axs, files):
    ax.imshow(mpimg.imread(os.path.join(d, f)))
    ax.set_title(f, fontsize=7)
    ax.axis('off')
fig.tight_layout()
fig.savefig(out, dpi=80)
print('ok', out, n, 'figs')
