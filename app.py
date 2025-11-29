import streamlit as st
import pandas as pd
import numpy as np

# === CONFIGURAÇÃO DO APP ===
st.set_page_config(
    page_title="Bora Alí – Dashboard",
    page_icon="✈️",
    layout="wide"
)

# === CSS DO TEMA AQUARELA BORA ALÍ ===
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
.big-title {
    font-size: 48px !important;
    font-weight: 800;
    color: #3C1A66;
}
.subtitle {
    font-size: 20px !important;
    color: #3C1A66;
}
</style>
""", unsafe_allow_html=True)

# === CABEÇALHO DO DASHBOARD ===
st.markdown("<h1 class='big-title'>🎨 Bora Alí – Painel Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Escolha uma seção no menu lateral para visualizar os insights.</p>", unsafe_allow_html=True)

# === MENU LATERAL ===
st.sidebar.title("🌈 Navegação Bora Alí")
st.sidebar.write("Escolha uma página nas opções abaixo.")

st.write("👈 Use o menu à esquerda para navegar entre as páginas.")

# Nada mais é necessário aqui.
# As páginas dentro de /pages/ são carregadas automaticamente pelo Streamlit.
