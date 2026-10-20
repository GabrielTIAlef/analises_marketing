import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from marketing.contracts import DataError
from marketing.pipeline import publish
from marketing.synthetic import generate

ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'outputs'
        self.data = generate(n=60)

    def test_manifest_hashes_and_generation_complete(self):
        manifest = publish(self.data, self.output, synthetic=True)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text()), manifest)
        directory = self.output / manifest['directory']
        self.assertEqual(len(manifest['files_sha256']), 6)
        for name, sha in manifest['files_sha256'].items():
            self.assertEqual(hashlib.sha256((directory / name).read_bytes()).hexdigest(), sha)
        self.assertTrue(json.loads((directory / 'resumo.json').read_text())['synthetic'])

    def test_invalid_data_leaves_previous_generation(self):
        first = publish(self.data, self.output, synthetic=True)
        with self.assertRaises(DataError): publish(self.data.head(0), self.output, synthetic=True)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text()), first)

    def test_plot_failure_leaves_previous_generation(self):
        first = publish(self.data, self.output, synthetic=True)
        with patch('marketing.pipeline.render', side_effect=OSError('failure')):
            with self.assertRaises(OSError): publish(self.data, self.output, synthetic=True)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text()), first)
        self.assertFalse(list(self.output.glob('.pending-*')))

    def test_pointer_failure_leaves_previous_generation(self):
        first = publish(self.data, self.output, synthetic=True)
        actual_replace = os.replace
        def replace(source, destination):
            if Path(destination).name == 'latest.json': raise OSError('failure')
            return actual_replace(source, destination)
        with patch('marketing.pipeline.os.replace', side_effect=replace):
            with self.assertRaises(OSError): publish(self.data, self.output, synthetic=True)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text()), first)
        self.assertFalse(list(self.output.glob('.latest-*.tmp')))

    def test_origin_must_be_explicit(self):
        with self.assertRaises(ValueError): publish(self.data, self.output, synthetic='yes')

    def test_user_supplied_data_not_marked_synthetic(self):
        result = publish(self.data, self.output, synthetic=False)
        self.assertFalse(result['synthetic'])

    def test_cli_runs_outside_repository(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_analysis.py'), '--demo',
                                 '--output', str(self.output)], cwd=self.temp.name, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'complete')

    def test_cli_error_sanitized_and_nonzero(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_analysis.py'), '--input',
                                 str(Path(self.temp.name) / 'private-client.csv')], capture_output=True, text=True, timeout=90)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('private-client', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_cli_requires_source(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_analysis.py')], capture_output=True, timeout=90)
        self.assertNotEqual(result.returncode, 0)
