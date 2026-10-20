"""Contrato mínimo sem nomes ou documentos pessoais."""
import numpy as np
import pandas as pd

FEATURES = ['idade', 'renda_anual', 'pontuacao_gastos']
COLUMNS = ['id_cliente', *FEATURES]
MAX_ROWS = 2000


class DataError(ValueError):
    """Erro de contrato sem valores de registros."""


def validate(data):
    if not isinstance(data, pd.DataFrame):
        raise DataError('A entrada deve ser uma tabela.')
    if set(data.columns) != set(COLUMNS) or len(data.columns) != 4:
        raise DataError('Colunas devem ser exatamente id_cliente, idade, renda_anual e pontuacao_gastos.')
    if not 6 <= len(data) <= MAX_ROWS:
        raise DataError(f'A entrada deve conter entre 6 e {MAX_ROWS} clientes.')
    result = data[COLUMNS].copy()
    ids = result.id_cliente
    if not ids.map(lambda x: isinstance(x, str) and bool(x.strip()) and x == x.strip()).all():
        raise DataError('IDs devem ser textos não vazios, sem espaços nas extremidades.')
    if not ids.str.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_-]{0,63}').all() or ids.duplicated().any():
        raise DataError('IDs devem ser únicos, usando letras, números, hífen ou sublinhado.')
    for column in FEATURES:
        if result[column].map(lambda x: isinstance(x, (bool, np.bool_))).any():
            raise DataError('Variáveis numéricas não aceitam booleanos.')
        if not pd.api.types.is_numeric_dtype(result[column]) or pd.api.types.is_complex_dtype(result[column]):
            raise DataError('Variáveis devem ter tipos numéricos; não há coerção silenciosa.')
        values = result[column].to_numpy(dtype=float, na_value=np.nan)
        if not np.isfinite(values).all():
            raise DataError('Variáveis devem ser completas e finitas.')
        result[column] = values
    if not result.idade.between(18, 100).all() or not (result.idade % 1 == 0).all():
        raise DataError('Idade deve ser inteira entre 18 e 100 anos.')
    if not result.renda_anual.between(0, 1_000_000_000).all():
        raise DataError('Renda anual deve estar entre zero e um bilhão de unidades monetárias.')
    if not result.pontuacao_gastos.between(0, 100).all():
        raise DataError('Pontuação deve estar entre zero e 100.')
    if (result[FEATURES].nunique() < 2).any():
        raise DataError('Cada variável deve ter pelo menos dois valores distintos.')
    return result.reset_index(drop=True)


def read_csv(path):
    try:
        frame = pd.read_csv(path, dtype={'id_cliente': str}, keep_default_na=False)
    except (OSError, ValueError, pd.errors.ParserError):
        raise DataError('Não foi possível ler o CSV; confira o contrato.') from None
    return validate(frame)
