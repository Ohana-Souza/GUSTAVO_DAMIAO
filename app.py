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
# ESTILO VISUAL
# =============================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        scroll-behavior: smooth;
    }

    .block-container {
        max-width: 640px;
        padding-top: clamp(0.35rem, 1.5vw, 0.8rem);
        padding-bottom: 0.35rem;
        padding-left: clamp(0.7rem, 3vw, 1.2rem);
        padding-right: clamp(0.7rem, 3vw, 1.2rem);
        margin: auto;
    }

    .main-title {
        text-align: center;
        font-size: clamp(1.55rem, 6vw, 2.35rem);
        font-weight: 650;
        margin: 0.2rem auto 0.15rem auto;
        color: #ffffff;
        text-shadow: 0 3px 12px rgba(0,0,0,0.55);
    }

    .small-title {
        text-align: center;
        font-size: clamp(0.98rem, 4vw, 1.25rem);
        font-weight: 850;
        margin: 0.05rem auto 0.35rem auto;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0,0,0,0.55);
    }

    .subtitle {
        text-align: center;
        font-size: clamp(0.82rem, 3vw, 0.98rem);
        color: #d5dce8;
        margin: 0 auto 1rem auto;
        line-height: 1.35;
        max-width: 520px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.55);
    }

    .motivation {
        text-align: center;
        font-size: clamp(0.72rem, 2.7vw, 0.9rem);
        font-weight: 800;
        color: #f0f6fc;
        margin: 0.25rem auto 0.45rem auto;
        padding: 0.42rem 0.7rem;
        max-width: 520px;
        border-radius: 999px;
        background: rgba(13, 17, 23, 0.54);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(7px);
        line-height: 1.25;
    }

    .question-card {
        max-width: 600px;
        margin: 0.30rem auto 0.45rem auto;
        text-align: center;
        background: rgba(13, 17, 23, 0.74);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: clamp(0.6rem, 2.4vw, 1rem);
        box-shadow: 0 8px 22px rgba(0,0,0,0.30);
        color: #f0f6fc;
        backdrop-filter: blur(8px);
    }

    .question-type {
        text-align: center;
        font-size: clamp(0.55rem, 2.1vw, 0.7rem);
        color: #b8c0cc;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 850;
        margin-bottom: 0.35rem;
    }

    .question-text {
        text-align: center;
        font-size: clamp(0.94rem, 3.8vw, 1.2rem);
        font-weight: 800;
        line-height: 1.28;
        color: #ffffff;
        margin: 0;
    }

    .config-card {
        max-width: 600px;
        margin: 1rem auto;
        padding: 1.1rem;
        border-radius: 24px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.20);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
        color: #ffffff;
    }

    .fake-label {
        width: fit-content;
        min-width: 170px;
        max-width: 230px;
        margin: 0.18rem auto 0.08rem auto;
        padding: 0.32rem 0.72rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.68);
        border: 1px solid rgba(255,255,255,0.30);
        color: #111827;
        font-size: 0.78rem;
        font-weight: 750;
        text-align: center;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    /* Selectbox de nível */
    div[data-testid="stSelectbox"] {
        max-width: 180px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div {
        max-width: 180px !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.20) !important;
        border: 1px solid rgba(255,255,255,0.24) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(8px);
        min-height: 32px !important;
    }

    div[data-testid="stSelectbox"] * {
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
    }

    div[role="listbox"] {
        background: rgba(20,20,28,0.92) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    div[role="option"]:hover {
        background: rgba(88,166,255,0.25) !important;
    }

    /* Sliders */
    div[data-testid="stSlider"] {
        max-width: 340px !important;
        margin: 0 auto !important;
    }

    /* Base de centralização dos botões */
    div[data-testid="stButton"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
    }

    div[data-testid="stButton"] > button {
        box-shadow: 0 5px 16px rgba(0,0,0,0.16) !important;
        border: 1px solid #e5e7eb !important;
        background: rgba(255,255,255,0.92) !important;
        color: #111827 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stButton"] > button:hover {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border-color: #2563eb !important;
    }

    div[data-testid="stButton"] > button p {
        margin: 0 !important;
        color: inherit !important;
    }

    /* ===== BOTÕES DA TELA INICIAL: Vocabulário / Verbos / Ambos ===== */
    .mode-buttons div[data-testid="stButton"] {
        margin-bottom: 0.06rem !important;
    }

    .mode-buttons div[data-testid="stButton"] > button {
        width: 180px !important;
        max-width: 72vw !important;
        min-height: 30px !important;
        padding: 0.18rem 0.50rem !important;
        border-radius: 13px !important;
        margin: 0.03rem auto !important;
        background: rgba(255,255,255,0.74) !important;
        border: 1px solid rgba(255,255,255,0.28) !important;
    }

    .mode-buttons div[data-testid="stButton"] > button p {
        font-size: 0.74rem !important;
        font-weight: 500 !important;
        line-height: 1.1 !important;
    }

    .mode-buttons div[data-testid="stButton"] > button:hover {
        background: rgba(255,255,255,0.96) !important;
        border-color: #2563eb !important;
    }

    /* ===== BOTÃO COMMENCER ===== */
    .start-button div[data-testid="stButton"] > button {
        width: 190px !important;
        max-width: 74vw !important;
        min-height: 34px !important;
        padding: 0.28rem 0.70rem !important;
        border-radius: 13px !important;
        margin-top: 0.35rem !important;
        background: rgba(255,255,255,0.95) !important;
    }

    .start-button div[data-testid="stButton"] > button p {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    /* ===== BOTÃO X ===== */
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
        font-size: 1.25rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    /* ===== BOTÕES DAS ALTERNATIVAS ===== */
    .answer-button div[data-testid="stButton"] > button {
        width: min(340px, 82vw) !important;
        max-width: 340px !important;
        min-height: 42px !important;
        border-radius: 16px !important;
        padding: 0.65rem 0.9rem !important;
        background: #ffffff !important;
    }

    .answer-button div[data-testid="stButton"] > button p {
        font-size: clamp(0.9rem, 3vw, 1.05rem) !important;
        font-weight: 800 !important;
    }

    /* ===== BOTÃO PRÓXIMA QUESTÃO ===== */
    .next-button div[data-testid="stButton"] > button {
        width: 54px !important;
        height: 54px !important;
        min-height: 54px !important;
        max-width: 54px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        background: #ffffff !important;
    }

    .next-button div[data-testid="stButton"] > button p {
        font-size: 1.55rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    .options-wrapper {
        width: 100% !important;
        max-width: 420px !important;
        margin: 0.45rem auto 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.35rem !important;
    }

    .option-box {
        width: min(340px, 82vw) !important;
        max-width: 340px !important;
        margin: 0.22rem auto !important;
        text-align: center !important;
        padding: 0.65rem 0.9rem !important;
        border-radius: 16px !important;
        font-size: clamp(0.9rem, 3vw, 1.05rem) !important;
        font-weight: 800 !important;
        line-height: 1.25 !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
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

    .translation-box {
        max-width: 600px;
        margin: 0.45rem auto 0 auto;
        text-align: center;
        padding: 0.55rem 0.75rem;
        border-radius: 14px;
        background: rgba(13, 17, 23, 0.80);
        border: 1px solid rgba(255,255,255,0.14);
        font-size: clamp(0.72rem, 2.6vw, 0.9rem);
        color: #f0f6fc;
        line-height: 1.45;
        backdrop-filter: blur(7px);
    }

    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #d5dce8;
        font-weight: 800;
        font-size: clamp(0.68rem, 2.4vw, 0.82rem);
        margin-top: -0.2rem;
        margin-bottom: 0.25rem;
    }

    h1, h2, h3, .stSubheader {
        text-align: center;
        color: #ffffff;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.28rem;
    }

    @media (max-width: 600px) {
        .block-container {
            max-width: 100%;
            padding-top: 0.25rem;
            padding-left: 0.65rem;
            padding-right: 0.65rem;
        }

        .small-title {
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }

        .motivation {
            margin-top: 0.15rem;
            margin-bottom: 0.35rem;
            padding: 0.36rem 0.55rem;
        }

        .question-card {
            border-radius: 15px;
            margin: 0.35rem auto 0.4rem auto;
            padding: 0.62rem;
        }

        .mode-buttons div[data-testid="stButton"] > button {
            width: 160px !important;
            min-height: 28px !important;
        }

        .mode-buttons div[data-testid="stButton"] > button p {
            font-size: 0.68rem !important;
        }

        .option-box,
        .answer-button div[data-testid="stButton"] > button {
            width: min(300px, 84vw) !important;
            min-height: 38px !important;
            border-radius: 14px !important;
            padding: 0.55rem 0.75rem !important;
        }

        .close-button div[data-testid="stButton"] > button {
            width: 38px !important;
            height: 38px !important;
            min-height: 38px !important;
            max-width: 38px !important;
        }

        .next-button div[data-testid="stButton"] > button {
            width: 50px !important;
            height: 50px !important;
            min-height: 50px !important;
            max-width: 50px !important;
        }
    }
    /* CENTRALIZA TODOS OS BOTÕES */
    div[data-testid="stButton"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* CENTRALIZA COLUNAS */
    div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    
    /* BOTÕES DA MODALIDADE */
    .mode-buttons {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.15rem !important;
    }
    
    /* BOTÕES DAS RESPOSTAS */
    .answer-button {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    /* BOTÃO START */
    .start-button {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    /* BOTÃO NEXT */
    .next-button {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
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
else:
    st.markdown('<div class="small-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)

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
    
    col1, col2, col3 = st.columns([1.2,2,1.2])
    with col2:
        st.markdown('<div class="mode-buttons">', unsafe_allow_html=True)

        if st.button("Vocabulário", key="btn_modo_vocab"):
            st.session_state.modalidade = "Vocabulário"
    
        if st.button("Verbos", key="btn_modo_verbos"):
            st.session_state.modalidade = "Verbos"
        
        if st.button("Ambos", key="btn_modo_ambos"):
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
        st.markdown('<div class="fake-label">Nº verbos</div>',unsafe_allow_html=True)
        qtd_verbos = st.slider("", 1, 50, 10, key="slider_verbos",label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="start-button">', unsafe_allow_html=True)
        iniciar = st.button("Commencer", key="btn_commencer")
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
    colx1, colx2, colx3 = st.columns([8,1,1])

    with colx3:
        st.markdown('<div class="close-button">', unsafe_allow_html=True)
        if st.button("×", key="fechar_treino"):
            reiniciar()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
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

    for opcao in pergunta["opcoes"]:
        opcao_html = html.escape(opcao)

        if st.session_state.respondido:
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
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="answer-button">', unsafe_allow_html=True)
                st.button(
                    opcao,
                    key=f"opcao_{indice}_{opcao}",
                    on_click=selecionar_resposta,
                    args=(opcao,)
                )
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.respondido:
        col1, col2, col3 = st.columns([1,1,1])
        
        with col2:
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
