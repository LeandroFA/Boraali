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
st.sidebar.title("✌️ Bora Alí – Navegação")

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
body { background-color: var(--cinza); }
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
st.markdown("<div class='subtitle'>Comparação entre LATAM, GOL e AZUL usando a média histórica 2023–2025</div>", unsafe_allow_html=True)

# ==========================================
# CARREGAR DATASET
# ==========================================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

meses_nome = {
    1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',
    7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'
}

# Filtrar somente as 3 companhias
df = df[df["COMPANHIA"].isin(["LATAM", "GOL", "AZUL"])]

# ==========================================
# AGRUPAMENTO
# ==========================================
df_group = (
    df.groupby(["COMPANHIA", "MES"])["TARIFA"]
      .mean()
      .reset_index()
)
df_group["MES_NOME"] = df_group["MES"].map(meses_nome)

# ==========================================
# CALCULAR MÉTRICAS
# ==========================================
metrics = df_group.groupby("COMPANHIA")["TARIFA"].agg(["mean", "std", "min", "max"])

# volatilidade percentual
metrics["volatilidade_%"] = (metrics["max"] - metrics["min"]) / metrics["mean"] * 100

# estabilidade (0 a 100)
metrics["estabilidade"] = 100 - (metrics["std"] / metrics["mean"] * 100)

# transformar em dicionário fácil
m = metrics.round(2)

# ==========================================
# CARDS PRINCIPAIS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    mais_barata = m["mean"].idxmin()
    st.markdown(f"""
    <div class='card'>
        <b>💰 Companhia Mais Barata</b><br>
        <span class='metric'>{mais_barata}</span><br>
        Média: R$ {m.loc[mais_barata, 'mean']:.2f}
    </div>
    """, unsafe_allow_html=True)

with col2:
    mais_estavel = m["estabilidade"].idxmax()
    st.markdown(f"""
    <div class='card'>
        <b>📉 Companhia Mais Estável</b><br>
        <span class='metric'>{mais_estavel}</span><br>
        Estabilidade: {m.loc[mais_estavel, 'estabilidade']:.1f}/100
    </div>
    """, unsafe_allow_html=True)

with col3:
    maior_vol = m["volatilidade_%"].idxmax()
    st.markdown(f"""
    <div class='card'>
        <b>⚠️ Maior Oscilação</b><br>
        <span class='metric'>{maior_vol}</span><br>
        Variação: {m.loc[maior_vol, 'volatilidade_%']:.1f}%
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# GRÁFICO PRINCIPAL — LINHA
# ==========================================
st.markdown("### 📈 Evolução das Tarifas por Companhia (2023–2025)")

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
    height=480,
    xaxis_title="Mês",
    yaxis_title="Tarifa Média (R$)",
    plot_bgcolor="#F5F4FA",
    paper_bgcolor="#F5F4FA"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# INSIGHTS
# ==========================================
st.markdown("### 🧠 Insights Automáticos")

ins = "<div class='card'>"

ins += f"• A companhia mais barata em média é <b>{mais_barata}</b>.<br>"
ins += f"• A mais estável (perfeita para quem quer previsibilidade) é <b>{mais_estavel}</b>.<br>"
ins += f"• A que mais oscila no ano é <b>{maior_vol}</b> com {m.loc[maior_vol, 'volatilidade_%']:.1f}% de variação.<br>"

ins += "</div>"

st.markdown(ins, unsafe_allow_html=True)
