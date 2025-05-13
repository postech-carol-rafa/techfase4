# Importando bibiotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose


# Carregando dataframe
url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
df_ipea_brent = pd.read_html(url 
                             ,encoding='utf-8' 
                             ,attrs={'id':'grd_DXMainTable'} 
                             ,thousands= '.'
                             ,skiprows=1 
                             )[0] 
df_ipea_brent.columns = ['data', 'preco_uss']
df_ipea_brent['data'] = pd.to_datetime(df_ipea_brent['data'], format="%d/%m/%Y")
df_ipea_brent['preco_uss'] = df_ipea_brent['preco_uss'].str.replace(',','.')
df_ipea_brent['preco_uss'] = pd.Series(df_ipea_brent['preco_uss'], dtype='Float64')
df_ipea_brent = df_ipea_brent.set_index('data')
df_ipea_brent = df_ipea_brent.sort_index()
nome_dia_semana = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}
df_ipea_brent['dia'] = df_ipea_brent.index.day
df_ipea_brent['mes'] = df_ipea_brent.index.month
df_ipea_brent['ano'] = df_ipea_brent.index.year
df_ipea_brent['dia_semana'] = df_ipea_brent.index.weekday
df_ipea_brent['nome_dia_semana'] = df_ipea_brent['dia_semana'].map(nome_dia_semana)
df_ipea_brent['bimestre'] = ((df_ipea_brent['mes'] - 1) // 2) + 1
df_ipea_brent['trimestre'] = ((df_ipea_brent['mes'] - 1) // 3) + 1
df_ipea_brent['semestre'] = ((df_ipea_brent['mes'] - 1) // 6) + 1

df_ipea_brent['variacao'] = df_ipea_brent['preco_uss'].diff() # vendo a diferença do dia atual pelo dia anterior

df_ipea_brent['p_variacao'] = ((df_ipea_brent['preco_uss'] / df_ipea_brent['preco_uss'].shift(1)) - 1) # Em porcentagem a diferença entre o dia atual e anterior

df_ipea_brent = df_ipea_brent.drop(df_ipea_brent.index[0])


#DataFrame de eventos

from datetime import datetime
import pandas as pd

# Lista de eventos históricos sem a coluna 'figura'
dados_eventos_novos = [
    {
        "data": datetime(1990, 9, 27),
        "titulo": "Guerra do Golfo",
        "preco": 41.45
    },
    {
        "data": datetime(1997, 2, 11),
        "titulo": "Crise Financeira Asiática",
        "preco": 21.25
    },
    {
        "data": datetime(2004, 10, 30),
        "titulo": "Tensões no Oriente Médio",
        "preco": 52.28
    },
    {
        "data": datetime(2008, 7, 7),
        "titulo": "Crescimento da Demanda Global",
        "preco": 143.00
    },
    {
        "data": datetime(2008, 12, 30),
        "titulo": "Crise Bolha Imobiliária Americana",
        "preco": 33.73
    },
    {
        "data": datetime(2010, 5, 7),
        "titulo": "Primavera Árabe",
        "preco": 88.09
    },
    {
        "data": datetime(2015, 1, 16),
        "titulo": "Excesso de Oferta Global",
        "preco": 46.90
    },
    {
        "data": datetime(2016, 10, 8),
        "titulo": "Recuperação Econômica Global",
        "preco": 51.23
    },
    {
        "data": datetime(2020, 4, 21),
        "titulo": "COVID-19 – Colapso da Demanda",
        "preco": 9.12
    },
    {
        "data": datetime(2022, 3, 8),
        "titulo": "Invasão da Ucrânia pela Rússia",
        "preco": 133.18
    },
    {
        "data": datetime(2025, 4, 8),
        "titulo": "Aumento Produção Países fora da OPEP+",
        "preco": 64.86
    }
]

# Criação do DataFrame
df_eventos_novos = pd.DataFrame(dados_eventos_novos)
df_eventos_novos.set_index("data", inplace=True)



# Array e DataFrames filtrados
anos = df_ipea_brent['ano'].unique()
precos_anuais = [df_ipea_brent[df_ipea_brent['ano'] == ano]['preco_uss'].mean().round(2) for ano in anos]
df_grouped = df_ipea_brent.groupby('ano')['preco_uss'].mean().reset_index() # Agrupar por ano e calcular a média
df_grouped['diferenca'] = ((df_grouped['preco_uss'] / df_grouped['preco_uss'].shift(1)) - 1) # Calcular a diferença ano a ano
df_grouped = df_grouped.drop(df_grouped.index[0])


#Funções

def plot_preco_brent(df, ano_inicial, ano_final, df_eventos=None, range_y=None):
    # Filtra o DataFrame principal pela data
    df_filtrado = df[(df['ano'] >= ano_inicial) & (df['ano'] <= ano_final)]

    fig = go.Figure()

    # Linha principal do preço
    fig.add_trace(go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_uss'],
        mode='lines',
        name='Preço do Brent (USD)',
        line=dict(color='#71C5E8', width=2),
        customdata=df_filtrado[['nome_dia_semana','p_variacao']].values,
        hovertemplate=(
            "<b>Data:</b> %{x|%d/%m/%Y}<br>" +
            "<b>Preço:</b> %{y:.2f} USD<br>" +
            "<b>Variação Diária:</b> %{customdata[1]:.2%}<br>" +
            "<b>Dia da Semana:</b> %{customdata[0]}<br>" +
            "<extra></extra>"
        )       
    ))

    # Adiciona anotações, se df_eventos for fornecido
    if df_eventos is not None:
        df_eventos_filtrado = df_eventos[(df_eventos.index.year >= ano_inicial) & (df_eventos.index.year <= ano_final)]

        for data, row in df_eventos_filtrado.iterrows():
            fig.add_annotation(
                x=data,
                y=row['preco'],
                xref='x',
                yref='y',
                text=f"<b>{row['titulo']}</b>",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor='orange',
                ax=0,
                ay=-40,
                bgcolor='rgba(0,0,0,0.6)',
                bordercolor='orange',
                font=dict(size=10, color='white'),
                align='center'
            )

    # Configurações do layout
    layout_config = dict(
        title=f'Preço do Petróleo Brent no período de {ano_inicial} até {ano_final}',
        xaxis_title='Ano',
        yaxis_title='Preço em USD',
        template='plotly_dark',
        xaxis=dict(
            tickformat='%Y',
            dtick="M24"
        )
    )

    if range_y:
        layout_config['yaxis'] = dict(range=range_y)

    fig.update_layout(**layout_config)

    st.plotly_chart(fig)





def plot_preco_brent_anual(df_anual, ano_ini, ano_fim):
    # Filtrar o DataFrame
    df_ano = df_anual[(df_anual['ano'] >= ano_ini) & (df_anual['ano'] <= ano_fim)].copy()

    # Criar o gráfico de barras
    fig = go.Figure()

    # Adicionar as barras
    fig.add_trace(go.Bar(
        x=df_ano['ano'],
        y=df_ano['preco_uss'],
        text=df_ano['preco_uss'].apply(lambda x: f"$ {x:.2f}"),
        textposition='inside',
        insidetextfont=dict(color='rgb(14, 17, 23)'),
        marker_color='#71C5E8',
        showlegend=False,
        hoverinfo='skip'
    ))

    # Adicionar anotações com a variação percentual (coloridas)
    for i, row in df_ano.iterrows():
        if pd.notna(row['diferenca']):
            cor = 'lightcoral' if row['diferenca'] < 0 else 'lightskyblue'
            sinal = "+" if row['diferenca'] >= 0 else "−"
            fig.add_annotation(
                x=row['ano'],
                y=row['preco_uss'] + 5,
                text=f"<span style='color:{cor}'>{sinal}{abs(row['diferenca']):.2f}%</span>",
                showarrow=False,
                font=dict(size=11)
            )

    # Layout
    fig.update_layout(
        title=f'Preço Médio Anual do Petróleo Brent de {ano_ini} até {ano_fim}',
        font=dict(color='white'),
        xaxis=dict(tickmode='linear', tick0=ano_ini, dtick=1, title='Ano'),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        uniformtext_minsize=8,
        uniformtext_mode='show',
        showlegend=False,
        hovermode=False
    )

    st.plotly_chart(fig, use_container_width=True)




def plot_var_brent(df, ano_inicial, ano_final):
    # Filtra o DataFrame pelo intervalo de anos
    df_filtrado = df[(df['ano'] >= ano_inicial) & (df['ano'] <= ano_final)]

    # Criação da figura
    fig = go.Figure()

    # Linha da variação percentual
    fig.add_trace(go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['p_variacao'],
        mode='lines',
        name='Variação Percentual do Brent',
        line=dict(color='#71C5E8', width=2),
    ))

    # Configurações do layout
    fig.update_layout(
        title=f'Variação Percentual do Preço do Petróleo Brent de {ano_inicial} até {ano_final}',
        xaxis_title='Data',
        yaxis_title='Variação Percentual',
        template='plotly_dark',
        xaxis=dict(
            tickformat='%Y',
            dtick='M12'
        ),
        yaxis=dict(
        tickformat='.0%',  # Formatar como percentual com 2 casas decimais
    )
    )

    # Exibe no Streamlit
    st.plotly_chart(fig, use_container_width=True)



######

st.title('Storytelling')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visão Geral", "💡 Insight - Eventos", "📅 Análise Temporal", "↗️ Variações","🛢️ Produção"])

with tab1:
   st.write('Abaixo apresentamos a variação do preço brent ao longo dos anos, é possível filtrar o período e passar o mouse na linha do tempo para visualizar os valores')
   st.empty() # Cria um espaço em branco

   # Filtrando ano
   ano_ini, ano_fim = st.slider(
      'Selecione o período de anos',
      min_value=anos.min(),
      max_value=anos.max(),
      value=(anos.min(), anos.max()),  # Definindo o intervalo padrão como todo o período
      step=1,  # Incremento de 1 ano
   )


   plot_preco_brent(df_ipea_brent,ano_ini,ano_fim)

   ##
   st.write('''  
      <div style="text-align: justify; font-size: 18px; color: #71C5E8">
         <strong>Visão Geral do Comportamento do Preço do Petróleo Brent</strong>
            </div>
            ''', unsafe_allow_html=True)



   st.write('''
            <div style="text-align: justify;">
               Ao analisar o gráfico anual com o período de 1987 até os dias atuais é possível visualizar uma tendencia crescente, evidenciando grandes variações em diversos anos.
               Um grande destaque para os anos de 2008 e 2020, onde em 2008 atingiu o maior pico, enquanto no ano de 2020 teve uma forte queda.
               Alguns fatores externos para esses anos que devem ser destacados, é que em 2008 tivemos a grande crise da bolha imobiliaria americana e em 2020 a epidemia do covid-19. Ambos afetaram a macroeconomia global, tendo relação direta com essas variações.
               Analisando esse cenário é possível dizer que trata-se de uma série temporal não estacionária.
            </div>
            ''', unsafe_allow_html=True)

################## ********************************


with tab2:
         
    periodo2 = (
    "1987 - 2000",
    "2000 - 2013",
    "2013 - 2025"
    )
 
    periodo_valor2 = st.segmented_control(
      "Selecione o Período", list(periodo2), selection_mode="single", key="segmento_periodo_valor2", default = "1987 - 2000"
    )

   
    if periodo_valor2 == "1987 - 2000":     
         plot_preco_brent(df_ipea_brent, 1987, 2000,df_eventos_novos, [0, 200])
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> 1990: Guerra do Golfo </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    A Guerra do Golfo teve um impacto significativo no mercado de petróleo. O conflito começou com a invasão do Kuwait pelo Iraque, um importante exportador da commodity, sob o comando de Saddam Hussein. Essa ação gerou uma grave instabilidade no Oriente Médio, região crucial para a produção global de petróleo.
                    Durante a guerra, ocorreu um dos maiores derramamentos de petróleo da história, quando tropas iraquianas despejaram milhões de barris no Golfo Pérsico, causando danos ambientais e comprometendo a produção. Além disso, os poços de petróleo do Kuwait foram incendiados, agravando a crise e elevando ainda mais os preços.
                    A instabilidade gerada pelo conflito levou à imposição de sanções ao Iraque e a esforços internacionais para garantir o fornecimento de petróleo aos mercados globais. O impacto no setor energético foi duradouro, influenciando políticas de segurança e estratégias de produção em países exportadores.
                    Como resultado, o preço do petróleo Brent disparou, quase dobrando em poucos meses diante do receio do mercado sobre um possível colapso na oferta. A instabilidade persistiu até o início de 1991, quando a coalizão liderada pelos EUA lançou a operação "Tempestade no Deserto", expulsando o Iraque do Kuwait e trazendo um novo equilíbrio ao mercado petrolífero.
                    
                    Referência: https://pt.wikipedia.org/wiki/Guerra_do_Golfo https://brasilescola.uol.com.br/historiag/guerra-golfo.htm
                    </div>
                    ''', unsafe_allow_html=True)
         

         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> (1997-1998): Crise financeira asiática </strong>
            </div>
            ''', unsafe_allow_html=True)


        
         st.write('''
                    <div style="text-align: justify;">
                    A crise reduziu a demanda por petróleo, pois países como China, Japão, Tailândia e Indonésia diminuíram suas importações devido à desaceleração econômica. Paralelamente, a superprodução de petróleo, impulsionada por membros da OPEC, especialmente a Rússia, criou um excesso de oferta, resultando em uma queda de 50% nos preços do petróleo entre 1997 e o final de 1998. Isso impactou severamente países que dependiam da receita petrolífera, como Rússia, Irã e Venezuela. Em 1999, os preços começaram a se recuperar com a redução da produção pela OPEC e outros produtores para equilibrar a oferta e a demanda.
                    
                    Referência: https://pt.wikipedia.org/wiki/Crise_financeira_asi%C3%A1tica_de_1997
                    </div>
                    ''', unsafe_allow_html=True)
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong>    </strong>
            </div>
            ''', unsafe_allow_html=True)

   
    if periodo_valor2 == "2000 - 2013": 
         plot_preco_brent(df_ipea_brent, 2000, 2013,df_eventos_novos, [0, 200])
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> 2004: Tensões no Oriente Médio </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    
                    A combinação de instabilidade geopolítica no Oriente Médio, especialmente no Iraque após a invasão de 2003, e o crescimento da demanda global por petróleo, impulsionado por economias emergentes como China e Índia, resultou na alta do preço do petróleo Brent. Além disso, a capacidade limitada de produção da OPEP, que enfrentou dificuldades para aumentar rapidamente a oferta, contribuiu para a pressão sobre os preços. Esses fatores juntos levaram a um período de volatilidade no mercado petrolífero.
                    <br>
                    Referência: https://www.iea.org/reports/world-energy-outlook-2004
                    </div>
                    ''', unsafe_allow_html=True)
         
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> (2006-2008): Crescimento da Demanda Global   </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    A produção mundial de petróleo atingiu seu pico em 2006 e começou a declinar, conforme apontado pelo Energy Watch Group, gerando preocupações sobre possíveis conflitos e instabilidade social devido à escassez de combustíveis fósseis.
                    Em janeiro de 2008, o preço do barril ultrapassou US 100 pela primeira vez, impulsionado por tensões geopolíticas no Irã, Nigéria e Paquistão. Posteriormente, em 11 de julho, os preços atingiram máximos históricos: US$ 147,50 para o Brent (referência na Europa e Brasil) e US 147,27 para o WTI (referência nos EUA).
                    Além disso, a China aumentou o processamento de petróleo bruto nos primeiros meses de 2008 para combater a escassez de suprimentos no país, evidenciando um crescimento significativo na demanda global por energia
                    <br>
                    
                    Referências:  https://www.china-briefing.com/news/china-processes-more-crude-to-meet-growing-demand/
                    <br>
                    <https://oglobo.globo.com/economia/veja-outros-momentos-em-que-preco-do-petroleo-passou-de-us-100-25408184>
                    <https://www.theguardian.com/business/2007/oct/22/oilandpetrol.news?utm_source=chatgpt.com>   
                    </div>
                    ''', unsafe_allow_html=True)
         
         st.text("")
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> 2008: Crise da bolha imobiliária americana e impacto global   </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    A queda do preço do petróleo foi impulsionada por diversos fatores. A crise financeira global de 2008, iniciada com a falência do banco americano Lehman Brothers devido ao estouro da bolha imobiliária, levou a uma recessão que reduziu drasticamente a demanda por petróleo. Antes disso, uma bolha especulativa havia inflado os preços, mas com a crise, investidores retiraram seus recursos, acelerando a desvalorização da commodity. Além disso, o fortalecimento do dólar americano encareceu o petróleo para compradores internacionais, reduzindo ainda mais a demanda. Ao mesmo tempo, a produção excessiva e estoques elevados, sem um ajuste imediato, criaram um desequilíbrio entre oferta e demanda, intensificando a queda nos preços. Os impactos foram profundos: empresas energéticas sofreram perdas, investimentos foram cancelados e países exportadores enfrentaram dificuldades econômicas. A volatilidade no mercado petrolífero também resultou em maior cautela nos mercados financeiros e influenciou políticas energéticas globais
                    A crise financeira global e a recessão que se seguiu reduziram significativamente a demanda por petróleo. Como resultado, o preço do barril despencou, chegando a US$ 33,36 em 24 de dezembro, representando apenas 23% do valor registrado em 3 de julho do mesmo ano.
                    
                    Referências: <https://exame.com/economia/precos-do-petroleo-se-aproximam-do-fundo-do-poco-de-2008/>
                    https://classic.exame.com/economia/precos-do-petroleo-se-aproximam-do-fundo-do-poco-de-2008/?utm_source=copiaecola&utm_medium=compartilhamento
                    <https://www.investopedia.com/ask/answers/052715/how-did-financial-crisis-affect-oil-and-gas-sector.asp>
                    </div>
                    ''', unsafe_allow_html=True)
         
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> (2010 e 2011): Primavera Árabe  </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    Entre 2010 e 2011, o mercado de combustíveis no Brasil registrou crescimento significativo, impulsionado pelo aumento da demanda e pelas mudanças nos preços internacionais. Em 2010, o consumo cresceu 8,4%, totalizando 117,936 milhões de metros cúbicos, com expectativa de crescimento de 7% em 2011. A alta dos preços do açúcar no mercado global favoreceu o aumento do consumo de gasolina, enquanto o uso de etanol e GNV recuou.
                    No cenário internacional, a Primavera Árabe e a guerra civil na Líbia causaram instabilidade no mercado de petróleo. Entre fevereiro e março de 2011, o preço do Brent subiu US$ 15 por barril, reflexo da interrupção de 1,5 milhão de barris/dia das exportações líbias. A baixa capacidade de produção dificultou a resposta da OPEP, gerando pressões adicionais sobre a oferta global.
                    Além disso, a crescente demanda por petróleo em China e Oriente Médio impulsionou a valorização da commodity. No primeiro semestre de 2011, o consumo de derivados de petróleo em países fora da OCDE aumentou quase 4%, apesar da queda na demanda nos países da OCDE. No geral, o consumo global de petróleo teve um crescimento de 1,2% (1,1 milhão de barris/dia), destacando o papel dos mercados emergentes na dinâmica energética mundial. 
                    
                    Referências: https://oglobo.globo.com/politica/mercado-de-combustiveis-cresce-84-em-2010-bate-recorde-2822277


                    </div>
                    ''', unsafe_allow_html=True)
         
 
 
 
         
    if periodo_valor2 == "2013 - 2025": 
         plot_preco_brent(df_ipea_brent, 2013, 2025,df_eventos_novos, [0, 200])
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> (2014-2016): Excesso de oferta global   </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    Entre 2014 e 2016, o mercado de petróleo enfrentou quedas acentuadas e alta volatilidade devido ao excesso de oferta global. Em 2014, a produção mundial atingiu níveis recordes, impulsionada pelo boom do petróleo de xisto nos EUA, adicionando milhões de barris ao mercado diariamente. A demanda, por outro lado, ficou abaixo do esperado na Europa e Ásia, pressionando os preços para baixo.
                    Nos anos seguintes, o cenário de oferta excessiva continuou, intensificado pelo avanço do fraturamento hidráulico (fracking) nos EUA e pelo aumento da produção em Iraque e Rússia. Em 2015 e 2016, o mercado sofreu forte volatilidade, com um excedente diário de quase 1 milhão de barris, dificultando a recuperação dos preços da commodity.
                    Como resultado, os preços despencaram para mínimas históricas, ficando abaixo de US$ 30 por barril entre 2015 e 2016. Em 2015, a commodity acumulou uma queda de 35%, e no início de 2016, as perdas continuaram devido à desaceleração da economia chinesa, à crise diplomática entre Irã e Arábia Saudita e ao aumento dos estoques de derivados nos EUA.
                    A OPEP, liderada por Arábia Saudita, optou por manter sua produção em novembro de 2014, buscando preservar sua participação de mercado e pressionar os produtores de shale oil nos EUA. Paralelamente, a demanda global permaneceu abaixo das expectativas, com o crescimento econômico modesto nos Estados Unidos e China, prolongando o desequilíbrio entre oferta e consumo.
                    O declínio dos preços se intensificou em 5 de janeiro de 2016, após um aumento inesperado nos estoques de gasolina dos EUA, somado às tensões geopolíticas geradas pelo teste de bomba de hidrogênio da Coreia do Norte. A queda na demanda na Europa e na Ásia, devido ao crescimento econômico fraco, também contribuiu para a desvalorização do petróleo.
                    
                    Referências:
                    https://time.com/3678080/global-forecast/
                    https://time.com/3678080/global-forecast/
                    https://blogs.worldbank.org/en/developmenttalk/what-triggered-oil-price-plunge-2014-2016-and-why-it-failed-deliver-economic-impetus-eight-charts
                    https://g1.globo.com/economia/mercados/noticia/2016/01/por-que-o-preco-do-petroleo-caiu-tanto-veja-perguntas-e-respostas.html
                    
                    </div>
                    ''', unsafe_allow_html=True)
         
         
         
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> (2016-2018): Recuperação econômica global   </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    Em novembro de 2016, a OPEP+, que reúne a OPEP e países produtores como Rússia, firmou um acordo para reduzir a produção, buscando equilibrar o mercado global e recuperar os preços, que haviam despencado em 2015 e 2016 devido ao excesso de oferta. A implementação desses cortes foi essencial para a estabilização do setor.
                    Nos Estados Unidos, a produção de petróleo de xisto registrou crescimento moderado entre 2016 e 2018, evitando um aumento excessivo da oferta global e contribuindo para a manutenção dos preços elevados. Esse avanço na extração também permitiu aos EUA reduzir sua dependência de petróleo importado. A recuperação econômica mundial teve um papel importante na valorização da commodity. Após a crise financeira de 2008, países como China e Estados Unidos voltaram a expandir suas economias, aumentando a demanda por energia e petróleo. O FMI projetou um crescimento global de 3,9% para 2018, fortalecendo a expectativa de maior consumo.
                    Outro fator decisivo foi a escalada das tensões geopolíticas e as sanções ao Irã. Em maio de 2018, o então presidente dos EUA, Donald Trump, retirou o país do acordo nuclear com o Irã e reimpôs sanções ao setor petrolífero iraniano, limitando suas exportações e impulsionando os preços. Entre 2016 e 2018, houve uma redução significativa nos estoques globais de petróleo, indicando um equilíbrio mais estável entre oferta e demanda, o que consolidou a tendência de alta nos preços da commodity.
                    
                    Referências https://www.axios.com/2018/05/28/who-to-blame-rising-gasoline-prices?
                    https://g1.globo.com/economia/noticia/2018/10/01/petroleo-brent-supera-us-83-e-renova-maxima-desde-2014.ghtml 
                    </div>
                    ''', unsafe_allow_html=True)
         
         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong> 2020: Covid-19 - Colapso da demanda   </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    Em 2020, o preço do petróleo Brent registrou uma queda acentuada, encerrando o ano a US 51,80 por barril, uma redução de 21,5% em relação a 2019. O pior momento ocorreu em abril, quando o Brent atingiu US 15,98 por barril, devido à queda na demanda global e ao excesso de oferta. O WTI chegou a registrar valores negativos pela primeira vez na história, fechando a -US$ 37,63 por barril, devido à falta de capacidade de armazenamento. O principal fator por trás dessa queda foi a pandemia de COVID-19, que reduziu drasticamente a demanda por energia. O confinamento global gerou uma queda de aproximadamente 20 milhões de barris por dia em abril. No segundo semestre, os preços começaram a se recuperar, impulsionados pelos cortes na produção da OPEP+ e pelos sinais de retomada econômica. No entanto, a recuperação foi gradual, e os valores permaneceram abaixo dos níveis pré-pandemia.
                    
                    Referências: https://www.investopedia.com/articles/investing/100615/will-oil-prices-go-2017.asp
                    </div>
                    ''', unsafe_allow_html=True)


         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong>  2022: Invasão da Ucrânia pela Rússia  </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    
                    Em 2022, o preço do petróleo foi impactado por diversos fatores. A recuperação da demanda pós-pandemia, impulsionada pela reabertura das economias e pelo aumento da atividade industrial, levou a um crescimento significativo no consumo de petróleo. Ao mesmo tempo, os conflitos geopolíticos, especialmente a guerra entre Rússia e Ucrânia, geraram instabilidade no mercado energético, afetando a oferta global e elevando os preços. Além disso, as decisões da OPEP+ ao longo do ano foram determinantes para a precificação da commodity, pois ajustes na produção impactaram diretamente a oferta disponível. Outro fator relevante foi a inflação global e a política monetária, já que a alta dos preços e as medidas adotadas pelos bancos centrais para conter esse avanço influenciaram tanto o consumo quanto o valor do petróleo no mercado.

                    A guerra entre Rússia e Ucrânia gerou um forte impacto no mercado de petróleo, elevando os preços para US$ 120 por barril devido ao temor de interrupções no fornecimento global. As sanções ocidentais limitaram a exportação de petróleo russo, levando Moscou a buscar compradores como China e Índia, que passaram a adquirir o produto com descontos.

                    A instabilidade geopolítica aumentou as preocupações com o abastecimento energético na Europa, altamente dependente do gás e petróleo russos. Em resposta, os países europeus aceleraram a transição para fontes renováveis e buscaram alternativas para reduzir essa dependência. Para tentar equilibrar o mercado diante das oscilações na oferta e demanda, a OPEP+ ajustou sua produção ao longo do período.
                    
                    Referências https://www.cnnbrasil.com.br/economia/macroeconomia/fmi-demanda-e-preco-do-petroleo-seguem-altamente-incertos-em-meio-a-conflitos-geopoliticos/
                    </div>
                    ''', unsafe_allow_html=True)


         st.write('''  
                <div style="text-align: justify; font-size: 16px; color: #71C5E8">
                <strong>  (2023-2025) Aumento produção em países fora da OPEP+ e Guerra Comercial (EUA x China)  </strong>
            </div>
            ''', unsafe_allow_html=True)



         st.write('''
                    <div style="text-align: justify;">
                    Entre 2023 e 2025, o preço do petróleo Brent tem registrado uma queda contínua devido a fatores que impactam tanto a oferta quanto a demanda global. O aumento da produção nos Estados Unidos e em países fora da OPEP+, incluindo Arábia Saudita e Rússia, ampliou a oferta no mercado, pressionando os preços para baixo.Ao mesmo tempo, a desaceleração econômica global, especialmente na China, que enfrenta uma recuperação mais lenta pós-pandemia, reduziu o consumo de petróleo.

                    A guerra comercial entre EUA e China, intensificada pelas tarifas impostas por Donald Trump, trouxe incertezas ao mercado, agravando a volatilidade dos preços. Além disso, o fortalecimento do câmbio e a redução de gastos da Arábia Saudita, especialmente no segundo trimestre, contribuíram para o excesso de oferta em períodos de menor demanda.

                    O Departamento de Energia dos EUA (DoE) revisou suas projeções para 2025 e 2026, prevendo preços mais baixos diante da instabilidade do mercado. A queda nos preços também impactou empresas como a Petrobras, segundo o G1. Diante dessas condições, o Brent atingiu os menores níveis em quatro anos, operando próximo de US$ 60 por barril, reflexo da oferta elevada e da menor demanda. A produção recorde de petróleo nos EUA e a expansão da OPEP+ intensificaram o excesso de oferta, sustentando a pressão sobre os preços. O temor de uma recessão global devido às tensões comerciais segue influenciando negativamente o mercado, sem perspectivas concretas de estabilização.
                    
                    Referências https://www1.folha.uol.com.br/mercado/2025/05/eua-e-china-se-reunem-na-suica-para-negociacao-de-alto-risco-sobre-futuro-das-tarifas.shtml https://www.cnnbrasil.com.br/economia/macroeconomia/petroleo-cai-8-com-retaliacao-da-china-as-tarifas-dos-eua/
                    
                    </div>
                    ''', unsafe_allow_html=True)



with tab3:
   st.empty()
   
   periodo = {
    "Mensal": 30,
    "Bimestral": 60,
    "Trimestral": 90,
    "Anual": 292
   }
 
   
   periodo_valor = st.segmented_control(
      "Selecione o Período", list(periodo.keys()), selection_mode="single", key="segmento_periodo_valor3", default= "Mensal"  
   )
   
   if periodo_valor != None:

      periodo_decomposicao = periodo[periodo_valor]
      st.write(f"Período selecionado: {periodo_decomposicao} dias")
      decomposicao = seasonal_decompose(df_ipea_brent['1988-01-01':'2024-12-31']['preco_uss'], model="additive", period=periodo_decomposicao)
      # Gráfico de Tendência
      fig_tendencia = go.Figure()
      # Plotando a Tendência
      fig_tendencia.add_trace(go.Scatter(
      x=decomposicao.trend.index,
      y=decomposicao.trend,
      mode='lines',
      name='Tendência',
      line=dict(color='blue')
      ))
   # Configuração do layout
      fig_tendencia.update_layout(
         title="Tendência",
         xaxis_title="Ano",
         yaxis_title="Valor",
         xaxis=dict(
            tickvals=anos,
            ticktext=[str(ano) for ano in anos],
            tickformat="%Y"
         ),
         template="plotly_dark"
        )
      # Exibir gráfico no Streamlit
      st.plotly_chart(fig_tendencia)
      ultimo_ano = decomposicao.seasonal.index.year.max()
      # Filtra os dados da sazonalidade para o último ano
      dados_sazonalidade = decomposicao.seasonal[decomposicao.seasonal.index.year == ultimo_ano]
      # Cria o gráfico
      fig_sazonalidade = go.Figure()
      fig_sazonalidade.add_trace(go.Scatter(
         x=dados_sazonalidade.index,
         y=dados_sazonalidade,
         mode='lines',
         name=f"Sazonalidade {ultimo_ano}",
         line=dict(color='green')
      ))
      # Configura o layout para exibir o mês no eixo x
      fig_sazonalidade.update_layout(
         title=f"Sazonalidade de {ultimo_ano}",
         xaxis_title="Mês",
         yaxis_title="Valor",
         xaxis=dict(
            tickformat="%b",  # Mostra apenas o nome abreviado do mês (Jan, Feb, etc.)
            ticklabelmode="period"  # Garante que o label represente o início do mês
         ),
         template="plotly_dark"
        )
      # Exibe o gráfico no Streamlit
      st.plotly_chart(fig_sazonalidade)

   

with tab4:
    periodo4 = (
    "1987 - 2000",
    "2000 - 2013",
    "2013 - 2025"
    )
 
   
    periodo_valor4 = st.segmented_control(
      "Selecione o Período", list(periodo4), selection_mode="single", key="segmento_periodo_valor4", default= "1987 - 2000"
    )

   
    if periodo_valor4 == "1987 - 2000":
        plot_preco_brent_anual(df_grouped, 1987, 2000)
        plot_var_brent(df_ipea_brent, 1987, 2000)
        
    if periodo_valor4 == "2000 - 2013":
        plot_preco_brent_anual(df_grouped, 2000, 2013)
        plot_var_brent(df_ipea_brent, 2000, 2013)
        
    if periodo_valor4 == "2013 - 2025":
        plot_preco_brent_anual(df_grouped, 2013, 2025)
        plot_var_brent(df_ipea_brent, 2013, 2025)

with tab5:
 st.write('''
            <div style="text-align: justify;">
               **Talvez mover o mês aqui possa ser uma boa ideia e deixar 2 linhas comparativas. Ou usar dispersão **
            </div>
            ''', unsafe_allow_html=True)
 
 df_ipea_brent_media = df_ipea_brent.groupby(['data','ano','mes']).preco_uss.mean().reset_index()
 df_ipea_brent_media.set_index('data', inplace=True)
 df_ipea_brent_media.sort_index(ascending=True, inplace=True)
 
 df_prod_petroleo_soma2 = pd.read_csv('https://github.com/nascimentorafael1/techfase4/raw/refs/heads/main/data/df_eia_prod_mundial.csv')
 df_prod_petroleo_soma2.set_index('data', inplace=True)
 df_prod_petroleo_soma2.sort_index(ascending=True, inplace=True)
 
 def plot_brent_vs_mmbpd(df_brent, df_mmbpd, ano_inicio1, ano_fim2):
    # Filtra os DataFrames pelo intervalo de anos desejado
    df_brent_filtrado = df_brent[(df_brent['ano'] >= ano_inicio1) & (df_brent['ano'] <= ano_fim2)]
    df_mmbpd_filtrado = df_mmbpd[(df_mmbpd['ano'] >= ano_inicio1) & (df_mmbpd['ano'] <= ano_fim2)]

    # Cria a figura
    fig = go.Figure()

    # Linha do preço do Brent (azul escuro)
    fig.add_trace(go.Scatter(
        x=df_brent_filtrado.index,
        y=df_brent_filtrado['preco_uss'],
        mode='lines',
        name='Preço Brent (USD)',
        line=dict(color='#0d3b66', width=3),
        yaxis='y2'
    ))

    # Barras da produção de petróleo (azul claro)
    fig.add_trace(go.Scatter(
        x=df_mmbpd_filtrado.index,
        y=df_mmbpd_filtrado['valor_mensal'],
        mode='lines',
        name='Produção de Petróleo (MMBPD)',
        marker_color='#71C5E8',
        yaxis='y1'
    ))

    # Layout com dois eixos Y
    fig.update_layout(
        title=f'Produção de Petróleo (MMBPD) vs Preço Brent (USD) — {ano_inicio1} a {ano_fim2}',
        xaxis_title='Ano',
        yaxis=dict(title='Produção (MMBPD)', side='left', showgrid=False),
        yaxis2=dict(title='Preço Brent (USD)', overlaying='y', side='right'),
        template='plotly_dark',
        legend=dict(
    orientation='h',
    yanchor='top',
    y=-0.2,
    xanchor='center',
    x=0.5
)
    )

    # Exibe no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
 periodo5 = (
    "1987 - 2000",
    "2000 - 2013",
    "2013 - 2025"
    )
 
   
 periodo_valor5 = st.segmented_control(
      "Selecione o Período", list(periodo5), selection_mode="single", key="segmento_periodo_valor5", default= "1987 - 2000"
    )

   
 if periodo_valor5 == "1987 - 2000":
  plot_brent_vs_mmbpd(df_ipea_brent_media, df_prod_petroleo_soma2, 1987, 2000)

        
 if periodo_valor5 == "2000 - 2013":
  plot_brent_vs_mmbpd(df_ipea_brent_media, df_prod_petroleo_soma2, 2000, 2013)

        
 if periodo_valor5 == "2013 - 2025":
  plot_brent_vs_mmbpd(df_ipea_brent_media, df_prod_petroleo_soma2, 2013, 2025)




