import pandas as pd
import streamlit as st
from auth import authenticator
import tabula
from pathlib import Path
from tratamento import tratamento_dados


# Criar pasta de dados se não existir
Path("data").mkdir(parents=True, exist_ok=True)

# Login 
authenticator.login()

if st.session_state.get('authentication_status'):
    authenticator.logout('Logout', 'sidebar')
    adicionar_pdf = st.sidebar.file_uploader("Adicionar PDF", type="pdf")
    if adicionar_pdf:
        st.sidebar.write("Carregando PDF...")
        tabula.convert_into(adicionar_pdf, "./data/extrato.csv", output_format="csv", pages='all', guess=False)
        tratamento_dados()

    
        # Tenta carregar o arquivo CSV, mas continua se não existir
    df = pd.DataFrame()
    try:
        
        df = pd.read_csv("data/dados.csv")
        df['Data'] = pd.to_datetime(df['Data'])
        df['Data'] = df['Data'].dt.date


        #Filtros
        st.sidebar.header("Filtros")

        # Verifica se há dados antes de tentar filtrar
        if len(df) > 0:
            #Filtro dataframe
            tipos = ["Guardado", "Resgatado", "Rendimentos", "Ajuste nos rendimentos"]
            lista = st.sidebar.multiselect("Selecione o tipo de movimentação",tipos,default=tipos[0])
            tipo= df["Tipo de movimentação"].isin(lista)

            #Filtro de datas
            data = tipo
            data_filtro = df.loc[data]
            data_inicial = data_filtro['Data'].min()
            data_final = data_filtro['Data'].max()
            
            # Se há apenas uma data, não mostra o slider e usa essa data única
            if data_inicial == data_final:
                data_filtrada = data_filtro
                st.sidebar.info(f"Apenas uma data disponível: {data_inicial.strftime('%d/%m/%Y')}")
            else:
                intervalo_datas = st.sidebar.slider("Selecione o período",
                                                    min_value=data_inicial,
                                                    max_value=data_final,
                                                    value=(data_inicial,data_final))
                data_filtrada = data_filtro[
                    (data_filtro['Data'] >= intervalo_datas[0]) &
                    (data_filtro['Data'] <= intervalo_datas[1])
                ]

        #KPI's
        # rendimentos
        rendimentos = df['Tipo de movimentação'].isin(["Rendimentos"])
        kpi_rendimentos = df.loc[rendimentos]
        total_rendimentos = kpi_rendimentos['Valor'].sum()

        #ajuste nos rendimentos
        ajuste_rendimentos = df['Tipo de movimentação'].isin(['Ajuste nos rendimentos'])
        kpi_ajuste_rendimentos = df.loc[ajuste_rendimentos]
        total_ajuste_rendimentos = kpi_ajuste_rendimentos['Valor'].sum()

        if total_ajuste_rendimentos >=0:
            total_ajuste_rendimentos + total_rendimentos
        else:
            total_ajuste_rendimentos - total_rendimentos

        # Guardado
        guardado = df['Tipo de movimentação'].isin(['Guardado'])
        kpi_guardado = df.loc[guardado]
        total_guardado = kpi_guardado['Valor'].sum()

        # Resgatado
        resgatado = df['Tipo de movimentação'].isin(['Resgatado'])
        kpi_resgatado = df.loc[resgatado]
        total_resgatado = kpi_resgatado['Valor'].sum()

        # Saldo
        saldo = total_ajuste_rendimentos + total_resgatado + total_guardado + total_rendimentos

        # Verifica se há dados antes de criar KPIs e gráficos
        if len(df) > 0:
            dados= {
                "Depositado": [total_guardado],
                "Resgatado": [total_resgatado],
                "Rendimentos": [total_rendimentos],
                "Saldo Total": [saldo]
            }

            kpi_dataframe = pd.DataFrame(dados)

            #Cálculo Total por periodo
            soma_total = data_filtrada['Valor'].sum()
            resultado = soma_total

            #Título
            st.title("Cofrinho PicPay")

            #KPI's
            st.dataframe(kpi_dataframe)

            #Gráficos
            
            # Criar uma cópia do DataFrame para manter os tipos originais
            df_plot = data_filtrada.copy()
            
            # Criar uma coluna de legendas com o tipo de movimentação
            df_plot['legenda'] = df_plot['Tipo de movimentação']
            
            # Criar o gráfico usando plotly para mais controle visual
            import plotly.express as px
            
            # Criar o gráfico de barras
            fig = px.bar(
                df_plot,
                x='Data',
                y='Valor',
                color='legenda',
                color_discrete_map={
                    'Guardado': '#588157',
                    'Resgatado': '#d62728',
                    'Rendimentos': '#2ca02c',
                    'Ajuste nos rendimentos': '#1f77b4'
                },
                title='Movimentações por Data',
                labels={'Valor': 'Valor (R$)', 'Data': 'Data'},
                category_orders={'Data': df_plot['Data'].unique()}
            )
            
            # Atualizar o layout para mostrar os valores
            fig.update_traces(
                texttemplate='%{value:.2f}',
                textposition='auto'
            )
            
            # Adicionar valores nos pontos
            fig.update_layout(
                showlegend=True,
                legend_title_text='Tipo de Movimentação',
                yaxis_title='Valor (R$)',
                xaxis_title='Data',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_type='category'  # Força o eixo X a tratar como categorias
            )
            
            # Exibir o gráfico
            st.plotly_chart(fig, use_container_width=True)
            st.text("Total do período")
            st.text(f"R${resultado:.2f}")
        else:
            st.info("Nenhum dado disponível. Faça upload de um PDF para começar.")
        

    except FileNotFoundError:
        st.info("Nenhum arquivo de dados encontrado. Faça upload de um PDF para começar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}") 

elif st.session_state.get('authentication_status') is None:
    st.warning("Faça o login para continuar")


      
        



#streamlit run app.py



