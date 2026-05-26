# ARQUIVO CORRIGIDO
# Ajuste do CSS compactado sem quebrar o Python

import base64
import csv
import random
import html
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Treino de Francês",
    page_icon="🇫🇷",
    layout="centered"
)

BASE_DIR = Path(__file__).parent
ARQUIVO_VOCABULARIO = BASE_DIR / "vocabulario.csv"
ARQUIVO_VERBOS = BASE_DIR / "verbos.csv"
CAMINHO_FUNDO = BASE_DIR / "fundo.png"


def adicionar_fundo_animado(imagem):
    imagem = Path(imagem)

    if not imagem.exists():
        return

    with open(imagem, "rb") as arquivo:
        encoded = base64.b64encode(arquivo.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color: #0d1117;
            background-image: url("data:image/png;base64,{encoded}");
            background-repeat: repeat-x;
            background-size: auto 100vh;
            background-position: 0 0;
            animation: moverFundo 150s linear infinite;
            overflow-x: hidden;
        }}

        @keyframes moverFundo {{
            from {{ background-position: 0 0; }}
            to {{ background-position: -2200px 0; }}
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(5, 8, 13, 0.58);
            z-index: 0;
            pointer-events: none;
        }}

        .block-container {{
            max-width: 720px;
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            padding-left: 0.7rem;
            padding-right: 0.7rem;
            margin: auto;
            position: relative;
            z-index: 1;
        }}

        .element-container {{
            margin-bottom: 0rem !important;
        }}

        .stMarkdown {{
            margin-bottom: 0rem !important;
        }}

        div[data-testid="stVerticalBlock"] > div {{
            gap: 0.02rem !important;
        }}

        div[data-testid="stHorizontalBlock"] {{
            gap: 0.12rem !important;
        }}

        .question-card {{
            max-width: min(500px, 92vw);
            margin: 0.02rem auto 0.06rem auto;
            text-align: center;
            background: rgba(13, 17, 23, 0.76);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 14px;
            padding: 0.38rem 0.55rem;
            box-shadow: 0 8px 22px rgba(0,0,0,0.30);
            color: #f0f6fc;
            backdrop-filter: blur(8px);
        }}

        .question-text {{
            font-size: clamp(0.85rem, 3vw, 1.05rem);
            line-height: 1.18;
            margin: 0;
        }}

        .option-box {{
            width: min(260px, 72vw) !important;
            max-width: 260px !important;
            min-height: 28px !important;
            margin: 0.03rem auto !important;
            padding: 0.20rem 0.45rem !important;
            border-radius: 12px !important;
            font-size: 0.75rem !important;
            line-height: 1.1 !important;
        }}

        .small-title {{
            text-align: center;
            font-size: 1.15rem;
            margin-top: 0.2rem;
            margin-bottom: 0.12rem;
            color: white;
            font-weight: 800;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


adicionar_fundo_animado(CAMINHO_FUNDO)

st.write("Arquivo corrigido com compactação funcionando.")
