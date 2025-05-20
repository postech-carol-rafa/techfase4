# Importando bibiotecas
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from utils import ColunasDatas, ColunasVariacaoDia, ColunasVariacaoMensal, ColunasVariacaoAnual, DeletarNulos


# Funções

def pipeline_ipea_streamlit(df):
    pipeline_dados_ipea_streamlit = Pipeline([
         ('ColunasDatas', ColunasDatas())
        ,('ColunasVariacaoDia', ColunasVariacaoDia(df_modelo = False))
        ,('ColunasVariacaoMensal', ColunasVariacaoMensal(df_modelo = False))
        ,('ColunasVariacaoAnual', ColunasVariacaoAnual(df_modelo = False))
        ,('DeletarNulos', DeletarNulos())
    ])
    df_pipeline_ipea_streamlit = pipeline_dados_ipea_streamlit.fit_transform(df)
    return df_pipeline_ipea_streamlit


# Carregando DataFrame IPEA - Brent
df_ipea_brent = pd.read_csv("data/df_ipea_brent.csv")
df_ipea_brent['data'] = pd.to_datetime(df_ipea_brent['data'])
df_ipea_brent['valor'] = pd.Series(df_ipea_brent['valor'], dtype='Float64')


# Array e DataFrames filtrados para aplicação para seleção de anos e controles. Por exemplo: Filtros da aplicação.
df_media_anual = df_ipea_brent.groupby('ano').media_anual.first().reset_index()
anos = sorted(df_ipea_brent['ano'].unique(), reverse=True)


nome_meses = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}

nome_completo_mes = {
   "Todos": 0,
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12
}

ordenacao_meses = list(nome_meses.values())




# Área dos filtros do Dashboard
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
   ano_selecionado = st.selectbox(
                        "Selecione o ano",
                        anos,                       
                     )
   
limite_mes = df_ipea_brent[df_ipea_brent['ano'] == ano_selecionado]['mes'].max() + 1

with col_f2:
   mes_selecionado = st.selectbox(
                        "Selecione o mês",
                        list(nome_completo_mes.keys())[:limite_mes],
                        
                     )
   
with col_f3:
   Tipo_dados = st.selectbox(
                        "Selecione a periodicidade",
                        ['Em Lote', 'Tempo Real'],
                        index= 0 
                     )
   
## Selecionando o DataFrame para Dashboard (Histórico ou Tempo Real)
if Tipo_dados == 'Tempo Real':  
   url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'

   df_ipea_brent_tempo_real = pd.read_html(url
                                             ,encoding='utf-8'
                                             ,attrs={'id':'grd_DXMainTable'} 
                                             ,thousands= '.' 
                                             ,skiprows=1 
                                             )[0]

   df_ipea_brent_tempo_real.columns = ['data', 'valor']
   df_ipea_brent_tempo_real['data'] = pd.to_datetime(df_ipea_brent_tempo_real['data'] , format="%d/%m/%Y")
   df_ipea_brent_tempo_real['valor'] = df_ipea_brent_tempo_real['valor'].str.replace(',','.')
   df_ipea_brent_tempo_real['valor'] = df_ipea_brent_tempo_real['valor'].astype(float)
   df_ipea_brent_tempo_real = df_ipea_brent_tempo_real.set_index('data')
   df_ipea_brent_tempo_real = df_ipea_brent_tempo_real.sort_index(ascending=True)
   df_ipea_brent_tempo_real = pipeline_ipea_streamlit(df_ipea_brent_tempo_real)
   df_ipea_brent_tempo_real = df_ipea_brent_tempo_real.reset_index()
   df_ipea_brent = df_ipea_brent_tempo_real


with col_f4:
  data_formatada = df_ipea_brent['data'].max().strftime('%d/%m/%Y')
  st.write(f"Última Atualização:  {data_formatada}")

# Variáveis para os filtros selecionados e para cor do gráfico
numero_mes = nome_completo_mes[mes_selecionado]
ultimos_anos = df_ipea_brent[(df_ipea_brent['ano'] >= ano_selecionado - 2) & (df_ipea_brent['ano'] <= ano_selecionado)].groupby(['ano','mes']).media_mensal.first().reset_index()
ultimos_anos["mes_nome"] = ultimos_anos["mes"].map(nome_meses)
ultimos_anos["mes_nome"] = pd.Categorical(ultimos_anos["mes_nome"],categories=ordenacao_meses,ordered=True)
cores_azul = [ "#71C5E8",  "#F28E2B", "#59A14F"]

valor_mensal_ticket = ''
max_mensal_ticket = ''

if numero_mes > 0:
   valor_mensal_ticket = df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado) & (df_ipea_brent['mes'] == numero_mes)]['media_mensal'].round(2).iloc[0]
   max_mensal_ticket = df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado) & (df_ipea_brent['mes'] == numero_mes)]['valor'].max()
