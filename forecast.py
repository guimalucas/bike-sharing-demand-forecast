"""Experimento reproduzível de previsão diária com validação temporal."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_URL = "https://raw.githubusercontent.com/alura-cursos/data_science_projeto/2015d5713c3cdbc1ee78cdc93d9a833b1cc59eeb/Dados/bicicletas.csv"
METHODS = ("ultimo_dia_semana", "ano_anterior_52_semanas", "prophet_padrao",
           "prophet_anual", "prophet_anual_sem_outliers")


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
    if metodo == "ano_anterior_52_semanas":
        # 52 semanas mantêm o dia da semana; nunca consultamos o período previsto.
        anterior = (datas["ds"] - pd.Timedelta(weeks=52)).map(treino.set_index("ds")["y"])
        ultimos = treino.assign(semana=treino["ds"].dt.dayofweek).groupby("semana")["y"].last()
        fallback = datas["ds"].dt.dayofweek.map(ultimos)
        return anterior.fillna(fallback).to_numpy(), 0
    if metodo not in METHODS:
        raise ValueError(f"Método desconhecido: {metodo}")
    # A preparação e os testes de divisão temporal não dependem do Prophet.
    from prophet import Prophet

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
    denominador = np.abs(real).sum()
    return {
        "RMSE": float(np.sqrt(mean_squared_error(real, previsto))),
        "MAE": float(mean_absolute_error(real, previsto)),
        "WAPE": float(np.abs(real - previsto).sum() / denominador) if denominador else float("nan"),
    }


def validacao_historica(
    serie: pd.DataFrame, horizonte: int = 90, cortes: tuple[int, ...] | None = None,
    metodos: tuple[str, ...] = METHODS, preditor=None,
) -> pd.DataFrame:
    """Repete a previsão em datas anteriores ao teste reservado, sem acessar o futuro.

    Cada janela contém `horizonte` dias *completos* da série, que pode ter
    lacunas no calendário por causa dos dias excluídos na preparação.
    """
    _, _, historico, teste = dividir(serie, validacao=horizonte)
    ultimo_corte = len(historico) - horizonte
    if cortes is None:
        cortes = tuple(range(366, ultimo_corte + 1, 50))
        if ultimo_corte > 365 and ultimo_corte not in cortes:
            cortes += (ultimo_corte,)
    if not cortes or any(c <= 365 or c > ultimo_corte for c in cortes):
        raise ValueError("Cada corte precisa de mais de 365 dias anteriores e horizonte completo.")

    preditor = preditor or prever
    linhas = []
    for corte in cortes:
        treino = historico.iloc[:corte]
        janela = historico.iloc[corte:corte + horizonte]
        assert treino["ds"].max() < janela["ds"].min()
        assert janela["ds"].max() < teste["ds"].min()
        for metodo in metodos:
            previsao, removidos = preditor(metodo, treino, janela)
            linhas.append({
                "corte": treino["ds"].max().date(),
                "janela_inicio": janela["ds"].min().date(),
                "janela_fim": janela["ds"].max().date(),
                "modelo": metodo,
                **pontuar(janela["y"].to_numpy(), previsao),
                "outliers_removidos": removidos,
            })
    return pd.DataFrame(linhas)


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
    previsao_referencia, _ = prever("ano_anterior_52_semanas", treino, teste)
    previsao_fixa, _ = prever("ultimo_dia_semana", treino, teste)
    resultado = {
        "modelo": vencedor, "teste": pontuar(teste["y"], previsao_teste),
        "referencia_teste": pontuar(teste["y"], previsao_referencia),
        "referencia_fixa_teste": pontuar(teste["y"], previsao_fixa),
        "previsoes": teste.assign(yhat=previsao_teste),
        "outliers_removidos_no_treino": removidos,
        "tamanhos": (len(desenvolvimento), len(validacao), len(treino), len(teste)),
    }
    return tabela, resultado


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=DATA_URL, help="CSV local ou URL de origem da Alura")
    parser.add_argument("--backtest", action="store_true", help="Avaliar também janelas históricas anteriores ao teste")
    args = parser.parse_args()
    serie, incompletos = preparar_dados(pd.read_csv(args.data))
    tabela, resultado = experimento(serie)
    print(f"Dias completos: {len(serie)}; dias incompletos excluídos: {incompletos}")
    print(f"Desenvolvimento/validação/treino total/teste: {resultado['tamanhos']}")
    print("\nValidação (escolha do modelo):\n", tabela.to_string(index=False, float_format=lambda n: f"{n:.2f}"))
    print(f"\nModelo selecionado: {resultado['modelo']}")
    print("Teste final: " + ", ".join(f"{k}={v:.2f}" for k, v in resultado["teste"].items()))
    print("Referência 52 semanas no teste: " + ", ".join(
        f"{k}={v:.2f}" for k, v in resultado["referencia_teste"].items()
    ))
    print("Referência semanal fixa no teste: " + ", ".join(
        f"{k}={v:.2f}" for k, v in resultado["referencia_fixa_teste"].items()
    ))
    if args.backtest:
        historico = validacao_historica(serie)
        print("\nDiagnóstico histórico (fora do teste reservado):")
        print(historico[["corte", "modelo", "RMSE", "MAE", "WAPE"]].to_string(
            index=False, float_format=lambda n: f"{n:.2f}"
        ))


if __name__ == "__main__":
    main()
