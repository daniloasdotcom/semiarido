import streamlit as st

# Configurações da página
st.set_page_config(page_title="Danilo Andrade Santos", layout="centered")
st.sidebar.image("images/logo_geosab.webp")
st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
        Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Adicionando Font Awesome para ícones
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <style>
        .perfil-box {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 2px;
            margin-bottom: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .icon-link {
            font-size: 18px;
            margin-right: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Seção: Desenvolvedor
st.markdown("""<div class='perfil-box'>""", unsafe_allow_html=True)
st.title("Danilo Andrade Santos")

st.subheader("🔬 Formação e Pesquisa")
st.markdown(
    """
    - Agrônomo  
    - [Professor de Bioquímica (UFES - 2022-2024)](https://bioquimicacomdanilo.com.br/)
    - Pesquisador em Produção Vegetal (M.Sc., D.Sc. - UFES)  
    - [Especialista em Biocarvões (desde 2012)](https://biochardatablog.streamlit.app/)
    - [Especialista em Agroecologia (IFES)](https://agroecossistemas.online/home)  
    - Especializando em Bioinsumos (IFGO)
    - Especializando em Agropecuária Sustentável (IFRO)    
    """,
    unsafe_allow_html=True
)

st.subheader("🤖 Tecnologia e Dados")
st.markdown(
    """
    - Gestor de IA  
    - Programador Jr. Web/Mobile  
    - Analista de dados (Python, VBA, R, SIG)  
    - Cursando Análise e Des. de Sistemas (UNIP)  
    - Especializando em IA na Agricultura (UTFPR)  
    """
)

st.subheader("🌿 Valores e Abordagem")
st.markdown(
    """
    - Cristão  
    - Aprendiz  
    - Problem Solver  
    """
)

st.markdown(
    """
    <a class="icon-link" href="https://www.instagram.com/daniloas.com_" target="_blank"><i class="fab fa-instagram"></i> Instagram</a>
    <a class="icon-link" href="https://daniloas.com" target="_blank"><i class="fas fa-globe"></i> Website</a>
    <a class="icon-link" href="https://www.linkedin.com/in/daniloandradesantos/" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
    <a class="icon-link" href="https://github.com/daniloasdotcom" target="_blank"><i class="fab fa-github"></i> GitHub</a>
    <a class="icon-link" href="mailto:danilo_as@live.com" target="_blank"><i class="fas fa-envelope"></i> Email</a>
    """,
    unsafe_allow_html=True
)
st.markdown("""</div>""", unsafe_allow_html=True)

# Seção: Código Agro
st.markdown("""<div class='perfil-box'>""", unsafe_allow_html=True)
st.subheader("🤝 Apoio:")
col1, col2 = st.columns([1, 2])
with col1:
    st.image("images/codigo_agro.png", use_container_width=True)
with col2:
    st.subheader("Código Agro")
    st.markdown("Tecnologia para transformar o agro.")
    st.markdown(
        """
        <a class="icon-link" href="https://www.instagram.com/codigo.agro/" target="_blank"><i class="fab fa-instagram"></i> Instagram</a>
        """,
        unsafe_allow_html=True
    )
st.markdown("""</div>""", unsafe_allow_html=True)

# Seção: Dados Agro
col1, col2 = st.columns([1, 2])
with col1:
    st.image("images/dados_agro.png", use_container_width=True)
with col2:
    st.subheader("Dados Agro")
    st.markdown("Tecnologia, dados e agricultura conectados!")
    st.markdown(
        """
        <a class="icon-link" href="https://dadosagro.com" target="_blank"><i class="fas fa-globe"></i> dadosagro.com</a>
        """,
        unsafe_allow_html=True
    )
st.markdown("""</div>""", unsafe_allow_html=True)