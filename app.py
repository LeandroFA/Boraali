import streamlit as st

# =========================================
# CONFIGURAÇÃO DO APP
# =========================================
st.set_page_config(
    page_title="Bora Alí – Dashboard",
    page_icon="✌️",
    layout="wide"
)

# =========================================
# CSS - FUNDO AQUARELA + REMOVER MENU NATIVO
# =========================================
st.markdown("""
<style>

/* Remove o menu interno de páginas do Streamlit */
div[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Fundo aquarela */
body {
    background: linear-gradient(
      135deg,
      rgba(255,138,71,0.25),
      rgba(126,200,126,0.25),
      rgba(193,141,240,0.25)
    );
    background-size: 400% 400%;
    animation: gradientFlow 18s ease infinite;
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Estilos do título e subtítulo */
.big-title {
    font-size: 48px !important;
    font-weight: 800 !important;
    color: #3C1A66 !important;
}

.subtitle {
    font-size: 20px !important;
    color: #3C1A66 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# CABEÇALHO PRINCIPAL
# =========================================
st.markdown("<h1 class='big-title'>🎨 Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dashboard nacional com previsões, históricos e insights do viajante brasileiro.</p>", unsafe_allow_html=True)



# =========================================
# MENU LATERAL PERSONALIZADO
# =========================================
st.sidebar.title("✌️ Navegação Bora Alí")

opcao = st.sidebar.radio(
    "Escolha uma seção:",
    [
        "📍 Histórico por Rota",
        "🏆 Ranking por Estação",
        "📈 Previsão 2026",
        "💸 Mês Ideal x Orçamento",
        "🎯 Radar de Oportunidades"
    ]
)

# Mapeamento de páginas /pages
mapa_paginas = {
    "📍 Histórico por Rota": "historico_por_rota",
    "🏆 Ranking por Estação": "ranking_por_estacao",
    "📈 Previsão 2026": "previsao_2026",
    "💸 Mês Ideal x Orçamento": "mes_ideal_orcamento",
    "🎯 Radar de Oportunidades": "radar_de_oportunidades"
}

# =========================================
# REDIRECIONAMENTO SEM PACOTES EXTERNOS
# =========================================
# Isso altera a URL e carrega a página correta — solução oficial do Streamlit
st.experimental_set_query_params(page=mapa_paginas[opcao])

st.write("👈 Use o menu à esquerda para navegar.")
