# Previsão de demanda de bicicletas

Parti de registros horários de bicicletas, consolidei os dias completos e comparei previsões da **demanda diária**. A escolha do modelo usa dados anteriores ao período de teste; o [notebook de exploração](EDA_Bike_Sharing.ipynb) mostra o preparo da série e o [de previsão](Forecast_Prophet.ipynb) reúne os gráficos e erros.

## Resultados

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
| WAPE no teste reservado | **17% da demanda observada** |
| RMSE da referência sazonal (52 semanas) | 8.703,21 viagens/dia |
| WAPE da referência sazonal | 22% da demanda observada |
| RMSE da referência semanal fixa | 13.849,16 viagens/dia |

A validação escolheu o Prophet anual (RMSE 6.605,41). No mesmo período, a referência de **52 semanas** teve RMSE 9.133,07 e a semanal fixa, 9.549,77. Reajustei o método escolhido com o histórico disponível e só então medi o erro nos 140 dias reservados. Os valores da tabela vêm de [`forecast.py`](forecast.py) com a versão do CSV indicada abaixo; pequenas diferenças são possíveis entre versões do Prophet.

### Comparação em três datas

Também repeti a previsão a partir de três datas anteriores ao teste, sempre olhando os 90 dias completos seguintes. O RMSE abaixo está em viagens por dia:

| Última data de treino | Semanal fixa | 52 semanas | Prophet padrão | Prophet anual | Anual sem outliers |
|---|---:|---:|---:|---:|---:|
| 22/01/2016 | 5.062 | 5.202 | 12.619 | 4.025 | **3.963** |
| 15/03/2016 | 9.593 | 7.110 | 13.788 | **6.439** | 6.780 |
| 07/05/2016 | 9.550 | 9.133 | 6.992 | **6.605** | 6.610 |

O Prophet anual superou **as duas referências** nos três cortes. Remover outliers ajudou no primeiro corte e piorou os outros dois. As janelas de 90 dias se sobrepõem; a tabela mostra a variação entre datas, não três testes independentes.

## Dados e decisões

Fonte: [`bicicletas.csv` no repositório educacional da Alura](https://github.com/alura-cursos/data_science_projeto/blob/2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb/Dados/bicicletas.csv), commit `2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb`. O CSV é lido diretamente da origem e não é redistribuído aqui. O período vai de 04/01/2015 a 03/01/2017.

Após remover duplicatas, encontrei 34 dias com menos de 24 medições. Retirei esses dias antes de somar a demanda diária; a série usada ficou com 696 dias. Essa escolha altera a amostra, como mostra o notebook de exploração. Clima aparece nos gráficos exploratórios e **não** entra nos modelos de previsão.

Reservei os 20% finais dos dias completos para teste e usei os 90 dias anteriores para escolher o método. Uma referência repete o último valor observado de cada dia da semana; a outra consulta o mesmo dia da semana **52 semanas antes**. Se o dia correspondente não existe na série, uso o último valor conhecido daquele dia da semana (aconteceu em 10 dos 140 dias de teste). Comparei as duas com Prophet padrão, Prophet anual e Prophet anual com outliers removidos **apenas do treino**. A WAPE soma os erros absolutos e divide pela demanda observada no período. A sazonalidade anual foi ajustada com menos de dois anos de histórico.

## Como executar

```bash
git clone https://github.com/guimalucas/bike-sharing-demand-forecast.git
cd bike-sharing-demand-forecast
python -m venv .venv
# Ative o ambiente virtual no seu sistema
pip install -r requirements.txt
python forecast.py
python forecast.py --backtest
python -m unittest discover -s tests -v
jupyter notebook
```

Abra [a exploração](EDA_Bike_Sharing.ipynb) e [a previsão](Forecast_Prophet.ipynb) a partir da raiz do projeto. A execução padrão requer internet para baixar o CSV. Também é possível passar uma cópia local por `python forecast.py --data caminho/para/bicicletas.csv`.

## Estrutura

- [`forecast.py`](forecast.py): preparação, divisão temporal, comparação e teste final.
- [`EDA_Bike_Sharing.ipynb`](EDA_Bike_Sharing.ipynb): qualidade dos dados e padrões descritivos.
- [`Forecast_Prophet.ipynb`](Forecast_Prophet.ipynb): escolha do modelo, diagnóstico em três cortes e visualização do teste.
- [`tests/`](tests/): casos de duplicação, dias incompletos e ordem das divisões.

**Autor:** Lucas Guimarães · Engenharia da Computação, FIAP
