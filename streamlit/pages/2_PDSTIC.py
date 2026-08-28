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

# LOGO (mesma lógica do OT)
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
def carregar_dados() -> pd.DataFrame:
    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}"
        f"/{os.environ['DB_STREAMLIT_DATABASE']}"
    )
    df = pd.read_sql("SELECT * FROM ouro.fato_pdstic", engine)
    return df


def formatar_reais(valor) -> str:
    if valor is None or pd.isna(valor):
        return "R$ 0"
    return f"R$ {valor:,.0f}".replace(",", ".")


def montar_linhas_tabela(df: pd.DataFrame) -> str:
    classe_status = {
        "Concluída": "concluida",
        "Em Andamento": "andamento",
        "Não Iniciada": "nao_iniciada",
    }
    linhas = []
    for _, row in df.sort_values("percentual_executado").iterrows():
        classe = classe_status.get(row["status"], "andamento")
        linhas.append(
            f'<tr>'
            f'<td>{row["area_responsavel"]}</td>'
            f'<td>{row["objeto"]}</td>'
            f'<td><span class="pill {classe}">{row["status"]}</span></td>'
            f'</tr>'
        )
    return "\n".join(linhas)


def identificar_criticos(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"] == "Não Iniciada"]


def gerar_resumo_executivo(total, concluidas, andamento, nao_iniciadas,
                            pct_concluidas, valor_previsto, valor_realizado,
                            qtd_criticos) -> str:
    return (
        f"Das <strong>{total} linhas de ação</strong> do PDSTIC, "
        f"<strong>{concluidas} ({pct_concluidas:.0f}%)</strong> já foram concluídas, "
        f"<strong>{andamento}</strong> estão em andamento e "
        f"<strong>{nao_iniciadas}</strong> ainda não foram iniciadas. "
        f"O orçamento previsto totaliza <strong>{formatar_reais(valor_previsto)}</strong>, "
        f"dos quais <strong>{formatar_reais(valor_realizado)}</strong> já foram liquidados. "
        f"{f'<strong>{qtd_criticos} linha(s)</strong> exigem atenção prioritária por ainda não terem sido iniciadas.' if qtd_criticos else 'Nenhuma linha crítica no momento.'}"
    )


# STREAMLIT — barra lateral
if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df = carregar_dados()
df = df.dropna(subset=["objeto"])

if not LOGO_BASE64:
    st.sidebar.code(str(CAMINHO_LOGO))

# KPIs
total = len(df)
concluidas = int((df["status"] == "Concluída").sum())
andamento = int((df["status"] == "Em Andamento").sum())
nao_iniciadas = int((df["status"] == "Não Iniciada").sum())

pct_concluidas = (concluidas / total * 100) if total else 0
pct_andamento = (andamento / total * 100) if total else 0
pct_nao_iniciadas = (nao_iniciadas / total * 100) if total else 0

valor_previsto = df["valor_previsto"].sum()
valor_realizado = df["valor_realizado"].sum()
diferenca = df["diferenca"].sum()

df_criticos = identificar_criticos(df)
resumo_executivo = gerar_resumo_executivo(
    total, concluidas, andamento, nao_iniciadas,
    pct_concluidas, valor_previsto, valor_realizado, len(df_criticos)
)

HTML_TEMPLATE = f"""
<div class="painel-conformidade pagina-pdstic">
<div class="deck">

  <section class="slide">
    <span class="tag">Governança de TIC · SMSUB</span>
    <h1>PLANO DIRETOR DE <span>TIC PDSTIC</span></h1>
    <p class="lead">
       Acompanhamento das linhas de ação do PDSTIC: percentual de execução,
      orçamento previsto e valores já liquidados por área responsável.
    </p>
     <div class="resumo-executivo">{resumo_executivo}</div>
    <div class="kpi-cards">
      <div class="kpi total">
        <span class="ytag">Total de Linhas</span>
        <div class="num">{total}</div>
        <div class="cap">linhas de ação avaliadas</div>
      </div>
      <div class="kpi concluida">
        <span class="ytag">Concluídas</span>
        <div class="num">{concluidas}</div>
        <div class="cap">{pct_concluidas:.0f}% do total</div>
      </div>
      <div class="kpi andamento">
        <span class="ytag">Em Andamento</span>
        <div class="num">{andamento}</div>
        <div class="cap">{pct_andamento:.0f}% do total</div>
      </div>
      <div class="kpi nao_iniciada">
        <span class="ytag">Não Iniciadas</span>
        <div class="num">{nao_iniciadas}</div>
        <div class="cap">{pct_nao_iniciadas:.0f}% do total</div>
      </div>
    </div>

    <div class="barbox">
      <div class="bar-track">
        <div class="bar-fill" style="width:{pct_concluidas}%;background:var(--green);"></div>
        <div class="bar-fill" style="width:{pct_andamento}%;background:var(--orange);"></div>
        <div class="bar-fill" style="width:{pct_nao_iniciadas}%;background:#C63C3C;"></div>
      </div>
      <div class="legend">
        <span><span class="dot" style="background:var(--green);"></span>Concluídas</span>
        <span><span class="dot" style="background:var(--orange);"></span>Em Andamento</span>
        <span><span class="dot" style="background:#C63C3C;"></span>Não Iniciadas</span>
      </div>
    </div>

    <div class="orcamento-grid">
      <div class="orcamento-card">
        <div class="titulo">Valor Previsto no PDSTIC</div>
        <div class="valor">{formatar_reais(valor_previsto)}</div>
      </div>
      <div class="orcamento-card">
        <div class="titulo">Valor Liquidado</div>
        <div class="valor">{formatar_reais(valor_realizado)}</div>
      </div>
      <div class="orcamento-card">
        <div class="titulo">Diferença</div>
        <div class="valor">{formatar_reais(diferenca)}</div>
      </div>
    </div>

    <span class="tag" style="margin-top:32px;">Detalhamento</span>
    <h1 style="font-size:26px;">LINHAS DE AÇÃO <span>POR ÁREA</span></h1>
    <table class="seg">
      <tr><th> Setor </th><th> Item </th><th> Progresso </th></tr>
      {montar_linhas_tabela(df)}
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

components.html(pagina_html, height=1900, scrolling=True)

st.sidebar.markdown("---")
st.sidebar.caption(
    ""
)