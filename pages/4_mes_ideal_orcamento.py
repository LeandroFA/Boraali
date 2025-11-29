# pages/4_mes_ideal_orcamento.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ===========================
# CONFIGURAÇÃO
# ===========================
st.set_page_config(
    page_title="Melhor Mês pelo Orçamento — Bora Alí",
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
st.markdown("<div class='subtitle'>Descubra em qual mês a tarifa cabe no seu bolso</div>", unsafe_allow_html=True)

# ===========================
# CARREGAR DADOS
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
# FILTROS
# ===========================
col1, col2, col3 = st.columns(3)

with col1:
    origem = st.selectbox("Origem:", sorted(df["ORIGEM"].unique()))

with col2:
    destino = st.selectbox("Destino:", sorted(df["DESTINO"].unique()))

with col3:
    orcamento = st.number_input("Seu orçamento máximo (R$):", min_value=100.0, step=50.0)

df_filtro = df[(df["ORIGEM"] == origem) & (df["DESTINO"] == destino) & (df["ANO"].isin([2023, 2024, 2025]))]

if df_filtro.empty:
    st.warning("⚠️ Não há dados suficientes dessa rota para calcular.")
    st.stop()

# ===========================
# CÁLCULO DA MÉDIA HISTÓRICA
# ===========================
df_mes = (
    df_filtro.groupby("MES")["TARIFA"]
    .mean()
    .round(2)
    .reset_index()
)
df_mes["MES_NOME"] = df_mes["MES"].map(meses_nome)

# ===========================
# MELHOR MÊS DENTRO DO ORÇAMENTO
# ===========================
df_baratos = df_mes[df_mes["TARIFA"] <= orcamento]

if not df_baratos.empty:
    melhor = df_baratos.sort_values("TARIFA").iloc[0]
    msg_melhor = f"🌟 O melhor mês dentro do orçamento é <b>{melhor['MES_NOME']}</b> — R$ {melhor['TARIFA']:.2f}"
else:
    # Nenhum mês cabe no orçamento → pega o mais próximo
    mais_proximo = df_mes.iloc[(df_mes["TARIFA"] - orcamento).abs().argmin()]
    msg_melhor = (
        "⚠️ Nenhum mês cabe no orçamento.<br>"
        f"👉 O mês mais próximo é <b>{mais_proximo['MES_NOME']}</b> — R$ {mais_proximo['TARIFA']:.2f}"
    )

# ===========================
# CARTÃO PRINCIPAL
# ===========================
st.markdown(f"<div class='card'><span class='metric-value'>{msg_melhor}</span></div>", unsafe_allow_html=True)

# ===========================
# GRÁFICO DAS TARIFAS MENSAIS
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
# INSIGHTS AUTOMÁTICOS
# ===========================
st.markdown("### 🧠 Insights")

mais_caro = df_mes.loc[df_mes["TARIFA"].idxmax()]
mais_barato = df_mes.loc[df_mes["TARIFA"].idxmin()]

insights = f"""
<div class='card'>
• O mês mais barato historicamente é <b>{mais_barato['MES_NOME']}</b> — R$ {mais_barato['TARIFA']:.2f}.<br>
• O mês mais caro é <b>{mais_caro['MES_NOME']}</b> — R$ {mais_caro['TARIFA']:.2f}.<br>
• A diferença entre eles é de <b>{(mais_caro['TARIFA'] - mais_barato['TARIFA']):.2f}</b> reais.<br>
• O orçamento informado permite identificar rapidamente o mês de melhor custo-benefício.
</div>
"""

st.markdown(insights, unsafe_allow_html=True)


