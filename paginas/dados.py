# Importando bibiotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px



st.title('Dados Tecnicos')



st.image("imagens/fluxo.jpeg")


st.write('''
         <div style="text-align: justify;">
         Este trabalho apresenta uma solução técnica voltada para a análise do mercado de petróleo, utilizando dados do IPEA para 
         monitorar variações de preços do petróleo Brent e identificar padrões e fatores determinantes. A partir da análise dos dados, 
         é possivel identificar a influência de elementos externos na dinâmica do setor, permitindo uma avaliação mais abrangente do 
         comportamento do mercado.
        <br><br>
        Para enriquecer a pesquisa, integramos o projeto a uma base complementar do EIA, que fornece informações sobre a produção de 
        petróleo, possibilitando maior assertividade nas previsões e refinamento dos modelos criados. Dessa forma, a abordagem adotada 
        não apenas atende ao escopo inicial do projeto, mas garante maior completude e confiabilidade na análise.
        <br><br>
        Do ponto de vista técnico, foi estruturado um dataset a partir da base do IPEA, executado via Jupyter Notebook e exportado para 
        arquivos CSV. Além disso, desenvolvemos uma API capaz de conectar-se ao site do EIA, realizando consultas automatizadas para 
        enriquecer a modelagem e o processamento da aplicação. Com os dados tratados e analisados, elaboramos os modelos preditivos 
        para a projeção dos preços do petróleo.
        <br><br>
        E por fim, disponibilizamos a aplicação no GitHub, estruturada de forma a integrar todo o processo no Streamlit, proporcionando 
        uma experiência completa ao usuário. O projeto contempla storytelling, análise de eventos históricos, dashboards interativos e 
        informações técnicas, consolidando uma abordagem robusta e integrada para compreensão do comportamento do mercado de petróleo e 
        visualização do resultado final da entrega do trabalho.

         </div>
         ''', unsafe_allow_html=True)

st.write('''
        
---

**Modelo de Machine Learning**

''')

st.image("imagens/modelo.png")

st.write('''
         
         Embora o LightGBM tenha apresentado um desempenho superior em termos de RMSE (Raiz do Erro Quadrático Médio) — métrica que tende a penalizar mais os erros extremos —, nas demais métricas de avaliação o modelo Prophet demonstrou resultados mais consistentes.

         O Prophet teve melhor desempenho em termos de MAPE (%) (Erro Percentual Absoluto Médio), MAE (Erro Absoluto Médio) e acurácia, indicando uma performance mais estável e precisa na média geral das previsões.

        Diante disso, optamos por utilizar o Prophet como modelo final, considerando seu equilíbrio entre desempenho e interpretabilidade.
        
        A análise do modelo pode ser visualizada no notebook no github
        
        ---
         
         ''')

st.html('''
    <a target="_blank" href="https://github.com/postech-carol-rafa/techfase4"> Clique aqui para acessar o GitHub </a>
''')


st.write('''
---        
          
**Faculdade de Informática de Administração Paulista – FIAP**


*Pos Tech em Data Analytics*

Turma 7DTAT

Alunos:

* Caroline Yuri Noguti - RM 358779
* Rafael Nascimento Coutinho – RM 358930

          ''')