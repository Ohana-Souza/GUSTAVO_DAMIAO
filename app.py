import base64
import csv
import random
import html
from urllib.parse import quote, unquote
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Treino de Francês",
    page_icon="🇫🇷",
    layout="centered"
)

# =============================
# CONFIGURAÇÃO DOS ARQUIVOS
# =============================
BASE_DIR = Path(__file__).parent
ARQUIVO_VOCABULARIO = BASE_DIR / "vocabulario.csv"
ARQUIVO_VERBOS = BASE_DIR / "verbos.csv"
CAMINHO_FUNDO = BASE_DIR / "fundo.png"


# =============================
# FUNDO ANIMADO
# =============================
def adicionar_fundo_animado(imagem):
    imagem = Path(imagem)

    if not imagem.exists():
        st.warning(f"Imagem não encontrada: {imagem}")
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
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


adicionar_fundo_animado(CAMINHO_FUNDO)


# =============================
# ESTILO VISUAL
# =============================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        scroll-behavior: smooth;
    }

    .block-container {
        max-width: 720px;
        padding-top: 0.45rem;
        padding-bottom: 0.6rem;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
        margin: auto;
    }
    /* REMOVE espaço invisível entre widgets */
    div[data-testid="element-container"] {
        margin-bottom: 0rem !important;
    }
    
    /* REMOVE espaço do bloco vertical */
    div[data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    /* BOTÕES */
    .answer-button {
        margin: 0.08rem 0 !important;
        padding: 0 !important;
    }
    
    /* BOTÃO INTERNO */
    .answer-button div[data-testid="stButton"] > button {
        min-height: 24px !important;
        padding: 0rem 0.4rem !important;
        border-radius: 12px !important;
    }
    
    /* TEXTO */
    .answer-button div[data-testid="stButton"] > button p {
        font-size: 0.72rem !important;
        line-height: 0.8 !important;
    }
    /* Espaçamento geral controlado, sem margens negativas */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.24rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.35rem !important;
    }

    [data-testid="element-container"] {
        margin-bottom: 0.08rem !important;
    }

    .main-title {
        text-align: center;
        font-size: clamp(1.65rem, 5vw, 2.35rem);
        font-weight: 800;
        margin: 0.20rem auto 0.05rem auto;
        color: #ffffff;
        text-shadow: 0 3px 12px rgba(0,0,0,0.60);
        line-height: 1.12;
    }

    .small-title {
        text-align: center;
        font-size: clamp(1.00rem, 3.4vw, 1.22rem);
        font-weight: 850;
        margin: 0.05rem auto 0.22rem auto;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0,0,0,0.60);
        line-height: 1.15;
    }

    .subtitle {
        text-align: center;
        font-size: clamp(0.78rem, 2.7vw, 0.95rem);
        color: #d5dce8;
        margin: 0 auto 0.65rem auto;
        line-height: 1.25;
        max-width: 520px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.55);
    }

    .fake-label {
        width: fit-content;
        min-width: 150px;
        max-width: 230px;
        margin: 0.22rem auto 0.10rem auto;
        padding: 0.32rem 0.72rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(255,255,255,0.32);
        color: #111827;
        font-size: 0.74rem;
        font-weight: 800;
        text-align: center;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .motivation {
        text-align: center;
        font-size: clamp(0.70rem, 2.5vw, 0.88rem);
        font-weight: 800;
        color: #f0f6fc;
        margin: 0.10rem auto 0.10rem auto;
        padding: 0.36rem 0.70rem;
        max-width: 540px;
        border-radius: 999px;
        background: rgba(13, 17, 23, 0.56);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(7px);
        line-height: 1.2;
    }

    .question-card {
        max-width: min(620px, 92vw);
        margin: 0.20rem auto 0.30rem auto;
        text-align: center;
        background: rgba(13, 17, 23, 0.76);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 0.70rem 0.85rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.30);
        color: #f0f6fc;
        backdrop-filter: blur(8px);
    }

    .question-type {
        text-align: center;
        font-size: clamp(0.52rem, 1.9vw, 0.68rem);
        color: #b8c0cc;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 850;
        margin-bottom: 0.24rem;
    }

    .question-text {
        text-align: center;
        font-size: clamp(0.92rem, 3.4vw, 1.18rem);
        font-weight: 800;
        line-height: 1.23;
        color: #ffffff;
        margin: 0;
    }

    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #d5dce8;
        font-weight: 800;
        font-size: clamp(0.64rem, 2.3vw, 0.78rem);
        margin-top: -0.02rem;
        margin-bottom: 0.08rem;
    }

    div[data-testid="stSelectbox"] {
        max-width: 200px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div {
        max-width: 200px !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.22) !important;
        border: 1px solid rgba(255,255,255,0.24) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(8px);
        min-height: 34px !important;
    }

    div[data-testid="stSelectbox"] * {
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
    }

    div[role="listbox"] {
        background: rgba(20,20,28,0.92) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    div[data-testid="stSlider"] {
        max-width: 360px !important;
        margin: 0 auto !important;
    }

    /* Botões */
    div[data-testid="stButton"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    div[data-testid="stButton"] > button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 38px !important;
        padding: 0.42rem 0.75rem !important;
        margin: 0.06rem auto !important;
        border-radius: 14px !important;
        border: 1px solid #e5e7eb !important;
        background: rgba(255,255,255,0.92) !important;
        color: #111827 !important;
        box-shadow: 0 5px 16px rgba(0,0,0,0.16) !important;
    }

    div[data-testid="stButton"] > button:hover {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border-color: #2563eb !important;
    }

    div[data-testid="stButton"] > button p {
        margin: 0 !important;
        color: inherit !important;
        font-size: 0.90rem !important;
        line-height: 1.1 !important;
    }

    .mode-button div[data-testid="stButton"] > button p {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }

    .start-button div[data-testid="stButton"] > button p {
        font-size: 0.86rem !important;
        font-weight: 550 !important;
    }

    .close-button div[data-testid="stButton"] > button {
        width: 40px !important;
        height: 40px !important;
        min-height: 40px !important;
        max-width: 40px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        background: #ffffff !important;
    }

    .close-button div[data-testid="stButton"] > button p {
        font-size: 1.18rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    .answer-button {
        margin: 0.12rem 0 !important;
        padding: 0 !important;
    }

    .answer-button div[data-testid="stButton"] > button {
        min-height: 38px !important;
        padding: 0.36rem 0.70rem !important;
        margin: 0.02rem auto !important;
        border-radius: 14px !important;
    }

    .answer-button div[data-testid="stButton"] > button p {
        font-size: 0.92rem !important;
        font-weight: 650 !important;
    }

    .next-button div[data-testid="stButton"] > button {
        width: 48px !important;
        height: 48px !important;
        min-height: 48px !important;
        max-width: 48px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        background: #ffffff !important;
    }

    .next-button div[data-testid="stButton"] > button p {
        font-size: 1.40rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    .options-wrapper {
        width: 100% !important;
        max-width: 440px !important;
        margin: 0.12rem auto 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.18rem !important;
    }

    .option-box {
        width: min(340px, 82vw) !important;
        max-width: 340px !important;
        min-height: 38px !important;
        margin: 0.08rem auto !important;
        text-align: center !important;
        padding: 0.36rem 0.70rem !important;
        border-radius: 14px !important;
        font-size: 0.92rem !important;
        font-weight: 800 !important;
        line-height: 1.18 !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 5px 16px rgba(0,0,0,0.16) !important;
    }

    .correct-box {
        background: #d7f8df !important;
        border: 1px solid #37a852 !important;
        color: #145c25 !important;
    }

    .wrong-box {
        background: #ffe0e0 !important;
        border: 1px solid #d93025 !important;
        color: #8a1c15 !important;
    }

    .neutral-box {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        color: #111827 !important;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-top: 0.35rem !important;
            padding-left: 0.60rem !important;
            padding-right: 0.60rem !important;
        }

        .main-title {
            font-size: 1.52rem !important;
            line-height: 1.15 !important;
            margin-top: 0.05rem !important;
        }

        .subtitle {
            font-size: 0.72rem !important;
            margin-bottom: 0.45rem !important;
        }

        .fake-label {
            min-width: 145px !important;
            max-width: 190px !important;
            padding: 0.28rem 0.58rem !important;
            font-size: 0.70rem !important;
        }

        div[data-testid="stSelectbox"],
        div[data-testid="stSelectbox"] > div,
        div[data-testid="stSelectbox"] > div > div {
            width: 185px !important;
            max-width: 185px !important;
        }

        div[data-testid="stButton"] > button p {
            font-size: 0.82rem !important;
        }

        .answer-button div[data-testid="stButton"] > button,
        .option-box {
            min-height: 36px !important;
            padding: 0.32rem 0.60rem !important;
            font-size: 0.84rem !important;
        }

        .answer-button div[data-testid="stButton"] > button p {
            font-size: 0.84rem !important;
        }
    }

    /* ===== AJUSTE FINAL BALANCEADO ===== */
    .block-container {
        padding-top: 1.05rem !important;
        padding-bottom: 0.35rem !important;
        max-width: 720px !important;
    }

    .main-title {
        margin-top: 0.65rem !important;
        margin-bottom: 0.02rem !important;
        font-size: clamp(1.35rem, 4.2vw, 2.05rem) !important;
        line-height: 1.08 !important;
    }

    .subtitle {
        margin: 0 auto 0.32rem auto !important;
        font-size: clamp(0.68rem, 2.4vw, 0.86rem) !important;
    }

    .fake-label {
        margin: 0.08rem auto 0.04rem auto !important;
        padding: 0.22rem 0.58rem !important;
        font-size: 0.68rem !important;
        min-width: 135px !important;
        max-width: 190px !important;
    }

    div[data-testid="stSelectbox"] {
        max-width: 185px !important;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div {
        max-width: 185px !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        min-height: 30px !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.06rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.16rem !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    [data-testid="element-container"] {
        margin-bottom: 0rem !important;
    }

    .mode-button {
        margin: 0.18rem 0 !important;
        padding: 0 !important;
    }

    .mode-button div[data-testid="stButton"] > button {
        min-height: 30px !important;
        padding: 0.18rem 0.55rem !important;
        margin: 0.01rem auto !important;
    }

    .mode-button div[data-testid="stButton"] > button p {
        font-size: 0.76rem !important;
    }

    .start-button div[data-testid="stButton"] > button {
        min-height: 32px !important;
        padding: 0.22rem 0.60rem !important;
        margin-top: 0.10rem !important;
    }

    div[data-testid="stSlider"] {
        margin-top: -0.08rem !important;
        margin-bottom: -0.02rem !important;
    }

    .small-title {
        margin: 0.02rem auto 0.08rem auto !important;
        font-size: clamp(0.95rem, 3.2vw, 1.14rem) !important;
        line-height: 1.06 !important;
    }

    .motivation {
        margin: 0.03rem auto 0.06rem auto !important;
        padding: 0.26rem 0.58rem !important;
        max-width: 520px !important;
    }
    div[data-testid="stButton"] {
        margin-bottom: -0.55rem !important;
    }

    div[data-testid="stCaptionContainer"] {
        margin-top: -0.05rem !important;
        margin-bottom: 0.02rem !important;
    }

    .question-card {
        max-width: min(560px, 92vw) !important;
        margin: 0.08rem auto 0.10rem auto !important;
        padding: 0.52rem 0.70rem !important;
        border-radius: 14px !important;
    }

    .question-type {
        margin-bottom: 0.12rem !important;
        font-size: clamp(0.50rem, 1.8vw, 0.64rem) !important;
    }

    .question-text {
        font-size: clamp(0.86rem, 3vw, 1.06rem) !important;
        line-height: 1.14 !important;
    }

    .options-wrapper {
        width: 100% !important;
        max-width: 360px !important;
        margin: 0.02rem auto 0 auto !important;
        gap: 0 !important;
    }

    .answer-button {
        margin: -0.20rem 0 !important;
        padding: 0 !important;
    }

    .answer-button div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    .answer-button div[data-testid="stButton"] > button {
        min-height: 26px !important;
        padding: 0.05rem 0.45rem !important;
        margin: 0.01rem auto !important;
        border-radius: 13px !important;
    }

    .answer-button div[data-testid="stButton"] > button p {
        font-size: 0.76rem !important;
        line-height: 1 !important;
    }

    .option-box {
        width: min(320px, 80vw) !important;
        max-width: 320px !important;
        min-height: 32px !important;
        margin: 0.01rem auto !important;
        padding: 0.22rem 0.58rem !important;
        font-size: 0.82rem !important;
        line-height: 1.05 !important;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-top: 0.85rem !important;
            padding-left: 0.55rem !important;
            padding-right: 0.55rem !important;
        }

        .main-title {
            font-size: 1.34rem !important;
            margin-top: 0.48rem !important;
        }

        .subtitle {
            margin-bottom: 0.22rem !important;
        }

        .fake-label {
            font-size: 0.64rem !important;
            padding: 0.20rem 0.50rem !important;
        }

        .answer-button div[data-testid="stButton"] > button,
        .option-box {
            min-height: 30px !important;
            padding: 0.20rem 0.50rem !important;
        }

        .answer-button div[data-testid="stButton"] > button p {
            font-size: 0.78rem !important;
        }
    }

</style>
    """,
    unsafe_allow_html=True
)


# =============================
# FUNÇÕES DE DADOS
# =============================
def carregar_csv(caminho):
    if not caminho.exists():
        st.error(f"Arquivo não encontrado: {caminho}")
        st.stop()

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        return list(leitor)


def filtrar_por_nivel(dados, nivel):
    return [item for item in dados if item.get("nivel", "").strip().upper() == nivel]


def gerar_opcoes(resposta_certa, lista_opcoes, quantidade=4):
    resposta_certa = str(resposta_certa).strip()
    lista_limpa = []

    for op in lista_opcoes:
        op = str(op).strip()
        if op and op not in lista_limpa:
            lista_limpa.append(op)

    opcoes_erradas = [op for op in lista_limpa if op != resposta_certa]
    qtd_erradas = min(quantidade - 1, len(opcoes_erradas))

    opcoes = random.sample(opcoes_erradas, qtd_erradas)
    opcoes.append(resposta_certa)
    random.shuffle(opcoes)
    return opcoes


# =============================
# GERAÇÃO DE PERGUNTAS
# =============================
def pergunta_portugues_para_frances(vocabulario):
    item = random.choice(vocabulario)
    resposta_certa = item["frances"].strip()
    todas = [v["frances"].strip() for v in vocabulario]
    opcoes = gerar_opcoes(resposta_certa, todas)

    traducoes_opcoes = {
        v["frances"].strip(): v["portugues"].strip()
        for v in vocabulario
    }

    return {
        "tipo": "Vocabulário — Português → Francês",
        "pergunta": f"Como se diz **{item['portugues']}** em francês?",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": "",
        "traducoes_opcoes": traducoes_opcoes,
        "tempos_opcoes": {}
    }


def pergunta_frances_para_portugues(vocabulario):
    item = random.choice(vocabulario)
    resposta_certa = item["portugues"].strip()
    todas = [v["portugues"].strip() for v in vocabulario]
    opcoes = gerar_opcoes(resposta_certa, todas)

    traducoes_opcoes = {
        v["portugues"].strip(): v["frances"].strip()
        for v in vocabulario
    }

    return {
        "tipo": "Vocabulário — Francês → Português",
        "pergunta": f"O que significa **{item['frances']}** em português?",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": "",
        "traducoes_opcoes": traducoes_opcoes,
        "tempos_opcoes": {}
    }


def pergunta_conjugacao(verbos):
    item = random.choice(verbos)
    resposta_certa = item["resposta_certa"].strip()

    opcoes = [
        item["resposta_certa"].strip(),
        item["opcao_errada_1"].strip(),
        item["opcao_errada_2"].strip(),
        item["opcao_errada_3"].strip(),
    ]
    random.shuffle(opcoes)

    tempo_certo = item.get("tempo_resposta", item.get("tempo", "")).strip()
    tempos_opcoes = {
        item["resposta_certa"].strip(): tempo_certo,
        item["opcao_errada_1"].strip(): item.get("tempo_errada_1", item.get("tempo_opcao_errada_1", item.get("tempo", ""))).strip(),
        item["opcao_errada_2"].strip(): item.get("tempo_errada_2", item.get("tempo_opcao_errada_2", item.get("tempo", ""))).strip(),
        item["opcao_errada_3"].strip(): item.get("tempo_errada_3", item.get("tempo_opcao_errada_3", item.get("tempo", ""))).strip(),
    }

    return {
        "tipo": "Conjugação",
        "pergunta": f"**({item['tempo']})**\n\n{item['frase_lacuna']}",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": item.get("traducao_frase", ""),
        "frase_completa": item.get("frase_completa", ""),
        "traducoes_opcoes": {},
        "tempos_opcoes": tempos_opcoes
    }


def gerar_teste(vocabulario, verbos, qtd_vocabulario, qtd_verbos, modalidade):
    perguntas = []

    if modalidade in ["Vocabulário", "Vocabulário + Verbos"]:
        for _ in range(qtd_vocabulario):
            tipo = random.choice(["pt_fr", "fr_pt"])
            if tipo == "pt_fr":
                perguntas.append(pergunta_portugues_para_frances(vocabulario))
            else:
                perguntas.append(pergunta_frances_para_portugues(vocabulario))

    if modalidade in ["Verbos", "Vocabulário + Verbos"]:
        for _ in range(qtd_verbos):
            perguntas.append(pergunta_conjugacao(verbos))

    random.shuffle(perguntas)
    return perguntas


# =============================
# CONTROLE DE ESTADO
# =============================
def iniciar_estado():
    valores_padrao = {
        "tela": "configuracao",
        "teste": [],
        "indice": 0,
        "resposta_selecionada": None,
        "respondido": False,
        "acertos": 0,
    }

    for chave, valor in valores_padrao.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def reiniciar():
    st.session_state.tela = "configuracao"
    st.session_state.teste = []
    st.session_state.indice = 0
    st.session_state.resposta_selecionada = None
    st.session_state.respondido = False
    st.session_state.acertos = 0


def selecionar_resposta(opcao):
    if not st.session_state.respondido:
        st.session_state.resposta_selecionada = opcao
        st.session_state.respondido = True

        pergunta = st.session_state.teste[st.session_state.indice]
        if opcao == pergunta["resposta"]:
            st.session_state.acertos += 1


def proxima_questao():
    st.session_state.indice += 1
    st.session_state.resposta_selecionada = None
    st.session_state.respondido = False

    if st.session_state.indice >= len(st.session_state.teste):
        st.session_state.tela = "resultado"


def texto_opcao_respondida(pergunta, opcao):
    if pergunta["tipo"] == "Conjugação" and opcao != pergunta["resposta"]:
        tempo = pergunta.get("tempos_opcoes", {}).get(opcao, "")
        return f"{opcao} — {tempo}" if tempo else opcao

    traducao = pergunta.get("traducoes_opcoes", {}).get(opcao, "")
    return f"{opcao} = {traducao}" if traducao and opcao != pergunta["resposta"] else opcao


# =============================
# INTERFACE
# =============================
iniciar_estado()

if st.session_state.tela == "configuracao":
    st.markdown('<div class="main-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">GUSTAVO DAMIÃO</div>', unsafe_allow_html=True)

vocabulario = carregar_csv(ARQUIVO_VOCABULARIO)
verbos = carregar_csv(ARQUIVO_VERBOS)

if st.session_state.tela == "configuracao":
    st.markdown('<div class="fake-label">Nível de dificuldade</div>', unsafe_allow_html=True)

    nivel = st.selectbox(
        "",
        ["A1", "A2", "B1", "B2", "C1"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="fake-label">O que você quer treinar?</div>', unsafe_allow_html=True)

    if "modalidade" not in st.session_state:
        st.session_state.modalidade = "Vocabulário"

    col1, col2, col3 = st.columns([1.25, 1, 1.25], gap="small")

    with col2:
        st.markdown('<div class="mode-button">', unsafe_allow_html=True)
        if st.button("Vocabulário", key="btn_modo_vocab", use_container_width=True):
            st.session_state.modalidade = "Vocabulário"
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="mode-button">', unsafe_allow_html=True)
        if st.button("Verbos", key="btn_modo_verbos", use_container_width=True):
            st.session_state.modalidade = "Verbos"
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="mode-button">', unsafe_allow_html=True)
        if st.button("Ambos", key="btn_modo_ambos", use_container_width=True):
            st.session_state.modalidade = "Vocabulário + Verbos"
        st.markdown("</div>", unsafe_allow_html=True)

    modalidade = st.session_state.modalidade

    qtd_vocabulario = 0
    qtd_verbos = 0

    if modalidade == "Vocabulário":
        st.markdown('<div class="fake-label">Nº palavras</div>', unsafe_allow_html=True)
        qtd_vocabulario = st.slider("", 1, 50, 10, label_visibility="collapsed")

    elif modalidade == "Verbos":
        st.markdown('<div class="fake-label">Nº verbos</div>', unsafe_allow_html=True)
        qtd_verbos = st.slider("", 1, 50, 10, label_visibility="collapsed")
    else:
        st.markdown('<div class="fake-label">Nº vocabulário</div>', unsafe_allow_html=True)
        qtd_vocabulario = st.slider("", 1, 50, 10, label_visibility="collapsed")
        st.markdown('<div class="fake-label">Nº verbos</div>', unsafe_allow_html=True)
        qtd_verbos = st.slider("", 1, 50, 10, key="slider_verbos", label_visibility="collapsed")

    col1, col2, col3 = st.columns([1.25, 1, 1.25], gap="small")

    with col2:
        st.markdown('<div class="start-button">', unsafe_allow_html=True)
        iniciar = st.button("Commencer", key="btn_commencer", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if iniciar:
        vocabulario_nivel = filtrar_por_nivel(vocabulario, nivel)
        verbos_nivel = filtrar_por_nivel(verbos, nivel)

        if modalidade in ["Vocabulário", "Vocabulário + Verbos"] and len(vocabulario_nivel) < 4:
            st.error("É necessário ter pelo menos 4 palavras cadastradas para esse nível.")
        elif modalidade in ["Verbos", "Vocabulário + Verbos"] and len(verbos_nivel) < 1:
            st.error("É necessário ter pelo menos 1 verbo cadastrado para esse nível.")
        else:
            st.session_state.teste = gerar_teste(
                vocabulario_nivel,
                verbos_nivel,
                qtd_vocabulario,
                qtd_verbos,
                modalidade
            )
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.resposta_selecionada = None
            st.session_state.respondido = False
            st.session_state.tela = "questao"
            st.rerun()


elif st.session_state.tela == "questao":
    colx1, colx2, colx3 = st.columns([8, 1, 1], gap="small")

    with colx3:
        st.markdown('<div class="close-button">', unsafe_allow_html=True)
        if st.button("×", key="fechar_treino", use_container_width=True):
            reiniciar()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="small-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)

    total = len(st.session_state.teste)
    indice = st.session_state.indice
    pergunta = st.session_state.teste[indice]

    st.markdown(
        '<div class="motivation">🇫🇷 La pratique quotidienne fait la différence.</div>',
        unsafe_allow_html=True
    )

    st.caption(f"Questão {indice + 1} de {total}")

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-type">{pergunta["tipo"]}</div>
            <div class="question-text">{pergunta["pergunta"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="options-wrapper">', unsafe_allow_html=True)

    if st.session_state.respondido:
        for opcao in pergunta["opcoes"]:
            opcao_html = html.escape(opcao)
            texto = html.escape(texto_opcao_respondida(pergunta, opcao))

            if opcao == pergunta["resposta"]:
                st.markdown(
                    f'<div class="option-box correct-box">✓ {opcao_html}</div>',
                    unsafe_allow_html=True
                )
            elif opcao == st.session_state.resposta_selecionada:
                st.markdown(
                    f'<div class="option-box wrong-box">✕ {texto}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="option-box neutral-box">{texto}</div>',
                    unsafe_allow_html=True
                )
    else:
        col1, col2, col3 = st.columns([1.25, 1, 1.25], gap="small")
        with col2:
            for opcao in pergunta["opcoes"]:
                st.markdown('<div class="answer-button">', unsafe_allow_html=True)
                st.button(
                    opcao,
                    key=f"opcao_{indice}_{opcao}",
                    on_click=selecionar_resposta,
                    args=(opcao,),
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.respondido:
        col1, col2, col3 = st.columns([1.4, 0.35, 1.4], gap="small")

        with col2:
            st.markdown('<div class="next-button">', unsafe_allow_html=True)
            simbolo_botao = "✓" if indice + 1 == total else "→"

            if st.button(simbolo_botao, key=f"proxima_{indice}", use_container_width=True):
                proxima_questao()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.tela == "resultado":
    total = len(st.session_state.teste)
    acertos = st.session_state.acertos

    st.success("Treino finalizado!")
    st.header(f"Pontuação: {acertos}/{total}")
    st.write(f"Aproveitamento: **{(acertos / total) * 100:.1f}%**")

    if st.button("Fazer novo treino"):
        reiniciar()
        st.rerun()
