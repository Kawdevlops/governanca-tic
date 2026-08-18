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

# ==========================================================================
# LOGO (mesma lógica do OT)
# ==========================================================================

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

# ==========================================================================
# CSS — mesma paleta e fonte do painel de OT
# ==========================================================================

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
.painel-conformidade .kpi .cap{ font-size:12px; color:var(--gray); margin-top:6px; line-height:1.4; }
.painel-conformidade .kpi.total .num{ color:var(--blue); }
.painel-conformidade .kpi.concluida .num{ color:var(--green); }
.painel-conformidade .kpi.andamento .num{ color:var(--orange); }
.painel-conformidade .kpi.nao_iniciada .num{ color:#C63C3C; }

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

.painel-conformidade .orcamento-grid{
  display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:28px;
}
.painel-conformidade .orcamento-card{
  background:var(--beige); border-radius:12px; padding:20px 22px;
}
.painel-conformidade .orcamento-card .titulo{
  font-size:13px; color:var(--gray); font-weight:700; text-transform:uppercase; letter-spacing:.04em;
}
.painel-conformidade .orcamento-card .valor{
  font-size:26px; font-weight:900; color:var(--blue-dark); margin-top:6px;
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
.painel-conformidade .pill.concluida   { background:#EAF7EE; color:var(--green); }
.painel-conformidade .pill.andamento   { background:#FFF1E3; color:#B5601C; }
.painel-conformidade .pill.nao_iniciada{ background:#FBEAEA; color:#C63C3C; }

.painel-conformidade .footnote{
  font-size:12px; color:var(--gray); border-top:1px dashed var(--line);
  margin-top:32px; padding-top:16px;
}

@media (max-width:820px){
  .painel-conformidade .kpi-cards,
  .painel-conformidade .orcamento-grid{ grid-template-columns:1fr; }
}
"""

# ==========================================================================
# DADOS
# ==========================================================================

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
        pct = f"{(row['percentual_executado'] or 0) * 100:.0f}%"
        linhas.append(
            f'<tr>'
            f'<td>{row["area_responsavel"]}</td>'
            f'<td>{row["objeto"]}</td>'
            f'<td><span class="pill {classe}">{row["status"]}</span></td>'
            f'<td>{pct}</td>'
            f'</tr>'
        )
    return "\n".join(linhas)


# ==========================================================================
# STREAMLIT — barra lateral
# ==========================================================================

st.sidebar.header("Fonte de dados")
st.sidebar.caption(
    f"Banco: {os.environ.get('DB_STREAMLIT_DATABASE', '?')} · Tabela: ouro.fato_pdstic"
)
if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

df = carregar_dados()

if not LOGO_BASE64:
    st.sidebar.warning("Logo não encontrada.")
    st.sidebar.code(str(CAMINHO_LOGO))
else:
    st.sidebar.success("Logo encontrada.")

# ==========================================================================
# KPIs
# ==========================================================================

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

HTML_TEMPLATE = f"""
<div class="painel-conformidade">
<div class="deck">

  <section class="slide">
    <span class="tag">Governança de TI · SMSUB</span>
    <h1>PLANO DIRETOR DE <span>TIC — PDSTIC</span></h1>
    <p class="lead">
      Acompanhamento das linhas de ação do PDSTIC: percentual de execução,
      orçamento previsto e valores já liquidados por área responsável.
    </p>

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
      <tr><th>Área Responsável</th><th>Objeto</th><th>Status</th><th>% Executado</th></tr>
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
    "Dica: para o painel refletir novos dados, rode a DAG "
    "carga_indicadores_pdstic e clique em 'Atualizar dados'."
)