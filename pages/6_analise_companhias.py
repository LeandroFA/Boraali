# pages/6_analise_companhias.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# === REMOVER MENU NATIVO ===
st.markdown("""
<style>
div[data-testid="stSidebarNav"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# === MENU CUSTOMIZADO ===
st.sidebar.title("✌️ Bora Alí ")

st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/1_historico_por_rota.py", label="📍 Histórico por Rota")
st.sidebar.page_link("pages/2_ranking_por_estacao.py", label="🏆 Ranking por Estação")
st.sidebar.page_link("pages/3_previsao_2026.py", label="📈 Previsão 2026")
st.sidebar.page_link("pages/4_mes_ideal_orcamento.py", label="💸 Mês Ideal x Orçamento")
st.sidebar.page_link("pages/5_radar_de_oportunidades.py", label="🎯 Radar de Oportunidades")
st.sidebar.page_link("pages/6_analise_companhias.py", label="✈️ Análise das Companhias")

# ==========================================
# CONFIGURAÇÃO DE TELA
# ==========================================
st.set_page_config(
    page_title="Análise das Companhias Aéreas — Bora Alí",
    layout="wide"
)

# ==========================================
# ESTILO BORA ALÍ
# ==========================================
st.markdown("""
<style>
:root {
    --laranja: #FF9F68;
    --roxo: #9B6DFF;
    --verde: #62D99C;
    --cinza: #F5F4FA;
}
.big-title { font-size: 40px; font-weight: 900; color: var(--roxo); }
.subtitle { font-size: 18px; color: #444; margin-bottom: 18px; }
.card { background: white; padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07); margin-bottom: 15px; }
.metric { font-size: 32px; font-weight: 800; color: var(--roxo); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# TITULO
# ==========================================
st.markdown("<div class='big-title'>✈️ Análise das Companhias Aéreas</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Comparação entre LATAM, GOL e AZUL por estação do ano</div>", unsafe_allow_html=True)

# ==========================================
# CARREGAR DATA
# ==========================================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# Apenas as três principais
df = df[df["COMPANHIA"].isin(["LATAM", "GOL", "AZUL"])]

# Nome dos meses
meses_nome = {
    1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',
    7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'
}

# Estações
estacoes = {
    "Verão": [12, 1, 2],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

# ==========================================
# FILTRO — ESTAÇÃO DO ANO
# ==========================================
st.markdown("### ❄️ Escolha a estação do ano para comparar as companhias:")
estacao = st.selectbox("Estação:", ["Selecione", "Verão", "Outono", "Inverno", "Primavera"])

if estacao == "Selecione":
    st.info("👈 Selecione uma estação para visualizar os dados.")
    st.stop()

meses_filtrados = estacoes[estacao]

df = df[df["MES"].isin(meses_filtrados)]

if df.empty:
    st.warning("⚠️ Não há dados suficientes para esta estação.")
    st.stop()

# ==========================================
# AGRUPAMENTO POR COMPANHIA
# ==========================================
df_group = (
    df.groupby(["COMPANHIA", "MES"])["TARIFA"]
      .mean()
      .reset_index()
)
df_group["MES_NOME"] = df_group["MES"].map(meses_nome)

# ==========================================
# MÉTRICAS
# ==========================================
metrics = df_group.groupby("COMPANHIA")["TARIFA"].agg(["mean", "std", "min", "max"])
metrics["volatilidade_%"] = (metrics["max"] - metrics["min"]) / metrics["mean"] * 100
metrics["estabilidade"] = 100 - (metrics["std"] / metrics["mean"] * 100)
m = metrics.round(2)

# ==========================================
# CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    c = m["mean"].idxmin()
    st.markdown(f"""
    <div class='card'>
        <b>💰 Companhia Mais Barata</b><br>
        <span class='metric'>{c}</span><br>
        Média: R$ {m.loc[c,'mean']:.2f}
    </div>""", unsafe_allow_html=True)

with col2:
    c = m["estabilidade"].idxmax()
    st.markdown(f"""
    <div class='card'>
        <b>📉 Mais Estável</b><br>
        <span class='metric'>{c}</span><br>
        Estabilidade: {m.loc[c,'estabilidade']:.1f}/100
    </div>""", unsafe_allow_html=True)

with col3:
    c = m["volatilidade_%"].idxmax()
    st.markdown(f"""
    <div class='card'>
        <b>⚠️ Maior Oscilação</b><br>
        <span class='metric'>{c}</span><br>
        Variação: {m.loc[c,'volatilidade_%']:.1f}%
    </div>""", unsafe_allow_html=True)

# ==========================================
# GRÁFICO
# ==========================================
st.markdown(f"### 📈 Evolução das Tarifas — {estacao}")

fig = px.line(
    df_group,
    x="MES_NOME",
    y="TARIFA",
    color="COMPANHIA",
    markers=True,
    line_shape="spline",
    color_discrete_map={
        "LATAM": "#9B6DFF",
        "GOL": "#FF9F68",
        "AZUL": "#62D99C"
    }
)

fig.update_layout(
    height=460,
    xaxis_title="Mês",
    yaxis_title="Tarifa Média (R$)",
    plot_bgcolor="#F5F4FA",
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# INSIGHTS
# ==========================================
st.markdown("### 🧠 Insights da Estação")

comp_cheap = m["mean"].idxmin()
comp_stable = m["estabilidade"].idxmax()
comp_vol = m["volatilidade_%"].idxmax()

ins = f"""
<div class='card'>
• Na estação **{estacao}**, a companhia mais barata é <b>{comp_cheap}</b>.<br>
• A mais estável — ideal para quem evita surpresas — é <b>{comp_stable}</b>.<br>
• A que mais oscila é <b>{comp_vol}</b>, com variação de {m.loc[comp_vol,'volatilidade_%']:.1f}%.<br>
</div>
"""

st.markdown(ins, unsafe_allow_html=True)
