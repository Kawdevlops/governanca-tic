# app.py
import streamlit as st

st.set_page_config(
    page_title="Painel de Indicadores TI",
    layout="wide",
)

# NAVEGAÇÃO

# Página inicial
home_page = st.Page(
    "pages/home.py",  
    title="Home",
    default=True
)

# Páginas secundárias
ot_page = st.Page(
    "pages/1_OT.py",
    title="OT - Orientações Técnicas",
)

# Cria a navegação
pg = st.navigation([home_page, ot_page])

# Executa a página selecionada
pg.run()