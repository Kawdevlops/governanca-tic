import base64
from pathlib import Path
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sqlalchemy import create_engine


st.set_page_config(page_title="Painel de conformidade TI", layout="wide")

# LOGO
# Aviso: a pasta streamlit/assets/ ainda não existe neste projeto.
# O código abaixo não quebra por causa disso (o try/except devolve ""
# se o arquivo não for encontrado) — só significa que a marca d'água
# fica invisível até você criar streamlit/assets/marcadagua.png e
# adicionar "COPY assets ./assets" no Dockerfile do Streamlit.

PASTA_PROJETO = Path(__file__).resolve().parent

CAMINHO_LOGO = (
    PASTA_PROJETO
    / "assets"
    / "marcadagua.png"
)


def logo_em_base64(caminho: Path) -> str:
    if not caminho.exists():
        return ""

    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""


LOGO_BASE64 = logo_em_base64(CAMINHO_LOGO)


# CSS

CSS_TEMPLATE = """
:root{
  --navy:#12203D;
  --blue:#2E5AAC;
  --blue-dark:#1F3E7A;
  --orange:#E8813A;
  --yellow:#F6D64A;
  --beige:#F2E9D8;
  --paper:#FFFFFF;
  --gray:#5B6373;
  --line:#E7E9EF;
}

html, body{
  width:100%;
  margin:0;
  padding:0;
}

body{
  background:transparent;
}

.painel-conformidade *{
  box-sizing:border-box;
}

.painel-conformidade{
  font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',
  Roboto,Oxygen,Ubuntu,Cantarell,'Open Sans','Helvetica Neue',sans-serif;
  color:var(--navy);
  width:100%;
  display:flex;
  justify-content:center;
}

.painel-conformidade .deck{
  width:100%;
  max-width:1450px;
  margin:0 auto;
  padding:16px 12px 48px;
}

.painel-conformidade .slide{
  background:var(--paper);
  border-radius:18px;
  padding:42px 46px;
  margin-bottom:32px;
  box-shadow:0 2px 18px rgba(18,32,61,0.08);
  position:relative;
  overflow:hidden;
}


/* 
   MARCA D'ÁGUA
 */

.painel-conformidade .slide::before{
  content:"";
  position:absolute;
  bottom: 20px;
  right: 20px;
  width: 150px;
  height: 150px;

  background-image:url("data:image/png;base64,{{LOGO_BASE64}}");
  background-repeat:no-repeat;
  background-position:center;
  background-size:contain;

  opacity:0.10;
  pointer-events:none;
  z-index:0;
}

/* 
   TEXTOS
*/

.painel-conformidade .tag{
  display:inline-block;
  font-size:16px;
  letter-spacing:.14em;
  font-weight:800;
  color:var(--blue-dark);
  background:#EAF0FB;
  border-radius:26px;
  padding:6px 15px;
  margin-bottom:14px;
  text-transform:uppercase;
}

.painel-conformidade h1{
  font-size:36px;
  line-height:1.08;
  font-weight:900;
  margin:0 0 4px;
  letter-spacing:-0.5px;
}

.painel-conformidade h1 span{
  color:var(--blue);
}

.painel-conformidade .lead{
  color:var(--gray);
  font-size:18px;
  line-height:1.8;
  max-width:480px;
  margin-top:16px;
}


/* 
   PRINCIPAL
*/

.painel-conformidade .grid-2{
  display:grid;
  grid-template-columns:1.10fr 1fr;
  gap:36px;
  align-items:start;
}

.painel-conformidade .stat-row{
  display:flex;
  align-items:center;
  gap:16px;
  margin-bottom:18px;
}

.painel-conformidade .stat-big{
  font-size:62px;
  font-weight:900;
  color:var(--navy);
  line-height:1.6;
}

.painel-conformidade .stat-arrow{
  color:var(--orange);
  font-size:22px;
  font-weight:900;
}

.painel-conformidade .stat-branch{
  display:flex;
  flex-direction:column;
  gap:10px;
  margin-left:6px;
}

.painel-conformidade .stat-branch .b{
  display:flex;
  align-items:baseline;
  gap:8px;
}

.painel-conformidade .stat-branch .n{
  font-size:30px;
  font-weight:900;
  color:var(--blue);
}

.painel-conformidade .stat-branch .l{
  font-size:18px;
  color:var(--gray);
  max-width:220px;
  line-height:1.6;
}


/* 
   KPIs
*/

.painel-conformidade .kpi-cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:18px;
  margin-top:32px;
}

.painel-conformidade .kpi{
  background:#F7F9FC;
  border:1px solid var(--line);
  border-radius:12px;
  padding:20px 18px;
  position:relative;
  overflow:hidden;
}

.painel-conformidade .kpi .ytag{
  display:inline-block;
  background:var(--yellow);
  color:var(--navy);
  font-weight:800;
  font-size:14px;
  letter-spacing:.06em;
  text-transform:uppercase;
  border-radius:6px;
  padding:3px 9px;
  margin-bottom:10px;
}

.painel-conformidade .kpi .num{
  font-size:32px;
  font-weight:900;
  line-height:1;
}

.painel-conformidade .kpi .cap{
  font-size:12px;
  color:var(--gray);
  margin-top:6px;
  line-height:1.4;
}

.painel-conformidade .kpi.total .num{
  color:var(--blue);
}

.painel-conformidade .kpi.parcial .num{
  color:var(--orange);
}

.painel-conformidade .kpi.nao .num{
  color:#C63C3C;
}


/* 
   BARRA
*/

.painel-conformidade .barbox{
  margin-top:10px;
}

.painel-conformidade .bar-track{
  background:#EEF1F6;
  border-radius:8px;
  height:10px;
  overflow:hidden;
  display:flex;
}

.painel-conformidade .bar-fill{
  height:100%;
}

.painel-conformidade .legend{
  display:flex;
  column-gap:40px;
  font-size:12px;
  color:var(--gray);
  margin-top:18px;
  flex-wrap:wrap;
}

.painel-conformidade .dot{
  display:inline-block;
  width:8px;
  height:8px;
  border-radius:50%;
  margin-right:5px;
}


/* 
   OT
*/

.painel-conformidade .ot-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:24px;
  margin-top:12px;
}

.painel-conformidade .ot-card{
  background:var(--beige);
  border-radius:14px;
  padding:30px 28px;
}

.painel-conformidade .ot-card h3{
  font-size:19px;
  margin:0 0 8px;
  font-weight:900;
}

.painel-conformidade .ot-card .sub{
  font-size:14px;
  color:var(--gray);
  margin-bottom:18px;
}

.painel-conformidade .ot-card .pct{
  font-size:48px;
  font-weight:900;
  color:var(--blue-dark);
}

.painel-conformidade .ot-card .pctcap{
  font-size:14px;
  color:var(--gray);
  margin-bottom:18px;
}

.painel-conformidade .mini-row{
  display:flex;
  justify-content:space-between;
  font-size:15px;
  padding:16px 0;
  border-top:1px solid rgba(18,32,61,0.08);
}

.painel-conformidade .mini-row b{
  color:var(--navy);
}


/*
   TABELA
*/

.painel-conformidade table.seg{
  width:100%;
  border-collapse:collapse;
  margin-top:18px;
  font-size:16px;
}

.painel-conformidade table.seg th{
  text-align:left;
  font-size:16px;
  letter-spacing:.06em;
  text-transform:uppercase;
  color:var(--gray);
  border-bottom:2px solid var(--navy);
  padding:12px 14px;
}

.painel-conformidade table.seg td{
  padding:16px;
  border-bottom:1px solid var(--line);
}

.painel-conformidade table.seg tr:hover td{
  background:#F7F9FC;
}


/*
   OTS
*/

.painel-conformidade .pill{
  display:inline-block;
  padding:3px 10px;
  border-radius:20px;
  font-size:11px;
  font-weight:800;
}

.painel-conformidade .pill.ot007{
  background:#E9F0FF;
  color:var(--blue-dark);
}

.painel-conformidade .pill.ot013{
  background:#FFF1E3;
  color:#B5601C;
}

.painel-conformidade .pill.ot014{
  background:#EAF7EE;
  color:#1D7A3C;
}


/* 
   RODAPÉ
 */

.painel-conformidade .footnote{
  font-size:12px;
  color:var(--gray);
  border-top:1px dashed var(--line);
  margin-top:32px;
  padding-top:16px;
}

.painel-conformidade .section-divider{
  border-top:1px solid var(--line);
  margin:8px 0 0;
}


/* 
   RESPONSIVO
 */

@media (max-width:820px){

  .painel-conformidade .grid-2,
  .painel-conformidade .ot-grid,
  .painel-conformidade .kpi-cards{
    grid-template-columns:1fr;
  }

  .painel-conformidade .slide{
    padding:28px 24px;
  }

  .painel-conformidade .slide::before{
    width:400px;
    height:400px;
  }
}
"""

