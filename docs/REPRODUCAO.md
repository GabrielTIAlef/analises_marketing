# Reprodução

Use Python 3.12 em ambiente virtual isolado e instale `requirements-lock.txt`. Execute `python -m pip check`, `python scripts/run_tests.py`, `python scripts/run_analysis.py --demo` e `python scripts/validate_notebook.py`. A instalação pode precisar de internet; a análise não baixa bases ou acessa APIs.

Os scripts localizam o código a partir de seu próprio caminho; podem ser chamados por caminho absoluto a partir de outra pasta. O notebook localiza a raiz a partir do diretório de execução: abra-o na raiz ou na pasta notebooks, ou use o validador fornecido.

Abra `outputs/demo/latest.json` e, a partir de `directory`, localize os seis arquivos confirmados. O manifesto inclui SHA-256 de cada arquivo. Cada execução cria uma pasta própria; CSVs e gráficos de uma mesma geração não são sobrescritos por outra execução.

O ponteiro é substituído atomicamente no mesmo filesystem somente após sucesso. Isso protege consumidores que usam esse contrato. Não existe transação distribuída, bloqueio para ordenação cronológica entre produtores concorrentes ou garantia contra perda de energia em todos os filesystems. Em concorrência, vence o último replace; evite escritores simultâneos se a ordem temporal for importante. Uma falha de ponteiro pode deixar uma geração órfã, sem torná-la confirmada.

O notebook é publicado sem saídas, para evitar dados acidentais e ruído. O validador usa kernel temporário apontando para o Python ativo, executa todas as células e confirma a publicação sintética. Não modifica kernels globais e não salva caminhos temporários no notebook versionado.

A reprodução de partições é esperada com a mesma entrada, configuração e ambiente fixado. BLAS, plataforma e versões podem alterar arredondamentos ou rótulos. Compare partições por ARI, não pelo número arbitrário do cluster. Bytes de PNG, manifestos com UUID e arquivos de versões não são prometidos como idênticos entre sistemas.

Dados privados devem permanecer em data/ e saídas em outputs/, ambos ignorados pelo Git. A amostra em examples/ é fictícia e explicitamente permitida. Não adicione arquivos reais apenas para demonstrar a execução.
