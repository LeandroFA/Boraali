# pages/3_previsao_2026.py
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
# CONFIGURAÇÃO
# ===========================
st.set_page_config(
    page_title="Previsão 2026 — Bora Alí",
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
.metric-value { font-size: 32px; font-weight: 900; color: var(--roxo); }
.small { font-size: 13px; color:#666; }
</style>
""", unsafe_allow_html=True)

# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>🔮 Previsão de Tarifas 2026</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Previsão baseada na média histórica (2023–2025)</div>", unsafe_allow_html=True)

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

# ===========================
# FILTROS DE ROTA
# ===========================
col1, col2 = st.columns(2)

with col1:
    origem = st.selectbox("Origem:", sorted(df["ORIGEM"].unique()))

with col2:
    destino = st.selectbox("Destino:", sorted(df["DESTINO"].unique()))

df_filtro = df[(df["ORIGEM"] == origem) & (df["DESTINO"] == destino) & (df["ANO"].isin([2023, 2024, 2025]))]

if df_filtro.empty:
    st.warning("⚠️ Não há dados suficientes dessa rota para gerar previsão.")
    st.stop()

# ===========================
# AGRUPAR DADOS POR MÊS (MÉDIA 2023–2025)
# ===========================
df_grouped = (
    df_filtro.groupby("MES")["TARIFA"]
    .mean()
    .reset_index()
)

df_grouped["MES_NOME"] = df_grouped["MES"].map(meses)

# ===========================
# APLICAR PREVISÃO (1,1% NÃO CUMULATIVO)
# ===========================
df_grouped["PREVISAO_2026"] = (df_grouped["TARIFA"] * 1.011).round(2)

# ===========================
# MELHOR MÊS DE 2026
# ===========================
melhor_mes = df_grouped.loc[df_grouped["PREVISAO_2026"].idxmin()]
melhor_mes_nome = melhor_mes["MES_NOME"]
melhor_valor = melhor_mes["PREVISAO_2026"]

# ===========================
# MÉTRICA: MELHOR MÊS
# ===========================
st.markdown(f"""
<div class='card'>
    <b>🌟 Melhor mês para viajar em 2026:</b><br>
    <span class='metric-value'>{melhor_mes_nome}</span><br>
    Tarifa estimada: <b>R$ {melhor_valor:.2f}</b>
</div>
""", unsafe_allow_html=True)

# ===========================
# GRÁFICO DE PREVISÃO
# ===========================
st.markdown("### 📈 Previsão Mensal da Tarifa — 2026")

fig = px.line(
    df_grouped,
    x="MES_NOME",
    y="PREVISAO_2026",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#9B6DFF"]
)

fig.update_layout(
    height=450,
    xaxis_title="Mês",
    yaxis_title="Tarifa Prevista (R$)",
    plot_bgcolor="#F5F4FA",
    paper_bgcolor="#F5F4FA"
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# TABELA DE PREVISÃO
# ===========================
st.markdown("### 📋 Tabela Completa da Previsão 2026")

df_exibir = df_grouped[["MES_NOME", "PREVISAO_2026"]].rename(columns={
    "MES_NOME": "Mês",
    "PREVISAO_2026": "Tarifa Prevista (R$)"
})

st.dataframe(df_exibir.style.format({"Tarifa Prevista (R$)": "R$ {:.2f}".format}), height=350)

# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights Automáticos")

insights = ""

# tendência
if df_grouped["PREVISAO_2026"].iloc[-1] < df_grouped["PREVISAO_2026"].iloc[0]:
    insights += "• A previsão sugere tendência de **queda** ao longo do ano.<br>"
else:
    insights += "• A previsão sugere tendência de **alta** ao longo do ano.<br>"

# melhor vs pior mês
pior_mes = df_grouped.loc[df_grouped["PREVISAO_2026"].idxmax()]
insights += f"• Melhor mês: <b>{melhor_mes_nome}</b> — R$ {melhor_valor:.2f}.<br>"
insights += f"• Mês mais caro previsto: <b>{pior_mes['MES_NOME']}</b> — R$ {pior_mes['PREVISAO_2026']:.2f}.<br>"

# variação
variacao = ((pior_mes["PREVISAO_2026"] - melhor_valor) / melhor_valor) * 100
insights += f"• Diferença entre melhor e pior mês: <b>{variacao:.1f}%</b>."

st.markdown(f"<div class='card'>{insights}</div>", unsafe_allow_html=True)

