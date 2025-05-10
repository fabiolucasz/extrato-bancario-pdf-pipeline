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
    adicionar_pdf = st.file_uploader("Adicionar PDF", type="pdf")
    if adicionar_pdf:
        st.write("Carregando PDF...")
        tabula.convert_into(adicionar_pdf, "./data/extrato.csv", output_format="csv", pages='all', guess=False)
        tratamento_dados()

    
        # Tenta carregar o arquivo CSV, mas continua se não existir
    df = pd.DataFrame()
    try:
        
        df = pd.read_csv("data/dados.csv")
        df['Data'] = pd.to_datetime(df['Data'])


        #Filtros
        st.sidebar.header("Filtros")

        # Verifica se há dados antes de tentar filtrar
        if len(df) > 0:
            #Filtro dataframe
            tipos = ["Guardado", "Resgatado", "Rendimentos"]
            lista = st.sidebar.multiselect("Selecione o tipo de movimentação",tipos,default=tipos[0])
            tipo= df["Tipo de movimentação"].isin(lista)

            #Filtro de datas
            data = tipo
            data_filtro = df.loc[data]
            data_inicial = data_filtro['Data'].min().to_pydatetime()
            data_final = (data_filtro['Data'].max()).to_pydatetime()

            intervalo_datas = st.sidebar.slider("Selecione o período",
                                                min_value=data_inicial,
                                                max_value=data_final,
                                                value=(data_inicial,data_final))

            data_filtrada = data_filtro[
                (data_filtro['Data'] >= intervalo_datas[0]) &
                (data_filtro['Data'] <= intervalo_datas[1])
            ]
        else:
            st.info("Nenhum dado disponível. Faça upload de um PDF para começar.")
            # Cria um DataFrame vazio para evitar erros
            data_filtrada = pd.DataFrame({"Data": [], "Valor": []})

        #KPI's
        # rendimentos
        rendimentos = df['Tipo de movimentação'].isin(["Rendimentos"])
        kpi_rendimentos = df.loc[rendimentos]
        total_rendimentos = kpi_rendimentos['Valor'].sum()

        # Guardado
        guardado = df['Tipo de movimentação'].isin(['Guardado'])
        kpi_guardado = df.loc[guardado]
        total_guardado = kpi_guardado['Valor'].sum()

        # Resgatado
        resgatado = df['Tipo de movimentação'].isin(['Resgatado'])
        kpi_resgatado = df.loc[resgatado]
        total_resgatado = kpi_resgatado['Valor'].sum()

        # Saldo
        saldo = total_resgatado + total_guardado + total_rendimentos

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
            
            st.bar_chart(data_filtrada.sort_values(by="Data"), x="Data", y="Valor")
            st.text("Total do período")
            st.text(f"R${resultado:.2f}")
        else:
            st.info("Nenhum dado disponível. Faça upload de um PDF para começar.")
        authenticator.logout('Logout', 'sidebar')

    except FileNotFoundError:
        st.info("Nenhum arquivo de dados encontrado. Faça upload de um PDF para começar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}") 

elif st.session_state.get('authentication_status') is None:
    st.warning("Faça o login para continuar")


      
        



#streamlit run app.py



