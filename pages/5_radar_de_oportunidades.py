import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ============================================================
# CONFIGURAÇÃO
# ============================================================
st.set_page_config(
    page_title="Radar de Oportunidades — Bora Alí",
    layout="wide"
)

# ============================================================
# ESTILO (BORA ALÍ)
# ============================================================
st.markdown("""
<style>
:root {
    --laranja: #FF9F68;
    --roxo: #9B6DFF;
    --verde: #62D99C;
    --cinza: #F5F4FA;
}
body { background-color: var(--cinza); }
.big-title { font-size: 40px !important; font-weight: 900; color: var(--roxo); margin-bottom: -4px; }
.subtitle { font-size: 17px !important; color: #444; margin-bottom: 20px; }
.card { background: white; padding: 18px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 14px; }
.metric-value { font-size: 28px; font-weight: 900; color: var(--roxo); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO
# ============================================================
st.markdown("<div class='big-title'>🗺️ Radar de Oportunidades</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Descubra qual destino tem o melhor custo-benefício no período selecionado</div>", unsafe_allow_html=True)

# ============================================================
# CARREGAR DADOS
# ============================================================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

meses_nome = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}

# ============================================================
# FILTROS
# ============================================================
col1, col2 = st.columns(2)

with col1:
    origem = st.selectbox("Origem:", sorted(df["ORIGEM"].unique()))

with col2:
    periodo_tipo = st.selectbox(
        "Período:",
        ["Mês", "Trimestre", "Ano Completo"]
    )

# FILTRO DE PERÍODO  -----------------------------
if periodo_tipo == "Mês":
    periodo = st.selectbox("Selecione o mês:", list(meses_nome.keys()))
    df_filtro = df[df["MES"] == periodo]

elif periodo_tipo == "Trimestre":
    trimestre = st.selectbox(
        "Selecione o trimestre:",
        ["1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre"]
    )
    mapa_trim = {
        "1º Trimestre": [1,2,3],
        "2º Trimestre": [4,5,6],
        "3º Trimestre": [7,8,9],
        "4º Trimestre": [10,11,12]
    }
    df_filtro = df[df["MES"].isin(mapa_trim[trimestre])]

else:  # ano completo
    df_filtro = df.copy()

df_filtro = df_filtro[df_filtro["ORIGEM"] == origem]

if df_filtro.empty:
    st.warning("Nenhum dado disponível para essa combinação.")
    st.stop()

# ============================================================
# AGRUPAR POR DESTINO
# ============================================================
agg = (
    df_filtro.groupby("DESTINO", as_index=False)["TARIFA"]
    .mean()
    .round(0)
    .rename(columns={"TARIFA": "TARIFA_MEDIA"})
)

# ============================================================
# CLASSIFICAR EM CATEGORIAS (BARATO / MÉDIO / CARO)
# ============================================================
p20 = agg["TARIFA_MEDIA"].quantile(0.33)
p80 = agg["TARIFA_MEDIA"].quantile(0.66)

def classificar(valor):
    if valor <= p20:
        return "Barato"
    elif valor <= p80:
        return "Médio"
    else:
        return "Caro"

agg["CATEGORIA"] = agg["TARIFA_MEDIA"].apply(classificar)

cores = {
    "Barato": "#62D99C",
    "Médio": "#FF9F68",
    "Caro": "#9B6DFF"
}

# ============================================================
# GRÁFICO DE BOLHAS
# ============================================================
st.markdown("### 🌍 Mapa de Oportunidades por Destino")

fig = px.scatter(
    agg,
    x="DESTINO",
    y="TARIFA_MEDIA",
    size="TARIFA_MEDIA",
    color="CATEGORIA",
    color_discrete_map=cores,
    hover_data={"TARIFA_MEDIA": True, "CATEGORIA": True},
    size_max=60
)

fig.update_layout(
    xaxis_title="Destino",
    yaxis_title="Tarifa Média (R$)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================
# INSIGHTS AUTOMÁTICOS
# ============================================================
st.markdown("### 🧠 Insights do Período")

mais_barato = agg.loc[agg["TARIFA_MEDIA"].idxmin()]
mais_caro = agg.loc[agg["TARIFA_MEDIA"].idxmax()]

mediana = agg["TARIFA_MEDIA"].median()

insights = f"""
<div class='card'>
<b>• Melhor oportunidade:</b> {mais_barato['DESTINO']} — R$ {mais_barato['TARIFA_MEDIA']:.0f}<br><br>
<b>• Destino mais caro:</b> {mais_caro['DESTINO']} — R$ {mais_caro['TARIFA_MEDIA']:.0f}<br><br>
<b>• Mediana geral:</b> R$ {mediana:.0f}<br><br>
<b>• Oportunidade:</b> {mais_barato['DESTINO']} está {((mediana - mais_barato['TARIFA_MEDIA'])/mediana*100):.1f}% abaixo da mediana.
</div>
"""

st.markdown(insights, unsafe_allow_html=True)