# HTML

HTML_TEMPLATE = """
<div class="painel-conformidade">

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


  <div class="kpi-cards">

    <div class="kpi total">
      <span class="ytag">Cumprida Totalmente</span>
      <div class="num">{{TOTALMENTE}}</div>
      <div class="cap">{{PCT_TOTALMENTE}}% das recomendações auditadas</div>
    </div>

    <div class="kpi parcial">
      <span class="ytag">Cumprida Parcialmente</span>
      <div class="num">{{PARCIAL}}</div>
      <div class="cap">{{PCT_PARCIAL}}% — em andamento / ação incompleta</div>
    </div>

    <div class="kpi nao">
      <span class="ytag">Não Cumprida</span>
      <div class="num">{{NAO}}</div>
      <div class="cap">{{PCT_NAO}}% — requer plano de ação</div>
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
        Índice de cumprimento: {{INDICE_CUMPRIMENTO}}%
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


  <span class="tag">
    Prioridade de ação
  </span>

  <h1 style="font-size:32px;">
    <br>
    SEGMENTOS
    <span>MAIS CRÍTICOS</span>
  </h1>

  <p class="lead" style="max-width:640px;">
    Segmentos com maior número de recomendações não cumpridas,
    bons candidatos a plano de ação imediato.
  </p>

  <table class="seg">

    <tr>
      <th>OT</th>
      <th>Segmento</th>
      <th>Total</th>
      <th>Não cumprida</th>
      <th>% Cumprimento</th>
    </tr>

    {{LINHAS_SEGMENTOS}}

  </table>


  <div class="footnote">
    Governança DGTIC/SMSUB 2026
  </div>

</section>

</div>
</div>
"""