else:
   valor_mensal_ticket = '--'
   max_mensal_ticket = '--'

variacao_diaria = ((df_ipea_brent['valor'].iloc[-1].round(2) / df_ipea_brent['valor'].iloc[-2].round(2)) - 1) * 100


# Área dos cards e data

col_met1, col_met2, col_met3, col_met4, col_met5 = st.columns(5)


# Formatação da fonte dos cards
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        }
   [data-testid="stMetricDelta"] {
      font-size: 14px;
      }
    </style>
    """,
    unsafe_allow_html=True
)


with col_met1:
   with st.container(border=True):
      st.metric(label="Valor Atual Brent", value=df_ipea_brent['valor'].tail(1).iloc[0].round(2), 
                #delta=f"{variacao_diaria:.2f}%", delta_color="inverse"
                )
with col_met2:
   with st.container(border=True):
      st.metric(label="Valor Brent Médio Anual", value=df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado)]['media_anual'].round(2).iloc[0])
with col_met3:
   with st.container(border=True):
      st.metric(label="Máxima Brent Anual", value=df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado)]['valor'].max())
if numero_mes > 0:
   with col_met4:
      with st.container(border=True):
         st.metric(label="Valor Brent Médio Mensal", value=valor_mensal_ticket)
   with col_met5:
      with st.container(border=True):
         st.metric(label="Máxima Brent Mensal", value=max_mensal_ticket)
else:
   with col_met4:
      st.html('''
                    <div style="text-align: justify; font-size: 12px; font-style: italic;">
                    Selecione o mês para apresentar métricas mensais
                    </div>
            ''')
      



# Primeira área dos gráficos (Média mensal dos últimos 3 anos - Top 5 Maiores Médias)

colg11, colg12 = st.columns([2,1])

with colg11: 
   fig1 = px.line(ultimos_anos, x="mes_nome", y="media_mensal", color="ano", color_discrete_sequence=cores_azul)
   fig1.update_layout(
      title_text="Média mensal dos últimos 3 anos",
      xaxis=dict(title=''),
      yaxis=dict(title='')
   )
   with st.container(border=True):
     st.plotly_chart(fig1, use_container_width=True)

with colg12:
   fig2 = px.bar(
      df_media_anual.sort_values('media_anual', ascending = False).head(5),
      x="ano",
      y="media_anual",
      text="media_anual"
   )

   fig2.update_traces(
      texttemplate='%{text:,.2f}',
      textposition="outside",
      textfont=dict(
         size=14, 
         color="white"
      )
   )

   fig2.update_layout(
      title_text="Top 5 maiores médias",
      xaxis=dict(type='category',title='',showgrid=False),
      yaxis=dict(
         title='',  # Remover título do eixo Y
         range=[0, df_media_anual["media_anual"].max() * 1.2],  # Ajustar o intervalo do eixo Y
         showgrid=False,  # Remove as linhas de grade no eixo Y
         showticklabels=False  # Remove os valores (ticks) no eixo Y
      )
   )
   
   with st.container(border=True):
      st.plotly_chart(fig2, use_container_width=True)

# Segunda área dos gráficos (Média mensal dos últimos 3 anos - Top 5 Maiores Médias)
if numero_mes == 0:
   st.write('Selecione um mês para visualizar o valor diário')

else:

   with st.container(border=True):
      fig3 = px.line(df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado) & (df_ipea_brent['mes'] == numero_mes)], x="data", y="valor", markers= True, text = df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado) & (df_ipea_brent['mes'] == numero_mes)]['valor'])
      fig3.update_layout(
            title_text="Valor Diário do Petróleo Brent",
            xaxis=dict(title=''),
            yaxis=dict(title=''),
         )
      
      fig3.update_traces(textposition="top center",textfont=dict(color="#87CEEB", size=14),line=dict(color="#636363"))  
      # cores_azul = [ "#71C5E8",  "#F28E2B", "#59A14F"] 
      
      valor_medio = df_ipea_brent[(df_ipea_brent['ano'] == ano_selecionado) & (df_ipea_brent['mes'] == numero_mes)]['valor'].mean()
               
      
      fig3.add_hline(
         y=valor_medio,
         line_dash="dot",
         line_color="#59A14F",
         annotation_text=f"Valor Médio: {valor_medio:.2f}",  # valor com 2 casas decimais
         annotation_position="bottom right"
      )
      
      fig3.update_layout(
    title_text="Valor Diário do Petróleo Brent",
    xaxis=dict(
        title='',
        tickformat="%d"
    ),
    yaxis=dict(title='')
   )
            
      
      st.plotly_chart(fig3, use_container_width=True)
