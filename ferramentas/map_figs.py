# Mapeia crops do MinerU (extracted/capNN*.md) para figuras/capNN/fig_NN_XX.jpg
# Uso: python map_figs.py NN
# Regra: cada "Figure N.M" recebe as imagens acumuladas desde a legenda
# anterior; >1 imagem => sufixos a, b, c...
import os, re, shutil, sys, glob

NN = sys.argv[1].zfill(2)
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ext = os.path.join(root, 'extracted')
dest = os.path.join(root, 'figuras', f'cap{NN}')
os.makedirs(dest, exist_ok=True)

# fontes .md: capNN.md (mesclado) ou fatias capNNa.md, capNNb.md...
mds = sorted(glob.glob(os.path.join(ext, f'cap{NN}[a-z]*.md')))
merged = os.path.join(ext, f'cap{NN}.md')
if os.path.exists(merged):
    mds = [merged]
if not mds:
    sys.exit(f'nenhum .md para cap{NN}')

# indice hash -> caminho do asset
assets = {}
for d in glob.glob(os.path.join(ext, f'cap{NN}*_assets')):
    for f in os.listdir(d):
        assets[f] = os.path.join(d, f)

img_re = re.compile(r'!\[\]\(images/([0-9a-f]+\.jpg)\)')
fig_re = re.compile(r'^#*\s*Figure\s+(\d+)\.(\d+[a-z]?)', re.IGNORECASE)

mapped, missing, pend = [], [], []
for md in mds:
    for line in open(md, encoding='utf-8'):
        m = img_re.search(line)
        if m:
            pend.append(m.group(1))
            continue
        f = fig_re.match(line.strip())
        if f and pend:
            cap, num = f.group(1), f.group(2)
            sufs = [''] if len(pend) == 1 else 'abcdefgh'[:len(pend)]
            for img, suf in zip(pend, sufs):
                name = f'fig_{int(cap):02d}_{num}{suf}.jpg'
                if img in assets:
                    shutil.copyfile(assets[img], os.path.join(dest, name))
                    mapped.append(name)
                else:
                    missing.append((name, img))
            pend = []
        elif f:
            missing.append((f'fig_{int(f.group(1)):02d}_{f.group(2)}', 'SEM IMAGEM'))

print(f'cap{NN}: {len(mapped)} mapeadas -> {dest}')
print(' '.join(mapped))
if missing:
    print('FALTANDO:', missing)
