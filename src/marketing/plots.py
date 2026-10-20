"""Gráficos estáticos exportáveis; sem dependência de Power BI."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def render(analysis, directory, *, synthetic):
    label = 'Dados fictícios' if synthetic else 'Dados fornecidos pelo usuário'
    with plt.rc_context({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False}):
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
        frame = analysis.customers
        for cluster, group in frame.groupby('cluster'):
            axes[0].scatter(group.renda_anual, group.pontuacao_gastos, label=f'Grupo {cluster}', alpha=.7, s=26)
        axes[0].set(xlabel='Renda anual (unidades monetárias)', ylabel='Pontuação de gastos (0–100)', title='Projeção em duas das três variáveis')
        axes[0].legend()
        axes[1].bar(analysis.profiles.cluster.astype(str), analysis.profiles.clientes, color='#247c94')
        axes[1].set(xlabel='Rótulo do grupo (arbitrário)', ylabel='Clientes', title='Distribuição dos grupos')
        fig.suptitle(f'Segmentação exploratória | {label}')
        fig.savefig(directory / 'segmentos.png', dpi=140)
        plt.close(fig)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
        metrics = analysis.metrics
        axes[0].plot(metrics.k, metrics.inertia, 'o-', color='#247c94')
        axes[0].set(xlabel='k', ylabel='Inércia', title='Dispersão interna')
        valid = metrics.loc[metrics.eligible]
        axes[1].plot(valid.k, valid.silhouette, 'o-', color='#a14c26')
        axes[1].set(xlabel='k elegível', ylabel='Silhouette', title='Coesão e separação exploratórias', ylim=(-1, 1))
        fig.suptitle(label)
        fig.savefig(directory / 'avaliacao.png', dpi=140)
        plt.close(fig)
