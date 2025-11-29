import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Bora Alí – Dashboard",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
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
.section-title {
    font-size: 32px !important;
    font-weight: bold;
    color: #3C1A66;
    margin-top: 20px;
    margin-bottom: 8px;
}
.big-title {
    font-size: 48px !important;
    font-weight: 800;
    color: #3C1A66;
}
.card {
    background: rgba(255,255,255,0.75);
    border-radius: 20px;
    padding: 25px;
    border: 2px solid rgba(0,0,0,0.05);
    backdrop-filter: blur(6px);
}
</style>
""", unsafe_allow_html=True)  
st.markdown("<h1 class='big-title'>🎨 Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.sidebar.title("🌈 Navegação Bora Alí")
opcao = st.sidebar.radio(
    "Escolha uma seção:",
    ["📍 Histórico por Rota", "🏆 Ranking por Estação", "📈 Previsão 2026", "💸 Mês Ideal x Orçamento", "🎯 Radar de Oportunidades"]
)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>📍 Histórico por Rota</p>", unsafe_allow_html=True)
mostrar_historico()
st.markdown("</div>", unsafe_allow_html=True)


