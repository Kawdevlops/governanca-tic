import base64
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sqlalchemy import create_engine

# Configuração de caminhos e estilo lateral
sys.path.append(str(Path(__file__).resolve().parent.parent))
from style_lateral import aplicar_estilo_lateral

aplicar_estilo_lateral()

# Definindo caminhos de assets
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

# CSS EMBARCADO (CSS INTERNO NO PRÓPRIO ARQUIVO) ==============================
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
  --alert:#C63C3C;
}

html, body{
  width:100%;
  margin:0;
  padding:0;
}

body{
  background:transparent;
}

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

/* MARCA D'ÁGUA */
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

/* TEXTOS */
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
  max-width:680px;
  margin-top:16px;
}

/* RESUMO EXECUTIVO */
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

/* KPIs */
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
  padding:20px 20px;
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

.painel-conformidade .kpi .num{ font-size:32px; font-weight:900; line-height:1; }
.painel-conformidade .kpi .cap{ font-size:12px; color:var(--gray); margin-top:6px; line-height:1.4; }
.painel-conformidade .kpi.total .num{ color:var(--blue); }
.painel-conformidade .kpi.concluida .num{ color:var(--green); }
.painel-conformidade .kpi.andamento .num{ color:var(--orange); }
.painel-conformidade .kpi.nao_iniciada .num{ color:var(--alert); }

/* BARRA DE PROGRESSO */
.painel-conformidade .barbox{ margin-top:10px; }
.painel-conformidade .bar-track{
  background:#EEF1F6; 
  border-radius:8px; 
  height:10px; 
  overflow:hidden; 
  display:flex;
}
.painel-conformidade .bar-fill{ height:100%; }
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

/* ORÇAMENTO GRID */
.painel-conformidade .orcamento-grid{
  display:grid; 
  grid-template-columns:repeat(3,1fr); 
  gap:18px; 
  margin-top:28px;
}

.painel-conformidade .orcamento-card{
  background:var(--beige); 
  border-radius:12px; 
  padding:20px 22px;
}

.painel-conformidade .orcamento-card .titulo{
  font-size:13px; color:var(--gray); 
  font-weight:700; 
  text-transform:uppercase; 
  letter-spacing:.04em;
}

.painel-conformidade .orcamento-card .valor{
  font-size:26px; 
  font-weight:900; 
  color:var(--blue-dark); 
  margin-top:6px;
}

/* LISTAS DE AÇÃO E DOTAÇÃO (CARDS EXPANSÍVEIS) */
.painel-conformidade .acao-lista{
  margin-top:20px;
  display:flex;
  flex-direction:column;
  gap:12px;
}

.painel-conformidade .acao-card{
  background:#F7F9FC;
  border:1px solid var(--line);
  border-radius:10px;
  margin-bottom:6px;
  overflow:hidden;
  transition:all 0.2s ease;
}

.painel-conformidade .acao-card:hover{
  border-color:var(--blue);
  box-shadow:0 2px 10px rgba(18,32,61,0.06);
}

.painel-conformidade .acao-card summary{
  display:flex;
  align-items:center;
  gap:16px;
  padding:14px 20px;
  cursor:pointer;
  list-style:none;
}

.painel-conformidade .acao-card summary::-webkit-details-marker{
  display:none;
}

/* PILLS / STATUS */
.painel-conformidade .pill{
  display:inline-block; 
  padding:4px 12px; 
  border-radius:20px; 
  font-size:11px; 
  font-weight:800;
  white-space:nowrap;
  min-width:105px;
  text-align:center;
}

