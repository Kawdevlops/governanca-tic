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

HTML_TEMPLATE = """
<div class="painel-conformidade pagina-ot">

<div class="deck">

<section class="slide">

  <div class="grid-2">

    <div>

      <span class="tag">
        Auditoria de Conformidade · TIC
      </span>

      <h1>
        <br>
        PAINEL DE<br>
        <span>CONFORMIDADE</span>
      </h1>

      <p class="lead">
        As Orientações Técnicas (OT) definem boas práticas de TI para os Órgãos
        Setoriais: OT007 trata de política e rotinas de backup, OT013 de segurança
        da informação e OT014 de infraestrutura e ambiente físico de TI. Cada
        recomendação foi verificada individualmente, com evidência documental
        sempre que disponível. Este painel serve de referência para priorizar
        o plano de ação e acompanhar a evolução da conformidade ao longo do tempo.
      </p>

    </div>

    <div>

      <div class="stat-row">

        <div class="stat-big">
          {{TOTAL}}
        </div>

        <div style="display:flex;flex-direction:column;">
          <div style="font-size:13px;font-weight:800;color:var(--gray);">
            RECOMENDAÇÕES<br>AVALIADAS
          </div>
        </div>

      </div>

      <div class="stat-branch">
        {{BRANCH_OT}}
      </div>

    </div>

  </div>

  <div class="resumo-executivo">{{RESUMO_EXECUTIVO}}</div>

  <div class="kpi-cards" style="grid-template-columns: repeat(4, 1fr);">

    <div class="kpi total">
      <span class="ytag">Cumprida Totalmente</span>
      <div class="num">{{TOTALMENTE}}</div>
      <div class="cap">{{PCT_TOTALMENTE}}% das recomendações</div>
    </div>

    <div class="kpi parcial">
      <span class="ytag">Cumprida Parcialmente</span>
      <div class="num">{{PARCIAL}}</div>
      <div class="cap">{{PCT_PARCIAL}}% — em andamento</div>
    </div>

    <div class="kpi nao">
      <span class="ytag">Não Cumprida</span>
      <div class="num">{{NAO}}</div>
      <div class="cap">{{PCT_NAO}}% — requer ação</div>
    </div>

    <div class="kpi evidencia" style="border-left: 4px solid var(--navy, #1E293B);">
      <span class="ytag">Com Evidência Documentada</span>
      <div class="num">{{EVIDENCIA_QTD}}</div>
      <div class="cap">{{PCT_EVIDENCIA}}% do total auditado</div>
    </div>

  </div>


  <div class="barbox">

    <div class="bar-track">

      <div class="bar-fill"
           style="width:{{PCT_TOTALMENTE}}%;background:var(--blue);">
      </div>

      <div class="bar-fill"
           style="width:{{PCT_PARCIAL}}%;background:var(--orange);">
      </div>

      <div class="bar-fill"
           style="width:{{PCT_NAO}}%;background:#C63C3C;">
      </div>

      <div class="bar-fill"
           style="width:{{PCT_INDEFINIDO}}%;background:#CBD1DC;">
      </div>

    </div>

    <div class="legend">

      <span>
        <span class="dot" style="background:var(--blue);"></span>
        Cumprida Totalmente
      </span>

      <span>
        <span class="dot" style="background:var(--orange);"></span>
        Cumprida Parcialmente
      </span>

      <span>
        <span class="dot" style="background:#C63C3C;"></span>
        Não Cumprida
      </span>

      <span>
        <span class="dot" style="background:#CBD1DC;"></span>
        Indefinida
      </span>

      <span style="margin-left:auto;font-weight:800;color:var(--navy);">
        Índice de cumprimento oficial: {{INDICE_CUMPRIMENTO}}%
      </span>

    </div>

  </div>


  <div class="section-divider">
    <br><br>
  </div>


  <span class="tag">
    Detalhamento
  </span>

  <h1 style="font-size:32px;">
    <br>
    CUMPRIMENTO POR
    <span>ORIENTAÇÃO TÉCNICA</span>
  </h1>

  <p class="lead" style="max-width:640px;">
    Comparativo de maturidade entre as Orientações Técnicas avaliadas.
  </p>

  <div class="ot-grid">
    {{CARDS_OT}}
  </div>


  <div class="section-divider">
    <br><br>
  </div>

  <div class="footnote">
    Governança DGTIC/SMSUB 2026
  </div>

</section>

</div>
</div>
"""


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{os.environ.get('DB_STREAMLIT_USER', 'postgres')}:{os.environ.get('DB_STREAMLIT_PASSWORD', '')}"
        f"@{os.environ.get('DB_STREAMLIT_HOST', 'localhost')}:{os.environ.get('DB_STREAMLIT_PORT', '5432')}"
        f"/{os.environ.get('DB_STREAMLIT_DATABASE', 'indicadores_tic')}"
    )

    df = pd.read_sql("SELECT * FROM ouro.fato_ot", engine)

    df = df.rename(
        columns={
            "ot": "OT",
            "ot_titulo": "OT_TITULO",
            "segmento": "SEGMENTO",
            "status": "STATUS",
            "pessoa_contato": "PESSOA_CONTATO",
            "tem_evidencia": "TEM_EVIDENCIA",
        }
    )

    df["SEGMENTO"] = df["SEGMENTO"].astype(str).str.strip()

    if "TEM_EVIDENCIA" not in df.columns:
        df["TEM_EVIDENCIA"] = False

    return df


