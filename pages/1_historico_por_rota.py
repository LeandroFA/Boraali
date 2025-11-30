import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st

# === REMOVER MENU NATIVO ===
st.markdown("""
<style>
div[data-testid="stSidebarNav"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# === MENU CUSTOMIZADO (FUNCIONA EM TODAS AS PÁGINAS) ===
st.sidebar.title("✌️ Bora Alí – Navegação")

st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/1_historico_por_rota.py", label="📍 Histórico por Rota")
st.sidebar.page_link("pages/2_ranking_por_estacao.py", label="🏆 Ranking por Estação")
st.sidebar.page_link("pages/3_previsao_2026.py", label="📈 Previsão 2026")
st.sidebar.page_link("pages/4_mes_ideal_orcamento.py", label="💸 Mês Ideal x Orçamento")
st.sidebar.page_link("pages/5_radar_de_oportunidades.py", label="🎯 Radar de Oportunidades")

# ===========================
# CONFIG GERAL
# ===========================
st.set_page_config(
    page_title="Histórico por Rota — Bora Alí",
    layout="wide"
)

# ===========================
# ESTILO BORA ALÍ
# ===========================
st.markdown("""
<style>

:root {
    --laranja: #FF9F68;
    --roxo: #9B6DFF;
    --verde: #62D99C;
    --cinza: #F5F4FA;
}

body {
    background-color: var(--cinza);
}

.big-title {
    font-size: 42px !important;
    font-weight: 900 !important;
    color: var(--roxo);
    margin-bottom: -5px;
}

.subtitle {
    font-size: 20px !important;
    color: #444;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.10);
    font-size: 18px;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 34px;
    font-weight: 900;
    color: var(--roxo);
}
</style>
""", unsafe_allow_html=True)

# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>📍 Histórico por Rota</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Visualize o comportamento da tarifa ao longo dos anos</div>", unsafe_allow_html=True)

# ===========================
# CARREGAR DATA
# ===========================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")

df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# ===========================
# NOMES DOS MESES
# ===========================
meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

df["MES_NOME"] = df["MES"].map(meses)

# ===========================
# FILTROS DE ROTA (AGORA COM “SELECIONE”)
# ===========================
col1, col2 = st.columns(2)

with col1:
    origens = sorted(df["ORIGEM"].unique())
    origem = st.selectbox("Origem:", ["Selecione a origem"] + origens)

with col2:
    destinos = sorted(df["DESTINO"].unique())
    destino = st.selectbox("Destino:", ["Selecione o destino"] + destinos)

# Impede execução se não escolher origem e destino
if origem == "Selecione a origem" or destino == "Selecione o destino":
    st.warning("Por favor, selecione a origem e o destino para visualizar os gráficos.")
    st.stop()

df_filtro = df[(df["ORIGEM"] == origem) & (df["DESTINO"] == destino)]

if df_filtro.empty:
    st.warning("⚠️ Não há dados para essa rota.")
    st.stop()

# ===========================
# AGRUPAR PARA NÃO TER MESES DUPLICADOS
# ===========================
df_grouped = (
    df_filtro.groupby(["ANO", "MES", "MES_NOME"])["TARIFA"]
    .mean()
    .reset_index()
)

# ===========================
# CÁLCULO DE MÉTRICAS
# ===========================
media_geral = df_grouped["TARIFA"].mean()

melhor_mes = (
    df_grouped.groupby("MES")["TARIFA"]
    .mean()
    .idxmin()
)

melhor_valor = (
    df_grouped.groupby("MES")["TARIFA"]
    .mean()
    .min()
)

# ===========================
# CARDS
# ===========================
colA, colB = st.columns(2)

with colA:
    st.markdown(f"""
    <div class='card'>
        <b>🎯 Tarifa média geral:</b><br>
        <span class='metric-value'>R$ {media_geral:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class='card'>
        <b>🔥 Melhor época para viajar:</b><br>
        <span class='metric-value'>{meses[melhor_mes]} — R$ {melhor_valor:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

# ===========================
# GRÁFICO DE LINHA — MESES ORDENADOS
# ===========================
st.markdown("### 📈 Evolução Mensal da Tarifa (por Ano)")

ordem_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

fig = px.line(
    df_grouped,
    x="MES_NOME",
    y="TARIFA",
    color="ANO",
    markers=True,
    line_shape="spline",
    category_orders={"MES_NOME": ordem_meses},
    color_discrete_sequence=["#9B6DFF", "#FF9F68", "#62D99C"]
)

fig.update_traces(marker=dict(size=10))
fig.update_layout(
    height=440,
    xaxis_title="Mês",
    yaxis_title="Tarifa Média (R$)",
    plot_bgcolor="#F5F4FA",
    paper_bgcolor="#F5F4FA"
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# GRÁFICO ANUAL — SEM 2023.5
# ===========================
st.markdown("### 📊 Média Anual da Tarifa")

df_ano = (
    df_grouped.groupby("ANO")["TARIFA"]
    .mean()
    .reset_index()
)

df_ano["ANO"] = df_ano["ANO"].astype(str)

fig2 = px.bar(
    df_ano,
    x="ANO",
    y="TARIFA",
    text_auto=".2f",
    color="ANO",
    color_discrete_sequence=["#9B6DFF", "#FF9F68", "#62D99C"]
)

fig2.update_layout(
    height=400,
    xaxis_type="category",
    xaxis_title="Ano",
    yaxis_title="Tarifa Média (R$)"
)

st.plotly_chart(fig2, use_container_width=True)

# ===========================
# INSIGHTS AUTOMÁTICOS
# ===========================
st.markdown("### 🧠 Insights da Rota")

trend = df_ano["TARIFA"].astype(float)

insights = ""

if trend.iloc[-1] < trend.iloc[0]:
    insights += "• A rota está ficando **mais barata** ao longo dos anos.<br>"
else:
    insights += "• A rota está ficando **mais cara** ao longo dos anos.<br>"

insights += f"• O mês historicamente mais vantajoso é <b>{meses[melhor_mes]}</b>.<br>"
insights += "• Meses de baixa estação geralmente apresentam tarifas menores."

st.markdown(f"<div class='card'>{insights}</div>", unsafe_allow_html=True)
