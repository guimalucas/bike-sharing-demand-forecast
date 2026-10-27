# Previsão de demanda de bicicletas

Análise de uma série horária de empréstimos de bicicletas e previsão da **demanda diária** com validação cronológica. O foco é demonstrar tratamento da qualidade dos dados, comparação com uma referência simples e avaliação fora da amostra.

## Resultado reproduzido

| Etapa | Resultado |
|---|---:|
| Registros horários na fonte | 17.429 |
| Duplicatas exatas | 15 |
| Dias incompletos excluídos | 34 de 730 |
| Dias usados | 696 |
| Desenvolvimento / validação / teste | 466 / 90 / 140 |
| Método escolhido pela validação | Prophet com sazonalidade anual |
| RMSE no teste reservado | **6.160,98 viagens/dia** |
| MAE no teste reservado | **4.937,92 viagens/dia** |
| RMSE da referência no mesmo teste | 13.849,16 viagens/dia |

A validação escolheu o Prophet anual (RMSE 6.605,41). No mesmo recorte, a referência que repete o último valor por dia da semana teve RMSE 9.549,77. O teste final foi consultado **após** escolher o método; a referência também foi avaliada no teste para dar escala ao resultado. Os números foram obtidos executando `forecast.py` com a fonte fixada no commit indicado abaixo; podem variar um pouco conforme a versão do Prophet.

## Dados e decisões

Fonte: [`bicicletas.csv` no repositório educacional da Alura](https://github.com/alura-cursos/data_science_projeto/blob/2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb/Dados/bicicletas.csv), commit `2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb`. O CSV é lido diretamente da origem e não é redistribuído aqui. O período vai de 04/01/2015 a 03/01/2017.

Após remover duplicatas, 34 dias têm menos de 24 medições. Não é correto comparar uma soma parcial com um total diário completo, por isso esses dias são excluídos da modelagem. A exclusão pode introduzir viés; o notebook de exploração mostra essa decisão. Variáveis climáticas ajudam na exploração, mas **não** entram como regressores no modelo de previsão.

Os 20% finais dos dias completos são reservados para teste. Do trecho anterior, os 90 dias finais servem como validação. Comparamos a referência ingênua, Prophet padrão, Prophet anual e Prophet anual após tratamento de outliers apenas no treino. O método com menor RMSE de validação é reajustado no treino total e avaliado uma vez no teste.

## Como executar

```bash
git clone https://github.com/guimalucas/bike-sharing-demand-forecast.git
cd bike-sharing-demand-forecast
python -m venv .venv
# Ative o ambiente virtual no seu sistema
pip install -r requirements.txt
python forecast.py
python -m unittest discover -s tests -v
jupyter notebook
```

Abra [a exploração](EDA_Bike_Sharing.ipynb) e [a previsão](Forecast_Prophet.ipynb) a partir da raiz do projeto. A execução padrão requer internet para baixar o CSV. Também é possível passar uma cópia local por `python forecast.py --data caminho/para/bicicletas.csv`.

## Estrutura

- [`forecast.py`](forecast.py): preparação, divisão temporal, comparação e teste final.
- [`EDA_Bike_Sharing.ipynb`](EDA_Bike_Sharing.ipynb): qualidade dos dados e padrões descritivos.
- [`Forecast_Prophet.ipynb`](Forecast_Prophet.ipynb): tabela gerada pelo experimento e visualização do teste.
- [`tests/`](tests/): casos de duplicação, dias incompletos e ordem das divisões.

## Limitações

O teste representa apenas um período histórico. O Prophet com sazonalidade anual foi ajustado com menos de dois anos de dados e sua decomposição pode ser instável. A próxima avaliação deveria usar mais histórico e várias janelas temporais. Não há evidência aqui de que clima *cause* mudanças na demanda, nem de que o erro do teste se repetiria em operação.

**Autor:** Lucas Guimarães · Engenharia da Computação, FIAP