def kpis_gerais(df: pd.DataFrame) -> dict:
    total = len(df)
    cont = df["STATUS"].value_counts()

    totalmente = int(cont.get("Cumprida Totalmente", 0))
    parcial = int(cont.get("Cumprida Parcialmente", 0))
    nao = int(cont.get("Não Cumprida", 0))
    indefinido = total - (totalmente + parcial + nao)

    evidencia_qtd = int(df["TEM_EVIDENCIA"].astype(bool).sum())

    if total > 0:
        pct_totalmente = totalmente / total * 100
        pct_parcial = parcial / total * 100
        pct_nao = nao / total * 100
        pct_indefinido = indefinido / total * 100
        pct_evidencia = evidencia_qtd / total * 100
        # CORREÇÃO DA FÓRMULA OFICIAL: peso 0,5 para cumprida parcialmente
        indice = ((totalmente + (0.5 * parcial)) / total) * 100
    else:
        pct_totalmente = 0
        pct_parcial = 0
        pct_nao = 0
        pct_indefinido = 0
        pct_evidencia = 0
        indice = 0

    return {
        "total": total,
        "totalmente": totalmente,
        "parcial": parcial,
        "nao": nao,
        "indefinido": indefinido,
        "evidencia_qtd": evidencia_qtd,
        "pct_totalmente": pct_totalmente,
        "pct_parcial": pct_parcial,
        "pct_nao": pct_nao,
        "pct_indefinido": pct_indefinido,
        "pct_evidencia": pct_evidencia,
        "indice_cumprimento": indice,
    }


def gerar_resumo_executivo(k: dict, tab_seg: pd.DataFrame) -> str:
    pior = tab_seg.iloc[0] if len(tab_seg) else None

    if pior is not None and pior["Não Cumprida"] > 0:
        alerta = (
            f'O segmento com mais pendências é <strong>{pior["SEGMENTO"]}</strong> '
            f'(<strong>{pior["OT"]}</strong>), com '
            f'<strong>{int(pior["Não Cumprida"])} recomendação(ões) não cumprida(s)</strong>.'
        )
    else:
        alerta = "Nenhum segmento crítico identificado no momento."

    return (
        f'Das <strong>{k["total"]} recomendações avaliadas</strong>, '
        f'<strong>{k["totalmente"]} ({k["pct_totalmente"]:.0f}%)</strong> foram cumpridas totalmente, '
        f'<strong>{k["parcial"]}</strong> parcialmente e '
        f'<strong>{k["nao"]}</strong> ainda não foram cumpridas. '
        f'O índice oficial de cumprimento ponderado está em '
        f'<strong>{k["indice_cumprimento"]:.1f}%</strong> (considerando peso 0,5 para itens parciais). '
        f'Há evidência documentada em <strong>{k["evidencia_qtd"]} ({k["pct_evidencia"]:.0f}%)</strong> dos casos. {alerta}'
    )


