import streamlit as st
import pandas as pd
import pydeck as pdk

# Título
st.title("🏢 Dashboard Imobiliário")

# Carrega os dados
df = pd.read_csv("dados_apartamentos.csv", sep=";")
df.columns = df.columns.str.strip()

COLUNAS_OCULTAS = ["lat", "lon"]

# Estado inicial guardado entre reruns
if "modo" not in st.session_state:
    st.session_state["modo"] = None
    st.session_state["dados_exibir"] = None
    st.session_state["imovel_selecionado"] = None


def exibir_tabela(dados):
    st.dataframe(dados.drop(columns=COLUNAS_OCULTAS, errors="ignore"))


# -----------------------------
# Filtros
# -----------------------------
st.subheader("Pesquisar apartamentos")

# Filtro por bairro
usar_cidade = st.checkbox("Filtrar por bairro")

if usar_cidade:
    cidade = st.selectbox(
        "bairro",
        sorted(df["Bairro"].unique())
    )

# Filtro por valor (intervalo, mas aceita valor exato se min = max)
usar_valor = st.checkbox("Filtrar por valor")

if usar_valor:
    col_valor_min, col_valor_max = st.columns(2)

    with col_valor_min:
        valor_min = st.number_input(
            "Valor mínimo (R$)",
            min_value=0,
            step=10000
        )

    with col_valor_max:
        valor_max = st.number_input(
            "Valor máximo (R$)",
            min_value=0,
            step=10000,
            value=1000000
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


# -----------------------------
# Função para exibir o mapa
# -----------------------------
def mostrar_mapa(dados):
    dados_mapa = dados.dropna(subset=["lat", "lon"])
    if dados_mapa.empty:
        st.info("Esse imóvel não possui coordenadas cadastradas.")
        return

    st.subheader("📍 Localização no mapa")
    st.caption("Localização aproximada, baseada no bairro.")

    camada_pontos = pdk.Layer(
        "ScatterplotLayer",
        data=dados_mapa,
        get_position="[lon, lat]",
        get_radius=1,
        radius_units="pixels",
        radius_min_pixels=6,
        radius_max_pixels=10,
        get_fill_color=[220, 60, 60, 200],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=dados_mapa["lat"].mean(),
        longitude=dados_mapa["lon"].mean(),
        zoom=14,
    )

    st.pydeck_chart(pdk.Deck(layers=[camada_pontos], initial_view_state=view_state))


# -----------------------------
# Ao clicar em um botão, guarda o resultado no session_state
# (isso evita que trocar a seleção do imóvel apague a pesquisa)
# -----------------------------
if mostrar_todos:
    st.session_state["modo"] = "todos"
    st.session_state["dados_exibir"] = df.reset_index(drop=True)
    st.session_state["imovel_selecionado"] = None

if pesquisar:
    resultado = df.copy()

    if usar_cidade:
        resultado = resultado[resultado["Bairro"] == cidade]

    if usar_valor:
        resultado = resultado[
            (resultado["Valor"] >= valor_min) & (resultado["Valor"] <= valor_max)
        ]

    if usar_vagas:
        resultado = resultado[resultado["Vagas"] == vagas]

    if usar_quartos:
        resultado = resultado[resultado["Quartos"] == quartos]

    st.session_state["modo"] = "pesquisa"
    st.session_state["dados_exibir"] = resultado.reset_index(drop=True)
    st.session_state["imovel_selecionado"] = None

# -----------------------------
# Renderiza o que estiver salvo no session_state
# -----------------------------
if st.session_state["modo"] is not None:
    dados_atual = st.session_state["dados_exibir"]

    if st.session_state["modo"] == "todos":
        st.subheader("Todos os imóveis")
    else:
        st.success(f"Foram encontrados {len(dados_atual)} apartamentos.")

    exibir_tabela(dados_atual)

    if not dados_atual.empty:
        opcoes = dados_atual.apply(
            lambda linha: f"#{linha.name + 1} — {linha['Bairro']} — R$ {linha['Valor']:,.0f} — "
                          f"{linha['Quartos']} quarto(s), {linha['Vagas']} vaga(s)",
            axis=1,
        )

        indice_escolhido = st.selectbox(
            "Escolha um imóvel",
            options=dados_atual.index,
            format_func=lambda i: opcoes[i],
            key="seletor_imovel",
        )

        if st.button("📍 Mostrar mapa"):
            st.session_state["imovel_selecionado"] = indice_escolhido

        if st.session_state["imovel_selecionado"] is not None:
            imovel = dados_atual.loc[[st.session_state["imovel_selecionado"]]]
            mostrar_mapa(imovel)
