import streamlit as st
import csv
import random
from pathlib import Path

st.set_page_config(
    page_title="Treino de Francês",
    page_icon="🇫🇷",
    layout="centered"
)

# =============================
# CONFIGURAÇÃO DOS ARQUIVOS
# =============================
ARQUIVO_VOCABULARIO = Path("vocabulario.csv")
ARQUIVO_VERBOS = Path("verbos.csv")


# =============================
# ESTILO VISUAL
# =============================
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 2rem;
    }
    .question-card {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 22px;
        padding: 28px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        color: #f0f6fc;
    }
    .question-type {
        font-size: 0.9rem;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .question-text {
        font-size: 1.35rem;
        font-weight: 650;
        margin-bottom: 8px;
        line-height: 1.45;
    }
    .translation-box {
        padding: 14px 16px;
        border-radius: 14px;
        background: #161b22;
        border: 1px solid #30363d;
        margin-top: 18px;
        font-size: 1rem;
        color: #f0f6fc;
    }
    .correct-box {
        padding: 12px 16px;
        border-radius: 12px;
        background: #d7f8df;
        border: 1px solid #37a852;
        color: #145c25;
        font-weight: 700;
        margin-top: 10px;
    }
    .wrong-box {
        padding: 12px 16px;
        border-radius: 12px;
        background: #ffe0e0;
        border: 1px solid #d93025;
        color: #8a1c15;
        font-weight: 700;
        margin-top: 10px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        border: 1px solid #30363d;
        background: #161b22;
        color: #f0f6fc;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border: 1px solid #58a6ff;
        background: #1f2937;
        transform: translateY(-1px);
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

st.markdown('<div class="main-title">🇫🇷 Treino de Francês</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Vocabulário, conjugação ou os dois — uma questão por vez.</div>', unsafe_allow_html=True)

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
    total = len(st.session_state.teste)
    indice = st.session_state.indice
    pergunta = st.session_state.teste[indice]

    st.markdown(
        """
        <div style="
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
            color: #c9d1d9;
        ">
            🧠 La pratique quotidienne fait la différence.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress((indice + 1) / total)
    st.caption(f"Questão {indice + 1} de {total}")

    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-type">{pergunta["tipo"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{pergunta["pergunta"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    for opcao in pergunta["opcoes"]:
        if st.session_state.respondido:
            if opcao == pergunta["resposta"]:
                st.markdown(f'<div class="correct-box">✅ {opcao}</div>', unsafe_allow_html=True)
            elif opcao == st.session_state.resposta_selecionada:
                st.markdown(f'<div class="wrong-box">❌ {opcao}</div>', unsafe_allow_html=True)
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
        st.markdown(
            f'<div class="translation-box"><strong>Tradução das outras opções:</strong><br>{pergunta.get("traducao", "")}</div>',
            unsafe_allow_html=True
        )

        if pergunta["tipo"] == "Conjugação" and pergunta.get("frase_completa"):
            st.info(f"Frase completa: {pergunta['frase_completa']}")

        texto_botao = "Ver resultado" if indice + 1 == total else "Próxima questão"
        if st.button(texto_botao):
            proxima_questao()
            st.rerun()

    st.write("")
    if st.button("Cancelar treino"):
        reiniciar()
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
