"""Experimento reproduzível de previsão diária com validação temporal."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_URL = "https://raw.githubusercontent.com/alura-cursos/data_science_projeto/2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb/Dados/bicicletas.csv"
METHODS = ("ultimo_dia_semana", "prophet_padrao", "prophet_anual", "prophet_anual_sem_outliers")


def preparar_dados(dados: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    dados = dados.copy()
    dados["data_hora"] = pd.to_datetime(dados["data_hora"], errors="raise")
    dados = dados.drop_duplicates().sort_values("data_hora")
    if dados["data_hora"].duplicated().any():
        raise ValueError("Há mais de uma medição para a mesma hora.")
    dados["ds"] = dados["data_hora"].dt.normalize()
    por_dia = dados.groupby("ds").agg(y=("contagem", "sum"), horas=("data_hora", "nunique"))
    incompletos = int(por_dia["horas"].ne(24).sum())
    serie = por_dia.loc[por_dia["horas"].eq(24), ["y"]].reset_index()
    if serie["y"].isna().any() or serie["ds"].duplicated().any():
        raise ValueError("Série diária inválida.")
    return serie, incompletos


def dividir(serie: pd.DataFrame, validacao: int = 90):
    serie = serie.sort_values("ds").reset_index(drop=True)
    corte = int(len(serie) * 0.8)
    treino, teste = serie.iloc[:corte].copy(), serie.iloc[corte:].copy()
    if len(treino) <= validacao + 365:
        raise ValueError("Histórico insuficiente para a validação com ciclo anual.")
    return treino.iloc[:-validacao].copy(), treino.iloc[-validacao:].copy(), treino, teste


def prever(metodo: str, treino: pd.DataFrame, datas: pd.DataFrame) -> tuple[np.ndarray, int]:
    if metodo == "ultimo_dia_semana":
        ultimos = treino.assign(semana=treino["ds"].dt.dayofweek).groupby("semana")["y"].last()
        return datas["ds"].dt.dayofweek.map(ultimos).to_numpy(), 0
    if metodo not in METHODS:
        raise ValueError(f"Método desconhecido: {metodo}")
    anual = metodo != "prophet_padrao"
    modelo = Prophet(yearly_seasonality=anual, weekly_seasonality=True)
    modelo.fit(treino[["ds", "y"]])
    removidos = 0
    if metodo == "prophet_anual_sem_outliers":
        # A amostragem usada nos intervalos do Prophet é estocástica.
        np.random.seed(4587)
        ajuste = modelo.predict(treino[["ds"]])
        mascara = treino["y"].between(ajuste["yhat_lower"], ajuste["yhat_upper"])
        removidos = int((~mascara).sum())
        modelo = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        modelo.fit(treino.loc[mascara, ["ds", "y"]])
    return modelo.predict(datas[["ds"]])["yhat"].to_numpy(), removidos


def pontuar(real: pd.Series, previsto: np.ndarray) -> dict:
    return {
        "RMSE": float(np.sqrt(mean_squared_error(real, previsto))),
        "MAE": float(mean_absolute_error(real, previsto)),
    }


def experimento(serie: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    desenvolvimento, validacao, treino, teste = dividir(serie)
    linhas = []
    for metodo in METHODS:
        previsao, removidos = prever(metodo, desenvolvimento, validacao)
        linhas.append({"modelo": metodo, **pontuar(validacao["y"], previsao),
                       "outliers_removidos_no_ajuste": removidos})
    tabela = pd.DataFrame(linhas).sort_values("RMSE").reset_index(drop=True)
    vencedor = tabela.loc[0, "modelo"]
    previsao_teste, removidos = prever(vencedor, treino, teste)
    resultado = {
        "modelo": vencedor, "teste": pontuar(teste["y"], previsao_teste),
        "previsoes": teste.assign(yhat=previsao_teste),
        "outliers_removidos_no_treino": removidos,
        "tamanhos": (len(desenvolvimento), len(validacao), len(treino), len(teste)),
    }
    return tabela, resultado


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=DATA_URL, help="CSV local ou URL de origem da Alura")
    args = parser.parse_args()
    serie, incompletos = preparar_dados(pd.read_csv(args.data))
    tabela, resultado = experimento(serie)
    print(f"Dias completos: {len(serie)}; dias incompletos excluídos: {incompletos}")
    print(f"Desenvolvimento/validação/treino total/teste: {resultado['tamanhos']}")
    print("\nValidação (escolha do modelo):\n", tabela.to_string(index=False, float_format=lambda n: f"{n:.2f}"))
    print(f"\nModelo selecionado: {resultado['modelo']}")
    print("Teste final: " + ", ".join(f"{k}={v:.2f}" for k, v in resultado["teste"].items()))


if __name__ == "__main__":
    main()
