import pandas as pd
import streamlit as st

# Carregando o arquivo CSV
df = pd.read_csv("data/dados.csv")
print(df)

#mostrar venda e compra
filtro1= df["Tipo de movimentação"].isin(["Guardado", "Resgatado"])
filtro1_apply= df.loc[filtro1]
st.dataframe(filtro1_apply)


#rendimentos
filtro_rendimentos = df["Tipo de movimentação"].isin(["Rendimentos"])
rendimento_filtrado = df.loc[filtro_rendimentos]

st.title("Rendimentos da carteira")
st.bar_chart(rendimento_filtrado.sort_values(by="Data"), x="Data", y="Valor")
st.caption("Total de rendimentos")
#total de rendimentos
total_acumulado = rendimento_filtrado["Valor"].sum()
st.text(total_acumulado)

#depósitos
filtro_guardado = df["Tipo de movimentação"].isin(["Guardado"])
guardado_filtrado = df.loc[filtro_guardado]

st.title("Depósitos na carteira")
st.bar_chart(guardado_filtrado.sort_values(by="Data"), x="Data", y="Valor")
st.caption("Total depositado")
#total depositado
total_guardado = guardado_filtrado["Valor"].sum()
st.text(total_guardado)


#saques
filtro_resgatado = df["Tipo de movimentação"].isin(["Resgatado"])
resgatado_filtrado = df.loc[filtro_resgatado]

st.title("Resgates na carteira")
st.bar_chart(resgatado_filtrado.sort_values(by="Data"), x="Data", y="Valor",color="#FF0000")
st.caption("Total de Saques")
#total sacado
#total depositado
total_sacado = resgatado_filtrado["Valor"].sum()
st.text(total_sacado)

st.caption("Total Acumulado")
rend_dep = total_acumulado + total_guardado
saldo_final = rend_dep + total_sacado
st.text(saldo_final)

#streamlit run app.py



