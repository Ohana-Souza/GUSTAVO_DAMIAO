import streamlit as st
import csv
import random
from pathlib import Path

st.set_page_config(
    page_title="Teste de Vocabulário Francês",
    page_icon="🇫🇷",
    layout="centered"
)

PASTA_DADOS = Path("dados")
ARQUIVO_VOCABULARIO = Path("vocabulario.csv")
ARQUIVO_VERBOS = Path("verbos.csv")


def carregar_csv(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        return list(leitor)


def filtrar_por_nivel(dados, nivel):
    return [item for item in dados if item["nivel"] == nivel]


def gerar_opcoes(resposta_certa, lista_opcoes, quantidade=3):
    opcoes_erradas = [op for op in lista_opcoes if op != resposta_certa]
    opcoes = random.sample(opcoes_erradas, min(quantidade - 1, len(opcoes_erradas)))
    opcoes.append(resposta_certa)
    random.shuffle(opcoes)
    return opcoes


def pergunta_portugues_para_frances(vocabulario):
    item = random.choice(vocabulario)

    resposta_certa = item["frances"]
    todas_traducoes = [v["frances"] for v in vocabulario]

    return {
        "tipo": "Tradução PT → FR",
        "pergunta": f"Como se diz **{item['portugues']}** em francês?",
        "opcoes": gerar_opcoes(resposta_certa, todas_traducoes),
        "resposta": resposta_certa
    }


def pergunta_frances_para_portugues(vocabulario):
    item = random.choice(vocabulario)

    resposta_certa = item["portugues"]
    todas_traducoes = [v["portugues"] for v in vocabulario]

    return {
        "tipo": "Tradução FR → PT",
        "pergunta": f"O que significa **{item['frances']}** em português?",
        "opcoes": gerar_opcoes(resposta_certa, todas_traducoes),
        "resposta": resposta_certa
    }


def pergunta_conjugacao(verbos):
    item = random.choice(verbos)

    resposta_certa = item["conjugacao_certa"]

    opcoes = [
        item["conjugacao_certa"],
        item["opcao_errada_1"],
        item["opcao_errada_2"]
    ]

    random.shuffle(opcoes)

    return {
        "tipo": "Conjugação",
        "pergunta": (
            f"Complete a conjugação do verbo **{item['verbo']}** "
            f"no tempo **{item['tempo']}**:\n\n"
            f"**{item['pronome']} ____**"
        ),
        "opcoes": opcoes,
        "resposta": resposta_certa
    }


def gerar_teste(vocabulario, verbos, quantidade):
    perguntas = []

    tipos = [
        "pt_fr",
        "fr_pt",
        "conjugacao"
    ]

    for _ in range(quantidade):
        tipo = random.choice(tipos)

        if tipo == "pt_fr":
            perguntas.append(pergunta_portugues_para_frances(vocabulario))
        elif tipo == "fr_pt":
            perguntas.append(pergunta_frances_para_portugues(vocabulario))
        else:
            perguntas.append(pergunta_conjugacao(verbos))

    return perguntas


st.title("🇫🇷 Teste de Vocabulário e Conjugação")
st.write("Escolha seu nível e responda às perguntas.")

nome = st.text_input("Nome do aluno")

nivel = st.selectbox(
    "Nível de dificuldade",
    ["A1", "A2", "B1", "B2", "C1"]
)

quantidade = st.slider(
    "Quantidade de perguntas",
    min_value=5,
    max_value=20,
    value=10
)

if "teste" not in st.session_state:
    st.session_state.teste = []
    st.session_state.finalizado = False

if st.button("Gerar teste"):
    vocabulario = carregar_csv(ARQUIVO_VOCABULARIO)
    verbos = carregar_csv(ARQUIVO_VERBOS)

    vocabulario_nivel = filtrar_por_nivel(vocabulario, nivel)
    verbos_nivel = filtrar_por_nivel(verbos, nivel)

    if len(vocabulario_nivel) < 3:
        st.error("É necessário ter pelo menos 3 palavras cadastradas para esse nível.")
    elif len(verbos_nivel) < 1:
        st.error("É necessário ter pelo menos 1 verbo cadastrado para esse nível.")
    else:
        st.session_state.teste = gerar_teste(
            vocabulario_nivel,
            verbos_nivel,
            quantidade
        )
        st.session_state.finalizado = False

if st.session_state.teste:
    st.divider()

    if nome:
        st.subheader(f"Bonjour, {nome}! 👋")

    respostas_usuario = []

    for i, pergunta in enumerate(st.session_state.teste):
        st.markdown(f"### Questão {i + 1}")
        st.caption(pergunta["tipo"])
        st.markdown(pergunta["pergunta"])

        resposta = st.radio(
            "Escolha uma opção:",
            pergunta["opcoes"],
            key=f"pergunta_{i}"
        )

        respostas_usuario.append(resposta)

    if st.button("Finalizar teste"):
        acertos = 0

        st.divider()
        st.header("Resultado")

        for i, pergunta in enumerate(st.session_state.teste):
            resposta_usuario = respostas_usuario[i]
            resposta_certa = pergunta["resposta"]

            if resposta_usuario == resposta_certa:
                acertos += 1
                st.success(f"Questão {i + 1}: correta ✅")
            else:
                st.error(
                    f"Questão {i + 1}: incorreta ❌ "
                    f"Resposta certa: {resposta_certa}"
                )

        st.subheader(f"Pontuação final: {acertos}/{len(st.session_state.teste)}")
