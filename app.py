
import streamlit as st

st.set_page_config(page_title="FR Treino de Francês", page_icon="🇫🇷", layout="centered")

# =========================
# CSS
# =========================
st.markdown("""
<style>

.stApp{
    background:#0d1117;
}

.main-title{
    text-align:center;
    color:white;
    font-size:2.1rem;
    font-weight:800;
    margin-bottom:0.5rem;
}

.question-card{
    max-width:700px;
    margin:auto;
    background:rgba(10,10,10,0.72);
    border-radius:22px;
    padding:1.2rem;
    text-align:center;
    color:white;
    margin-top:1rem;
    margin-bottom:1rem;
}

.question-type{
    font-size:0.78rem;
    opacity:0.8;
    margin-bottom:0.4rem;
    font-weight:700;
}

.question-text{
    font-size:1.8rem;
    font-weight:800;
}

.option-box{
    width:100%;
    max-width:320px;
    margin:0.45rem auto;
    padding:0.9rem;
    border-radius:16px;
    text-align:center;
    font-weight:700;
    font-size:1.05rem;
}

.correct-box{
    background:#d7f8df;
    color:#145c25;
    border:1px solid #37a852;
}

.wrong-box{
    background:#ffe0e0;
    color:#8a1c15;
    border:1px solid #d93025;
}

.neutral-box{
    background:white;
    color:#111827;
    border:1px solid #e5e7eb;
}

div[data-testid="stButton"]{
    display:flex !important;
    justify-content:center !important;
    width:100% !important;
}

div[data-testid="stButton"] > button{
    width:100% !important;
    max-width:320px !important;
    background:white !important;
    color:#111827 !important;
    border-radius:16px !important;
    border:1px solid #e5e7eb !important;
    font-weight:700 !important;
}

.top-close{
    position:fixed;
    top:18px;
    right:18px;
    width:44px;
    height:44px;
    background:white;
    border-radius:50%;
    display:flex;
    justify-content:center;
    align-items:center;
    color:#111827;
    text-decoration:none;
    font-size:1.5rem;
    font-weight:800;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Dados fake
# =========================
pergunta = {
    "tipo":"VOCABULÁRIO — PORTUGUÊS ➜ FRANCÊS",
    "pergunta":"Como se diz **responsável** em francês?",
    "opcoes":["responsable","optionnel","obligatoire","simple"],
    "resposta":"responsable",
    "traducoes_opcoes":{
        "optionnel":"opcional",
        "obligatoire":"obrigatório",
        "simple":"simples"
    }
}

# =========================
# Estado
# =========================
if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "resposta" not in st.session_state:
    st.session_state.resposta = None

def selecionar(opcao):
    st.session_state.respondido = True
    st.session_state.resposta = opcao

# =========================
# Interface
# =========================
st.markdown('<a class="top-close" href="#">×</a>', unsafe_allow_html=True)

st.markdown('<div class="main-title">🇫🇷 FR Treino de Francês</div>', unsafe_allow_html=True)

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

    if st.session_state.respondido:

        if opcao == pergunta["resposta"]:

            st.markdown(
                f'<div class="option-box correct-box">✓ {opcao}</div>',
                unsafe_allow_html=True
            )

        elif opcao == st.session_state.resposta:

            st.markdown(
                f'<div class="option-box wrong-box">✕ {opcao}</div>',
                unsafe_allow_html=True
            )

        else:

            traducao = pergunta["traducoes_opcoes"].get(opcao, "")

            texto = f"{opcao} = {traducao}" if traducao else opcao

            st.markdown(
                f'<div class="option-box neutral-box">{texto}</div>',
                unsafe_allow_html=True
            )

    else:

        st.button(
            opcao,
            key=opcao,
            on_click=selecionar,
            args=(opcao,)
        )

if st.session_state.respondido:
    st.button("→")
