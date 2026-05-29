import base64
import csv
import random
import html
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Treino de Francês",
    page_icon="🥐",
    layout="centered"
)

# =============================
# CONFIGURAÇÃO DOS ARQUIVOS
# =============================
BASE_DIR = Path(__file__).parent
ARQUIVO_VOCABULARIO = BASE_DIR / "vocabulario.csv"
ARQUIVO_VERBOS = BASE_DIR / "verbos.csv"

# Imagem usada no layout do Figma/Make
URL_FUNDO_FIGMA = "https://images.unsplash.com/photo-1638290046992-db6003db69d1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwyfHxwYXJpcyUyMGNhZmUlMjBlaWZmZWwlMjB0b3dlciUyMGJhY2tncm91bmR8ZW58MXx8fHwxNzgwMDYxOTc5fDA&ixlib=rb-4.1.0&q=80&w=1080"


# =============================
# FUNDO + ESTILO FIGMA
# =============================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp, button, input, select, textarea {{
        font-family: 'Inter', sans-serif !important;
    }}

    html, body, [class*="css"] {{
        scroll-behavior: smooth;
    }}

    .stApp {{
        background-color: #0d1117;
        background-image: url("{URL_FUNDO_FIGMA}");
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        overflow-x: hidden !important;
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
        max-width: 620px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-bottom: 4.2rem !important;
    }}

    div[data-testid="stVerticalBlock"] > div {{
        gap: 0.08rem !important;
    }}

    [data-testid="element-container"] {{
        margin-bottom: 0.02rem !important;
    }}

    .page-config {{
        padding-top: 96px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .page-question {{
        padding-top: 116px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .main-title {{
        text-align: center;
        color: #ffffff;
        font-family: Inter, sans-serif;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.30);
    }}

    .small-title {{
        text-align: center;
        color: #ffffff;
        font-family: Inter, sans-serif;
        font-size: 24px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.30);
    }}

    .handle {{
        text-align: center;
        color: #D5DCE8;
        font-family: Inter, sans-serif;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.04em;
        margin-top: 4px;
        margin-bottom: 34px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.60);
    }}

    .handle-question {{
        text-align: center;
        color: #D5DCE8;
        font-family: Inter, sans-serif;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.04em;
        margin-top: 6px;
        margin-bottom: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.60);
    }}

    .footer-instagram {{
        position: fixed;
        bottom: 18px;
        left: 0;
        right: 0;
        z-index: 9999;
        text-align: center;
        color: #D5DCE8;
        font-family: Inter, sans-serif;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-shadow: 0 2px 8px rgba(0,0,0,0.70);
        pointer-events: none;
    }}

    .fake-label {{
        width: fit-content;
        min-width: 140px;
        max-width: 230px;
        margin-left: auto;
        margin-right: auto;
        padding: 6px 12px;
        border-radius: 12px;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.16);
        color: #ffffff;
        font-family: Inter, sans-serif;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: none;
    }}

    .nivel-label {{
        margin-top: 0;
        margin-bottom: 16px;
    }}

    .treino-label {{
        margin-top: 40px;
        margin-bottom: 12px;
    }}

    .slider-label {{
        margin-top: 40px;
        margin-bottom: 6px;
        text-align: center;
        color: #ffffff;
        font-family: Inter, sans-serif;
        font-weight: 500;
        font-size: 14px;
    }}

    div[data-testid="stSelectbox"] {{
        width: 210px !important;
        max-width: 210px !important;
        margin: 0 auto 0 auto !important;
    }}

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div {{
        width: 210px !important;
        max-width: 210px !important;
    }}

    div[data-testid="stSelectbox"] > div > div {{
        min-height: 38px !important;
        border-radius: 14px !important;
        background: rgba(255,255,255,0.98) !important;
        border: 1px solid rgba(255,255,255,0.28) !important;
        backdrop-filter: blur(8px);
        color: #111827 !important;
    }}

    div[data-testid="stSelectbox"] * {{
        font-family: Inter, sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    div[data-testid="stSelectbox"] [data-baseweb="select"] span,
    div[data-testid="stSelectbox"] [data-baseweb="select"] div {{
        color: #111827 !important;
    }}

    div[data-baseweb="select"] svg {{
        width: 22px !important;
        height: 22px !important;
        margin-top: 1px !important;
    }}

    div[role="listbox"] {{
        background: rgba(255,255,255,0.98) !important;
        border-radius: 14px !important;
    }}

    div[data-testid="stSlider"] {{
        width: 320px !important;
        max-width: 82vw !important;
        margin: 0 auto 0 auto !important;
    }}

    div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    div[data-testid="stButton"] > button {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border: 2px solid #E5E7EB !important;
        background: rgba(255,255,255,0.98) !important;
        color: #111827 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        border-radius: 14px !important;
        box-sizing: border-box !important;
        font-family: Inter, sans-serif !important;
    }}

    div[data-testid="stButton"] > button p {{
        margin: 0 !important;
        color: inherit !important;
        text-align: center !important;
    }}

    .st-key-mode-buttons {{
        width: 230px !important;
        max-width: 82vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    .st-key-mode-buttons div[data-testid="stButton"] {{
        margin: 0 0 4px 0 !important;
    }}

    .st-key-mode-buttons div[data-testid="stButton"] > button {{
        width: 230px !important;
        max-width: 82vw !important;
        min-height: 38px !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    .st-key-start-button-box {{
        width: 240px !important;
        max-width: 82vw !important;
        margin: 40px auto 0 auto !important;
    }}

    .st-key-start-button-box div[data-testid="stButton"] > button {{
        width: 240px !important;
        height: 40px !important;
        min-height: 40px !important;
        padding: 0 12px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    .top-close {{
        position: fixed !important;
        top: max(18px, env(safe-area-inset-top)) !important;
        right: 12px !important;
        z-index: 2147483647 !important;
        width: 42px !important;
        height: 42px !important;
        border-radius: 50% !important;
        background: rgba(255,255,255,0.98) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #111827 !important;
        text-decoration: none !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25) !important;
    }}

    .motivation {{
        text-align: center;
        max-width: 320px;
        margin: 12px auto 8px auto;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.16);
        color: #ffffff;
        font-family: Inter, sans-serif;
        font-size: 12px;
        font-weight: 500;
        backdrop-filter: blur(10px);
        line-height: 1.15;
    }}

    div[data-testid="stCaptionContainer"] {{
        text-align: center;
        color: #D5DCE8;
        font-family: Inter, sans-serif;
        font-weight: 500;
        font-size: 12px;
        margin-top: 8px;
        margin-bottom: 0;
    }}

    .question-card {{
        width: 92%;
        max-width: 360px;
        margin: 80px auto 0 auto;
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        background: rgba(255,255,255,0.95);
        border: none;
        box-shadow: 0 8px 22px rgba(0,0,0,0.25);
        color: #111827;
        backdrop-filter: blur(10px);
    }}

    .question-type {{
        text-align: center;
        font-family: Inter, sans-serif;
        font-size: 11px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-weight: 600;
        margin-bottom: 8px;
    }}

    .question-text {{
        text-align: center;
        font-family: Inter, sans-serif;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.25;
        color: #111827;
        margin: 0;
    }}

    .options-wrapper,
    .st-key-answer-buttons {{
        width: 320px !important;
        max-width: 82vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
        box-sizing: border-box !important;
    }}

    .st-key-answer-buttons {{
        margin-top: 40px !important;
    }}

    .st-key-answer-buttons div[data-testid="stButton"] {{
        width: 100% !important;
        margin: 0 0 4px 0 !important;
        padding: 0 !important;
    }}

    .st-key-answer-buttons div[data-testid="stButton"] > button {{
        width: 100% !important;
        max-width: 100% !important;
        min-height: 34px !important;
        margin: 0 !important;
        padding: 8px 12px !important;
        border-radius: 13px !important;
        box-sizing: border-box !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border: 2px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}

    .option-box {{
        width: 320px !important;
        max-width: 82vw !important;
        min-height: 50px !important;
        margin: 0 auto 4px auto !important;
        padding: 10px 12px !important;
        border-radius: 13px !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        font-family: Inter, sans-serif !important;
        color: #111827 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        border: 2px solid #E5E7EB !important;
    }}

    .option-main {{
        font-weight: 600;
        font-size: 14px;
        line-height: 1.05;
    }}

    .option-translation {{
        margin-top: 2px;
        font-weight: 400;
        font-size: 12px;
        color: #6B7280;
        line-height: 1.05;
    }}

    .correct-box {{
        background: #D1FAE5 !important;
        border-color: #10B981 !important;
    }}

    .wrong-box {{
        background: #FEE2E2 !important;
        border-color: #EF4444 !important;
    }}

    .neutral-box {{
        background: #ffffff !important;
        border-color: #E5E7EB !important;
    }}

    .st-key-next-button-box {{
        width: 54px !important;
        max-width: 54px !important;
        margin: 24px auto 0 auto !important;
    }}

    .st-key-next-button-box div[data-testid="stButton"] > button {{
        width: 54px !important;
        height: 54px !important;
        min-height: 54px !important;
        max-width: 54px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 24px !important;
    }}

    @media (max-width: 600px) {{
        .stApp {{
            background-attachment: scroll;
            background-size: cover;
            background-position: center center;
        }}

        .block-container {{
            max-width: 100% !important;
            padding-left: 0.55rem !important;
            padding-right: 0.55rem !important;
            padding-top: 0 !important;
        }}

        .page-config {{
            padding-top: 92px;
        }}

        .page-question {{
            padding-top: 112px;
        }}

        .main-title {{
            font-size: 28px !important;
        }}

        .small-title {{
            font-size: 24px !important;
        }}

        .question-card {{
            margin-top: 80px !important;
        }}

        .options-wrapper,
        .st-key-answer-buttons,
        .option-box {{
            width: 320px !important;
            max-width: 82vw !important;
        }}
    }}
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

if st.query_params.get("cancelar") == "1":
    reiniciar()
    st.query_params.clear()
    st.rerun()

vocabulario = carregar_csv(ARQUIVO_VOCABULARIO)
verbos = carregar_csv(ARQUIVO_VERBOS)

st.markdown('<div class="footer-instagram">@GUSTAVODAMIAO.FR</div>', unsafe_allow_html=True)

if st.session_state.tela == "configuracao":
    st.markdown('<div class="page-config">', unsafe_allow_html=True)

    st.markdown('<div class="main-title">🥐 Treino de Francês</div>', unsafe_allow_html=True)
    st.markdown('<div class="handle">@GUSTAVODAMIAO.FR</div>', unsafe_allow_html=True)

    st.markdown('<div class="fake-label nivel-label">Nível de dificuldade</div>', unsafe_allow_html=True)

    nivel = st.selectbox(
        "",
        ["A1", "A2", "B1", "B2", "C1"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="fake-label treino-label">O que você quer treinar?</div>', unsafe_allow_html=True)

    if "modalidade" not in st.session_state:
        st.session_state.modalidade = "Vocabulário"

    opcoes_modo = ["Vocabulário", "Verbos", "Ambos"]
    modo_atual = "Ambos" if st.session_state.modalidade == "Vocabulário + Verbos" else st.session_state.modalidade

    with st.container(key="mode_buttons"):
        for opcao in opcoes_modo:
            texto_botao = f"✓ {opcao}" if opcao == modo_atual else opcao
            if st.button(texto_botao, key=f"modo_{opcao}", use_container_width=True):
                st.session_state.modalidade = "Vocabulário + Verbos" if opcao == "Ambos" else opcao
                st.rerun()

    modalidade = st.session_state.modalidade

    qtd_vocabulario = 0
    qtd_verbos = 0

    if modalidade == "Vocabulário":
        st.markdown('<div class="slider-label">Número de palavras</div>', unsafe_allow_html=True)
        qtd_vocabulario = st.slider("", 1, 50, 10, label_visibility="collapsed")

    elif modalidade == "Verbos":
        st.markdown('<div class="slider-label">Número de verbos</div>', unsafe_allow_html=True)
        qtd_verbos = st.slider("", 1, 50, 10, label_visibility="collapsed")
    else:
        st.markdown('<div class="slider-label">Número de vocabulário</div>', unsafe_allow_html=True)
        qtd_vocabulario = st.slider("", 1, 50, 10, label_visibility="collapsed")
        st.markdown('<div class="slider-label" style="margin-top: 18px;">Número de verbos</div>', unsafe_allow_html=True)
        qtd_verbos = st.slider("", 1, 50, 10, key="slider_verbos", label_visibility="collapsed")

    with st.container(key="start_button_box"):
        iniciar = st.button("Commencer", key="btn_commencer", use_container_width=True)

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

    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.tela == "questao":
    st.markdown('<a class="top-close" href="?cancelar=1" target="_self">✕</a>', unsafe_allow_html=True)

    st.markdown('<div class="page-question">', unsafe_allow_html=True)

    st.markdown('<div class="small-title">🥐 Treino de Francês</div>', unsafe_allow_html=True)

    total = len(st.session_state.teste)
    indice = st.session_state.indice
    pergunta = st.session_state.teste[indice]

    st.markdown(
        '<div class="motivation">🇫🇷 La pratique quotidienne fait la différence.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="handle-question">@GUSTAVODAMIAO.FR</div>', unsafe_allow_html=True)

    st.caption(f"Questão {indice + 1} de {total}")

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-type">{html.escape(pergunta["tipo"])}</div>
            <div class="question-text">{html.escape(pergunta["pergunta"]).replace("**", "")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.respondido:
        st.markdown('<div class="options-wrapper" style="margin-top:40px !important;">', unsafe_allow_html=True)

        for opcao in pergunta["opcoes"]:
            opcao_html = html.escape(opcao)
            traducao = html.escape(texto_opcao_respondida(pergunta, opcao))
            # Remove "opção = tradução" duplicada, deixando a tradução como subtítulo
            if " = " in traducao:
                traducao = traducao.split(" = ", 1)[1]
            elif " — " in traducao:
                traducao = traducao.split(" — ", 1)[1]
            elif traducao == opcao_html:
                traducao = ""

            if opcao == pergunta["resposta"]:
                classe = "option-box correct-box"
            elif opcao == st.session_state.resposta_selecionada:
                classe = "option-box wrong-box"
            else:
                classe = "option-box neutral-box"

            st.markdown(
                f"""
                <div class="{classe}">
                    <div class="option-main">{opcao_html}</div>
                    {f'<div class="option-translation">{traducao}</div>' if traducao else ''}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        with st.container(key="answer_buttons"):
            for pos, opcao in enumerate(pergunta["opcoes"]):
                if st.button(opcao, key=f"resposta_{indice}_{pos}", use_container_width=True):
                    selecionar_resposta(opcao)
                    st.rerun()

    if st.session_state.respondido:
        simbolo_botao = "✓" if indice + 1 == total else "→"

        with st.container(key="next_button_box"):
            if st.button(simbolo_botao, key=f"proxima_{indice}", use_container_width=True):
                proxima_questao()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.tela == "resultado":
    st.markdown('<div class="page-question">', unsafe_allow_html=True)
    total = len(st.session_state.teste)
    acertos = st.session_state.acertos
    aproveitamento = (acertos / total) * 100 if total else 0

    st.markdown('<div class="small-title">🥐 Résultat</div>', unsafe_allow_html=True)
    st.markdown('<div class="handle">@GUSTAVODAMIAO.FR</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="question-card" style="margin-top: 30px;">
            <div class="question-text" style="font-size: 34px;">{acertos}/{total}</div>
            <div class="question-type" style="margin-top: 10px;">Aproveitamento: {aproveitamento:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(key="start_button_box"):
        if st.button("Recommencer", key="btn_recommencer", use_container_width=True):
            reiniciar()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
