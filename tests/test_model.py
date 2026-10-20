import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from marketing.contracts import DataError, FEATURES
from marketing.model import analyze
from marketing.synthetic import generate


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generate(n=90)
        cls.analysis = analyze(cls.data)

    def test_profiles_reconcile_clients(self):
        self.assertEqual(self.analysis.profiles.clientes.sum(), len(self.data))
        self.assertEqual(len(self.analysis.customers), len(self.data))
        self.assertEqual(self.analysis.customers.id_cliente.tolist(), self.data.id_cliente.tolist())

    def test_three_designed_components_recovered(self):
        self.assertEqual(self.analysis.summary['selected_k'], 3)
        row = self.analysis.metrics.query('k == 3').iloc[0]
        self.assertGreater(row.silhouette, .4)
        self.assertGreater(row.stability_min_ari, .95)

    def test_same_data_same_partition(self):
        again = analyze(self.data)
        self.assertEqual(adjusted_rand_score(self.analysis.customers.cluster, again.customers.cluster), 1)

    def test_ids_not_training_features(self):
        changed = self.data.copy()
        changed['id_cliente'] = [f'other-{i}' for i in range(len(changed))]
        again = analyze(changed)
        self.assertEqual(adjusted_rand_score(self.analysis.customers.cluster, again.customers.cluster), 1)
        self.assertEqual(again.summary['features'], FEATURES)

    def test_k_is_selected_from_eligible_candidates(self):
        valid = self.analysis.metrics.query('eligible')
        best = valid.sort_values(['silhouette', 'k'], ascending=[False, True]).iloc[0]
        self.assertEqual(best.k, self.analysis.summary['selected_k'])
        self.assertTrue(valid.silhouette.between(-1, 1).all())

    def test_explicit_k_supported(self):
        self.assertEqual(analyze(self.data, k=2).summary['selection'], 'explicit')
        self.assertEqual(analyze(self.data, k=2).summary['selected_k'], 2)

    def test_invalid_k_rejected(self):
        for k in (True, 1, 7, 2.5, '3'):
            with self.subTest(k=k):
                with self.assertRaises(DataError): analyze(self.data, k=k)

    def test_invalid_minimum_size_rejected(self):
        for minimum in (True, 1, 2.5):
            with self.subTest(minimum=minimum):
                with self.assertRaises(DataError): analyze(self.data, min_cluster_size=minimum)

    def test_ineligible_k_rejected(self):
        with self.assertRaises(DataError): analyze(self.data, min_cluster_size=100)

    def test_only_two_distinct_observations_limit_candidates(self):
        data = pd.DataFrame({'id_cliente': [str(i) for i in range(12)], 'idade': [25, 60] * 6,
                             'renda_anual': [20000, 90000] * 6, 'pontuacao_gastos': [10, 90] * 6})
        result = analyze(data)
        self.assertEqual(result.metrics.k.tolist(), [2])
        self.assertEqual(result.summary['selected_k'], 2)
        with self.assertRaises(DataError): analyze(data, k=3)

    def test_insufficient_sizes_do_not_compute_undefined_silhouette(self):
        with patch('marketing.model.silhouette_score') as score:
            with self.assertRaises(DataError): analyze(self.data.head(6))
            score.assert_not_called()

    def test_outlier_is_diagnosed_and_preserved(self):
        data = self.data.copy()
        data.loc[0, 'renda_anual'] = 666666
        result = analyze(data, min_cluster_size=2)
        self.assertGreaterEqual(result.summary['iqr_flagged_rows'], 1)
        self.assertEqual(len(result.customers), len(data))
        self.assertEqual(result.customers.renda_anual.max(), 666666)
        self.assertTrue(-1 <= result.summary['standard_vs_robust_ari'] <= 1)

    def test_profile_means_in_original_units(self):
        result = self.analysis
        for _, profile in result.profiles.iterrows():
            rows = result.customers.query('cluster == @profile.cluster')
            self.assertAlmostEqual(profile.renda_anual_mean, rows.renda_anual.mean())

    def test_label_permutation_does_not_change_ari(self):
        a = np.array([0, 0, 1, 1, 2, 2])
        self.assertEqual(adjusted_rand_score(a, (a + 1) % 3), 1)
