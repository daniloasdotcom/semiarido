import streamlit as st
import openai
import time

# Layout da página
st.set_page_config(page_title="IA para Cultivo no Semiárido", layout="centered")
st.sidebar.image("images/logo_geosab.webp")
st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
        Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🐦 SAB-IÁ - A IA do GeoSAB que fala sobre o semiárido brasileiro")
st.markdown("Faça perguntas sobre sistemas agrícolas sustentáveis no semiárido e receba sugestões com base em conhecimento técnico e ecológico.")

# Acesso à chave e ID do assistente
openai.api_key = st.secrets["api_key"]
assistant_id = st.secrets["assistant_id"]

# Inicializa o histórico e o thread_id
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = openai.beta.threads.create().id

# Botão para novo chat
if st.button("🆕 Novo chat"):
    st.session_state["mensagens"] = []
    st.session_state["thread_id"] = openai.beta.threads.create().id
    st.rerun()

# Entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre cultivo no semiárido...")

# Exibe histórico
for msg in st.session_state["mensagens"]:
    avatar = "🧑‍🌾" if msg["role"] == "user" else "🌵"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Processa nova pergunta
if pergunta:
    avatar = "🧑‍🌾"
    st.chat_message("user", avatar=avatar).markdown(pergunta)
    st.session_state["mensagens"].append({"role": "user", "content": pergunta})

    with st.chat_message("assistant", avatar="🌵"):
        with st.spinner("Pensando..."):
            openai.beta.threads.messages.create(
                thread_id=st.session_state["thread_id"],
                role="user",
                content=pergunta
            )

            run = openai.beta.threads.runs.create(
                thread_id=st.session_state["thread_id"],
                assistant_id=assistant_id
            )

            # Aguarda finalização
            while True:
                status = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state["thread_id"],
                    run_id=run.id
                )
                if status.status == "completed":
                    break
                time.sleep(1)

            # Recupera a resposta
            resposta = openai.beta.threads.messages.list(
                thread_id=st.session_state["thread_id"]
            ).data[0].content[0].text.value

            st.markdown(resposta)
            st.session_state["mensagens"].append({"role": "assistant", "content": resposta})