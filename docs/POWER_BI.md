# Consumo dos resultados no Power BI

Este é um guia de importação, não um dashboard validado. Não há PBIX ou medidas DAX executadas nesta versão. A saída comprovada é formada por CSVs, JSON e gráficos estáticos.

1. Execute a demonstração e consulte `outputs/demo/latest.json`.
2. Importe clientes_segmentados.csv da pasta indicada em directory. Preserve id_cliente como texto; use ponto como separador decimal no parsing da localidade.
3. Use cluster como categoria, não soma. Mostre contagem de clientes, renda média e pontuação média por cluster; essas medidas não representam compras, receita ou retenção.
4. Para tabela de perfis, importe perfis.csv. Evite relacionamentos que multipliquem as contagens; há uma linha por cluster nessa tabela e uma por cliente na tabela segmentada.
5. Ao atualizar a geração, ajuste a fonte conforme o manifesto. Não combine clientes de uma execução com perfis de outra. Valide a soma de clientes antes de apresentar resultados.

Páginas possíveis: distribuição dos grupos, perfis demográficos e comparação de renda/pontuação. Campanhas, recorrência, conversão e fidelização exigem outras fontes e não são inferidas deste conjunto. Nenhum caminho corporativo ou conexão externa é necessário.
