import re
import csv
import pandas as pd
import streamlit as st



def tratamento_dados():
#Tratamento dos dados recebidos no csv
    with open("./data/extrato.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")  # Define o delimitador como ","
        lines = list(reader)
    rows = []
    current_date = None

    for line in lines:

        if line and line[0].startswith("Data:"):
            current_date = re.search(r"Data:\s([\d\w\/]+)", line[0]).group(1)

        elif any(keyword in line[0] for keyword in ["Guardado", "Rendimentos", "Resgatado", "Ajuste nos rendimentos"]):

            movement_type = line[0].strip()
            if len(line) > 1:  # Garantir que a linha contém um valor válido
                value_match = re.search(r"[-+]R\$\s\d{1,3}(?:\.\d{3})*,\d{2}", line[1])
                if value_match:
                    value = value_match.group(0)  # Captura o valor completo
                    rows.append([current_date, movement_type, value])


    df = pd.DataFrame(rows, columns=["Data","Tipo de movimentação", "Valor"])

    #Conversão para o formato padrão de data e moeda
    df["Data"] = (df["Data"]
                .str.replace("jan", "01")
                .str.replace("fev", "02")
                .str.replace("mar", "03")
                .str.replace("abr", "04")
                .str.replace("mai", "05")
                .str.replace("jun", "06")
                .str.replace("jul", "07")
                .str.replace("ago", "08")
                .str.replace("set", "09")
                .str.replace("out", "10")
                .str.replace("nov", "11")
                .str.replace("dez", "12")
                )
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

    df["Valor"] = ((df["Valor"].str.replace("R$", "")
                .str.replace(" ", ""))
                .str.replace(".","")
                .str.replace(",","."))
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    df.to_csv("./data/dados.csv", index=False, encoding="utf-8")
    st.write("Dados carregados, caso não apareça os dados, atualize a página.")
