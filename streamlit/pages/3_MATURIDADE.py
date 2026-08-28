import base64
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sqlalchemy import create_engine

sys.path.append(str(Path(__file__).resolve().parent.parent))
from style_lateral import aplicar_estilo_lateral

aplicar_estilo_lateral()

PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_LOGO = PASTA_PROJETO / "assets" / "marcadagua.png"


def logo_em_base64(caminho: Path) -> str:
    if not caminho.exists():
        return ""
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""


LOGO_BASE64 = logo_em_base64(CAMINHO_LOGO)


def carregar_css() -> str:
    caminho_css = PASTA_PROJETO / "assets" / "style.css"
    with open(caminho_css, "r", encoding="utf-8") as f:
        return f.read()


CSS_TEMPLATE = carregar_css()




# CSS Padrão =================================================================


# DADOS
@st.cache_data
def carregar_dados():
    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}"
        f"/{os.environ['DB_STREAMLIT_DATABASE']}"
    )
    org = pd.read_sql("SELECT * FROM ouro.fato_maturidade", engine)
    pilares = pd.read_sql(
        "SELECT * FROM ouro.fato_maturidade_pilares ORDER BY percentual_obtido ASC", engine
    )
    return org, pilares


def classificar_percentual(pct) -> str:
    if pct is None or pd.isna(pct):
        return "atencao"
    if pct >= 60:
        return "boa"
    if pct >= 30:
        return "atencao"
    return "critica"


def montar_linhas_pilares(df: pd.DataFrame) -> str:
    linhas = []
    for _, row in df.iterrows():
        classe = classificar_percentual(row["percentual_obtido"])
        linhas.append(
            f'<tr>'
            f'<td>{row["nome_pilar"]}</td>'
            f'<td>{int(row["pontos_obtidos"])} / {int(row["pontos_possiveis"])}</td>'
            f'</tr>'
        )
    return "\n".join(linhas)


def gerar_resumo_executivo(sigla, nivel, pontos_obtidos, pontos_possiveis,
                            percentual, pilar_forte, pct_forte,
                            pilar_fraco, pct_fraco) -> str:
    return (
        f"A <strong>{sigla}</strong> está classificada no nível "
        f"<strong>{nivel}</strong> da escala de maturidade do PETIC, com "
        f"<strong>{pontos_obtidos} de {pontos_possiveis} pontos</strong> "
        f"({percentual:.1f}%). O pilar com melhor desempenho é "
        f"<strong>{pilar_forte}</strong> ({pct_forte:.0f}%), enquanto "
        f"<strong>{pilar_fraco}</strong> ({pct_fraco:.0f}%) é o que mais "
        f"precisa de atenção."
    )


# STREAMLIT — barra lateral

if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df_org, df_pilares = carregar_dados()

if not LOGO_BASE64:
    st.sidebar.code(str(CAMINHO_LOGO))

if df_org.empty:
    st.warning("Nenhum dado de maturidade carregado ainda. Rode a DAG carga_indicadores_maturidade.")
    st.stop()

org = df_org.iloc[0]

pilar_mais_forte = df_pilares.iloc[-1]
pilar_mais_fraco = df_pilares.iloc[0]

resumo_executivo = gerar_resumo_executivo(
    org["sigla_orgao"], org["nivel_maturidade"],
    int(org["pontos_obtidos"]), int(org["pontos_possiveis"]), org["percentual_obtido"],
    pilar_mais_forte["nome_pilar"], pilar_mais_forte["percentual_obtido"],
    pilar_mais_fraco["nome_pilar"], pilar_mais_fraco["percentual_obtido"],
)

HTML_TEMPLATE = f"""
<div class="painel-conformidade pagina-maturidade">
<div class="deck">

  <section class="slide">
    <span class="tag">Governança de TIC · SMSUB</span>
    <h1>ESCALA DE <span>MATURIDADE PETIC</span></h1>
    <p class="lead">
      Posicionamento da SMSUB na escala de maturidade dos órgãos setoriais
      em TIC, por pilar avaliado.
    </p>
    <div class="resumo-executivo">{resumo_executivo}</div>

    <div class="kpi-cards">
      <div class="kpi total">
        <span class="ytag">Critérios Existentes</span>
        <div class="num">{int(org["pontos_possiveis"])}</div>
        <div class="cap">total avaliado na escala</div>
      </div>
      <div class="kpi obtidos">
        <span class="ytag">Critérios Cumpridos</span>
        <div class="num">{int(org["pontos_obtidos"])}</div>
        <div class="cap">{org["percentual_obtido"]:.1f}% do total</div>
      </div>
      <div class="kpi faltam">
        <span class="ytag">Critérios Faltantes</span>
        <div class="num">{int(org["pontos_faltantes"])}</div>
        <div class="cap">para completar a escala</div>
      </div>
      <div class="kpi nivel">
        <span class="ytag">Nível Atual</span>
        <div class="num texto">{org["nivel_maturidade"]}</div>
        <div class="cap">classificação SMSUB</div>
      </div>
    </div>

    <div class="barbox">
      <div class="bar-track">
        <div class="bar-fill" style="width:{org['percentual_obtido']}%;background:var(--blue);"></div>
      </div>
      <div class="legend">
        <span><span class="dot" style="background:var(--blue);"></span>Cumprido</span>
        <span><span class="dot" style="background:#EEF1F6;"></span>Restante</span>
      </div>
    </div>

    <span class="tag" style="margin-top:32px;">Detalhamento</span>
    <h1 style="font-size:26px;">DESEMPENHO <span>POR PILAR</span></h1>
    <table class="seg">
      <tr><th>Pilar</th><th>Pontos</th><th></th></tr>
      {montar_linhas_pilares(df_pilares)}
    </table>

    <div class="footnote">Governança DGTIC/SMSUB 2026</div>
  </section>

</div>
</div>
"""

css_final = CSS_TEMPLATE.replace("{{LOGO_BASE64}}", LOGO_BASE64)

pagina_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
body {{ margin:0; background:transparent; }}
{css_final}
</style>
</head>
<body>
{HTML_TEMPLATE}
</body>
</html>"""

components.html(pagina_html, height=1500, scrolling=True)

st.sidebar.markdown("---")
st.sidebar.caption(
    ""
)