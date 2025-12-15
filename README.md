# Previsão de Demanda de Bicicletas com Prophet

## Objetivo

Este projeto tem como objetivo analisar a demanda diária por bicicletas compartilhadas e desenvolver um modelo de previsão de séries temporais capaz de capturar tendências de longo prazo, padrões sazonais e o comportamento típico da demanda. A análise considera fatores climáticos, efeitos de calendário e diferentes estratégias de modelagem, avaliando o impacto dessas decisões na performance preditiva.

---

## Conjunto de Dados

- Dataset público com registros de uso de bicicletas
- Granularidade diária após agregação
- 17.414 observações
- Variável alvo: contagem diária de bicicletas
- Variáveis disponíveis:
  - Temperatura
  - Sensação térmica
  - Umidade
  - Velocidade do vento
  - Condições climáticas
  - Estação do ano
  - Indicadores de feriado e final de semana

Os dados foram tratados para remoção de duplicatas e preenchimento de valores ausentes antes da etapa de análise.

---

## Análise Exploratória dos Dados

A análise exploratória foi conduzida para compreender a estrutura, variabilidade e os principais fatores associados à demanda por bicicletas. As etapas incluem:

- Análise estatística descritiva para avaliar escala, dispersão e assimetria
- Histogramas para investigar a distribuição das variáveis climáticas e da demanda
- Gráficos de dispersão para avaliar a relação entre clima e uso de bicicletas
- Análise de correlação entre variáveis numéricas
- Agregações por condição climática e estação do ano
- Comparação da demanda em feriados, finais de semana e dias úteis
- Teste estatístico de Mann–Whitney para verificar diferenças significativas entre estações

Os resultados indicam alta variabilidade na demanda diária, presença de sazonalidade anual bem definida e sensibilidade às condições climáticas, especialmente à temperatura.

---

## Abordagem de Modelagem

A modelagem foi realizada utilizando o Prophet, um modelo de séries temporais voltado para dados com tendência e sazonalidade. O pipeline de modelagem inclui:

1. Modelo Prophet básico como baseline
2. Modelo Prophet com sazonalidade anual explicitamente habilitada
3. Detecção de outliers com base nos intervalos de confiança do Prophet
4. Re-treinamento do modelo após a remoção de valores extremos
5. Divisão temporal dos dados em treino e teste (80/20)

Essa abordagem permite avaliar incrementalmente o impacto das escolhas de modelagem sobre o desempenho do modelo.

---

## Resultados

O desempenho dos modelos foi avaliado utilizando as métricas Mean Squared Error (MSE) e Root Mean Squared Error (RMSE):

| Modelo | RMSE |
|------|------|
| Prophet básico | ~21.454 |
| Prophet com sazonalidade anual | ~6.233 |
| Prophet sem outliers | ~3.744 |

O modelo final apresentou uma redução superior a 80% no erro em relação ao baseline, evidenciando a importância da sazonalidade anual e do tratamento de outliers para a previsão de demanda.

---

## Interpretação dos Resultados

- O modelo baseline captura a tendência geral, mas não representa adequadamente os padrões sazonais
- A inclusão explícita da sazonalidade anual permite ao modelo aprender ciclos recorrentes da demanda
- A remoção de outliers melhora a capacidade do modelo de prever o comportamento típico da série
- O erro residual está associado à variabilidade inerente ao comportamento humano e às condições climáticas

Considerando a escala e a variabilidade dos dados, o RMSE final é compatível com problemas reais de previsão de demanda.

---

## Limitações

- O modelo não incorpora variáveis exógenas futuras, como previsões meteorológicas
- Eventos extremos não são previstos explicitamente
- O foco da previsão está no comportamento típico da demanda, e não em anomalias raras

---

## Tecnologias Utilizadas

- Python
- pandas, numpy
- matplotlib, seaborn
- Prophet
- scikit-learn
- scipy
- plotly

---

## Como Executar o Projeto

Instale as dependências:

```bash
pip install -r requirements.txt
