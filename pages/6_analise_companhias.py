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


# ===========================
# CONFIGURAÇÃO
# ===========================
st.set_page_config(
    page_title="Análise das Companhias — Bora Alí",
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
body { background-color: var(--cinza); }
.big-title { font-size: 40px !important; font-weight: 900; color: var(--roxo); margin-bottom: -6px; }
.subtitle { font-size: 17px !important; color: #444; margin-bottom: 18px; }
.card { background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.08); margin-bottom: 16px; }
.metric { font-size: 32px; font-weight: 900; color: var(--roxo); }
.small { font-size: 13px; color:#666; }
</style>
""", unsafe_allow_html=True)

# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>✈️ Análise Global das Companhias Aéreas</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Comparação de preço, estabilidade e desempenho por estação do ano</div>", unsafe_allow_html=True)

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
    "Ano inteiro": list(range(1, 13)),
    "Verão": [12, 1, 2],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

# ===========================
# FILTRO
# ===========================
estacao_sel = st.selectbox(
    "Selecione a estação do ano:",
    list(estacoes.keys()),
    index=0
)

df_filtro = df[df["MES"].isin(estacoes[estacao_sel])]

# ===========================
# AGRUPAÇÃO POR COMPANHIA
# ===========================
agg = df_filtro.groupby("COMPANHIA")["TARIFA"].agg(
    preco_medio="mean",
    preco_min="min",
    preco_max="max",
    variacao=lambda x: x.max() - x.min(),
    estabilidade=lambda x: x.std()
).reset_index()

# ===========================
# DEFINIR TOPS
# ===========================
mais_barata = agg.loc[agg["preco_medio"].idxmin()]
mais_cara = agg.loc[agg["preco_medio"].idxmax()]
mais_estavel = agg.loc[agg["estabilidade"].idxmin()]
mais_oscilante = agg.loc[agg["variacao"].idxmax()]

# ===========================
# CARDS
# ===========================
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class='card'>
        <b>💸 Companhia mais barata:</b><br>
        <span class='metric'>{mais_barata['COMPANHIA']}</span><br>
        Média: R$ {mais_barata['preco_medio']:.2f}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card'>
        <b>🔥 Companhia mais cara:</b><br>
        <span class='metric'>{mais_cara['COMPANHIA']}</span><br>
        Média: R$ {mais_cara['preco_medio']:.2f}
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <b>🎯 Mais estável (menor variação):</b><br>
        <span class='metric'>{mais_estavel['COMPANHIA']}</span><br>
        Desvio: {mais_estavel['estabilidade']:.2f}
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='card'>
        <b>⚡ Maior oscilação de preços:</b><br>
        <span class='metric'>{mais_oscilante['COMPANHIA']}</span><br>
        Diferença: R$ {mais_oscilante['variacao']:.2f}
    </div>
    """, unsafe_allow_html=True)

# ===========================
# GRÁFICO DE OSCILAÇÃO
# ===========================
st.markdown("### 📉 Volatilidade das Tarifas por Companhia")

fig = px.bar(
    agg,
    x="COMPANHIA",
    y="variacao",
    text="variacao",
    color="variacao",
    color_continuous_scale=["#62D99C", "#FF9F68"],
)

fig.update_traces(texttemplate="R$ %{y:.2f}", textposition="outside")
fig.update_layout(height=420, yaxis_title="Oscilação (R$)", coloraxis_showscale=False)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# RANKING DE ESTABILIDADE
# ===========================
st.markdown("### 🏆 Ranking de Estabilidade (Menor → Maior)")

ranking = agg.sort_values("estabilidade")[["COMPANHIA", "estabilidade"]]
st.dataframe(ranking.style.format({"estabilidade": "{:.2f}"}))

# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights Automáticos")

insight = f"""
<div class='card'>
• Para a estação <b>{estacao_sel}</b>, a companhia mais econômica é <b>{mais_barata['COMPANHIA']}</b>.<br>
• A companhia mais estável é <b>{mais_estavel['COMPANHIA']}</b>, ideal para quem prefere previsibilidade.<br>
• <b>{mais_oscilante['COMPANHIA']}</b> apresenta a maior oscilação, indicando forte variação de demanda.<br>
• A comparação por estação mostra diferenças claras no comportamento das companhias.
</div>
"""

st.markdown(insight, unsafe_allow_html=True)

