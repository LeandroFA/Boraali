import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# CONFIGURAÇÕES GERAIS
# ===========================
st.set_page_config(
    page_title="Histórico por Rota — Bora Alí",
    layout="wide"
)

# ===========================
# CSS ESTILO BORA ALÍ
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
    margin-bottom: -10px;
}

.subtitle {
    font-size: 20px !important;
    color: #444;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    font-size: 18px;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: var(--roxo);
}

</style>
""", unsafe_allow_html=True)


# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>📍 Histórico por Rota</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Veja como os valores se comportaram nos últimos anos</div>", unsafe_allow_html=True)


# ===========================
# CARREGAR DATASET
# ===========================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")

df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# ===========================
# FILTROS
# ===========================
col1, col2 = st.columns([1, 1])

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

colA, colB = st.columns([1,1])

with colA:
    st.markdown(f"""
    <div class='card'>
        <b>🎯 Tarifa média da rota:</b><br>
        <span class='metric-value'>R$ {media_geral:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class='card'>
        <b>🔥 Melhor época para viajar:</b><br>
        <span class='metric-value'>Mês {melhor_mes} — R$ {melhor_valor:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)


# ===========================
# GRÁFICO HISTÓRICO
# ===========================
st.markdown("### 📈 Evolução Mensal da Tarifa (2023–2025)")

fig = px.line(
    df_filtro,
    x="MES",
    y="TARIFA",
    color="ANO",
    markers=True,
    color_discrete_sequence=["#9B6DFF", "#FF9F68", "#62D99C"]
)

fig.update_layout(
    height=450,
    xaxis_title="Mês",
    yaxis_title="Tarifa Média (R$)",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)


# ===========================
# MÉDIA ANUAL
# ===========================
st.markdown("### 📊 Média Anual da Rota")

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
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig2, use_container_width=True)


# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights da Rota")

insight = ""

if df_ano["TARIFA"].iloc[-1] < df_ano["TARIFA"].iloc[0]:
    insight += "• A rota ficou mais barata ao longo dos anos.<br>"
else:
    insight += "• A rota está encarecendo ano a ano.<br>"

insight += f"• O melhor mês histórico para viajar é <b>Mês {melhor_mes}</b> com tarifa média de <b>R$ {melhor_valor:,.2f}</b>.<br>"
insight += "• Os meses de baixa estação normalmente têm valores mais baixos."

st.markdown(f"<div class='card'>{insight}</div>", unsafe_allow_html=True)
