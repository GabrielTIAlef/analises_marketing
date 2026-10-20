# Metodologia e interpretação

## Recuperação do estudo

O PDF histórico mostrava Pandas → StandardScaler → KMeans(k=3) → CSV. A implementação pública nova mantém essa finalidade, mas não reconstrói registros ou resultados originais. A linha cortada e a página ausente não foram completadas com suposições apresentadas como fatos.

## Escolha exploratória de k

1. Validar a entrada; usar somente idade, renda anual e pontuação.
2. Ajustar StandardScaler sobre as observações analisadas.
3. Avaliar k de 2 a min(6, n−1, quantidade de observações distintas).
4. KMeans usa algoritmo Lloyd, `n_init=20` e semente principal 42. Candidatos com grupos vazios ou menos de cinco clientes em qualquer grupo não são elegíveis por padrão.
5. Para candidatos elegíveis, calcular inércia e silhouette completa, além do ARI entre três ajustes com sementes 42, 73 e 101.
6. Selecionar maior silhouette entre elegíveis; empate favorece menor k. `--k` permite decisão explícita, mas não ignora os critérios mínimos.

Silhouette é uma métrica interna de coesão/separação. O critério não prova a existência de segmentos naturais nem determina a melhor estratégia de negócio. Ajustes e avaliação usam a mesma base: não se apresentam como teste fora da amostra. Não há alvo supervisionado, acurácia ou promessa de previsão.

Estabilidade por sementes quantifica apenas a sensibilidade à inicialização; não é validação por reamostragem, temporal ou populacional. Para produção, seria necessário investigar essas dimensões com dados autorizados e hipóteses comerciais verificáveis.

## Extremos e escala

Valores fora de Q1−1,5×IQR ou Q3+1,5×IQR são sinalizados; nenhuma linha é excluída ou limitada. Comparar StandardScaler e RobustScaler com o mesmo k e semente produz outro ARI. Essa comparação mede sensibilidade à escala; não elimina a sensibilidade do KMeans a outliers. O relatório registra também quantos grupos o ajuste robusto efetivamente produziu.

## Dados artificiais e limites

O gerador desenha três componentes de idade/renda/pontuação com ruído e limites documentados no código. O número de componentes é uma escolha da demonstração, não uma descoberta sobre os dados originais. IDs são sequenciais fictícios, com zeros iniciais. Nenhum registro do PDF é utilizado.

Perfis são descrições de médias, medianas, extremos e tamanhos. Não serão chamados de fiéis, recorrentes, lucrativos ou responsivos sem medidas e validação independentes. Ações de marketing possíveis são hipóteses para experimento, não impactos comprovados.

## Referências primárias

- [KMeans e parâmetros](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Silhouette e condições de definição](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [StandardScaler e sensibilidade a extremos](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- [Adjusted Rand Index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)
