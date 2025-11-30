# pages/2_ranking_por_estacao.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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
# CONFIGURAÇÃO
# ===========================
st.set_page_config(
    page_title="Ranking por Estação — Bora Alí",
    layout="wide"
)

# ===========================
# ESTILO (BORA ALÍ)
# ===========================
st.markdown("""
<style>
:root {
    --laranja: #FF9F68;
    --roxo: #9B6DFF;
    --verde: #62D99C;
    --cinza: #F5F4FA;
}
body { background-color: var(--cinza); }
.big-title { font-size: 40px !important; font-weight: 900; color: var(--roxo); margin-bottom: -6px; }
.subtitle { font-size: 17px !important; color: #444; margin-bottom: 18px; }
.card { background: white; padding: 18px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 14px; }
.metric-value { font-size: 28px; font-weight: 800; color: var(--roxo); }
.small { font-size: 13px; color:#666; }
</style>
""", unsafe_allow_html=True)

# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>🍃 Ranking por Estação</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Veja os destinos com melhor custo-benefício na estação selecionada</div>", unsafe_allow_html=True)


# ===========================
# CARREGAR DADOS
# ===========================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# ===========================
# ADICIONAR ANO 2026 (+1%)
# ===========================
df_2026 = df.copy()
df_2026["ANO"] = 2026
df_2026["TARIFA"] = df_2026["TARIFA"] * 1.01   # <<<<< AQUI ENTRA O +1%

df = pd.concat([df, df_2026], ignore_index=True)

# ===========================
# ESTAÇÕES DO ANO
# ===========================
estacoes = {
    "Verão": [12, 1, 2],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

# ===========================
# FILTROS
# ===========================
col1, col2, col3 = st.columns(3)

with col1:
    origem_choices = ["Todas"] + sorted(df["ORIGEM"].unique().tolist())
    origem_sel = st.selectbox("Origem (opcional):", origem_choices, index=0)

with col2:
    estacao_sel = st.selectbox("Estação:", list(estacoes.keys()))

with col3:
    anos_disponiveis = sorted(df["ANO"].unique().tolist())
    anos_sel = st.multiselect("Anos:", anos_disponiveis, default=[2023, 2024, 2025, 2026])

if len(anos_sel) == 0:
    st.error("Selecione ao menos 1 ano para continuar.")
    st.stop()

# ===========================
# FILTRAR DATAFRAME
# ===========================
meses_est = estacoes[estacao_sel]

df_filtered = df[df["MES"].isin(meses_est) & df["ANO"].isin(anos_sel)]
if origem_sel != "Todas":
    df_filtered = df_filtered[df_filtered["ORIGEM"] == origem_sel]

if df_filtered.empty:
    st.warning("Nenhum dado disponível para essa combinação.")
    st.stop()

# ===========================
# AGREGAR POR DESTINO (ARREDONDADO)
# ===========================
agg = (
    df_filtered.groupby("DESTINO", as_index=False)["TARIFA"]
    .mean()
    .round(0)   # Arredonda
    .rename(columns={"TARIFA": "TARIFA_MEDIA_ESTACAO"})
).sort_values("TARIFA_MEDIA_ESTACAO", ascending=True)

# ===========================
# TOP 5 + TOP 3 EVITAR
# ===========================
top5 = agg.head(5)
evitar3 = agg.tail(3).sort_values("TARIFA_MEDIA_ESTACAO", ascending=False)

# ===========================
# CORES
# ===========================
cores = {
    "top": "#62D99C",
    "bad": "#9B6DFF"
}

# ===========================
# GRÁFICO TOP 5
# ===========================
st.markdown(f"## 📊 Resultados — Estação **{estacao_sel}**")
st.markdown("### 🟢 Top 5 destinos mais baratos")

fig_top5 = px.bar(
    top5,
    x="TARIFA_MEDIA_ESTACAO",
    y="DESTINO",
    orientation="h",
    text="TARIFA_MEDIA_ESTACAO",
    color_discrete_sequence=[cores["top"]]
)

fig_top5.update_traces(texttemplate="R$ %{x:.0f}", textposition="outside")
fig_top5.update_layout(height=380, margin=dict(l=120, r=20, t=30, b=30))

st.plotly_chart(fig_top5, use_container_width=True)

# ===========================
# GRÁFICO 3 DESTINOS A EVITAR
# ===========================
st.markdown("### 🔴 3 destinos mais caros (evite)")

fig_evitar = px.bar(
    evitar3,
    x="TARIFA_MEDIA_ESTACAO",
    y="DESTINO",
    orientation="h",
    text="TARIFA_MEDIA_ESTACAO",
    color_discrete_sequence=[cores["bad"]]
)

fig_evitar.update_traces(texttemplate="R$ %{x:.0f}", textposition="outside")
fig_evitar.update_layout(height=300, margin=dict(l=120, r=20, t=30, b=30))

st.plotly_chart(fig_evitar, use_container_width=True)

# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights rápidos")

melhor = top5.iloc[0]
mediana = agg["TARIFA_MEDIA_ESTACAO"].median()
pct_gap = ((mediana - melhor["TARIFA_MEDIA_ESTACAO"]) / mediana) * 100 if mediana != 0 else np.nan

st.markdown(f"""
<div class='card'>
    <b>Melhor destino:</b> {melhor['DESTINO']}<br>
    <b>Tarifa média:</b> R$ {melhor['TARIFA_MEDIA_ESTACAO']:.0f}<br><br>
    <b>Mediana da estação:</b> R$ {mediana:.0f}<br>
    <b>Vantagem vs mediana:</b> {pct_gap:.1f}% mais barato
</div>
""", unsafe_allow_html=True)

# ===========================
# RECOMENDAÇÕES
# ===========================
st.markdown("### 💬 Recomendações")
st.markdown(
    "- O Top 5 mostra os destinos com **melhor custo-benefício** na estação.<br>"
    "- Os destinos mais caros devem ser evitados devido à alta demanda sazonal.<br>",
    unsafe_allow_html=True
)