def resumo_por_ot(df: pd.DataFrame) -> pd.DataFrame:
    tab = (
        df.groupby(["OT", "OT_TITULO"])["STATUS"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(
            columns=[
                "Cumprida Totalmente",
                "Cumprida Parcialmente",
                "Não Cumprida",
            ],
            fill_value=0,
        )
        .reset_index()
    )

    tab["Total"] = tab[
        ["Cumprida Totalmente", "Cumprida Parcialmente", "Não Cumprida"]
    ].sum(axis=1)

    # Cálculo por OT também ajustado
    tab["% Cumprimento"] = (
        (tab["Cumprida Totalmente"] + (0.5 * tab["Cumprida Parcialmente"]))
        / tab["Total"]
        * 100
    )

    return tab.sort_values("OT").reset_index(drop=True)


def segmentos_criticos(
    df: pd.DataFrame, top_n: int = 7
) -> pd.DataFrame:
    tab = (
        df.groupby(["OT", "SEGMENTO"])["STATUS"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(
            columns=[
                "Cumprida Totalmente",
                "Cumprida Parcialmente",
                "Não Cumprida",
            ],
            fill_value=0,
        )
        .reset_index()
    )

    tab["Total"] = tab[
        ["Cumprida Totalmente", "Cumprida Parcialmente", "Não Cumprida"]
    ].sum(axis=1)

    tab["% Cumprimento"] = (
        (tab["Cumprida Totalmente"] + (0.5 * tab["Cumprida Parcialmente"]))
        / tab["Total"]
        * 100
    )

    tab = tab.sort_values(
        ["Não Cumprida", "% Cumprimento"], ascending=[False, True]
    )

    return tab.head(top_n).reset_index(drop=True)


OTS = {"OT007": "ot007", "OT013": "ot013", "OT014": "ot014"}


def montar_branch_ot(tab_ot: pd.DataFrame, indefinido: int) -> str:
    linhas = []
    for _, row in tab_ot.iterrows():
        nome_curto = str(row["OT_TITULO"]).split(" - ")[-1]
        linhas.append(
            f'<div class="b">'
            f'<span class="stat-arrow">↳</span>'
            f'<span class="n">{int(row["Total"])}</span>'
            f'<span class="l">{row["OT"]} — {nome_curto}</span>'
            f"</div>"
        )

    if indefinido:
        linhas.append(
            f'<div class="b">'
            f'<span class="stat-arrow">↳</span>'
            f'<span class="n">{indefinido}</span>'
            f'<span class="l">Sem status definido</span>'
            f"</div>"
        )

    return "\n".join(linhas)


def montar_cards_ot(tab_ot: pd.DataFrame) -> str:
    blocos = []
    for _, row in tab_ot.iterrows():
        nome_curto = str(row["OT_TITULO"]).split(" - ")[-1]
        blocos.append(
            f"""
        <div class="ot-card">
          <h3>{row['OT']} · {nome_curto}</h3>
          <div class="sub">
            {int(row['Total'])} recomendações avaliadas
          </div>
          <div class="pct">
            {row['% Cumprimento']:.1f}%
          </div>
          <div class="pctcap">
            índice ponderado (total + 0.5 × parcial)
          </div>
          <div class="mini-row">
            <span>Cumprida totalmente</span>
            <b>{int(row['Cumprida Totalmente'])}</b>
          </div>
          <div class="mini-row">
            <span>Cumprida parcialmente</span>
            <b>{int(row['Cumprida Parcialmente'])}</b>
          </div>
          <div class="mini-row">
            <span>Não cumprida</span>
            <b>{int(row['Não Cumprida'])}</b>
          </div>
        </div>
        """
        )
    return "\n".join(blocos)


def preencher_template(html_template: str, df: pd.DataFrame) -> str:
    k = kpis_gerais(df)
    tab_ot = resumo_por_ot(df)
    tab_seg = segmentos_criticos(df)

    substituicoes = {
        "{{TOTAL}}": str(k["total"]),
        "{{BRANCH_OT}}": montar_branch_ot(tab_ot, k["indefinido"]),
        "{{TOTALMENTE}}": str(k["totalmente"]),
        "{{PARCIAL}}": str(k["parcial"]),
        "{{NAO}}": str(k["nao"]),
        "{{EVIDENCIA_QTD}}": str(k["evidencia_qtd"]),
        "{{PCT_TOTALMENTE}}": f'{k["pct_totalmente"]:.1f}',
        "{{PCT_PARCIAL}}": f'{k["pct_parcial"]:.1f}',
        "{{PCT_NAO}}": f'{k["pct_nao"]:.1f}',
        "{{PCT_INDEFINIDO}}": f'{k["pct_indefinido"]:.1f}',
        "{{PCT_EVIDENCIA}}": f'{k["pct_evidencia"]:.1f}',
        "{{INDICE_CUMPRIMENTO}}": f'{k["indice_cumprimento"]:.1f}',
        "{{CARDS_OT}}": montar_cards_ot(tab_ot),
        "{{RESUMO_EXECUTIVO}}": gerar_resumo_executivo(k, tab_seg),
    }

    for chave, valor in substituicoes.items():
        html_template = html_template.replace(chave, valor)

    return html_template


if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df = carregar_dados()

if not LOGO_BASE64:
    st.sidebar.code(str(CAMINHO_LOGO))

conteudo = preencher_template(HTML_TEMPLATE, df)
css_final = CSS_TEMPLATE.replace("{{LOGO_BASE64}}", LOGO_BASE64)

pagina_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
body {{
  margin:0;
  background:transparent;
}}
{css_final}
</style>
</head>
<body>
{conteudo}
</body>
</html>
"""

components.html(pagina_html, height=2400, scrolling=True)