# app.py
import streamlit as st

st.set_page_config(
    page_title="Painel de Indicadores TI",
    layout="wide",
)

# NAVEGAÇÃO
# url_path definido explicitamente para os links do home.py baterem certo

home_page = st.Page(
    "pages/0_HOME.py",
    title="Home",
    default=True,
    url_path="",
)

ot_page = st.Page(
    "pages/1_OT.py",
    title="OT - Orientações Técnicas",
    url_path="ot",
)

pdstic_page = st.Page(
    "pages/2_PDSTIC.py",
    title="PDSTIC",
    url_path="pdstic",
)

maturidade_page = st.Page(
    "pages/3_MATURIDADE.py",
    title="Escala de Maturidade",
    url_path="maturidade",
)

pg = st.navigation([home_page, ot_page, pdstic_page, maturidade_page])
pg.run()