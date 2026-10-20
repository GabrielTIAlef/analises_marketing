from pathlib import Path
import tempfile
import unittest
import numpy as np
from pandas.testing import assert_frame_equal
from marketing.contracts import DataError, read_csv, validate
from marketing.synthetic import generate


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = generate(n=60)

    def test_valid_does_not_mutate_input(self):
        original = self.data.copy(deep=True)
        validate(self.data)
        assert_frame_equal(original, self.data)

    def test_generator_reproducible(self):
        assert_frame_equal(generate(), generate())

    def test_generator_seed_changes_values(self):
        self.assertFalse(generate(seed=1).equals(generate(seed=2)))

    def test_csv_preserves_leading_zeroes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.csv'
            self.data.to_csv(path, index=False)
            self.assertEqual(read_csv(path).id_cliente.tolist(), self.data.id_cliente.tolist())

    def test_duplicate_ids_rejected(self):
        self.data.loc[1, 'id_cliente'] = self.data.loc[0, 'id_cliente']
        with self.assertRaises(DataError): validate(self.data)

    def test_numeric_ids_rejected(self):
        self.data['id_cliente'] = range(len(self.data))
        with self.assertRaises(DataError): validate(self.data)

    def test_formula_ids_rejected(self):
        for value in ('=HYPERLINK(secret)', '+1', '-1', '@SUM', '-client'):
            with self.subTest(value=value):
                self.data.loc[0, 'id_cliente'] = value
                with self.assertRaises(DataError): validate(self.data)

    def test_complex_values_not_silently_truncated(self):
        self.data['renda_anual'] = self.data.renda_anual.astype(complex) + 1j
        with self.assertRaises(DataError): validate(self.data)

    def test_missing_column_rejected(self):
        with self.assertRaises(DataError): validate(self.data.drop(columns='idade'))

    def test_extra_personal_column_rejected(self):
        with self.assertRaises(DataError): validate(self.data.assign(nome='privado'))

    def test_duplicate_columns_rejected(self):
        frame = self.data.copy()
        frame.columns = ['id_cliente', 'idade', 'idade', 'pontuacao_gastos']
        with self.assertRaises(DataError): validate(frame)

    def test_nan_and_infinity_rejected(self):
        for value in (np.nan, np.inf, -np.inf):
            with self.subTest(value=value):
                frame = self.data.copy()
                frame.loc[0, 'renda_anual'] = value
                with self.assertRaises(DataError): validate(frame)

    def test_numeric_strings_not_coerced(self):
        self.data['idade'] = self.data.idade.astype(str)
        with self.assertRaises(DataError): validate(self.data)

    def test_booleans_rejected(self):
        self.data['idade'] = True
        with self.assertRaises(DataError): validate(self.data)

    def test_domains_rejected(self):
        for column, value in [('idade', 17), ('idade', 101), ('idade', 30.5), ('renda_anual', -1),
                              ('renda_anual', 1e10), ('pontuacao_gastos', 101), ('pontuacao_gastos', -1)]:
            with self.subTest(column=column, value=value):
                frame = self.data.copy().astype({'idade': float})
                frame.loc[0, column] = value
                with self.assertRaises(DataError): validate(frame)

    def test_empty_and_small_inputs_rejected(self):
        for count in (0, 1, 5):
            with self.subTest(count=count):
                with self.assertRaises(DataError): validate(self.data.head(count))

    def test_large_input_rejected(self):
        import pandas as pd
        with self.assertRaises(DataError): validate(pd.concat([self.data] * 34))

    def test_constant_feature_rejected(self):
        with self.assertRaises(DataError): validate(self.data.assign(idade=40))

    def test_missing_file_error_does_not_expose_path(self):
        with self.assertRaises(DataError) as raised: read_csv('/private/customer.csv')
        self.assertNotIn('private', str(raised.exception))

    def test_generator_rejects_invalid_sizes(self):
        for n in (0, 29, 2001, True, 30.5):
            with self.subTest(n=n):
                with self.assertRaises(ValueError): generate(n=n)
