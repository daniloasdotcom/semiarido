import streamlit as st
import openai
import time
import re  # <--- IMPORTANTE: adicionamos para limpeza dos marcadores

# Configuração da página
st.set_page_config(page_title="SAB-IÁ • IA do GeoSAB", layout="centered", page_icon="🌵")

# CSS customizado
st.markdown("""
<style>
    .chat-bubble {
        color: #111 !important;
        font-size: 1.1rem !important;
        line-height: 1.6;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        max-width: 85%;
    }
    .user-bubble {
        background-color: #f1f8e9;
        text-align: right;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #e0f7fa;
        text-align: left;
        margin-right: auto;
    }
    input[type="text"] {
        border: 2px solid #4CAF50 !important;
        border-radius: 10px;
        padding: 12px;
        font-size: 1.1rem !important;
        color: #111 !important;
    }
    html, body, [class*="css"] {
        font-size: 1.05rem !important;
        color: #111 !important;
    }
</style>
""", unsafe_allow_html=True)

# JS para rolar automaticamente
st.markdown("""
<script>
    window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("images/logo_geosab.webp")
st.sidebar.markdown("""
<div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
    Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
</div>
""", unsafe_allow_html=True)

# Título
st.markdown("""
<h1 style='text-align: center; font-size: 2.5rem;'>🌵🐦🌵 SAB-IÁ</h1>
<h3 style='text-align: center; font-weight: 400;'>A inteligência artificial do GeoSAB que fala sobre o semiárido brasileiro</h3>
<p style='text-align: center; font-size: 1.1rem; color: #aaa;'>
Faça perguntas sobre agricultura sustentável, ecologia e convivência com o semiárido.
</p>
""", unsafe_allow_html=True)

# API config
openai.api_key = st.secrets["api_key"]
assistant_id = st.secrets["assistant_id"]

# Sessão
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = openai.beta.threads.create().id

# Botão novo chat
if st.button("🆕 Novo chat", help="Limpa a conversa e inicia um novo diálogo"):
    st.session_state["mensagens"] = []
    st.session_state["thread_id"] = openai.beta.threads.create().id
    st.rerun()

st.divider()

# Exibe mensagens anteriores
for msg in st.session_state["mensagens"]:
    bubble_class = "assistant-bubble" if msg["role"] == "assistant" else "user-bubble"
    st.markdown(
        f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# Entrada
pergunta = st.chat_input("Digite sua pergunta sobre cultivo no semiárido...")

# Processamento da pergunta
if pergunta:
    st.session_state["mensagens"].append({"role": "user", "content": pergunta})
    st.markdown(
        f"<div class='chat-bubble user-bubble'>{pergunta}</div>",
        unsafe_allow_html=True
    )

    with st.chat_message("assistant", avatar="🐦"):
        with st.spinner("SAB-IÁ está pensando..."):
            try:
                openai.beta.threads.messages.create(
                    thread_id=st.session_state["thread_id"],
                    role="user",
                    content=pergunta
                )

                run = openai.beta.threads.runs.create(
                    thread_id=st.session_state["thread_id"],
                    assistant_id=assistant_id
                )

                for _ in range(30):
                    status = openai.beta.threads.runs.retrieve(
                        thread_id=st.session_state["thread_id"],
                        run_id=run.id
                    )
                    if status.status == "completed":
                        break
                    time.sleep(1)
                else:
                    resposta = "Desculpe, a resposta demorou demais para chegar."

                resposta = openai.beta.threads.messages.list(
                    thread_id=st.session_state["thread_id"]
                ).data[0].content[0].text.value

                # 🔧 Remove os marcadores tipo 【n:m†source】
                resposta = re.sub(r"【\d+:\d+†source】", "", resposta)

            except Exception as e:
                resposta = "Desculpe, ocorreu um erro ao processar sua pergunta."

        # Animação de digitação
        resposta_animada = ""
        placeholder = st.empty()
        for i in range(len(resposta)):
            resposta_animada += resposta[i]
            placeholder.markdown(
                f"<div class='chat-bubble assistant-bubble'>{resposta_animada}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.007)

        # Salva no histórico
        st.session_state["mensagens"].append({"role": "assistant", "content": resposta})