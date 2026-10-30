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
| WAPE no teste reservado | **17% da demanda observada** |
| RMSE da referência sazonal (52 semanas) | 8.703,21 viagens/dia |
| WAPE da referência sazonal | 22% da demanda observada |
| RMSE da referência semanal fixa | 13.849,16 viagens/dia |

A validação escolheu o Prophet anual (RMSE 6.605,41). Nesse recorte, a referência de **52 semanas** teve RMSE 9.133,07 e a referência semanal fixa, 9.549,77. O teste final foi consultado **após** escolher o método; ambas as referências foram avaliadas nele para dar escala ao resultado. Os números foram obtidos executando `forecast.py` com a fonte fixada no commit indicado abaixo; podem variar um pouco conforme a versão do Prophet.

### Diagnóstico em datas anteriores ao teste

Repeti previsões de 90 dias completos com três cortes no histórico **anterior ao teste**. O RMSE (viagens/dia) não depende de consultar os 140 dias reservados:

| Última data de treino | Semanal fixa | 52 semanas | Prophet padrão | Prophet anual | Anual sem outliers |
|---|---:|---:|---:|---:|---:|
| 22/01/2016 | 5.062 | 5.202 | 12.619 | 4.025 | **3.963** |
| 15/03/2016 | 9.593 | 7.110 | 13.788 | **6.439** | 6.780 |
| 07/05/2016 | 9.550 | 9.133 | 6.992 | **6.605** | 6.610 |

O Prophet anual superou **as duas referências** nos três cortes. A remoção de outliers venceu apenas no primeiro; o Prophet padrão ficou pior que as referências nos dois primeiros. As janelas se sobrepõem e não representam três testes independentes. A tabela serve para verificar a sensibilidade à data de corte, sem reescolher o método com base no teste final.

## Dados e decisões

Fonte: [`bicicletas.csv` no repositório educacional da Alura](https://github.com/alura-cursos/data_science_projeto/blob/2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb/Dados/bicicletas.csv), commit `2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb`. O CSV é lido diretamente da origem e não é redistribuído aqui. O período vai de 04/01/2015 a 03/01/2017.

Após remover duplicatas, 34 dias têm menos de 24 medições. Não é correto comparar uma soma parcial com um total diário completo, por isso esses dias são excluídos da modelagem. A exclusão pode introduzir viés; o notebook de exploração mostra essa decisão. Variáveis climáticas ajudam na exploração, mas **não** entram como regressores no modelo de previsão.

Os 20% finais dos dias completos são reservados para teste. Do trecho anterior, os 90 dias finais servem como validação. Comparamos duas referências sem dados futuros: a primeira repete o último valor observado por dia da semana, fixo em todo o horizonte; a segunda usa o valor do mesmo dia da semana **52 semanas antes**. Quando a data correspondente foi excluída como incompleta, a segunda recorre ao último valor disponível daquele dia da semana (10 de 140 dias no teste). Também comparamos Prophet padrão, Prophet anual e Prophet anual após tratamento de outliers apenas no treino. O método com menor RMSE de validação é reajustado no treino total e avaliado uma vez no teste. A WAPE é a soma dos erros absolutos dividida pela demanda total observada no período.

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

## Limitações

O teste representa apenas um período histórico; os três cortes de diagnóstico têm janelas sobrepostas e abrangem menos de dois anos de dados. A decomposição anual do Prophet pode ser instável com esse histórico. A referência sazonal de 52 semanas é mais competitiva que a semanal fixa, mas também depende de poucos anos e de uma regra de recuo para dias incompletos. Uma próxima avaliação deveria usar mais anos. Não há evidência aqui de que clima *cause* mudanças na demanda, nem de que o erro do teste se repetiria em operação.

**Autor:** Lucas Guimarães · Engenharia da Computação, FIAP
