import streamlit as st
import random

st.set_page_config(page_title="Teste de Vocabulário", page_icon="🇫🇷")

st.title("🇫🇷 Teste de Vocabulário")
st.write("Escolha seu nível e responda às perguntas.")

perguntas = {
    "A1": [
        {"pergunta": "Como se diz 'casa' em francês?", "opcoes": ["maison", "chien", "livre"], "resposta": "maison"},
        {"pergunta": "Como se diz 'gato' em francês?", "opcoes": ["chat", "table", "pomme"], "resposta": "chat"},
    ],
    "A2": [
        {"pergunta": "Como se diz 'viajar' em francês?", "opcoes": ["voyager", "manger", "dormir"], "resposta": "voyager"},
        {"pergunta": "Como se diz 'ontem' em francês?", "opcoes": ["hier", "demain", "aujourd'hui"], "resposta": "hier"},
    ],
    "B1": [
        {"pergunta": "Qual palavra significa 'embora'?", "opcoes": ["bien que", "toujours", "jamais"], "resposta": "bien que"},
        {"pergunta": "Como se diz 'conseguir' em francês?", "opcoes": ["réussir", "tomber", "fermer"], "resposta": "réussir"},
    ],
}

nome = st.text_input("Nome do aluno")
nivel = st.selectbox("Nível", ["A1", "A2", "B1"])

if nome:
    st.subheader(f"Bonjour, {nome}! 👋")

    score = 0

    for i, item in enumerate(perguntas[nivel]):
        resposta = st.radio(
            item["pergunta"],
            item["opcoes"],
            key=f"pergunta_{i}"
        )

        if resposta == item["resposta"]:
            score += 1

    if st.button("Finalizar teste"):
        st.success(f"Sua pontuação: {score}/{len(perguntas[nivel])}")
