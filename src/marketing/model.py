"""Agrupamento exploratório; IDs nunca entram no treinamento."""
from dataclasses import dataclass
from itertools import combinations
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import RobustScaler, StandardScaler
from threadpoolctl import threadpool_limits
from .contracts import DataError, FEATURES, validate

SEEDS = (42, 73, 101)
N_INIT = 20


@dataclass
class Analysis:
    customers: pd.DataFrame
    profiles: pd.DataFrame
    metrics: pd.DataFrame
    summary: dict


def fit(values, k, seed):
    return KMeans(n_clusters=k, random_state=seed, n_init=N_INIT, algorithm='lloyd').fit(values)


def analyze(data, *, k=None, min_cluster_size=5):
    frame = validate(data)
    if isinstance(min_cluster_size, bool) or not isinstance(min_cluster_size, int) or min_cluster_size < 2:
        raise DataError('Tamanho mínimo de grupo deve ser inteiro maior ou igual a dois.')
    if k is not None and (isinstance(k, bool) or not isinstance(k, int) or not 2 <= k <= 6):
        raise DataError('k explícito deve ser inteiro entre 2 e 6.')
    values = frame[FEATURES].to_numpy()
    upper = min(6, len(frame) - 1, len(np.unique(values, axis=0)))
    if upper < 2:
        raise DataError('Observações distintas insuficientes.')
    standardized = StandardScaler().fit_transform(values)
    records, models = [], {}
    with threadpool_limits(limits=1):
        for candidate in range(2, upper + 1):
            model = fit(standardized, candidate, SEEDS[0])
            counts = np.bincount(model.labels_, minlength=candidate)
            actual = len(np.unique(model.labels_))
            valid = actual == candidate and counts.min() >= min_cluster_size
            record = {'k': candidate, 'inertia': float(model.inertia_), 'actual_clusters': actual,
                      'min_cluster_size': int(counts.min()), 'eligible': bool(valid),
                      'silhouette': None, 'stability_mean_ari': None, 'stability_min_ari': None,
                      'reason': '' if valid else 'Grupo vazio ou abaixo do tamanho mínimo.'}
            if valid:
                partitions = [model.labels_, *[fit(standardized, candidate, seed).labels_ for seed in SEEDS[1:]]]
                scores = [adjusted_rand_score(a, b) for a, b in combinations(partitions, 2)]
                record.update(silhouette=float(silhouette_score(standardized, model.labels_)),
                              stability_mean_ari=float(np.mean(scores)), stability_min_ari=float(min(scores)))
                models[candidate] = model
            records.append(record)
        eligible = [r for r in records if r['eligible']]
        if not eligible:
            raise DataError('Nenhum k produziu grupos com o tamanho mínimo exigido.')
        selected = k if k is not None else max(eligible, key=lambda r: (r['silhouette'], -r['k']))['k']
        if selected not in models:
            raise DataError('k solicitado não é viável para os dados e o tamanho mínimo.')
        labels = models[selected].labels_
        robust_labels = fit(RobustScaler().fit_transform(values), selected, SEEDS[0]).labels_
        sensitivity = float(adjusted_rand_score(labels, robust_labels))
    output = frame.assign(cluster=labels)
    profiles = output.groupby('cluster')[FEATURES].agg(['mean', 'median', 'min', 'max'])
    profiles.columns = ['_'.join(pair) for pair in profiles.columns]
    profiles.insert(0, 'clientes', output.groupby('cluster').size())
    q1, q3 = frame[FEATURES].quantile(.25), frame[FEATURES].quantile(.75)
    iqr = q3 - q1
    extremes = ((frame[FEATURES] < q1 - 1.5 * iqr) | (frame[FEATURES] > q3 + 1.5 * iqr)).any(axis=1)
    summary = {'rows': len(frame), 'selected_k': selected,
               'selection': 'explicit' if k is not None else 'maximum_silhouette_among_eligible',
               'features': FEATURES, 'seeds': list(SEEDS), 'n_init': N_INIT,
               'minimum_cluster_size': min_cluster_size, 'iqr_flagged_rows': int(extremes.sum()),
               'outlier_policy': 'diagnose_only_no_removal', 'standard_vs_robust_ari': sensitivity,
               'robust_actual_clusters': int(len(np.unique(robust_labels))),
               'limits': 'Estabilidade entre sementes não mede generalização; silhouette não prova segmentos comerciais.'}
    return Analysis(output, profiles.reset_index(), pd.DataFrame(records), summary)
