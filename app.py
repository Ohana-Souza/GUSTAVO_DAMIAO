import base64
import csv
import random
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
        font-weight: 850;
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
        margin: 0.45rem auto 0.55rem auto;
        text-align: center;
        background: rgba(13, 17, 23, 0.74);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: clamp(0.7rem, 2.6vw, 1rem);
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

    div.stButton > button {
        width: 100% !important;
        max-width: 280px !important;
        min-height: 42px !important;
        margin: 0.35rem auto !important;
        display: block !important;
        border-radius: 14px !important;
        padding: 0.5rem 0.8rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: 1px solid #e5e7eb !important;
        background: #ffffff !important;
        color: #111827 !important;
    }
    
    div.stButton > button:hover {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border: 1px solid #2563eb !important;
    }
    div.stButton > button:disabled {
        opacity: 0.72;
        color: #111827 !important;
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
    }

    .correct-box,
    .wrong-box {
        max-width: 280px;
        margin: 0.30rem auto;
        text-align: center;
        padding: 0.55rem 0.75rem;
        border-radius: 14px;
        font-size: clamp(0.78rem, 3vw, 0.98rem);
        font-weight: 850;
        line-height: 1.25;
        box-shadow: 0 5px 16px rgba(0,0,0,0.16);
    }

    .correct-box {
        background: #d7f8df;
        border: 1px solid #37a852;
        color: #145c25;
    }

    .wrong-box {
        background: #ffe0e0;
        border: 1px solid #d93025;
        color: #8a1c15;
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

    .stProgress {
        margin-top: 0.15rem;
        margin-bottom: 0.1rem;
    }

    .stProgress > div > div > div > div {
        background-color: #58a6ff;
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

    /* Compacta espaços verticais padrão do Streamlit */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.35rem;
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

        div.stButton > button {
            width: 100%;
            max-width: 260px;
            min-height: 38px;
            margin: 0.35rem auto;
            display: block;
            border-radius: 14px;
            padding: 0.45rem 0.7rem;
            font-weight: 700;
            font-size: 0.9rem;
            border: 1px solid #e5e7eb;
            background: #ffffff;
            color: #111827;
        }

        .correct-box,
        .wrong-box,
        .translation-box {
            border-radius: 12px;
            padding: 0.45rem 0.55rem;
            margin-top: 0.24rem;
            margin-bottom: 0.24rem;
        }
    }
    .top-close {
        position: fixed;
        top: 14px;
        right: 18px;
        z-index: 9999;
    }
    
    .top-close + div button {
        width: 44px !important;
        min-height: 44px !important;
        border-radius: 50% !important;
        background: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #e5e7eb !important;
        font-size: 1.4rem !important;
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

    traducoes_erradas = []
    for opcao in opcoes:
        if opcao != resposta_certa:
            for v in vocabulario:
                if v["frances"].strip() == opcao:
                    traducoes_erradas.append(f"{opcao} = {v['portugues']}")
                    break

    return {
        "tipo": "Vocabulário — Português → Francês",
        "pergunta": f"Como se diz **{item['portugues']}** em francês?",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": "<br>".join(traducoes_erradas)
    }


def pergunta_frances_para_portugues(vocabulario):
    item = random.choice(vocabulario)
    resposta_certa = item["portugues"].strip()
    todas = [v["portugues"].strip() for v in vocabulario]

    opcoes = gerar_opcoes(resposta_certa, todas)

    traducoes_erradas = []
    for opcao in opcoes:
        if opcao != resposta_certa:
            for v in vocabulario:
                if v["portugues"].strip() == opcao:
                    traducoes_erradas.append(f"{opcao} = {v['frances']}")
                    break

    return {
        "tipo": "Vocabulário — Francês → Português",
        "pergunta": f"O que significa **{item['frances']}** em português?",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": "<br>".join(traducoes_erradas)
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

    return {
        "tipo": "Conjugação",
        "pergunta": f"**({item['tempo']})**\n\n{item['frase_lacuna']}",
        "opcoes": opcoes,
        "resposta": resposta_certa,
        "traducao": item.get("traducao_frase", ""),
        "frase_completa": item.get("frase_completa", "")
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


# =============================
# INTERFACE
# =============================
iniciar_estado()

if st.query_params.get("cancelar") == "1":
    reiniciar()
    st.query_params.clear()
    st.rerun()

if st.session_state.tela == "configuracao":
    st.markdown('<div class="main-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Vocabulário, conjugação ou os dois — uma questão por vez.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="small-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)

vocabulario = carregar_csv(ARQUIVO_VOCABULARIO)
verbos = carregar_csv(ARQUIVO_VERBOS)

if st.session_state.tela == "configuracao":
    st.subheader("Configuração do treino")

    nivel = st.selectbox("Nível de dificuldade", ["A1", "A2", "B1", "B2", "C1"])

    modalidade = st.radio(
        "O que você quer treinar?",
        ["Vocabulário", "Verbos", "Vocabulário + Verbos"],
        horizontal=True
    )

    qtd_vocabulario = 0
    qtd_verbos = 0

    if modalidade == "Vocabulário":
        qtd_vocabulario = st.slider("Quantidade de questões de vocabulário", 1, 50, 10)
    elif modalidade == "Verbos":
        qtd_verbos = st.slider("Quantidade de questões de verbos", 1, 50, 10)
    else:
        qtd_vocabulario = st.slider("Quantidade de questões de vocabulário", 1, 50, 10)
        qtd_verbos = st.slider("Quantidade de questões de verbos", 1, 50, 10)

    if st.button("Começar treino"):
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
    st.markdown('<div class="top-close">', unsafe_allow_html=True)
    if st.button("×", key="cancelar_x"):
        reiniciar()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
            
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

    for opcao in pergunta["opcoes"]:
        col_esq, col_centro, col_dir = st.columns([1, 1.4, 1])

        with col_centro:
            if st.session_state.respondido:
                if opcao == pergunta["resposta"]:
                    st.markdown(f'<div class="correct-box">✓ {opcao}</div>', unsafe_allow_html=True)
                elif opcao == st.session_state.resposta_selecionada:
                    st.markdown(f'<div class="wrong-box">✕ {opcao}</div>', unsafe_allow_html=True)
                else:
                    st.button(opcao, disabled=True, key=f"opcao_{indice}_{opcao}")
            else:
                st.button(
                    opcao,
                    key=f"opcao_{indice}_{opcao}",
                    on_click=selecionar_resposta,
                    args=(opcao,)
                )

    if st.session_state.respondido:
        titulo_traducao = "Tradução das outras opções:" if pergunta["tipo"] != "Conjugação" else "Tradução:"
        st.markdown(
            f'<div class="translation-box"><strong>{titulo_traducao}</strong><br>{pergunta.get("traducao", "")}</div>',
            unsafe_allow_html=True
        )

        if pergunta["tipo"] == "Conjugação" and pergunta.get("frase_completa"):
            st.markdown(
                f'<div class="translation-box"><strong>Frase completa:</strong><br>{pergunta["frase_completa"]}</div>',
                unsafe_allow_html=True
            )

        texto_botao = "Ver resultado" if indice + 1 == total else "Próxima questão"
        if st.button(texto_botao):
            proxima_questao()
            st.rerun()

elif st.session_state.tela == "resultado":
    total = len(st.session_state.teste)
    acertos = st.session_state.acertos

    st.success("Treino finalizado!")
    st.header(f"Pontuação: {acertos}/{total}")
    st.write(f"Aproveitamento: **{(acertos / total) * 100:.1f}%**")

    if st.button("Fazer novo treino"):
        reiniciar()
        st.rerun()
