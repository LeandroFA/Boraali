import streamlit as st

# ==========================
# CONFIG DO APLICATIVO
# ==========================
st.set_page_config(
    page_title="Bora Alí – Dashboard",
    page_icon="✌️",
    layout="wide"
)

# ==========================
# CSS - FUNDO AQUARELA + REMOVER MENU PADRÃO
# ==========================
st.markdown("""
<style>

div[data-testid="stSidebarNav"] {
    display: none !important;
}

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


# ==========================
# CABEÇALHO
# ==========================
st.markdown("<h1 class='big-title'>🎨 Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dashboard nacional com previsões, históricos e insights do viajante brasileiro.</p>", unsafe_allow_html=True)


# ==========================
# MENU LATERAL PROFISSIONAL (st.page_link)
# ==========================
st.sidebar.title("✌️ Navegação Bora Alí")

st.sidebar.page_link("app.py", label="🏠 Início")

st.sidebar.page_link("pages/historico_por_rota.py",
                     label="📍 Histórico por Rota")

st.sidebar.page_link("pages/ranking_por_estacao.py",
                     label="🏆 Ranking por Estação")

st.sidebar.page_link("pages/previsao_2026.py",
                     label="📈 Previsão 2026")

st.sidebar.page_link("pages/mes_ideal_orcamento.py",
                     label="💸 Mês Ideal x Orçamento")

st.sidebar.page_link("pages/radar_de_oportunidades.py",
                     label="🎯 Radar de Oportunidades")


# ==========================
# TELA INICIAL
# ==========================
st.write("👈 Use o menu à esquerda para navegar entre as páginas.")
