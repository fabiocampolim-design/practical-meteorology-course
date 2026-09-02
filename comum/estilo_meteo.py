# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
# estilo_meteo.py — estilo gráfico comum dos notebooks do curso
# Meteorologia Prática (baseado em R. Stull, Practical Meteorology, CC BY-NC-SA 4.0)
"""
Uso nos notebooks:

    import sys; sys.path.append('../comum')
    from estilo_meteo import aplicar_estilo, CORES, sombrear_camadas
    aplicar_estilo()
"""
import matplotlib as mpl

# paleta do curso ------------------------------------------------------------
CORES = {
    'azul':     '#1f5fa8',   # pressão / dados principais
    'vermelho': '#c9403a',   # temperatura
    'verde':    '#2e8b57',   # umidade / ponto de orvalho
    'laranja':  '#e08214',   # destaque secundário
    'roxo':     '#7b52a8',   # comparações
    'cinza':    '#6a6a6a',   # referências, atmosfera padrão
    'areia':    '#f5efe0',   # fundos suaves
}
CICLO = [CORES['azul'], CORES['vermelho'], CORES['verde'],
         CORES['laranja'], CORES['roxo'], CORES['cinza']]

# cores das camadas atmosféricas (do chão ao espaço)
CAMADAS = [
    (0,  11, '#cfe3f5', 'Troposfera'),
    (11, 20, '#e8f0e6', 'Tropopausa'),
    (20, 47, '#fdf3dc', 'Estratosfera'),
    (47, 51, '#f9e6d8', 'Estratopausa'),
]


def aplicar_estilo():
    """Aplica o estilo visual do curso a todos os gráficos do notebook."""
    mpl.rcParams.update({
        'figure.dpi': 115,
        'figure.facecolor': 'white',
        'axes.prop_cycle': mpl.cycler(color=CICLO),
        'axes.facecolor': '#fcfcfc',
        'axes.edgecolor': '#444444',
        'axes.linewidth': 0.9,
        'axes.grid': True,
        'axes.titlesize': 12,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'grid.color': '#d9d9d9',
        'grid.linewidth': 0.6,
        'grid.alpha': 0.7,
        'lines.linewidth': 2.2,
        'lines.solid_capstyle': 'round',
        'font.family': 'sans-serif',
        'font.size': 10.5,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': '#cccccc',
        'legend.fontsize': 9.5,
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'savefig.bbox': 'tight',
    })


def sombrear_camadas(ax, zmax_km=50, rotulos=True, eixo='y'):
    """Sombreia as camadas atmosféricas num eixo cuja coordenada vertical
    (eixo='y') ou horizontal (eixo='x') é altura em km."""
    span = ax.axhspan if eixo == 'y' else ax.axvspan
    for z0, z1, cor, nome in CAMADAS:
        if z0 >= zmax_km:
            break
        span(z0, min(z1, zmax_km), color=cor, alpha=0.55, zorder=0, lw=0)
        if rotulos and eixo == 'y':
            ax.annotate(nome, xy=(0.985, (z0 + min(z1, zmax_km))/2),
                        xycoords=('axes fraction', 'data'),
                        ha='right', va='center', fontsize=8.5,
                        color='#555555', style='italic')


def marco(ax, z_km, texto, x_frac=0.03):
    """Anota um marco de altitude (ex.: Everest, voo de cruzeiro) num perfil."""
    ax.axhline(z_km, color='#888888', lw=0.8, ls=':')
    ax.annotate(texto, xy=(x_frac, z_km), xycoords=('axes fraction', 'data'),
                fontsize=8.5, color='#555555', va='bottom')
