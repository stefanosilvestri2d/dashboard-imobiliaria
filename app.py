import streamlit as st
import pandas as pd

# Título
st.title("🏢 Dashboard Imobiliário")

# Carrega os dados
df = pd.read_csv("dados_apartamentos.csv", sep=";")

# Exibe os dados
st.subheader("Base de Dados")
st.dataframe(df)

# Informações
st.subheader("Resumo")
st.write(f"Quantidade de apartamentos: {len(df)}")
st.write(f"Quantidade de colunas: {len(df.columns)}")