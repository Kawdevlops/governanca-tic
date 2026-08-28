import base64
from pathlib import Path

import streamlit as st

from style_lateral import aplicar_estilo_lateral

aplicar_estilo_lateral()

# NÃO chame st.set_page_config aqui — já foi chamado uma vez no app.py,
# e o Streamlit só permite uma chamada por execução.

# CSS GLOBAL — Estilo melhorado

st.html("""
    <style>
    :root {
        --navy:#12203D;
        --blue:#2E5AAC;
        --blue-dark:#1F3E7A;
        --orange:#E8813A;
        --gray:#9AA3B2;
        --line:rgba(255,255,255,0.08);
        --success:#3FD17A;
        --warning:#F5A623;
    }

    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
        Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    /* MARCA D'ÁGUA - Logo centralizado e grande */
    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.06;
        z-index: 0;
        pointer-events: none;
        width: 55%;
        max-width: 700px;
        text-align: center;
    }
    .watermark img {
        width: 100%;
        height: auto;
        filter: grayscale(100%);
    }

    /* Garante que o conteúdo fique acima da marca d'água */

    .main > div {
        position: relative;
        z-index: 1;
    }

    .linha-destaque {
        height: 5px;
        width: 96px;
        background: linear-gradient(90deg, var(--orange), var(--blue));
        border-radius: 4px;
        margin-bottom: 22px;
    }

    .titulo-hero {
        font-size: 60px;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin: 0 0 14px 0;
        line-height: 1.08;
        color: #2E5AAC;
    }

    .subtitulo-hero {
        font-size: 20px;
        color: --line;
        max-width: 600px;
        line-height: 1.7;
    }

    /* Menu lateral de navegação (Home / OT / PDSTIC / ...) */

    [data-testid="stSidebarNav"] {
        padding-top: 16px;
    }
    [data-testid="stSidebarNav"] a {
        font-weight: 700;
        font-size: 15px;
        color: var(--gray);
        padding: 10px 18px;
        margin: 3px 10px;
        border-radius: 8px;
        transition: background 0.15s ease, color 0.15s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: var(--blue);
        color: var(--blue);
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: var(--blue);
        color: #FFFFFF !important;
    }

    /* Cards melhorados */

    .card-modern {
        background: white;
        border-radius: 16px;
        padding: 28px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f0f2f6;
        height: 100%;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .card-modern:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.10);
        transform: translateY(-4px);
    }

    /* Barra superior colorida nos cards */

    .card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .card-modern.ot::before { background: linear-gradient(90deg, var(--blue), var(--blue-dark)); }
    .card-modern.pdstic::before { background: linear-gradient(90deg, var(--orange), #F5A623); }
    .card-modern.maturidade::before { background: linear-gradient(90deg, var(--gray), #b8c4d0); }

    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .card-icon {
        font-size: 50px;
        line-height: 1;
    }
    .card-title {
        font-size: 22px;
        font-weight: 900;
        margin: 0;
        color: #1F3E7A;
    }
    .card-subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 4px;
    }

    .status-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: .06em;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 14px;
    }
    .status-disponivel {
        color: #1a8a3f;
        background: #e8f5ed;
    }
    .status-construcao {
        color: var(--gray);
        background: #f5f6f8;
    }

    .card-description {
        color: #555;
        line-height: 1.7;
        font-size: 16px;
        margin-bottom: 16px;
    }

    /* Lista de itens do card */

    .feature-list {
        margin: 12px 0 18px 0;
        padding: 0;
        list-style: none;
    }
    .feature-list li {
        padding: 6px 0;
        color: #444;
        font-size: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #f5f5f5;
    }
    .feature-list li:last-child {
        border-bottom: none;
    }
    .feature-list .bullet {
        color: var(--blue);
        font-weight: 700;
    }

    /* Badge de informação */
    
    .info-badge {
        display: inline-block;
        background: #f0f4ff;
        color: var(--blue);
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }

    .btn-primary {
        background: var(--blue);
        color: white !important;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        text-decoration: none;
        text-align: center;
        margin: 16px auto 0 auto;
        width: auto;
        min-width: 160px;
    }

    .btn-primary:hover {
        background: var(--blue-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(46, 90, 172, 0.3);
    }

    .btn-disabled {
        background: #e8eaed;
        color: #999 !important;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        cursor: not-allowed;
        display: inline-block;
        text-align: center;
        margin: 16px auto 0 auto;
        width: auto;
        min-width: 160px;
        opacity: 0.7;
    }

    .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #f0f2f6;
        text-align: center;
        color: var(--gray);
        font-size: 14px;
    }
    </style>
""")

