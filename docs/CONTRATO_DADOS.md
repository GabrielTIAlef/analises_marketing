# Contrato de dados

CSV UTF-8 com cabeçalho e separador vírgula. Exatamente quatro colunas, sem colunas extras ou duplicadas. Uma linha por cliente. Limite local de 6 a 2000 linhas: a silhouette é calculada com todas as observações e tem custo quadrático. Seis linhas satisfazem o contrato mínimo, mas não garantem grupos viáveis com o mínimo padrão de cinco clientes por grupo.

| Coluna | Regra |
| --- | --- |
| id_cliente | Texto único com 1–64 letras ASCII, números, hífen ou sublinhado; começa com letra, número ou sublinhado; zeros preservados; não é variável do modelo |
| idade | Inteiro entre 18 e 100 anos |
| renda_anual | Número finito entre 0 e 1 bilhão, na mesma unidade monetária para toda a entrada |
| pontuacao_gastos | Número finito entre 0 e 100, com definição e comparabilidade documentadas pelo fornecedor |

As três variáveis precisam variar. Não são aceitos booleanos, faltantes, NaN ou infinitos. A API Python exige tipos numéricos: não transforma strings em números silenciosamente. No CSV, Pandas infere os tipos; colunas inválidas continuam sendo rejeitadas. Não há conversão automática de separador decimal brasileiro ou de datas.

A demonstração usa renda em unidades monetárias fictícias e pontuação artificial. Não há medidas de compras, receita de campanha, fidelidade ou retenção. A origem sintética é declarada pelo comando; não é inferida por inspeção automática dos registros.

IDs inválidos e campos extras são rejeitados antes da exportação. Isso reduz riscos de fórmulas CSV e publicação de atributos pessoais adicionais, mas não constitui anonimização. IDs que atendem ao formato ainda podem identificar pessoas: use somente dados que você possa processar.

Saídas preservam todos os clientes validados, sem remover extremos. Perfis agregam os valores em suas unidades originais. `cluster` é rótulo arbitrário atribuído na execução; não serve como identificador persistente de segmento entre bases diferentes.

Falhas de contrato não publicam uma geração. O consumidor deve consultar `latest.json` e verificar os hashes, sem escolher a pasta mais recente por nome ou data.
