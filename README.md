# Análise Marketing

Projeto completo de análise de dados com Machine Learning desenvolvido para apoiar decisões estratégicas de marketing, segmentação de clientes e fidelização através de análise comportamental.

A solução foi construída utilizando Python, Power BI e algoritmos de clusterização KMeans, permitindo transformar dados brutos em insights estratégicos para campanhas, retenção e aumento de conversão.

---

## Objetivos do Projeto

Este projeto foi desenvolvido com foco em:

- Compreender o perfil dos clientes
- Identificar padrões de comportamento
- Segmentar clientes com KMeans
- Apoiar campanhas de marketing orientadas com dados
- Melhorar estratégias de fidelização
- Reduzir custos de aquisição
- Aumentar retenção e engajamento
- Transformar dados em decisões estratégicas

---

## Tecnologias Utilizadas

- Python
- PowerBI
- Pandas
- KMeans
- ScikitLearn
- DAX
  
---

# Arquitetura do projeto

```text
Excel / CSV
      ↓
ETL e Limpeza de Dados
      ↓
Python + Pandas
      ↓
Machine Learning (KMeans)
      ↓
Segmentação de Clientes
      ↓
Power BI
```
---

# Pipeline Analítico

O projeto foi estruturado para simular um fluxo completo de análise de marketing e CRM, desde a preparação dos dados até a segmentação automatizada dos clientes.

## Extração

- Leitura de arquivos CSV
- Estruturação da base de clientes
- Importação para análise exploratória

## Transformação

- Limpeza e padronização dos dados
- Conversão de variáveis
- Preparação para ML
- Tratamento de inconsistências

## Modelagem Analítica

- Padronização das variáveis com StandardScaler
- Clusterização utilizando KMeans
- Identificação automática de perfis de clientes
- Criação de segmentos estratégicos

---

# KMeans – Segmentação de Clientes

Foi utilizado o algoritmo KMeans para segmentação dos clientes em clusters com características semelhantes.

## Variáveis Utilizadas

- Idade
- Salário Anual
- Pontuação de Gastos

## Estrutura do Modelo

## Segmentos Identificados

### Grupo A
Alta recorrência e alto gasto médio

- Clientes fiéis
- Alto potencial de retenção
- Maior valor estratégico

### Grupo B
Recorrência intermediária

- Potencial de crescimento
- Clientes em desenvolvimento

### Grupo C
Baixa recorrência e baixo gasto

- Baixo engajamento
- Necessidade de campanhas específicas
  
---

# Diferenciais Técnicos

- Clusterização com KMeans 
- Padronização de variáveis com StandardScaler
- Análise comportamental de clientes
- Estrutura pronta para expansão analítica  

---

# Estrutura do Painel

O dashboard foi dividido em quatro páginas analíticas principais.

---

# Perfil dos Clientes

Página focada na análise demográfica e identificação do público ideal.

## Principais Recursos

- Idade
- Gênero
- Renda anual
- Perfil de fidelização
- Características predominantes
  
---

# Comportamento de Consumo

Página voltada para análise comportamental e padrões de compra.

## Principais Recursos

- Frequência de compras
- Valor médio gasto
- Produtos mais procurados
- Ciclo de recompra
- Tendências de consumo

---

# Campanhas de Marketing

Página destinada a análise de performance das campanhas.

## Principais Recursos

- Conversão por campanha
- Segmentos mais responsivos
- Correlação entre campanhas e vendas
- Análise de impacto comercial

---

# Fidelização e Clusters

Página focada na visualização dos clusters criados pelo algoritmo KMeans.

## Principais Recursos

- Segmentação automática
- Distribuição dos clusters
- Clientes mais valiosos
- Potencial de fidelização
- Análise preditiva comportamental

---

# Insights Estratégicos

Com o painel foi possível:

- Identificar clientes com maior potencial de fidelização
- Melhorar campanhas de marketing
- Segmentar clientes por comportamento
- Apoiar estratégias de retenção
- Reduzir custos de aquisição
- Direcionar campanhas com maior assertividade
- Detectar padrões de consumo

---

# Estrutura Analítica

## ETL
- Excel
- Power BI
- Tratamento de dados

## EDA
- Python
- Pandas
- Power Query
- Linguagem M

## Machine Learning
- KMeans
- Clusterização
- StandardScaler

## Visualização
- Power BI
- Dashboards interativos
- KPIs estratégicos
  
---

# Impacto do Projeto

Com este projeto foi possível:

- Transformar dados em decisões estratégicas
- Melhorar a compreensão do comportamento dos clientes
- Direcionar campanhas com maior eficiência
- Apoiar estratégias de retenção
- Identificar grupos de maior valor comercial
- Simular cenários reais de marketing analítico