CAMINHO_LOGO = Path(__file__).resolve().parent.parent / "assets" / "marcadagua.png"

if CAMINHO_LOGO.exists():
    with open(CAMINHO_LOGO, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    st.html(f"""
        <div class="watermark">
            <img src="data:image/png;base64,{img_data}" alt="Logo Subprefeitura">
        </div>
    """)

# CABEÇALHO

col_txt, col_vazio = st.columns([3.2, 0.8], vertical_alignment="center")

with col_txt:
    st.html('<div class="linha-destaque"></div>')
    st.html('<p class="titulo-hero">Painel de<br>Indicadores TI</p>')
    st.html(
        '<p class="subtitulo-hero">Governança de TI da Secretaria das '
        'Subprefeituras: acompanhe conformidade, execução e maturidade '
        'dos Órgãos Setoriais em um só lugar.</p>'
    )

st.write("")

# CARDS PRINCIPAIS - 3 cards lado a lado

col1, col2, col3 = st.columns(3)

# CARD 1 - OT

with col1:
    st.html("""
        <div class="card-modern ot">
            <div class="card-header">
                <span class="card-title">OT</span>
            </div>
            <div class="card-subtitle">Orientações Técnicas</div>
            <div class="status-tag status-disponivel">● Disponível</div>
            <div class="card-description">
                Acompanha o cumprimento das recomendações técnicas das Orientações Técnicas:
            </div>
            <ul class="feature-list">
                <li><span class="bullet">•</span> <strong>OT007</strong> — Política e rotinas de backup</li>
                <li><span class="bullet">•</span> <strong>OT013</strong> — Segurança da informação</li>
                <li><span class="bullet">•</span> <strong>OT014</strong> — Ambiente físico de TI</li>
            </ul>
            <div style="margin-top:12px;">
                <span class="info-badge">103 recomendações avaliadas</span>
                <span class="info-badge" style="margin-left:6px;">3 OTs</span>
            </div>
            <div class="btn-wrapper">
                <a href="/ot" target="_self" style="text-decoration:none;">
                    <div class="btn-primary">Abrir OT →</div>
                </a>
            </div>
        </div>
    """)

# CARD 2 - PDSTIC (ativado)

with col2:
    st.html("""
        <div class="card-modern pdstic">
            <div class="card-header">
                <span class="card-title">PDSTIC</span>
            </div>
            <div class="card-subtitle">Plano Diretor de TIC</div>
            <div class="status-tag status-disponivel">● Disponível</div>
            <div class="card-description">
                Acompanha as linhas de ação do Plano Diretor de Tecnologia da Informação e Comunicação:
            </div>
            <ul class="feature-list">
                <li><span class="bullet">•</span> Orçamento planejado x liquidado</li>
                <li><span class="bullet">•</span> Status de execução por área</li>
                <li><span class="bullet">•</span> Linhas concluídas / em andamento / não iniciadas</li>
            </ul>
            <div style="margin-top:12px;">
                <span class="info-badge">47 linhas de ação</span>
            </div>
            <div class="btn-wrapper">
                <a href="/pdstic" target="_self" style="text-decoration:none;">
                    <div class="btn-primary">Abrir PDSTIC →</div>
                </a>
            </div>
        </div>
    """)

# CARD 3 - MATURIDADE

with col3:
    st.html("""
        <div class="card-modern maturidade">
            <div class="card-header">
                <span class="card-title">Maturidade</span>
            </div>
            <div class="card-subtitle">Escala de Maturidade</div>
            <div class="status-tag status-disponivel">● Disponível</div>
            <div class="card-description">
                Mede o nível de maturidade dos processos de governança de TI dos Órgãos Setoriais:
            </div>
            <ul class="feature-list">
                <li><span class="bullet">•</span> Níveis de consolidação</li>
                <li><span class="bullet">•</span> Práticas por área</li>
                <li><span class="bullet">•</span> Evolução temporal</li>
            </ul>
            <div style="margin-top:10px;">
                <span class="info-badge"> 187 Critérios Existentes </span>
            </div>
            <div class="btn-wrapper">
                <a href="/pdstic" target="_self" style="text-decoration:none;">
                    <div class="btn-primary">Abrir Maturidade →</div>
                </a>
            </div>
        </div>
    """)

# RODAPÉ

st.html("""
    <div class="footer">
        Governança DGTIC/SMSUB 2026
    </div>
""")