# DADOS
# Fonte única agora: Postgres (banco indicadores_smsub, tabela recomendacoes_ot).
# Nada de Excel/upload dentro do app — quem alimenta essa tabela é um script
# de carga separado (ver explicação fora do código).

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}"
        f"/{os.environ['DB_STREAMLIT_DATABASE']}"
    )

    df = pd.read_sql("SELECT * FROM ouro.fato_ot", engine)

    df = df.rename(columns={
        "ot": "OT",
        "ot_titulo": "OT_TITULO",
        "segmento": "SEGMENTO",
        "status": "STATUS",
    })

    df["SEGMENTO"] = df["SEGMENTO"].astype(str).str.strip()

    return df


def kpis_gerais(df: pd.DataFrame) -> dict:

    total = len(df)
    cont = df["STATUS"].value_counts()

    totalmente = int(
        cont.get("Cumprida Totalmente", 0)
    )

    parcial = int(
        cont.get("Cumprida Parcialmente", 0)
    )

    nao = int(
        cont.get("Não Cumprida", 0)
    )

    indefinido = total - (
        totalmente + parcial + nao
    )

    if total:
        pct_totalmente = totalmente / total * 100
        pct_parcial = parcial / total * 100
        pct_nao = nao / total * 100
        pct_indefinido = indefinido / total * 100
        indice = (totalmente + parcial) / total * 100
    else:
        pct_totalmente = 0
        pct_parcial = 0
        pct_nao = 0
        pct_indefinido = 0
        indice = 0

    return {
        "total": total,
        "totalmente": totalmente,
        "parcial": parcial,
        "nao": nao,
        "indefinido": indefinido,
        "pct_totalmente": pct_totalmente,
        "pct_parcial": pct_parcial,
        "pct_nao": pct_nao,
        "pct_indefinido": pct_indefinido,
        "indice_cumprimento": indice,
    }


