import unittest

import pandas as pd

from forecast import dividir, preparar_dados


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


if __name__ == "__main__":
    unittest.main()
