import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# CONFIGURAÇÃO
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
st.markdown("<div class='subtitle'>Acompanhe o comportamento dos preços da rota escolhida ao longo do tempo</div>", unsafe_allow_html=True)

# ===========================
# CARREGAR DATA
# ===========================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")

df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# ===========================
# MAPEAMENTO DE MESES
# ===========================
meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

df["MES_NOME"] = df["MES"].map(meses)

# ===========================
# FILTROS
# ===========================
col1, col2 = st.columns(2)

with col1:
    origem = st.selectbox("Selecione a origem:", sorted(df["ORIGEM"].unique()))

with col2:
    destino = st.selectbox("Selecione o destino:", sorted(df["DESTINO"].unique()))

df_filtro = df[(df["ORIGEM"] == origem) & (df["DESTINO"] == destino)]

if df_filtro.empty:
    st.warning("⚠️ Não há dados para essa rota. Tente outra combinação.")
    st.stop()

# ===========================
# MÉTRICAS PRINCIPAIS
# ===========================
media_geral = df_filtro["TARIFA"].mean()
melhor_mes = df_filtro.groupby("MES")["TARIFA"].mean().idxmin()
melhor_valor = df_filtro.groupby("MES")["TARIFA"].mean().min()

colA, colB = st.columns(2)

with colA:
    st.markdown(f"""
    <div class='card'>
        <b>🎯 Tarifa média da rota (2023–2025):</b><br>
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
# GRÁFICO MELHORADO — LINHA
# ===========================
st.markdown("### 📈 Evolução Mensal da Tarifa (por ano)")

fig = px.line(
    df_filtro,
    x="MES_NOME",
    y="TARIFA",
    color="ANO",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#9B6DFF", "#FF9F68", "#62D99C"]
)

fig.update_traces(marker=dict(size=10, opacity=0.9))
fig.update_layout(
    height=450,
    xaxis_title="Mês",
    yaxis_title="Tarifa (R$)",
    plot_bgcolor="#F5F4FA",
    paper_bgcolor="#F5F4FA",
    font=dict(size=14),
    xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.07)"),
    yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.07)")
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# GRÁFICO MÉDIA ANUAL
# ===========================
st.markdown("### 📊 Média Anual da Tarifa")

df_ano = df_filtro.groupby("ANO")["TARIFA"].mean().reset_index()

fig2 = px.bar(
    df_ano,
    x="ANO",
    y="TARIFA",
    color="ANO",
    color_discrete_sequence=["#9B6DFF", "#FF9F68", "#62D99C"]
)

fig2.update_layout(
    height=400,
    xaxis_title="Ano",
    yaxis_title="Tarifa Média (R$)",
    plot_bgcolor="#FFFFFF",
)

st.plotly_chart(fig2, use_container_width=True)

# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights sobre a rota")

insight = ""

if df_ano_
