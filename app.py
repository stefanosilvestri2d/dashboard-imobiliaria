import streamlit as st
import pandas as pd

# Título
st.title("🏢 Dashboard Imobiliário")

# Carrega os dados
df = pd.read_csv("dados_apartamentos.csv", sep=";")
df.columns = df.columns.str.strip()

# -----------------------------
# Filtros
# -----------------------------
st.subheader("Pesquisar apartamentos")

# Filtro por cidade
usar_cidade = st.checkbox("Filtrar por cidade")

if usar_cidade:
    cidade = st.selectbox(
        "Cidade",
        sorted(df["Cidade"].unique())
    )

# Filtro por valor
usar_valor = st.checkbox("Filtrar por valor")

if usar_valor:
    valor = st.number_input(
        "Valor máximo (R$)",
        min_value=0,
        step=10000
    )

# Filtro por vagas
usar_vagas = st.checkbox("Filtrar por vagas")

if usar_vagas:
    vagas = st.number_input(
        "Quantidade de vagas",
        min_value=1,
        step=1
    )

# Filtro por quartos
usar_quartos = st.checkbox("Filtrar por quartos")

if usar_quartos:
    quartos = st.number_input(
        "Quantidade de quartos",
        min_value=1,
        step=1
    )

# -----------------------------
# Botões
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    pesquisar = st.button("🔍 Pesquisar")

with col2:
    mostrar_todos = st.button("🏢 Mostrar todos os imóveis")

# Mostra todos os imóveis
if mostrar_todos:
    st.subheader("Todos os imóveis")
    st.dataframe(df)

# Pesquisa com filtros
if pesquisar:

    resultado = df.copy()

    if usar_cidade:
        resultado = resultado[resultado["Cidade"] == cidade]

    if usar_valor:
        resultado = resultado[resultado["Valor"] <= valor]

    if usar_vagas:
        resultado = resultado[resultado["Vagas"] == vagas]

    if usar_quartos:
        resultado = resultado[resultado["Quartos"] == quartos]

    st.success(f"Foram encontrados {len(resultado)} apartamentos.")
    st.dataframe(resultado)
