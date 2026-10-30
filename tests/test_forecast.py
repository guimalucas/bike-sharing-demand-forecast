import unittest

import pandas as pd

import numpy as np

from forecast import dividir, pontuar, preparar_dados, prever, validacao_historica


class ForecastTests(unittest.TestCase):
    def test_deduplicates_and_excludes_incomplete_days(self):
        horas = pd.date_range("2020-01-01", periods=48, freq="h")
        dados = pd.DataFrame({"data_hora": horas, "contagem": 1})
        dados = pd.concat([dados.loc[dados["data_hora"].ne(horas[30])],
                           dados.iloc[[0]]], ignore_index=True)
        serie, incompletos = preparar_dados(dados)
        self.assertEqual(incompletos, 1)
        self.assertEqual(serie["y"].tolist(), [24])

    def test_validation_and_test_follow_training_dates(self):
        serie = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=600),
                              "y": range(600)})
        desenvolvimento, validacao, treino, teste = dividir(serie, validacao=90)
        self.assertLess(desenvolvimento["ds"].max(), validacao["ds"].min())
        self.assertLess(validacao["ds"].max(), teste["ds"].min())
        self.assertEqual(len(treino) + len(teste), len(serie))

    def test_historical_windows_never_use_reserved_test_or_future_values(self):
        serie = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=700),
                              "y": np.arange(700, dtype=float)})
        observado = []

        def preditor(metodo, treino, janela):
            observado.append((treino["ds"].max(), janela["ds"].min(), janela["ds"].max()))
            return np.repeat(treino["y"].iloc[-1], len(janela)), 0

        resultado = validacao_historica(
            serie, horizonte=90, cortes=(366, 416, 470),
            metodos=("referencia",), preditor=preditor,
        )
        teste_inicio = serie.iloc[int(len(serie) * 0.8)]["ds"]
        self.assertEqual(len(resultado), 3)
        self.assertTrue(all(a < b <= c < teste_inicio for a, b, c in observado))
        self.assertAlmostEqual(pontuar(np.array([10, 20]), np.array([8, 22]))["WAPE"], 4 / 30)

        with self.assertRaises(ValueError):
            validacao_historica(serie, horizonte=90, cortes=(500,), preditor=preditor)

    def test_prophet_forecast_runs_on_a_small_known_series(self):
        treino = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=400),
                               "y": 100 + np.arange(400) * 0.1})
        datas = pd.DataFrame({"ds": pd.date_range("2021-02-04", periods=7)})
        previsao, removidos = prever("prophet_anual", treino, datas)
        self.assertEqual(len(previsao), len(datas))
        self.assertTrue(np.isfinite(previsao).all())
        self.assertEqual(removidos, 0)

    def test_previous_year_reference_uses_only_known_days_and_fallback(self):
        treino = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=400),
                               "y": np.arange(400, dtype=float)})
        alvo = treino["ds"].iloc[-1] + pd.Timedelta(days=1)
        previsto, _ = prever("ano_anterior_52_semanas", treino,
                            pd.DataFrame({"ds": [alvo]}))
        esperado = treino.set_index("ds").loc[alvo - pd.Timedelta(weeks=52), "y"]
        self.assertEqual(previsto[0], esperado)

        ausente = alvo - pd.Timedelta(weeks=52)
        incompleto = treino.loc[treino["ds"].ne(ausente)]
        previsto, _ = prever("ano_anterior_52_semanas", incompleto,
                            pd.DataFrame({"ds": [alvo]}))
        ultimo = incompleto.loc[incompleto["ds"].dt.dayofweek.eq(alvo.dayofweek), "y"].iloc[-1]
        self.assertEqual(previsto[0], ultimo)


if __name__ == "__main__":
    unittest.main()
