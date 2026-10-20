"""Demonstração offline ou análise explícita de um CSV mínimo autorizado."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.local-test/matplotlib'))
sys.path.insert(0, str(ROOT / 'src'))
from marketing.contracts import DataError, read_csv
from marketing.pipeline import publish
from marketing.synthetic import generate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--demo', action='store_true')
    source.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'outputs/demo')
    parser.add_argument('--k', type=int)
    args = parser.parse_args()
    try:
        data = generate() if args.demo else read_csv(args.input)
        manifest = publish(data, args.output, synthetic=args.demo, k=args.k)
    except (DataError, OSError, ValueError):
        print('Análise não publicada. Confira o contrato, os parâmetros e as permissões da pasta.', file=sys.stderr)
        return 1
    print(json.dumps({'status': 'complete', 'synthetic': args.demo, 'run_id': manifest['run_id']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
