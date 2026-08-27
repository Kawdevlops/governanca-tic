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


# CSS — mesma paleta e fonte dos outros painéis
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
  --green:#1D7A3C;
}

html, body{ width:100%; margin:0; padding:0; }
body{ background:transparent; }

.painel-conformidade *{ box-sizing:border-box; }

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

.painel-conformidade .slide::before{
  content:"";
  position:absolute;
  bottom:20px;
  right:20px;
  width:150px;
  height:150px;
  background-image:url("data:image/png;base64,{{LOGO_BASE64}}");
  background-repeat:no-repeat;
  background-position:center;
  background-size:contain;
  opacity:0.10;
  pointer-events:none;
  z-index:0;
}

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
  line-height:1.15;
  font-weight:900;
  margin:0 0 4px;
  letter-spacing:-0.5px;
}
.painel-conformidade h1 span{ color:var(--blue); }

.painel-conformidade .lead{
  color:var(--gray);
  font-size:18px;
  line-height:1.8;
  max-width:640px;
  margin-top:16px;
}

.painel-conformidade .kpi-cards{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:18px;
  margin-top:32px;
}
.painel-conformidade .kpi{
  background:#F7F9FC;
  border:1px solid var(--line);
  border-radius:12px;
  padding:22px 20px;
}
.painel-conformidade .kpi .ytag{
  display:inline-block;
  background:var(--yellow);
  color:var(--navy);
  font-weight:800;
  font-size:12px;
  letter-spacing:.06em;
  text-transform:uppercase;
  border-radius:6px;
  padding:3px 9px;
  margin-bottom:10px;
}
.painel-conformidade .kpi .num{ font-size:32px; font-weight:900; line-height:1; }
.painel-conformidade .kpi .num.texto{ font-size:22px; }
.painel-conformidade .kpi .cap{ font-size:12px; color:var(--gray); margin-top:6px; line-height:1.4; }
.painel-conformidade .kpi.total .num{ color:var(--blue); }
.painel-conformidade .kpi.obtidos .num{ color:var(--green); }
.painel-conformidade .kpi.faltam .num{ color:var(--orange); }
.painel-conformidade .kpi.nivel .num{ color:var(--blue-dark); }

.painel-conformidade .barbox{ margin-top:28px; }
.painel-conformidade .bar-track{
  background:#EEF1F6; border-radius:8px; height:12px; overflow:hidden; display:flex;
}
.painel-conformidade .bar-fill{ height:100%; }
.painel-conformidade .legend{
  display:flex; gap:18px; font-size:13px; color:var(--gray); margin-top:12px; flex-wrap:wrap;
}
.painel-conformidade .dot{
  display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:6px;
}

.painel-conformidade table.seg{
  width:100%; border-collapse:collapse; margin-top:18px; font-size:14px;
}
.painel-conformidade table.seg th{
  text-align:left; font-size:11px; letter-spacing:.06em; text-transform:uppercase;
  color:var(--gray); border-bottom:2px solid var(--navy); padding:10px;
}
.painel-conformidade table.seg td{ padding:12px 10px; border-bottom:1px solid var(--line); }
.painel-conformidade table.seg tr:hover td{ background:#F7F9FC; }

.painel-conformidade .pill{
  display:inline-block; padding:3px 12px; border-radius:20px; font-size:11px; font-weight:800;
}
.painel-conformidade .pill.boa     { background:#EAF7EE; color:var(--green); }
.painel-conformidade .pill.atencao { background:#FFF1E3; color:#B5601C; }
.painel-conformidade .pill.critica { background:#FBEAEA; color:#C63C3C; }

.painel-conformidade .footnote{
  font-size:12px; color:var(--gray); border-top:1px dashed var(--line);
  margin-top:32px; padding-top:16px;
}

.painel-conformidade .resumo-executivo{
  background:#F7F9FC;
  border-left:4px solid var(--blue);
  border-radius:8px;
  padding:18px 22px;
  margin-top:24px;
  font-size:15px;
  line-height:1.7;
  color:var(--navy);
}
.painel-conformidade .resumo-executivo strong{ color:var(--blue-dark); }

@media (max-width:820px){
  .painel-conformidade .kpi-cards{ grid-template-columns:1fr; }
}
"""


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
            # f'<td><span class="pill {classe}">{row["percentual_obtido"]:.0f}%</span></td>'
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
st.sidebar.header("Fonte de dados")
st.sidebar.caption(
    f"Banco: {os.environ.get('DB_STREAMLIT_DATABASE', '?')} · "
    f"Tabelas: ouro.fato_maturidade / ouro.fato_maturidade_pilares"
)
if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df_org, df_pilares = carregar_dados()

if not LOGO_BASE64:
    st.sidebar.warning("Logo não encontrada.")
    st.sidebar.code(str(CAMINHO_LOGO))
else:
    st.sidebar.success("Logo encontrada.")

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
<div class="painel-conformidade">
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
    "Dica: para o painel refletir novos dados, rode a DAG "
    "carga_indicadores_maturidade e clique em 'Atualizar dados'."
)