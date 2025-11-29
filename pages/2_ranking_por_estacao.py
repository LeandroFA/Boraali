# pages/2_ranking_por_estacao.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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
# ESTAÇÕES
# ===========================
estacoes = {
    "Verão": [12, 1, 2],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

# ===========================
# FILTROS (origem opcional, estação, anos)
# ===========================
col1, col2, col3 = st.columns([1,1,1])

with col1:
    origem_choices = ["Todas"] + sorted(df["ORIGEM"].unique().tolist())
    origem_sel = st.selectbox("Origem (opcional):", origem_choices, index=0)

with col2:
    estacao_sel = st.selectbox("Estação:", list(estacoes.keys()))

with col3:
    anos_disponiveis = sorted(df["ANO"].unique().tolist())
    anos_sel = st.multiselect("Anos (filtrar):", anos_disponiveis, default=anos_disponiveis)

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
    st.warning("Nenhum dado disponível para essa combinação. Tente outra origem/estação/ano.")
    st.stop()

# ===========================
# AGREGAR POR DESTINO
# ===========================
agg = (
    df_filtered.groupby("DESTINO", as_index=False)["TARIFA"]
    .mean()
    .rename(columns={"TARIFA": "TARIFA_MEDIA_ESTACAO"})
).sort_values("TARIFA_MEDIA_ESTACAO", ascending=True)

# ===========================
# TOP 5 + TOP 3 A EVITAR
# ===========================
top5 = agg.head(5).copy()
evitar3 = agg.tail(3).sort_values("TARIFA_MEDIA_ESTACAO", ascending=False).copy()

# ===========================
# CORES BORA ALÍ
# ===========================
cores = {
    "top": "#62D99C",      # verde
    "bad": "#9B6DFF"       # roxo
}

# ===========================
# GRÁFICO TOP 5
# ===========================
fig_top5 = px.bar(
    top5,
    x="TARIFA_MEDIA_ESTACAO",
    y="DESTINO",
    orientation="h",
    text="TARIFA_MEDIA_ESTACAO",
    labels={"TARIFA_MEDIA_ESTACAO": "Tarifa média (R$)", "DESTINO": "Destino"},
    color_discrete_sequence=[cores["top"]]
)
fig_top5.update_traces(texttemplate="R$ %{x:.2f}", textposition="outside")
fig_top5.update_layout(height=380, margin=dict(l=120, r=20, t=30, b=30))

# ===========================
# GRÁFICO TOP 3 PARA EVITAR
# ===========================
fig_evitar = px.bar(
    evitar3,
    x="TARIFA_MEDIA_ESTACAO",
    y="DESTINO",
    orientation="h",
    text="TARIFA_MEDIA_ESTACAO",
    color_discrete_sequence=[cores["bad"]]
)
fig_evitar.update_traces(texttemplate="R$ %{x:.2f}", textposition="outside")
fig_evitar.update_layout(height=300, margin=dict(l=120, r=20, t=30, b=30))

# ===========================
# LAYOUT
# ===========================
st.markdown(f"### 📊 Resultados — Estação: **{estacao_sel}** ")

left, right = st.columns([2,1])

with left:
    st.markdown("### 🟢 Top 5 destinos mais baratos")
    st.plotly_chart(fig_top5, use_container_width=True)

    st.markdown("### 🔴 3 destinos mais caros (evite)")
    st.plotly_chart(fig_evitar, use_container_width=True)

with right:
    st.markdown("### 🧠 Insights rápidos")

    melhor = top5.iloc[0]
    mediana = agg["TARIFA_MEDIA_ESTACAO"].median()
    pct_gap = ((mediana - melhor["TARIFA_MEDIA_ESTACAO"]) / mediana) * 100 if mediana != 0 else np.nan

    st.markdown(f"""
    <div class='card'>
        <b>Melhor destino:</b> {melhor['DESTINO']}<br>
        <b>Tarifa média:</b> R$ {melhor['TARIFA_MEDIA_ESTACAO']:.2f}<br><br>
        <b>Mediana da estação:</b> R$ {mediana:.2f}<br>
        <b>Vantagem vs mediana:</b> {pct_gap:.1f}% mais barato
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💬 Recomendações")
    st.markdown(
        "- O top 5 representa o melhor custo-benefício médio na estação.<br>"
        "- Os destinos do bloco vermelho sofrem forte variação ou são alta demanda.<br>"
        "- Use para identificar oportunidades sazonais claras.",
        unsafe_allow_html=True
    )
