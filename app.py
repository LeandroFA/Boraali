import streamlit as st

# =========================================
# CONFIG DO APLICATIVO (sempre no topo)
# =========================================
st.set_page_config(
    page_title="Bora Alí – Dashboard",
    page_icon="✌️",
    layout="wide"
)

# =========================================
# REMOVER MENU NATIVO
# =========================================
st.markdown("""
<style>
div[data-testid="stSidebarNav"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# =========================================
# MENU CUSTOMIZADO (APARECE EM TODAS AS PÁGINAS)
# =========================================
st.sidebar.markdown("""
<style>
.sidebar-title {
    font-size: 26px;
    font-weight: bold;
    color: #9B59B6; /* lavanda */
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-title'>✌️ Bora Alí – Navegação</div>", unsafe_allow_html=True)

st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/1_historico_por_rota.py", label="📍 Histórico por Rota")
st.sidebar.page_link("pages/2_ranking_por_estacao.py", label="🏆 Ranking por Estação")
st.sidebar.page_link("pages/3_previsao_2026.py", label="📈 Previsão 2026")
st.sidebar.page_link("pages/4_mes_ideal_orcamento.py", label="💸 Mês Ideal x Orçamento")
st.sidebar.page_link("pages/5_radar_de_oportunidades.py", label="🎯 Radar de Oportunidades")

# =========================================
# CSS - AQUARELA LAVANDA + LARANJA + LILÁS
# =========================================

st.markdown("""
<style>

body {
    background: linear-gradient(
      135deg,
      rgba(155,89,182,0.25),   /* Lavanda */
      rgba(255,138,71,0.25),   /* Laranja */
      rgba(193,141,240,0.25)   /* Lilás */
    );
    background-size: 400% 400%;
    animation: gradientFlow 18s ease infinite;
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Título Principal */
.big-title {
    font-size: 48px !important;
    font-weight: 800 !important;
    color: #9B59B6 !important; /* Lavanda */
}

/* Subtítulo */
.subtitle {
    font-size: 22px !important;
    color: #FF8A47 !important; /* Laranja */
}

/* Cards padrão */
.card {
    background: rgba(255,255,255,0.75);
    padding: 25px;
    margin-top: 20px;
    border-radius: 20px;
    border: 2px solid rgba(0,0,0,0.05);
    backdrop-filter: blur(6px);
}

/* Card Lavanda */
.card-lavanda {
    background: rgba(155,89,182,0.15);
    padding: 25px;
    margin-top: 20px;
    border-radius: 20px;
    border: 2px solid rgba(155,89,182,0.3);
}

/* Card Laranja */
.card-laranja {
    background: rgba(255,138,71,0.15);
    padding: 25px;
    margin-top: 20px;
    border-radius: 20px;
    border: 2px solid rgba(255,138,71,0.3);
}

</style>
""", unsafe_allow_html=True)

# =========================================
# CABEÇALHO
# =========================================
st.markdown("<h1 class='big-title'>✌️ Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dashboard nacional com previsões, históricos e insights do viajante brasileiro.</p>", unsafe_allow_html=True)

# =========================================
# TELA INICIAL COM CARDS LAVANDA E LARANJA
# =========================================
st.markdown("<div class='card-lavanda'>", unsafe_allow_html=True)
st.write("💜 **Bem-vindo ao novo painel Bora Alí!** Aqui você pode navegar entre previsões, históricos, rankings e análises completas.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card-laranja'>", unsafe_allow_html=True)
st.write("👈 Use o menu à esquerda para acessar cada módulo.")
st.markdown("</div>", unsafe_allow_html=True)