def resumo_por_ot(df: pd.DataFrame) -> pd.DataFrame:

    tab = (
        df.groupby(["OT", "OT_TITULO"])["STATUS"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(
            columns=[
                "Cumprida Totalmente",
                "Cumprida Parcialmente",
                "Não Cumprida"
            ],
            fill_value=0
        )
        .reset_index()
    )

    tab["Total"] = tab[
        [
            "Cumprida Totalmente",
            "Cumprida Parcialmente",
            "Não Cumprida"
        ]
    ].sum(axis=1)

    tab["% Cumprimento"] = (
        (
            tab["Cumprida Totalmente"]
            + tab["Cumprida Parcialmente"]
        )
        / tab["Total"]
        * 100
    )

    return tab.sort_values("OT").reset_index(drop=True)


def segmentos_criticos(
    df: pd.DataFrame,
    top_n: int = 7
) -> pd.DataFrame:

    tab = (
        df.groupby(["OT", "SEGMENTO"])["STATUS"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(
            columns=[
                "Cumprida Totalmente",
                "Cumprida Parcialmente",
                "Não Cumprida"
            ],
            fill_value=0
        )
        .reset_index()
    )

    tab["Total"] = tab[
        [
            "Cumprida Totalmente",
            "Cumprida Parcialmente",
            "Não Cumprida"
        ]
    ].sum(axis=1)

    tab["% Cumprimento"] = (
        (
            tab["Cumprida Totalmente"]
            + tab["Cumprida Parcialmente"]
        )
        / tab["Total"]
        * 100
    )

    tab = tab.sort_values(
        ["Não Cumprida", "% Cumprimento"],
        ascending=[False, True]
    )

    return tab.head(top_n).reset_index(drop=True)

# HTML DINÂMICO

OTS = {
    "OT007": "ot007",
    "OT013": "ot013",
    "OT014": "ot014"
}


def montar_branch_ot(
    tab_ot: pd.DataFrame,
    indefinido: int
) -> str:

    linhas = []

    for _, row in tab_ot.iterrows():

        nome_curto = str(
            row["OT_TITULO"]
        ).split(" - ")[-1]

        linhas.append(
            f'<div class="b">'
            f'<span class="stat-arrow">↳</span>'
            f'<span class="n">{int(row["Total"])}</span>'
            f'<span class="l">{row["OT"]} — {nome_curto}</span>'
            f'</div>'
        )

    if indefinido:
        linhas.append(
            f'<div class="b">'
            f'<span class="stat-arrow">↳</span>'
            f'<span class="n">{indefinido}</span>'
            f'<span class="l">Sem status definido</span>'
            f'</div>'
        )

    return "\n".join(linhas)


def montar_cards_ot(tab_ot: pd.DataFrame) -> str:

    blocos = []

    for _, row in tab_ot.iterrows():

        nome_curto = str(
            row["OT_TITULO"]
        ).split(" - ")[-1]

        blocos.append(f"""
        <div class="ot-card">

          <h3>{row['OT']} · {nome_curto}</h3>

          <div class="sub">
            {int(row['Total'])} recomendações avaliadas
          </div>

          <div class="pct">
            {row['% Cumprimento']:.1f}%
          </div>

          <div class="pctcap">
            de cumprimento (total + parcial)
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
        """)

    return "\n".join(blocos)


def montar_linhas_segmentos(
    tab_seg: pd.DataFrame
) -> str:

    linhas = []

    for _, row in tab_seg.iterrows():

        classe = OTS.get(
            row["OT"],
            "ot007"
        )

        linhas.append(
            f'<tr>'
            f'<td><span class="pill {classe}">{row["OT"]}</span></td>'
            f'<td>{row["SEGMENTO"]}</td>'
            f'<td>{int(row["Total"])}</td>'
            f'<td>{int(row["Não Cumprida"])}</td>'
            f'<td>{row["% Cumprimento"]:.1f}%</td>'
            f'</tr>'
        )

    return "\n".join(linhas)


def preencher_template(
    html_template: str,
    df: pd.DataFrame
) -> str:

    k = kpis_gerais(df)
    tab_ot = resumo_por_ot(df)
    tab_seg = segmentos_criticos(df)

    substituicoes = {
        "{{TOTAL}}": str(k["total"]),
        "{{BRANCH_OT}}": montar_branch_ot(
            tab_ot,
            k["indefinido"]
        ),
        "{{TOTALMENTE}}": str(k["totalmente"]),
        "{{PARCIAL}}": str(k["parcial"]),
        "{{NAO}}": str(k["nao"]),
        "{{PCT_TOTALMENTE}}": f'{k["pct_totalmente"]:.1f}',
        "{{PCT_PARCIAL}}": f'{k["pct_parcial"]:.1f}',
        "{{PCT_NAO}}": f'{k["pct_nao"]:.1f}',
        "{{PCT_INDEFINIDO}}": f'{k["pct_indefinido"]:.1f}',
        "{{INDICE_CUMPRIMENTO}}": f'{k["indice_cumprimento"]:.1f}',
        "{{CARDS_OT}}": montar_cards_ot(tab_ot),
        "{{LINHAS_SEGMENTOS}}": montar_linhas_segmentos(tab_seg),
    }

    for chave, valor in substituicoes.items():
        html_template = html_template.replace(
            chave,
            valor
        )

    return html_template

# STREAMLIT

st.sidebar.header("Fonte de dados")

st.sidebar.caption(
    f"Banco: {os.environ.get('DB_STREAMLIT_DATABASE', '?')} "
    f"· Tabela: recomendacoes_ot"
)

if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df = carregar_dados()


# DIAGNÓSTICO DA LOGO

if not LOGO_BASE64:

    st.sidebar.warning(
        "Logo não encontrada."
    )

    st.sidebar.code(
        str(CAMINHO_LOGO)
    )

else:

    st.sidebar.success(
        "Logo encontrada."
    )


# HTML

conteudo = preencher_template(
    HTML_TEMPLATE,
    df
)


css_final = CSS_TEMPLATE.replace(
    "{{LOGO_BASE64}}",
    LOGO_BASE64
)


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


components.html(
    pagina_html,
    height=2400,
    scrolling=True
)


st.sidebar.markdown("---")

st.sidebar.caption(
    "Os dados vêm direto do banco Postgres (indicadores_smsub). "
    "Para atualizar, recarregue a tabela recomendacoes_ot e clique "
    "em 'Atualizar dados' na barra lateral."
)