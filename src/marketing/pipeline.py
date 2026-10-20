"""Publicação por geração imutável; latest.json é o ponto de confirmação."""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
from .model import analyze
from .plots import render


def write_json(path, payload):
    with path.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(payload, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def publish(data, output, *, synthetic, k=None, min_cluster_size=5):
    if not isinstance(synthetic, bool):
        raise ValueError('A origem sintética deve ser informada explicitamente.')
    analysis = analyze(data, k=k, min_cluster_size=min_cluster_size)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    stage = Path(tempfile.mkdtemp(prefix='.pending-', dir=output))
    pointer = output / ('.latest-' + run_id + '.tmp')
    final = output / ('run-' + run_id)
    try:
        analysis.customers.to_csv(stage / 'clientes_segmentados.csv', index=False)
        analysis.profiles.to_csv(stage / 'perfis.csv', index=False)
        analysis.metrics.to_csv(stage / 'comparacao_k.csv', index=False)
        summary = dict(analysis.summary, synthetic=synthetic,
                       input_sha256=hashlib.sha256(data.to_csv(index=False).encode()).hexdigest(),
                       python=sys.version.split()[0],
                       versions={name: version(name) for name in ('numpy', 'pandas', 'scikit-learn', 'matplotlib')})
        write_json(stage / 'resumo.json', summary)
        render(analysis, stage, synthetic=synthetic)
        files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in stage.iterdir()}
        # Rename e ponteiro estão no mesmo filesystem. Falha antes do replace preserva latest anterior.
        os.replace(stage, final)
        manifest = {'run_id': run_id, 'directory': final.name, 'synthetic': synthetic, 'files_sha256': files}
        write_json(pointer, manifest)
        os.replace(pointer, output / 'latest.json')
        return manifest
    finally:
        if stage.exists():
            shutil.rmtree(stage)
        pointer.unlink(missing_ok=True)
        # Uma geração órfã após falha no ponteiro é segura e nunca é apresentada como confirmada.
