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
# ESTILO VISUAL LIMPO
# =============================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        scroll-behavior: smooth;
    }

    .block-container {
        max-width: 620px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 0.6rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        margin: auto !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.18rem !important;
    }

    [data-testid="element-container"] {
        margin-bottom: 0.02rem !important;
    }

    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: clamp(1.45rem, 4.5vw, 2.15rem);
        font-weight: 850;
        line-height: 1.1;
        margin: 0.45rem auto 0.06rem auto;
        text-shadow: 0 3px 12px rgba(0,0,0,0.65);
    }

    .subtitle {
        text-align: center;
        color: #d5dce8;
        font-size: clamp(0.72rem, 2.5vw, 0.9rem);
        margin: 0 auto 0.55rem auto;
        text-shadow: 0 2px 8px rgba(0,0,0,0.55);
    }

    .small-title {
        text-align: center;
        color: #ffffff;
        font-size: clamp(0.98rem, 3.2vw, 1.16rem);
        font-weight: 850;
        line-height: 1.1;
        margin: 0.18rem auto 0.12rem auto;
        text-shadow: 0 2px 10px rgba(0,0,0,0.60);
    }

    .fake-label {
        width: fit-content;
        min-width: 140px;
        max-width: 210px;
        margin: 0.16rem auto 0.08rem auto;
        padding: 0.26rem 0.62rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.76);
        border: 1px solid rgba(255,255,255,0.32);
        color: #111827;
        font-size: 0.68rem;
        font-weight: 800;
        text-align: center;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    div[data-testid="stSelectbox"] {
        width: 210px !important;
        max-width: 210px !important;
        margin: 0 auto 0.35rem auto !important;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div {
        width: 210px !important;
        max-width: 210px !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        min-height: 36px !important;
        border-radius: 14px !important;
        background: rgba(255,255,255,0.22) !important;
        border: 1px solid rgba(255,255,255,0.24) !important;
        backdrop-filter: blur(8px);
    }

    div[data-testid="stSelectbox"] * {
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
    }

    div[role="listbox"] {
        background: rgba(20,20,28,0.92) !important;
        border-radius: 14px !important;
    }

    /* Modalidade como botões via radio */
    div[data-testid="stRadio"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    div[data-testid="stRadio"] > div {
        width: 100% !important;
    }

    div[data-testid="stRadio"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    div[data-testid="stRadio"] > div {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }


    /* Modalidade como botões via radio, centralizado por coluna */
    div[data-testid="stRadio"] {
        width: 100% !important;
    }

    div[data-testid="stRadio"] > div {
        width: 100% !important;
    }

    div[role="radiogroup"] {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.32rem !important;
        margin: 0.05rem auto 0.22rem auto !important;
    }

    div[role="radiogroup"] label {
        width: 230px !important;
        max-width: 100% !important;
        min-height: 38px !important;
        margin: 0 auto !important;
        padding: 0.28rem 0.7rem !important;
        border-radius: 14px !important;
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        color: #111827 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: 0 5px 16px rgba(0,0,0,0.16) !important;
    }

    div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    div[role="radiogroup"] label p {
        margin: 0 !important;
        color: #111827 !important;
        font-size: 0.88rem !important;
        font-weight: 550 !important;
        text-align: center !important;
    }

    div[role="radiogroup"] label:has(input:checked) {
        border: 2px solid #58a6ff !important;
        background: rgba(255,255,255,0.98) !important;
        font-weight: 800 !important;
    }

    div[data-testid="stSlider"] {
        width: 320px !important;
        max-width: 82vw !important;
        margin: 0.02rem auto 0.35rem auto !important;
    }

    div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
    }

    div[data-testid="stButton"] > button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1px solid #e5e7eb !important;
        background: rgba(255,255,255,0.94) !important;
        color: #111827 !important;
        box-shadow: 0 5px 16px rgba(0,0,0,0.16) !important;
        border-radius: 14px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stButton"] > button p {
        margin: 0 !important;
        color: inherit !important;
    }

    .start-button {
        max-width: 240px;
        margin: 0.2rem auto 0 auto;
    }

    .start-button div[data-testid="stButton"] > button {
        width: 240px !important;
        max-width: 82vw !important;
        min-height: 40px !important;
        padding: 0.32rem 0.7rem !important;
    }

    .start-button div[data-testid="stButton"] > button p {
        font-size: 0.9rem !important;
        font-weight: 550 !important;
    }

    .top-actions {
        position: fixed;
        top: 72px;
        right: 20px;
        z-index: 999999;
    }

    .top-actions div[data-testid="stButton"] > button {
        width: 42px !important;
        height: 42px !important;
        min-height: 42px !important;
        max-width: 42px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        background: #ffffff !important;
    }

    .top-actions div[data-testid="stButton"] > button p {
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    .motivation {
        text-align: center;
        max-width: 540px;
        margin: 0.08rem auto 0.08rem auto;
        padding: 0.30rem 0.65rem;
        border-radius: 999px;
        background: rgba(13, 17, 23, 0.58);
        border: 1px solid rgba(255,255,255,0.12);
        color: #f0f6fc;
        font-size: clamp(0.70rem, 2.5vw, 0.86rem);
        font-weight: 800;
        backdrop-filter: blur(7px);
        line-height: 1.15;
    }

    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #d5dce8;
        font-weight: 800;
        font-size: clamp(0.64rem, 2.3vw, 0.78rem);
        margin-top: -0.04rem;
        margin-bottom: 0.04rem;
    }

    .question-card {
        max-width: min(560px, 92vw);
        margin: 0.10rem auto 0.14rem auto;
        padding: 0.55rem 0.75rem;
        border-radius: 14px;
        text-align: center;
        background: rgba(13, 17, 23, 0.76);
        border: 1px solid rgba(255,255,255,0.14);
        box-shadow: 0 8px 22px rgba(0,0,0,0.30);
        color: #f0f6fc;
        backdrop-filter: blur(8px);
    }

    .question-type {
        text-align: center;
        font-size: clamp(0.50rem, 1.8vw, 0.64rem);
        color: #b8c0cc;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 850;
        margin-bottom: 0.12rem;
    }

    .question-text {
        text-align: center;
        font-size: clamp(0.88rem, 3vw, 1.08rem);
        font-weight: 800;
        line-height: 1.16;
        color: #ffffff;
        margin: 0;
    }

    .answers-area {
        max-width: 320px;
        margin: 0 auto 0 auto;
    }

    .answer-button {
        margin: -0.03rem 0 !important;
        padding: 0 !important;
    }

    .answer-button div[data-testid="stButton"] > button {
        width: 320px !important;
        max-width: 82vw !important;
        min-height: 30px !important;
        padding: 0.10rem 0.5rem !important;
    }

    .answer-button div[data-testid="stButton"] > button p {
        font-size: 0.82rem !important;
        line-height: 1 !important;
        font-weight: 600 !important;
    }

    .options-wrapper {
        width: 100% !important;
        max-width: 360px !important;
        margin: 0.03rem auto 0 auto !important;
    }

    .option-box {
        width: min(320px, 82vw) !important;
        max-width: 320px !important;
        min-height: 36px !important;
        margin: 0.05rem auto !important;
        padding: 0.24rem 0.6rem !important;
        border-radius: 13px !important;
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        line-height: 1.05 !important;
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

    .next-button {
        max-width: 54px;
        margin: 0.3rem auto 0 auto;
    }

    .next-button div[data-testid="stButton"] > button {
        width: 50px !important;
        height: 50px !important;
        min-height: 50px !important;
        max-width: 50px !important;
        border-radius: 50% !important;
        padding: 0 !important;
    }

    .next-button div[data-testid="stButton"] > button p {
        font-size: 1.4rem !important;
        font-weight: 900 !important;
    }

    @media (max-width: 600px) {
        .block-container {
            max-width: 100% !important;
            padding-top: 0.95rem !important;
            padding-left: 0.55rem !important;
            padding-right: 0.55rem !important;
        }

        .main-title {
            font-size: 1.35rem !important;
            margin-top: 0.45rem !important;
        }

        .subtitle {
            font-size: 0.68rem !important;
            margin-bottom: 0.42rem !important;
        }

        div[role="radiogroup"] {
            gap: 0.26rem !important;
        }

        div[role="radiogroup"] label {
            width: 220px !important;
            max-width: 100% !important;
            min-height: 36px !important;
        }

        .answers-area {
            max-width: 300px;
        }

        .answer-button div[data-testid="stButton"] > button,
        .option-box {
            width: 300px !important;
            max-width: 82vw !important;
            min-height: 34px !important;
        }
    }


    /* ===== AJUSTE FINAL MAIS FORTE: opções bem próximas ===== */

    .answers-area {
        max-width: 320px !important;
        margin: -0.10rem auto 0 auto !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 0.02rem !important;
    }

    .answers-area [data-testid="element-container"] {
        margin-top: -0.32rem !important;
        margin-bottom: -0.32rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    [data-testid="element-container"]:has(.answer-button) {
        margin-top: -0.32rem !important;
        margin-bottom: -0.32rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .answer-button {
        margin: -0.34rem 0 !important;
        padding: 0 !important;
        line-height: 0.8 !important;
    }

    .answer-button div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
        height: auto !important;
    }

    .answer-button div[data-testid="stButton"] > button {
        width: 320px !important;
        max-width: 82vw !important;
        min-height: 24px !important;
        height: 28px !important;
        padding: 0.02rem 0.40rem !important;
        margin: 0 !important;
        border-radius: 12px !important;
    }

    .answer-button div[data-testid="stButton"] > button p {
        font-size: 0.78rem !important;
        line-height: 0.9 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    @media (max-width: 600px) {
        .answers-area {
            max-width: 300px !important;
            gap: 0 !important;
        }

        .answers-area [data-testid="element-container"],
        [data-testid="element-container"]:has(.answer-button) {
            margin-top: -0.34rem !important;
            margin-bottom: -0.34rem !important;
        }

        .answer-button {
            margin: -0.36rem 0 !important;
        }

        .answer-button div[data-testid="stButton"] > button {
            width: 300px !important;
            max-width: 82vw !important;
            min-height: 23px !important;
            height: 27px !important;
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

    opcoes_modo = ["Vocabulário", "Verbos", "Ambos"]
    modo_atual = "Ambos" if st.session_state.modalidade == "Vocabulário + Verbos" else st.session_state.modalidade

    col_radio_1, col_radio_2, col_radio_3 = st.columns([1.2, 1, 1.2], gap="small")

    with col_radio_2:
        modalidade_escolhida = st.radio(
            "",
            opcoes_modo,
            index=opcoes_modo.index(modo_atual),
            label_visibility="collapsed",
            key="radio_modalidade"
        )

    st.session_state.modalidade = "Vocabulário + Verbos" if modalidade_escolhida == "Ambos" else modalidade_escolhida
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
    st.markdown('<div class="top-actions">', unsafe_allow_html=True)
    if st.button("×", key="fechar_treino"):
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
        st.markdown('<div class="answers-area">', unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.respondido:
        st.markdown('<div class="next-button">', unsafe_allow_html=True)
        simbolo_botao = "✓" if indice + 1 == total else "→"

        if st.button(simbolo_botao, key=f"proxima_{indice}"):
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
