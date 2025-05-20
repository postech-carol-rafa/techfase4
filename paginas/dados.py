# Importando bibiotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px



st.title('Dados Tecnicos')



st.image("imagens/fluxo_v2.jpg")


st.write('''
         <div style="text-align: justify;">
        Este trabalho apresenta uma solução técnica voltada para a análise do mercado de petróleo, utilizando dados do IPEA para monitorar 
        variações de preços do petróleo Brent e identificar padrões e fatores determinantes. A partir da análise dos dados, é possível 
        identificar a influência de elementos externos na dinâmica do setor, permitindo uma avaliação mais abrangente do comportamento do 
        mercado.
        <br><br>
        Para enriquecer a pesquisa, integramos o projeto a uma base complementar do EIA, que fornece informações sobre a produção de petróleo, 
        possibilitando maior assertividade nas previsões e refinamento dos modelos criados. Dessa forma, a abordagem adotada não apenas atende 
        ao escopo inicial do projeto, mas garante maior completude e confiabilidade na análise.
        <br><br>
        Do ponto de vista técnico, foi estruturado um dataset a partir da base do IPEA, executado via Jupyter Notebook e exportado para 
        arquivos CSV. Além disso, desenvolvemos uma API capaz de conectar-se ao site do EIA, realizando consultas automatizadas para 
        enriquecer a modelagem e o processamento da aplicação. Com os dados tratados e analisados, elaboramos os modelos preditivos para 
        a projeção dos preços do petróleo.
        <br><br>      
        A aplicação do Streamlit foi desenvolvida em phyton e é utilizada para executar o modelo de machine learning
        <br><br>
        E por fim, disponibilizamos a aplicação no GitHub, estruturada de forma a integrar todo o processo no Streamlit, 
        proporcionando uma experiência completa ao usuário. O projeto contempla storytelling, análise de eventos históricos, 
        dashboards interativos e informações técnicas, consolidando uma abordagem robusta e integrada para compreensão do comportamento 
        do mercado de petróleo e visualização do resultado da entrega do trabalho.
         </div>
         ''', unsafe_allow_html=True)

st.write('''
        
---

**Modelo de Machine Learning**

''')

st.image("imagens/modelo.png")

st.write('''
         <div style="text-align: justify;">
         Durante a análise dos modelos preditivos, percebemos que avaliar sua precisão e confiabilidade era essencial para garantir que as 
         previsões estivessem realmente próximas dos valores reais. Para isso, utilizamos algumas métricas fundamentais. 
         <br><br>
         O MAE (Erro Absoluto Médio), pois mede a média das diferenças absolutas entre as previsões e os valores reais, sendo intuitivo e 
         direto. Quanto menor seu valor, melhor a precisão do modelo. 
         <br><br>
         Exploramos também o RMSE (Raiz do Erro Quadrático Médio), que, além de calcular os erros ao quadrado antes da média, enfatiza 
         discrepâncias maiores nas previsões. Essa abordagem ajudou a identificar maiores variações. O melhor cenário é quando seu valor 
         está menor, pois indica previsões mais precisas e erros reduzidos. Como penaliza erros grandes, um valor alto sugere dificuldades 
         do modelo em lidar com desvios significativos.
          <br><br>
         Já o MAPE (Erro Percentual Absoluto Médio), expressa o erro em percentual, facilitando a compreensão do impacto das previsões em 
         relação aos valores reais. Essa métrica foi útil especialmente para comparar diferentes modelos sem depender de uma escala específica.
          <br><br>
        Embora o LightGBM tenha apresentado um desempenho superior em termos de RMSE (Raiz do Erro Quadrático Médio) — métrica que tende a 
         penalizar mais os erros extremos —, nas demais métricas de avaliação o modelo Prophet demonstrou resultados mais consistentes.
        <br><br>
         O Prophet teve melhor desempenho em termos de MAPE (%) (Erro Percentual Absoluto Médio), MAE (Erro Absoluto Médio) e acurácia, 
         indicando uma performance mais estável e precisa na média geral das previsões. 
        <br><br>
         Diante disso, optamos por utilizar o Prophet como modelo final, considerando seu equilíbrio entre desempenho e interpretabilidade.
        
         A análise do modelo pode ser visualizada no notebook no github
        
        ---
         
        </div>
         ''', unsafe_allow_html=True)

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
