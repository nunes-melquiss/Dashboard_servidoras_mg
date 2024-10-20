import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
from dataset import ser_df1, df_correlacionado
from utils import format_number



st.set_page_config(layout="wide",page_title="Servidoras em MG")
st.title("Representação Feminina no Funcionalismo Público de MG :small_red_triangle:")

aba1, aba2 = st.tabs(['Análises','Metodologia'])


with aba1:
    st.subheader('Em resumo...')

    n_mulheres = df_correlacionado[df_correlacionado['Sexo provavel do servidor'] == 'F'].shape[0]
    n_homens = df_correlacionado[df_correlacionado['Sexo provavel do servidor'] == 'M'].shape[0]
    percentual_mulheres = f'{round(n_mulheres / (n_mulheres + n_homens) * 100)}%'

    col0a, col0b, col0c = st.columns([1,1,1])
    with col0a:
        st.metric(label="Numero de servidores analisados*", value=format_number(n_mulheres+n_homens))


    col5a, colmeio, col5b = st.columns([2,0.5,2])

    with col5a:
        # Gráfico de pizza com % de mulheres e homens servidores
        labels = ['Mulheres:','Homens:']
        valores = [n_mulheres,n_homens]

        fig = go.Figure(data=[go.Pie(labels=labels, values=valores, hole=0, 
                                    marker=dict(colors=['#FF0000', '#7f7f7f']),
                                    hoverinfo='label+percent+value', 
                                    textinfo='label+percent',
                                    textfont=dict(size=[20,14],
                                                  color='white',
                                                  family='Arial',
                                                  weight='bold'))])
        fig.update_layout(title_text="Os servidores analisados são:*", showlegend=False)
        st.plotly_chart(fig)

        st.subheader("\n \n")

        #Barras com horas acumuladas de acordo com o sexo.
        soma_horas = df_correlacionado.groupby('Sexo provavel do servidor')['Carga Horária'].sum()
        labels4 = ['Mulheres:','Homens:']
        valores4 = soma_horas.get('F',0),soma_horas.get('M',0)
        rotulos4 = [f'Mulheres:<br>{format_number(valores4[0])}', 
                f'Homens:<br>{format_number(valores4[1])}']


        fig4 = go.Figure(data=[go.Bar(x=labels4, y=valores4, 
                                    marker=dict(color=['#FF0000', '#808080']),
                                    text=rotulos4,
                                    textfont=dict(size=[20, 14],  
                                                color='white', 
                                                family='Arial', 
                                                weight='bold'))])



        fig4.update_layout(
        title_text="Mas e se acumularmos as horas da jornada semanal de cada gênero, o quanto daria?",
        yaxis_title="Soma de Horas Acumuladas",)
        st.plotly_chart(fig4)







    with col5b:
        # Barras com remuneração por sexo
        soma_remuneracao = df_correlacionado.groupby('Sexo provavel do servidor')['Remuneração'].sum()
        labels1 = ['Mulheres:','Homens:']
        valores = soma_remuneracao.get('F',0),soma_remuneracao.get('M',0)
        rotulos = [f'Mulheres:<br>{format_number(valores[0], "R$ ")}', 
                f'Homens:<br>{format_number(valores[1], "R$ ")}']


        fig = go.Figure(data=[go.Bar(x=labels1, y=valores, 
                                    marker=dict(color=['#FF0000', '#808080']),
                                    text=rotulos,
                                    textfont=dict(size=[20, 14],  
                                                color='white', 
                                                family='Arial', 
                                                weight='bold'))])



        fig.update_layout(
        title_text="Por sua vez, a remuneração acumulada dos servidores é assim:",
        yaxis_title="Soma Acumulada de Remuneração",)
        st.plotly_chart(fig)

        st.subheader("\n \n")

        #Barras com valor hora médio.
        media_horas_mulheres = soma_remuneracao.get('F',0)/(soma_horas.get('F',1)*4)
        media_horas_homens = soma_remuneracao.get('M',0)/(soma_horas.get('M',1)*4)

        labels6 = ['Mulheres:','Homens:']
        valores6 = [media_horas_mulheres,media_horas_homens]
        rotulos6 = [f'Mulheres:<br>R$ {valores6[0]:.2f} / hora',
                f'Homens:<br>R$ {valores6[1]:.2f} / hora']


        fig6 = go.Figure(data=[go.Bar(x=labels6, y=valores6, 
                                    marker=dict(color=['#FF0000', '#808080']),
                                    text=rotulos6,
                                    textfont=dict(size=[20, 14],  
                                                color='white', 
                                                family='Arial', 
                                                weight='bold'))])



        fig6.update_layout(
        title_text="Ou seja, o valor médio da hora é aproximadamente:",
        yaxis_title="Valor médio da hora",)
        st.plotly_chart(fig6)
    




    st.subheader("\n \n Mas por qual motivo?")
    st.write('Para entender melhor a desigualdade entre os gêneros, vamos verificar as variáveis que podem estar influenciando os resultados acima apresentados.')
    st.write('Começaremos com uma pergunta: Os órgãos que empregam 90% dos funcionários públicos, tem predominância feminina ou masculina?')
    st.subheader('\n \n')

    col1a,col1c = st.columns([2,2])

    with col1a:
        # Gráfico de órgãos que mais empregam e composição
        servidores_por_orgao = df_correlacionado.groupby(['Órgão','Sexo provavel do servidor']).size().unstack(fill_value=0)
        servidores_por_orgao['Total'] = servidores_por_orgao['F'] + servidores_por_orgao['M']
        servidores_por_orgao = servidores_por_orgao.sort_values(by='Total', ascending=False)
        servidores_por_orgao['Percentual_Acumulado'] = servidores_por_orgao['Total'].cumsum() / servidores_por_orgao['Total'].sum()
        orgaos_principais = servidores_por_orgao[servidores_por_orgao['Percentual_Acumulado'] <= 0.9]
        orgaos_outros = servidores_por_orgao[servidores_por_orgao['Percentual_Acumulado'] > 0.9]
        outros = pd.DataFrame({
            'F': [orgaos_outros['F'].sum()],
            'M': [orgaos_outros['M'].sum()],
            'Total': [orgaos_outros['Total'].sum()]
        }, index=['Outros'])
        servidores_final = pd.concat([orgaos_principais, outros])

        fig7 = go.Figure()

        fig7.add_trace(go.Bar(
            x=servidores_final.index,
            y=servidores_final['M'],
            name='Homens',
            marker_color='#808080',
            text=servidores_final['M'].apply(lambda x: format_number(x)),
            textposition='auto',
            textfont=dict(size=12,
                    color='white',
                    family='Arial Black',
                    weight='bold')))

        fig7.add_trace(go.Bar(
            x=servidores_final.index,
            y=servidores_final['F'],
            name='Mulheres',
            marker_color='#FF0000',
            text=servidores_final['F'].apply(lambda x: format_number(x)),
            textposition='auto',
            textfont=dict(size=16,
                    color='white',
                    family='Arial Black',
                    weight='bold')))

        fig7.update_layout(
            barmode='stack',
            title_text="Órgãos que mais empregam e sua composição:",
            xaxis_title="Órgão",
            yaxis_title="Número Total de Servidores",
            legend_title="Gênero",
            height=600)
        
        st.plotly_chart(fig7)

    with col1c:
        # Gráfico de remuneração/hora por órgão
        df_orgaos = df_correlacionado.groupby('Órgão').agg({
            'Remuneração': 'sum',
            'Carga Horária': 'sum',
            'Sexo provavel do servidor': 'count'
        }).rename(columns={'Sexo provavel do servidor': 'Total Servidores'})
        df_orgaos['Valor Médio Hora'] = df_orgaos['Remuneração'] / (df_orgaos['Carga Horária'] * 4)
        df_orgaos = df_orgaos.sort_values(by='Total Servidores', ascending=False)
        df_orgaos['Percentual Acumulado'] = df_orgaos['Total Servidores'].cumsum() / df_orgaos['Total Servidores'].sum()
        orgaos_90_percent = df_orgaos[df_orgaos['Percentual Acumulado'] <= 0.9]
        orgaos_outros = df_orgaos[df_orgaos['Percentual Acumulado'] > 0.9]
        outros = pd.DataFrame({
            'Remuneração': [orgaos_outros['Remuneração'].sum()],
            'Carga Horária': [orgaos_outros['Carga Horária'].sum()],
            'Total Servidores': [orgaos_outros['Total Servidores'].sum()]
        }, index=['Outros'])
        outros['Valor Médio Hora'] = outros['Remuneração'] / (outros['Carga Horária'] * 4)
        df_final = pd.concat([orgaos_90_percent, outros])

        fig8 = go.Figure()

        fig8.add_trace(go.Bar(
            x=df_final.index,
            y=df_final['Valor Médio Hora'],
            marker_color='#818049',
            text=df_final['Valor Médio Hora'].apply(lambda x: f'R$ {round(x,2)} / hora'),
            textposition='auto',
            textfont=dict(size=14, color='white', family='Arial Black', weight='bold')
        ))

        fig8.update_layout(
            title_text="Nesses órgãos, o valor médio da hora de cada profissional é de:",
            xaxis_title="Órgão",
            yaxis_title="Valor Médio da Hora (R$)",
            height=600
        )
        st.plotly_chart(fig8)






    st.subheader('\n \n')
    st.write('Existe uma representação feminina maior em órgãos que, em geral, tem uma política de remuneração menos expressiva.')

    st.write('Mas e se analisarmos a remuneração conjuntamente com a distribuição de gêneros dentro de um órgão, como seria?')
    st.write('Selecione no filtro abaixo o órgão a ser analisado e verifique se existe um padrão de diferença salarial entre os gêneros.')

    st.subheader('\n')
    col2a, _, col2b, col2c = st.columns([1,0.5,1,1])


    with col2a:

        # Filtro para selecionar um órgão
        orgaos_unicos = df_correlacionado['Órgão'].unique()
        orgao_selecionado = st.selectbox("Órgão:", options=orgaos_unicos)

    df_filtrado = df_correlacionado[df_correlacionado['Órgão'] == orgao_selecionado]
    df_homens = df_filtrado[df_filtrado['Sexo provavel do servidor'] == 'M']
    df_mulheres = df_filtrado[df_filtrado['Sexo provavel do servidor'] == 'F']
    total_servidores = len(df_filtrado)


    with col2b:
        st.metric(label="Quantidade de servidores:", value=(format_number(total_servidores)))

    with col2c:
        st.metric(label="Percentual de mulheres:", value=(f'{round((len(df_mulheres)/total_servidores)*100)} %'))
    

    st.subheader('\n')
    
    # Gráfico de distribuição salarios


    def calcular_frequencia_relativa(df, total_servidores, n_bins=100):
        hist, bin_edges = np.histogram(df['Remuneração'], bins=n_bins) 
        percentual = hist / total_servidores  # Frequência relativa em relação ao total de servidores
        return bin_edges, percentual

    # Calcular a distribuição para homens e mulheres, em comparação ao total de servidores
    bins_homens, perc_homens = calcular_frequencia_relativa(df_homens, total_servidores)
    bins_mulheres, perc_mulheres = calcular_frequencia_relativa(df_mulheres, total_servidores)

    fig = go.Figure()

    # Linha para homens
    fig.add_trace(go.Scatter(
        x=bins_homens[:-1],
        y=perc_homens,
        mode='lines',  # Apenas linhas, sem pontos
        name='Homens',
        line=dict(color='#808080', width=2),
        hovertemplate='<b>Faixa de Remuneração</b>: %{x:.2f} R$<br>' + 
                    '<b>Percentual de Servidores Homens</b>: %{y:.2%}<extra></extra>'
    ))

    # Linha para mulheres
    fig.add_trace(go.Scatter(
        x=bins_mulheres[:-1],
        y=perc_mulheres,
        mode='lines',  # Apenas linhas, sem pontos
        name='Mulheres',
        line=dict(color='#FF0000', width=2),
        hovertemplate='<b>Faixa de Remuneração</b>: %{x:.2f} R$<br>' + 
                    '<b>Percentual de Servidores Mulheres</b>: %{y:.2%}<extra></extra>'
    ))

    # Layout do gráfico
    fig.update_layout(
        title_text=f"Essa é a densidade salarial por gênero do Órgão: {orgao_selecionado}",
        xaxis_title="Remuneração (R$)",
        yaxis_title="Percentual de Servidores na Faixa Salarial (%)",
        legend_title="Gênero",
        height=600,
        yaxis=dict(range=[0, 0.25], tickformat=".0%") 
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

    st.subheader('\n \n')
    st.write('Me ajude a terminar de construir esse dashboard, o que você gostaria de ver aqui?')
    st.write('Para entrar em contato comigo: https://www.linkedin.com/in/melquisedeque-nunes/')

with aba2:
    st.subheader("Metodologia Utilizada")

    st.markdown("""
    A análise da representação feminina no funcionalismo público de Minas Gerais foi conduzida utilizando um conjunto de dados robusto, adotando uma abordagem metódica para garantir a precisão e a relevância dos resultados. A seguir, descrevo as etapas detalhadas do processo metodológico:

    1. **Coleta de Dados**:
    - Os dados foram obtidos do **"Portal da Transparência do Estado de Minas Gerais"**, que disponibiliza informações sobre servidores públicos estaduais, incluindo:
        - **Nome do Servidor**
        - **Ocupação**
        - **Órgão**
        - **Unidade**
        - **Carga Horária**
        - **Remuneração**
    - Esses dados são fundamentais para a análise da composição de gênero e das condições laborais dos servidores, proporcionando uma base sólida para a investigação.

    2. **Limpeza e Preparação dos Dados**:
    - Inicialmente, realizei a limpeza do conjunto de dados para remover colunas irrelevantes que não contribuíam para a análise de gênero e remuneração. As colunas descartadas incluíam identificadores e dados auxiliares.
    - As colunas restantes foram renomeadas para facilitar a interpretação, resultando em um dataframe intuitivo.
    - Para assegurar a integridade dos dados, as colunas de **"Remuneração"** e **"Carga Horária"** foram convertidas de strings para valores numéricos. Esse processo envolveu a substituição de vírgulas por pontos, permitindo cálculos precisos.

    3. **Correlação de Sexo**:
    - Uma etapa crítica da análise foi a correlação entre os nomes dos servidores e seus respectivos sexos. Para isso:
        - Utilizei uma base de dados de nomes e suas prováveis classificações de gênero, de acordo com o IBGE, obtida de um trabalho realizado por Álvaro Justen.
        - O primeiro nome de cada servidor foi extraído e comparado com esta base, permitindo determinar o sexo mais provável.
        - Esta abordagem resultou na criação da coluna **"Sexo provável do servidor"**, essencial para análises subsequentes.

    4. **Filtragem de Dados**:
    - Após a correlação, registros sem uma classificação de sexo foram eliminados, garantindo que o dataframe final inclua apenas servidores com sexo identificado. Essa filtragem é crucial para assegurar que as análises subsequentes sejam baseadas em dados representativos e quase confiáveis (considerando a possibilidade de nomes não usuais e não etrando em questões de identidade de genêro por falta de dados).

    5. **Análise Estatística e Visualização**:
    - Com o conjunto de dados devidamente preparado, foram realizadas análises estatísticas abrangentes, incluindo:
        - Cálculo do número total de servidores.
        - Análise da distribuição de gênero entre os servidores.
        - Comparação da carga horária e da remuneração acumulada entre homens e mulheres.
    - Utilizando as bibliotecas **Plotly** e **Streamlit**, foram gerados gráficos interativos que facilitam a visualização dos dados. Os principais gráficos incluem:
        - **Gráfico de Pizza**: Para visualizar a proporção de servidores por gênero.
        - **Gráficos de Barras**: Para comparar a soma de carga horária e remuneração acumulada entre os gêneros.
        - **Distribuições Salariais**: Para analisar a distribuição de salários por gênero em diferentes órgãos.

    6. **Interpretação dos Resultados**:
    - Os resultados foram contextualizados em relação à composição de gênero nos órgãos públicos e à política de remuneração, permitindo discussões sobre padrões de desigualdade salarial. Observou-se uma predominância feminina em setores com remunerações geralmente inferiores, indicando possíveis áreas de intervenção.
    - A análise identificou potenciais causas da desigualdade de gênero no funcionalismo público, contribuindo para uma compreensão mais profunda da situação atual.

    ### Status do Trabalho
    O trabalho ainda está em andamento, com novas análises sendo incrementadas. O objetivo é aprofundar a compreensão das dinâmicas de gênero no funcionalismo público e explorar variáveis adicionais que possam influenciar os resultados encontrados.

    ### Escolha da Plataforma
    A escolha do **Streamlit** como plataforma para esta publicação se deu por sua flexibilidade e facilidade de uso. O Streamlit permite a criação de aplicações interativas de forma rápida e eficiente, tornando a visualização de dados acessível e envolvente. Isso é essencial para apresentar insights de maneira clara e impactante.

    Esta metodologia oferece um panorama abrangente e fundamentado sobre a representação feminina no funcionalismo público de Minas Gerais, permitindo reflexões sobre as implicações sociais e políticas dessas descobertas.
    """)
