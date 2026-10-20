# Dados fictícios

clientes_ficticios.csv é uma amostra produzida por `marketing.synthetic.generate(seed=42, n=30)`. Contém apenas valores inventados, sem extração ou anonimização da base original. A demonstração principal usa 180 linhas geradas pelo mesmo código; não depende deste CSV.

O gerador utiliza três componentes desenhados para a demonstração, com ruído e limites. Renda é expressa em unidades monetárias fictícias; a pontuação de gastos é artificial, entre zero e cem. Não há registros de compras ou campanhas, e não se pode calcular fidelização, retenção ou conversão a partir desses campos.
