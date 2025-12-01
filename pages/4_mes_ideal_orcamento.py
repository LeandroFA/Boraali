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

# === MENU CUSTOMIZADO ===
st.sidebar.title("✌️ Bora Alí")

st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/1_historico_por_rota.py", label="📍 Histórico por Rota")
st.sidebar.page_link("pages/2_ranking_por_estacao.py", label="🏆 Ranking por Estação")
st.sidebar.page_link("pages/3_previsao_2026.py", label="📈 Previsão 2026")
st.sidebar.page_link("pages/4_mes_ideal_orcamento.py", label="💸 Mês Ideal x Orçamento")
st.sidebar.page_link("pages/5_radar_de_oportunidades.py", label="🎯 Radar de Oportunidades")
st.sidebar.page_link("pages/6_analise_companhias.py", label="✈️ Análise das Companhias")


# ===========================
# CONFIG MODELO
# ===========================
st.set_page_config(
    page_title="Melhor Mês pelo Orçamento — Bora Alí",
    layout="wide"
)

# ===========================
# ESTILO
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
.big-title { font-size: 38px !important; font-weight: 900; color: var(--roxo); margin-bottom: -6px; }
.subtitle { font-size: 17px !important; color: #444; margin-bottom: 20px; }
.card { background: white; padding: 18px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 14px; }
.metric-value { font-size: 32px; font-weight: 900; color: var(--roxo); }
.small { font-size: 13px; color:#666; }
</style>
""", unsafe_allow_html=True)

# ===========================
# TÍTULO
# ===========================
st.markdown("<div class='big-title'>💸 Melhor Mês Pelo Seu Orçamento</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Veja todos os meses que cabem no seu bolso — e o melhor entre eles</div>", unsafe_allow_html=True)

# ===========================
# CARREGAR DATA
# ===========================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

meses_nome = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# ===========================
# FILTROS — NOVA ORDEM (Orçamento → Origem → Destino)
# ===========================
col1, col2, col3 = st.columns(3)

with col1:
    orcamento = st.number_input("Seu orçamento máximo (R$):", min_value=100.0, step=50.0)

with col2:
    origem = st.selectbox("Selecione a Origem:", ["Selecione"] + sorted(df["ORIGEM"].unique()))

with col3:
    destino = st.selectbox("Selecione o Destino:", ["Selecione"] + sorted(df["DESTINO"].unique()))

# Validação
if origem == "Selecione" or destino == "Selecione":
    st.info("🛫 Escolha a origem e destino para calcular.")
    st.stop()

# ===========================
# FILTRAR ROTA (2023–2025)
# ===========================
df_filtro = df[
    (df["ORIGEM"] == origem) &
    (df["DESTINO"] == destino) &
    (df["ANO"].isin([2023, 2024, 2025]))
]

if df_filtro.empty:
    st.warning("⚠️ Não há dados suficientes dessa rota para calcular.")
    st.stop()

# ===========================
# TEMPERATURA MÉDIA DA ROTA
# ===========================
temp_media = df_filtro["TEMP_MEDIA"].mean()

if temp_media < 20:
    clima = "❄️ Frio"
elif temp_media <= 25:
    clima = "🌤️ Ameno"
else:
    clima = "☀️ Quente"

# ===========================
# CÁLCULO DA MÉDIA HISTÓRICA POR MÊS
# ===========================
df_mes = (
    df_filtro.groupby("MES")["TARIFA"]
    .mean()
    .round(2)
    .reset_index()
)
df_mes["MES_NOME"] = df_mes["MES"].map(meses_nome)

# ===========================
# MESES QUE CABEM NO ORÇAMENTO
# ===========================
df_baratos = df_mes[df_mes["TARIFA"] <= orcamento].sort_values("TARIFA")

if not df_baratos.empty:
    melhor = df_baratos.iloc[0]

    msg_melhor = (
        f"🌟 O melhor mês dentro do orçamento é <b>{melhor['MES_NOME']}</b> — "
        f"R$ {melhor['TARIFA']:.2f}"
    )

    lista_meses = "<br>".join(
        [f"• <b>{row['MES_NOME']}</b> — R$ {row['TARIFA']:.2f}" for _, row in df_baratos.iterrows()]
    )

else:
    mais_proximo = df_mes.iloc[(df_mes["TARIFA"] - orcamento).abs().argmin()]

    msg_melhor = (
        "⚠️ Nenhum mês cabe no orçamento.<br>"
        f"👉 O mês mais próximo é <b>{mais_proximo['MES_NOME']}</b> — "
        f"R$ {mais_proximo['TARIFA']:.2f}"
    )
    lista_meses = "<i>Nenhum mês disponível com esse orçamento.</i>"

# ===========================
# CARD PRINCIPAL
# ===========================
colA, colB = st.columns(2)

with colA:
    st.markdown(f"<div class='card'><span class='metric-value'>{msg_melhor}</span></div>", unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class='card'>
        <b>🌡️ Temperatura média da rota:</b><br>
        <span class='metric-value'>{temp_media:.1f}°C — {clima}</span>
    </div>
    """, unsafe_allow_html=True)

# ===========================
# LISTA DE MESES POSSÍVEIS
# ===========================
st.markdown("### 🗓️ Meses que cabem no seu orçamento")
st.markdown(f"<div class='card'>{lista_meses}</div>", unsafe_allow_html=True)

# ===========================
# GRÁFICO
# ===========================
st.markdown("### 📈 Histórico de Tarifas Mensais (Média 2023–2025)")

fig = px.bar(
    df_mes.sort_values("MES"),
    x="MES_NOME",
    y="TARIFA",
    color="TARIFA",
    color_continuous_scale=["#62D99C", "#FF9F68"],
    text="TARIFA"
)

fig.update_traces(texttemplate="R$ %{y:.2f}", textposition="outside")
fig.update_layout(
    height=420,
    xaxis_title="Mês",
    yaxis_title="Tarifa Média (R$)",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# INSIGHTS
# ===========================
st.markdown("### 🧠 Insights")

mais_caro = df_mes.loc[df_mes["TARIFA"].idxmax()]
mais_barato = df_mes.loc[df_mes["TARIFA"].idxmin()]

insights = f"""
<div class='card'>
• O mês mais barato historicamente é <b>{mais_barato['MES_NOME']}</b> — R$ {mais_barato['TARIFA']:.2f}.<br>
• O mês mais caro é <b>{mais_caro['MES_NOME']}</b> — R$ {mais_caro['TARIFA']:.2f}.<br>
• Diferença entre eles: <b>R$ {(mais_caro['TARIFA'] - mais_barato['TARIFA']):.2f}</b>.<br>
• Temperatura média da rota: <b>{temp_media:.1f}°C</b> — {clima}.
</div>
"""

st.markdown(insights, unsafe_allow_html=True)
