import pandas as pd
import streamlit as st


# Carregando o arquivo CSV
df = pd.read_csv("data/dados.csv")
df['Data'] = pd.to_datetime(df['Data'])

#Filtros
st.sidebar.header("Filtros")

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
saldo = total_guardado + total_rendimentos - total_resgatado

dados= {
    "Depositado": [total_guardado],
    "Resgatado": [total_resgatado],
    "Rendimentos": [total_rendimentos],
    "Saldo Total": [saldo]
}

kpi_dataframe = pd.DataFrame(dados)
print(kpi_dataframe)
#Criação de gráficos


st.title("Cofrinho PicPay")
#KPI's
st.dataframe(kpi_dataframe)

#Gráficos
st.dataframe(data_filtrada)
st.bar_chart(data_filtrada.sort_values(by="Data"), x="Data", y="Valor")









#streamlit run app.py



