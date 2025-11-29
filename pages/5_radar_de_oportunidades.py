import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================
# CONFIG
# ==============================================
st.set_page_config(
    page_title="Radar de Oportunidades — Bora Alí",
    layout="wide"
)

# ==============================================
# ESTILO (cores Bora Alí)
# ==============================================
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
</style>
""", unsafe_allow_html=True)

# ==============================================
# TÍTULO
# ==============================================
st.markdown("<div class='big-title'>🗺️ Radar de Oportunidades</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Encontre os destinos mais vantajosos para viajar a partir da sua origem</div>", unsafe_allow_html=True)

# ==============================================
# CARREGAR DATA
# ==============================================
df = pd.read_csv("data/INMET_ANAC_EXTREMAMENTE_REDUZIDO.csv")
df["ANO"] = df["ANO"].astype(int)
df["MES"] = df["MES"].astype(int)

# ==============================================
# MÊS POR EXTENSO
# ==============================================
MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
MESES_INV = {v: k for k, v in MESES.items()}

# ==============================================
# COORDENADAS DAS CAPITAIS DO BRASIL
# ==============================================
CAPITAIS_COORDS = {
    "Rio Branco": {"lat": -9.97499, "lon": -67.8243},
    "Maceió": {"lat": -9.66599, "lon": -35.7350},
    "Macapá": {"lat": 0.03493, "lon": -51.0694},
    "Manaus": {"lat": -3.11866, "lon": -60.0212},
    "Salvador": {"lat": -12.9718, "lon": -38.5011},
    "Fortaleza": {"lat": -3.71722, "lon": -38.5434},
    "Brasília": {"lat": -15.7797, "lon": -47.9297},
    "Vitória": {"lat": -20.3155, "lon": -40.3128},
    "Goiânia": {"lat": -16.6864, "lon": -49.2643},
    "São Luís": {"lat": -2.53911, "lon": -44.2829},
    "Cuiabá": {"lat": -15.6010, "lon": -56.0974},
    "Campo Grande": {"lat": -20.4697, "lon": -54.6201},
    "Belo Horizonte": {"lat": -19.8157, "lon": -43.9542},
    "Belém": {"lat": -1.45502, "lon": -48.5024},
    "João Pessoa": {"lat": -7.11509, "lon": -34.8641},
    "Curitiba": {"lat": -25.4284, "lon": -49.2733},
    "Recife": {"lat": -8.04666, "lon": -34.8771},
    "Teresina": {"lat": -5.08921, "lon": -42.8016},
    "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
    "Natal": {"lat": -5.79448, "lon": -35.2110},
    "Porto Alegre": {"lat": -30.0277, "lon": -51.2287},
    "Porto Velho": {"lat": -8.76077, "lon": -63.8999},
    "Boa Vista": {"lat": 2.82384, "lon": -60.6753},
    "Florianópolis": {"lat": -27.5945, "lon": -48.5477},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Aracaju": {"lat": -10.9472, "lon": -37.0731},
    "Palmas": {"lat": -10.1675, "lon": -48.3277}
}

# ==============================================
# FILTROS
# ==============================================
col1, col2 = st.columns(2)

with col1:
    origem = st.selectbox("Origem:", sorted(df["ORIGEM"].unique()))

with col2:
    mes_nome = st.selectbox("Mês:", list(MESES.values()))
    mes = MESES_INV[mes_nome]

df_filtro = df[(df["ORIGEM"] == origem) & (df["MES"] == mes)]

# ==============================================
# AGRUPAMENTO POR DESTINO
# ==============================================
agg = (
    df_filtro.groupby("DESTINO", as_index=False)["TARIFA"]
    .mean()
    .round(0)
    .rename(columns={"TARIFA": "TARIFA_MEDIA"})
)

# adicionar coordenadas
agg["lat"] = agg["DESTINO"].apply(lambda x: CAPITAIS_COORDS[x]["lat"])
agg["lon"] = agg["DESTINO"].apply(lambda x: CAPITAIS_COORDS[x]["lon"])

# ==============================================
# CLASSIFICAÇÃO: BARATO / MÉDIO / CARO
# ==============================================
p20 = agg["TARIFA_MEDIA"].quantile(0.33)
p80 = agg["TARIFA_MEDIA"].quantile(0.66)

def categoria(v):
    if v <= p20:
        return "Barato"
    elif v <= p80:
        return "Médio"
    return "Caro"

agg["CATEGORIA"] = agg["TARIFA_MEDIA"].apply(categoria)

cores = {
    "Barato": "#62D99C",
    "Médio": "#FF9F68",
    "Caro": "#9B6DFF"
}

# ==============================================
# MAPA FINAL
# ==============================================
st.markdown("### 🗺️ Mapa de Oportunidades")

fig = px.scatter_mapbox(
    agg,
    lat="lat",
    lon="lon",
    size="TARIFA_MEDIA",
    color="CATEGORIA",
    hover_name="DESTINO",
    hover_data={"TARIFA_MEDIA": True},
    color_discrete_map=cores,
    zoom=3.4,
    height=650
)

fig.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig, use_container_width=True)

# ==============================================
# INSIGHTS AUTOMÁTICOS
# ==============================================
melhor = agg.loc[agg["TARIFA_MEDIA"].idxmin()]
pior = agg.loc[agg["TARIFA_MEDIA"].idxmax()]

st.markdown("### 🧠 Insights")
st.markdown(f"""
<div class='card'>
<b>• Destino mais barato:</b> {melhor['DESTINO']} — R$ {melhor['TARIFA_MEDIA']:.0f}<br><br>
<b>• Destino mais caro:</b> {pior['DESTINO']} — R$ {pior['TARIFA_MEDIA']:.0f}<br><br>
<b>• Diferença entre eles:</b> R$ {pior['TARIFA_MEDIA'] - melhor['TARIFA_MEDIA']:.0f}<br>
</div>
""", unsafe_allow_html=True)