.painel-conformidade .pill.concluida{ background:#EAF7EE; color:var(--green); }
.painel-conformidade .pill.andamento{ background:#FFF1E3; color:#B5601C; }
.painel-conformidade .pill.nao_iniciada{ background:#FBEAEA; color:var(--alert); }
.painel-conformidade .pill.descontinuada{ background:#EEF1F6; color:var(--gray); }

.painel-conformidade .acao-titulo{
  flex:1;
  font-size:15px;
  font-weight:700;
  color:var(--navy);
}

.painel-conformidade .acao-area{
  font-size:13px;
  color:var(--gray);
  font-weight:600;
}

.painel-conformidade .acao-pct{
  font-weight:900;
  font-size:15px;
  color:var(--blue-dark);
  margin-left:auto;
}

.painel-conformidade .acao-detalhe{
  padding:18px 20px;
  border-top:1px solid var(--line);
  background:var(--paper);
  font-size:14px;
  line-height:1.7;
}

.painel-conformidade .acao-detalhe p{
  margin:6px 0;
  color:var(--navy);
}

/* RODAPÉ */
.painel-conformidade .footnote{
  font-size:12px;
  color:var(--gray);
  border-top:1px dashed var(--line);
  margin-top:32px;
  padding-top:16px;
}

@media (max-width:820px){
  .painel-conformidade .kpi-cards,
  .painel-conformidade .orcamento-grid{
    grid-template-columns:1fr;
  }
  .painel-conformidade .slide{
    padding:28px 24px;
  }
}
"""


# CARREGAMENTO DE DADOS
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


def montar_cards_acoes(df: pd.DataFrame) -> str:
    classe_status = {
        "Concluída": "concluida",
        "Em Andamento": "andamento",
        "Não Iniciada": "nao_iniciada",
        "Descontinuada": "descontinuada",
    }
    cards = []
    for _, row in df.sort_values("percentual_executado").iterrows():
        classe = classe_status.get(row["status"], "andamento")
        titulo = row["objeto"] if pd.notna(row["objeto"]) else row["linha_acao"]

        percentual = row["percentual_executado"]
        percentual_txt = (
            f"{percentual * 100:.0f}%" if pd.notna(percentual) else "—"
        )

        prazo = row.get("prazo_contratacao")
        prazo_txt = (
            prazo.strftime("%d/%m/%Y") if pd.notna(prazo) else "Não informado"
        )

        publico_alvo = row.get("publico_alvo") or "—"
        numero_sei = row.get("numero_sei") or "Não informado"
        dotacao = row.get("dotacao_orcamentaria") or "Não informada"
        dotacao_contratacao = (
            row.get("dotacao_contratacao") or "Não informada"
        )
        projeto_atividade = row.get("projeto_atividade") or "Não informado"

        cards.append(f"""
        <details class="acao-card">
          <summary>
            <span class="pill {classe}">{row['status']}</span>
            <span class="acao-titulo">{titulo}</span>
            <span class="acao-area">{row['area_responsavel']}</span>
            <span class="acao-pct">{percentual_txt}</span>
          </summary>
          <div class="acao-detalhe">
            <p><strong>Linha de ação:</strong> {row['linha_acao']}</p>
            <p><strong>Público alvo:</strong> {publico_alvo}</p>
            <p><strong>Prazo da contratação:</strong> {prazo_txt}</p>
            <p><strong>Número do SEI:</strong> {numero_sei}</p>
            <p><strong>Dotação Orçamentária:</strong> {dotacao}</p>
            <p><strong>Dotação da Contratação:</strong> {dotacao_contratacao}</p>
            <p><strong>Projeto/Atividade:</strong> {projeto_atividade}</p>
            <p><strong>Valor Previsto:</strong> {formatar_reais(row['valor_previsto'])}</p>
            <p><strong>Valor Liquidado:</strong> {formatar_reais(row['valor_realizado'])}</p>
            <p><strong>Previsto no GC:</strong> {formatar_reais(row.get('orcamento_previsto_gc'))}</p>
          </div>
        </details>
        """)
    return "\n".join(cards)


def resumo_dotacao_orcamentaria(df: pd.DataFrame) -> pd.DataFrame:
    df_valido = df.dropna(subset=["dotacao_orcamentaria"])
    df_valido = df_valido[~df_valido["dotacao_orcamentaria"].isin(["NA", ""])]
    df_valido = df_valido[df_valido["valor_realizado"].fillna(0) > 0]
    return df_valido


def montar_cards_dotacao(df_valido: pd.DataFrame) -> str:
    totais = (
        df_valido.groupby("dotacao_orcamentaria")["valor_realizado"]
        .sum()
        .sort_values(ascending=False)
    )

    cards = []
    for dotacao, valor_total in totais.items():
        linhas_do_grupo = df_valido[
            df_valido["dotacao_orcamentaria"] == dotacao
        ]

        itens_html = []
        for _, row in linhas_do_grupo.iterrows():
            texto = (
                row["objeto"] if pd.notna(row["objeto"]) else row["linha_acao"]
            )
            texto = str(texto).strip().capitalize()
            itens_html.append(
                f'<p>• <strong>{texto}</strong> — {formatar_reais(row["valor_realizado"])}</p>'
            )

        cards.append(f"""
        <details class="acao-card">
          <summary>
            <span class="acao-titulo">{dotacao}</span>
            <span class="acao-pct">{formatar_reais(valor_total)}</span>
          </summary>
          <div class="acao-detalhe">
            {"".join(itens_html)}
          </div>
        </details>
        """)
    return "\n".join(cards)


def identificar_criticos(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"] == "Não Iniciada"]


def gerar_resumo_executivo(
    total,
    concluidas,
    andamento,
    nao_iniciadas,
    pct_concluidas,
    valor_previsto,
    valor_realizado,
    qtd_criticos,
) -> str:
    return (
        f"Das <strong>{total} linhas de ação</strong> do PDSTIC, "
        f"<strong>{concluidas} ({pct_concluidas:.0f}%)</strong> já foram concluídas, "
        f"<strong>{andamento}</strong> estão em andamento e "
        f"<strong>{nao_iniciadas}</strong> ainda não foram iniciadas. "
        f"O orçamento previsto totaliza <strong>{formatar_reais(valor_previsto)}</strong>, "
        f"dos quais <strong>{formatar_reais(valor_realizado)}</strong> já foram liquidados. "
        f"{f'<strong>{qtd_criticos} linha(s)</strong> exigem atenção prioritária por ainda não terem sido iniciadas.' if qtd_criticos else 'Nenhuma linha crítica no momento.'}"
    )


# BARRA LATERAL

df = carregar_dados()
df = df.dropna(subset=["objeto"])

df_dotacao = resumo_dotacao_orcamentaria(df)
total_dotacao = (
    df_dotacao["valor_realizado"].sum() if not df_dotacao.empty else 0
)

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
    total,
    concluidas,
    andamento,
    nao_iniciadas,
    pct_concluidas,
    valor_previsto,
    valor_realizado,
    len(df_criticos),
)

HTML_TEMPLATE = f"""
<div class="painel-conformidade">
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
        <div class="bar-fill" style="width:{pct_nao_iniciadas}%;background:var(--alert);"></div>
      </div>
      <div class="legend">
        <span><span class="dot" style="background:var(--green);"></span>Concluídas</span>
        <span><span class="dot" style="background:var(--orange);"></span>Em Andamento</span>
        <span><span class="dot" style="background:var(--alert);"></span>Não Iniciadas</span>
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

    <!-- SEÇÃO 1: LIQUIDADO POR DOTAÇÃO ORÇAMENTÁRIA -->
    <span class="tag" style="margin-top:36px;">Execução Orçamentária</span>
    <h1 style="font-size:26px;">LIQUIDADO POR <span>DOTAÇÃO ORÇAMENTÁRIA</span></h1>
    <p class="lead">
      Clique sobre cada dotação orçamentária para expandir e consultar os objetos e valores liquidados.
    </p>
    <div class="orcamento-grid" style="grid-template-columns:1fr; margin-bottom:16px;">
      <div class="orcamento-card">
        <div class="titulo">Total Liquidado em Dotações Mapeadas</div>
        <div class="valor">{formatar_reais(total_dotacao)}</div>
      </div>
    </div>
    <div class="acao-lista">
      {montar_cards_dotacao(df_dotacao)}
    </div>

    <!-- SEÇÃO 2: LINHAS DE AÇÃO DETALHADAS COM DOTAÇÃO INTERNA -->
    <span class="tag" style="margin-top:42px;">Detalhamento</span>
    <h1 style="font-size:26px;">LINHAS DE AÇÃO <span>POR ÁREA</span></h1>
    <p class="lead">
      Clique nas linhas abaixo para visualizar a dotação orçamentária, dotação de contratação, prazos e número SEI.
    </p>
    <div class="acao-lista">
      {montar_cards_acoes(df)}
    </div>

    <div class="footnote">Governança DGTIC/SMSUB 2026</div>
  </section>

</div>
</div>
"""

# Substitui marcador da logo no CSS interno
css_final = CSS_TEMPLATE.replace("{{LOGO_BASE64}}", LOGO_BASE64)

pagina_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
{css_final}
</style>
</head>
<body>
{HTML_TEMPLATE}
</body>
</html>"""

components.html(pagina_html, height=2600, scrolling=True)

