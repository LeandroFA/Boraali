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
# REMOVER MENU NATIVO DO STREAMLIT
# =========================================
st.markdown("""
<style>
div[data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================================
# 🎨 CSS – TEMA PREMIUM LAVANDA + LARANJA
# =========================================
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif !important;
}

/* Fundo suave aquarela */
body {
    background: linear-gradient(
      135deg,
      rgba(155,89,182,0.16),
      rgba(255,138,71,0.16),
      rgba(193,141,240,0.16)
    );
    background-size: 400% 400%;
    animation: bgMove 26s ease infinite;
}

@keyframes bgMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Título principal */
.big-title {
    font-size: 52px !important;
    font-weight: 850 !important;
    color: #9B59B6 !important; /* Lavanda */
    letter-spacing: -1px;
    margin-bottom: -8px;
}

/* Subtítulo */
.subtitle {
    font-size: 22px !important;
    color: #FF8A47 !important; /* Laranja */
    font-weight: 500;
    margin-top: -10px;
}

/* Cards premium */
.card {
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    padding: 32px;
    border: 1.5px solid rgba(0,0,0,0.05);
    backdrop-filter: blur(6px);
    margin-top: 10px;
}

/* Card lavanda */
.card-lavanda {
    background: rgba(155,89,182,0.12);
    border: 1.5px solid rgba(155,89,182,0.3);
    border-radius: 22px;
    padding: 28px;
    margin-top: 10px;
}

/* Card laranja */
.card-laranja {
    background: rgba(255,138,71,0.12);
    border: 1.5px solid rgba(255,138,71,0.25);
    border-radius: 22px;
    padding: 28px;
    margin-top: 14px;
}

/* Remover espaço grande no topo */
section.main > div {
    padding-top: 0 !important;
}
.block-container {
    padding-top: 0 !important;
}

/* Sidebar elegante */
.sidebar-title {
    font-size: 26px;
    font-weight: 800;
    color: #9B59B6;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# MENU CUSTOMIZADO (APARECE EM TODAS AS PÁGINAS)
# =========================================
st.sidebar.markdown("<div class='sidebar-title'>✌️ Bora Alí</div>", unsafe_allow_html=True)

st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/1_historico_por_rota.py", label="📍 Histórico por Rota")
st.sidebar.page_link("pages/2_ranking_por_estacao.py", label="🏆 Ranking por Estação")
st.sidebar.page_link("pages/3_previsao_2026.py", label="📈 Previsão 2026")
st.sidebar.page_link("pages/4_mes_ideal_orcamento.py", label="💸 Mês Ideal x Orçamento")
st.sidebar.page_link("pages/5_radar_de_oportunidades.py", label="🎯 Radar de Oportunidades")

# =========================================
# CABEÇALHO PRINCIPAL
# =========================================
st.markdown("<h1 class='big-title'>Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Insights estratégicos para o viajante brasileiro.</p>", unsafe_allow_html=True)

# =========================================
# SEÇÕES DE BOAS-VINDAS
# =========================================
st.markdown("<div class='card-lavanda'>", unsafe_allow_html=True)
st.write("💜 **Bem-vindo ao novo painel Bora Alí!** Explore previsões, históricos, rankings e inteligência de viagem.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card-laranja'>", unsafe_allow_html=True)
st.write("👈 Use o menu à esquerda para navegar pelas análises.")
st.markdown("</div>", unsafe_allow_html=True)
