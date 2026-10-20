"""Dados inventados; não são clientes anonimizados."""
import numpy as np
import pandas as pd


def generate(seed=42, n=180):
    if isinstance(n, bool) or not isinstance(n, int) or not 30 <= n <= 2000:
        raise ValueError('A demonstração aceita entre 30 e 2000 linhas.')
    rng = np.random.default_rng(seed)
    # Componentes artificiais: não demonstram estrutura de uma população comercial.
    group = np.arange(n) % 3
    age = np.array([30, 54, 42])[group] + rng.normal(0, 5, n)
    income = np.array([28000, 92000, 53000])[group] + rng.normal(0, 6500, n)
    score = np.array([25, 40, 82])[group] + rng.normal(0, 7, n)
    frame = pd.DataFrame({'id_cliente': [f'{i:06d}' for i in range(n)],
                          'idade': np.clip(np.rint(age), 18, 100).astype(int),
                          'renda_anual': np.clip(income, 0, 1e9).round(2),
                          'pontuacao_gastos': np.clip(score, 0, 100).round(2)})
    return frame.iloc[rng.permutation(n)].reset_index(drop=True)
