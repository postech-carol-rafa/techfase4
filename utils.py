import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class ColunasDatas(BaseEstimator, TransformerMixin):
  def __init__ (self, colunas_data=None):
    self.colunas_data = colunas_data

  def fit(self, df):
    return self

  def transform(self, df):

    if type(df.index) != pd.DatetimeIndex:
      print('O index do dataframe não é do tipo DatetimeIndex')
      return df
    else:
      nome_dia_semana = {
          0: 'Segunda-feira',
          1: 'Terça-feira',
          2: 'Quarta-feira',
          3: 'Quinta-feira',
          4: 'Sexta-feira',
          5: 'Sábado',
          6: 'Domingo'
      }

      df['dia'] = df.index.day
      df['mes'] = df.index.month
      df['ano'] = df.index.year
      df['dia_semana'] = df.index.weekday
      df['nome_dia_semana'] = df['dia_semana'].map(nome_dia_semana)
      df['bimestre'] = ((df['mes'] - 1) // 2) + 1
      df['trimestre'] = ((df['mes'] - 1) // 3) + 1
      df['semestre'] = ((df['mes'] - 1) // 6) + 1

      return df


class ColunasVariacaoDia(BaseEstimator, TransformerMixin):
    def __init__(self, colunas_variacao='valor', df_modelo=True):
        self.colunas_variacao = colunas_variacao
        self.df_modelo = df_modelo

    def fit(self, df):
        return self

    def transform(self, df):
        if self.colunas_variacao in df.columns:
            if self.df_modelo:
              df['variacao_lag1'] = df[self.colunas_variacao].shift(1).diff()
              df['p_variacao_lag1'] = (df[self.colunas_variacao].shift(1) / df[self.colunas_variacao].shift(2) - 1)

            else:
              df['variacao'] = df[self.colunas_variacao].diff()
              df['p_variacao'] = (df[self.colunas_variacao] / df[self.colunas_variacao].shift(1) - 1)
            return df
        else:
            print(f"A coluna 'valor' não existe no DataFrame.")
            return df


class ColunasVariacaoMensal(BaseEstimator, TransformerMixin):
    def __init__(self, coluna_valor='valor', df_modelo=True):
        self.coluna_valor = coluna_valor
        self.df_modelo = df_modelo


    def fit(self, df):
        return self

    def transform(self, df):
        if all(col in df.columns for col in ['ano', 'mes', self.coluna_valor]):
          if self.df_modelo:
              medias_mensais = df.groupby(['ano', 'mes'])[self.coluna_valor].mean().shift(1).reset_index()
              medias_mensais['variacao_mensal_lag1'] = medias_mensais[self.coluna_valor].shift(1).diff()
              medias_mensais['p_variacao_mensal_lag1'] = (medias_mensais[self.coluna_valor].shift(1) / medias_mensais[self.coluna_valor].shift(2) - 1)
              medias_mensais = medias_mensais.rename(columns={'valor': 'media_mensal_lag1'})
              df = df.reset_index()
              df = df.merge(medias_mensais, on=['ano', 'mes'], how='left')
              df = df.set_index('data')
              df = df.sort_index(ascending=True)
          else:
              medias_mensais = df.groupby(['ano', 'mes'])[self.coluna_valor].mean().reset_index()
              medias_mensais['variacao_mensal'] = medias_mensais[self.coluna_valor].diff()
              medias_mensais['p_variacao_mensal'] = (medias_mensais[self.coluna_valor] / medias_mensais[self.coluna_valor].shift(1) - 1)
              medias_mensais = medias_mensais.rename(columns={'valor': 'media_mensal'})
              df = df.reset_index()
              df = df.merge(medias_mensais, on=['ano', 'mes'], how='left')
              df = df.set_index('data')
              df = df.sort_index(ascending=True)
          return df
        else:
            print("As colunas 'ano', 'mes' ou 'valor' não existem no DataFrame.")
            return df


class ColunasVariacaoAnual(BaseEstimator, TransformerMixin):
    def __init__(self, coluna_valor='valor', df_modelo=True):
        self.coluna_valor = coluna_valor
        self.df_modelo = df_modelo

    def fit(self, df):
        return self

    def transform(self, df):
        if all(col in df.columns for col in ['ano', self.coluna_valor]):
          if self.df_modelo:
              medias_anuais = df.groupby('ano')[self.coluna_valor].mean().shift(1).reset_index()
              medias_anuais['variacao_anual_lag1'] = medias_anuais[self.coluna_valor].shift(1).diff()
              medias_anuais['p_variacao_anual_lag1'] = (medias_anuais[self.coluna_valor].shift(1) / medias_anuais[self.coluna_valor].shift(2) - 1)
              medias_anuais = medias_anuais.rename(columns={'valor': 'media_anual_lag1'})
              df = df.reset_index()
              df = df.merge(medias_anuais, on='ano', how='left')
              df = df.set_index('data')
              df = df.sort_index(ascending=True)
          else:
              medias_anuais = df.groupby('ano')[self.coluna_valor].mean().reset_index()
              medias_anuais['variacao_anual'] = medias_anuais[self.coluna_valor].diff()
              medias_anuais['p_variacao_anual'] = (medias_anuais[self.coluna_valor] / medias_anuais[self.coluna_valor].shift(1) - 1)
              medias_anuais = medias_anuais.rename(columns={'valor': 'media_anual'})
              df = df.reset_index()
              df = df.merge(medias_anuais, on='ano', how='left')
              df = df.set_index('data')
              df = df.sort_index(ascending=True)
          return df
        else:
            print("As colunas 'ano' ou 'valor' não existem no DataFrame.")
            return df

class RollingFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, n_rolling=28):
        self.n_rolling = n_rolling
        self.colunas_rolling = ['valor', 'variacao', 'p_variacao']

    def fit(self, df):
        return self

    def transform(self, df):
        for col in self.colunas_rolling:
            if col in df.columns:
                df[f'rolling_mean_{col}_{self.n_rolling}'] = (
                    df[col]
                    .rolling(window=self.n_rolling)
                    .mean()
                    .shift(1)
                )

                df[f'rolling_std_{col}_{self.n_rolling}'] = (
                    df[col]
                    .rolling(window=self.n_rolling)
                    .std()
                    .shift(1)
                )
            else:
                print(f"Coluna '{col}' não encontradas no DataFrame para Rolling")

        return df


class LagsFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, n_lags=5):
        self.n_lags = n_lags
        self.colunas_alvo = ['valor']

    def fit(self, df):
        return self

    def transform(self, df):
        for col in self.colunas_alvo:
            if col in df.columns:
                for lag in range(1, self.n_lags + 1):
                    df[f'lag_{lag}_{col}'] = df[col].shift(lag)
            else:
                print('Coluna valor não encontrada no DataFrame')

        return df

class DeletarNulos(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass  # Nenhum parâmetro necessário

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        df.dropna(inplace=True)
        return df









