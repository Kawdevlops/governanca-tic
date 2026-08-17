import streamlit as st


def aplicar_estilo_lateral():
    st.html("""
        <style>
        :root {
            --navy:#12203D;
            --blue:#2E5AAC;
            --gray:#9AA3B2;
        }
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
            background: rgba(46, 90, 172, 0.15);
            color: var(--blue);
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: var(--blue);
            color: #FFFFFF !important;
        }
        </style>
    """)