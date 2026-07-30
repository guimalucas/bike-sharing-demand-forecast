# Previsão da Demanda de Bicicletas com Séries Temporais

## Sobre o projeto

A previsão da demanda é um dos principais desafios enfrentados por serviços de compartilhamento de bicicletas, pois influencia diretamente o planejamento operacional, a distribuição das bicicletas e a qualidade do serviço oferecido aos usuários.

O objetivo deste projeto é analisar os fatores que influenciam a demanda diária por bicicletas compartilhadas e desenvolver modelos de previsão utilizando séries temporais com Prophet.

O projeto foi dividido em duas etapas principais: uma Análise Exploratória de Dados (EDA), voltada para compreensão do comportamento da demanda e validação de hipóteses, seguida da construção e aprimoramento de modelos preditivos utilizando a biblioteca Prophet.

Todo o projeto foi desenvolvido em Python utilizando bibliotecas especializadas em análise de dados, visualização, estatística e modelagem de séries temporais.

---

# Objetivos

- Realizar a limpeza e preparação dos dados;
- Explorar o comportamento das variáveis do conjunto de dados;
- Formular e validar hipóteses estatísticas;
- Identificar fatores que influenciam a demanda por bicicletas;
- Desenvolver modelos de previsão utilizando Prophet;
- Comparar diferentes estratégias de modelagem;
- Avaliar os modelos utilizando RMSE;
- Interpretar os resultados sob uma perspectiva de negócio.

---

# Dataset

O conjunto de dados utilizado contém informações diárias sobre o sistema de compartilhamento de bicicletas, incluindo variáveis climáticas, temporais e a quantidade de bicicletas alugadas.

As principais variáveis analisadas incluem:

- Data
- Temperatura
- Sensação térmica
- Umidade
- Velocidade do vento
- Estação do ano
- Condições climáticas
- Quantidade de bicicletas alugadas

> **Observação:** O dataset foi disponibilizado durante o curso de Data Science da Alura e, por questões de licença, não está incluído neste repositório.

---

# Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Statsmodels
- Prophet
- Scikit-Learn
- Jupyter Notebook

---

# Etapas do projeto

O projeto foi desenvolvido em duas etapas complementares.

## Parte 1 — Análise Exploratória de Dados

Nesta etapa foram realizadas:

- Limpeza dos dados;
- Tratamento de variáveis;
- Estatística descritiva;
- Visualizações gráficas;
- Formulação de hipóteses;
- Aplicação de testes estatísticos;
- Interpretação dos resultados.

## Parte 2 — Modelagem com Prophet

Após compreender o comportamento dos dados, foram desenvolvidos diferentes modelos utilizando Prophet, incluindo:

- Modelo inicial;
- Ajustes de sazonalidade;
- Tratamento de outliers;
- Comparação entre diferentes estratégias de modelagem;
- Avaliação utilizando RMSE.

---

# Principais análises realizadas

Durante a Análise Exploratória de Dados foram investigadas diversas relações entre as variáveis do conjunto de dados, incluindo:

- Influência da temperatura na demanda;
- Relação entre sensação térmica e quantidade de bicicletas alugadas;
- Impacto da umidade;
- Impacto da velocidade do vento;
- Diferenças entre dias úteis e finais de semana;
- Influência das estações do ano;
- Comportamento temporal da demanda;
- Validação das hipóteses utilizando testes estatísticos.

---

# Modelagem e avaliação

A etapa de modelagem utilizou Prophet para construir modelos de previsão capazes de capturar tendências e sazonalidades presentes na série temporal.

Ao longo do projeto foram avaliadas diferentes estratégias de modelagem, incluindo ajustes sucessivos no modelo e comparação entre seus desempenhos.

A qualidade preditiva foi avaliada utilizando a métrica RMSE, permitindo comparar objetivamente os modelos desenvolvidos.

---

# Principais conclusões

A análise demonstrou que fatores climáticos exercem influência significativa sobre a demanda por bicicletas compartilhadas.

Temperatura e sensação térmica apresentaram associação positiva com a quantidade de bicicletas alugadas, enquanto a umidade apresentou associação negativa.

Os modelos desenvolvidos utilizando Prophet conseguiram representar adequadamente o comportamento da série temporal e os ajustes realizados ao longo do projeto contribuíram para melhorar a capacidade preditiva em relação ao modelo inicial.

Os resultados obtidos demonstram como técnicas de análise exploratória, estatística e séries temporais podem apoiar processos de planejamento operacional e tomada de decisão.

---

# Estrutura do repositório

```
bike-sharing-demand-forecast
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── EDA_Bike_Sharing.ipynb
└── Forecast_Prophet.ipynb
```

---

# Como executar

Clone o repositório:

```bash
git clone https://github.com/guimalucas/bike-sharing-demand-forecast.git
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Como o dataset não está incluído neste repositório, será necessário obtê-lo e atualizar o caminho do arquivo utilizado nos notebooks.

Após isso, basta abrir os notebooks no Jupyter Notebook ou Google Colab e executar as células em sequência.

---

# Competências Demonstradas

Ao longo deste projeto foram aplicadas competências relacionadas à Ciência de Dados, incluindo:

- Limpeza e preparação de dados;
- Análise Exploratória de Dados (EDA);
- Estatística descritiva;
- Formulação e validação de hipóteses;
- Testes estatísticos;
- Visualização de dados;
- Séries temporais;
- Modelagem com Prophet;
- Avaliação de modelos;
- Interpretação de resultados;
- Comunicação de insights.

---

# Autor

Lucas Guimarães

Estudante de Engenharia da Computação – FIAP

GitHub: https://github.com/guimalucas
