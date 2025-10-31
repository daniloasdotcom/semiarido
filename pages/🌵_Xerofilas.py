import streamlit as st
from bs4 import BeautifulSoup
from plant_datum.plant_database import (
    criar_tabela,
    criar_tabela_receitas,
    listar_plantas,
    listar_receitas
)
from plant_datum.initial_data import dados_iniciais

st.set_page_config(page_title="Xerófitas", page_icon="🌿", layout="centered")
st.sidebar.image("images/logo_geosab.webp")
st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
        Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🌿 Visualizador de Plantas Xerófitas")

# Inicialização do banco de dados
criar_tabela()
criar_tabela_receitas()
dados_iniciais()

# Obter todas as plantas
plantas = listar_plantas()

if plantas:
    st.subheader("🔍 Buscar Planta")

    criterio = st.radio("Buscar por:", ["Nome popular", "Nome científico"], horizontal=True)

    opcoes = {p[2] if criterio == "Nome popular" else p[1]: p for p in plantas}
    termo = st.selectbox(
        "Digite ou selecione uma planta:",
        sorted(opcoes.keys()),
        index=None,
        placeholder="Digite aqui..."
    )

    if termo:
        planta = opcoes[termo]

        # Detectar tema atual
        theme = st.get_option("theme.base")
        bg_color = "#1e1e1e" if theme == "dark" else "#f9f9f9"
        text_color = "#ffffff" if theme == "dark" else "#000000"
        border_color = "#444" if theme == "dark" else "#ccc"

        # Exibir informações da planta (Uso foi removido daqui)
        st.markdown(f"""
            <div style="background-color: {bg_color}; color: {text_color};
                        padding: 1rem; border-radius: 10px; border: 1px solid {border_color};">
                <p><strong>🌿 Nome popular:</strong> {planta[2]}</p>
                <p><strong>🔬 Nome científico:</strong> <em>{planta[1]}</em></p>
                <p><strong>🌍 Origem:</strong> {planta[3]}</p>
                <p><strong>💧 Características adaptativas:</strong><br>{planta[5]}</p>
                <p><strong>📝 Observações:</strong><br>{planta[6]}</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Expanders dinâmicos para Uso ---
        uso_html = planta[4] or ""  # Coluna 4 é para Uso
        if uso_html:  # Só tenta processar se houver conteúdo
            uso_soup = BeautifulSoup(uso_html, "html.parser")

            uso_secoes = []
            atual_titulo_uso = None
            conteudo_uso = []

            for elem in uso_soup.children:
                if elem.name == "h3":
                    if atual_titulo_uso and conteudo_uso:
                        uso_secoes.append((atual_titulo_uso, "".join(str(e) for e in conteudo_uso)))
                        conteudo_uso = []
                    atual_titulo_uso = elem.get_text()
                elif atual_titulo_uso:
                    conteudo_uso.append(elem)

            if atual_titulo_uso and conteudo_uso:
                uso_secoes.append((atual_titulo_uso, "".join(str(e) for e in conteudo_uso)))

            if uso_secoes:
                st.markdown("### 🍽️ Uso")  # Título principal para a seção de Uso
                for titulo, conteudo_html in uso_secoes:
                    with st.expander(titulo):
                        st.markdown(conteudo_html, unsafe_allow_html=True)
            else:
                # Se não houver H3 na seção Uso, mas houver conteúdo, exiba como texto simples
                st.markdown("### 🍽️ Uso")
                st.markdown(uso_html, unsafe_allow_html=True)
        else:
            st.info("Nenhuma informação sobre Uso cadastrada para esta planta.")

        # --- Expanders dinâmicos para Aplicações em SAFs ---
        safs_html = planta[8] or ""  # Coluna 8 é para Aplicações em SAFs
        if safs_html:  # Só tenta processar se houver conteúdo
            safs_soup = BeautifulSoup(safs_html, "html.parser")

            safs_secoes = []
            atual_titulo_safs = None
            conteudo_safs = []

            for elem in safs_soup.children:
                if elem.name == "h3":
                    if atual_titulo_safs and conteudo_safs:
                        safs_secoes.append((atual_titulo_safs, "".join(str(e) for e in conteudo_safs)))
                        conteudo_safs = []
                    atual_titulo_safs = elem.get_text()
                elif atual_titulo_safs:
                    conteudo_safs.append(elem)

            if atual_titulo_safs and conteudo_safs:
                safs_secoes.append((atual_titulo_safs, "".join(str(e) for e in conteudo_safs)))

            if safs_secoes:
                st.markdown("### 🌳 Aplicações em SAFs")
                for titulo, conteudo_html in safs_secoes:
                    with st.expander(titulo):
                        st.markdown(conteudo_html, unsafe_allow_html=True)
            else:
                # Se não houver H3 na seção SAFs, mas houver conteúdo, exiba como texto simples
                st.markdown("### 🌳 Aplicações em SAFs")
                st.markdown(safs_html, unsafe_allow_html=True)
        else:
            st.info("Nenhuma informação sobre Aplicações em SAFs cadastrada para esta planta.")

        # --- Expanders dinâmicos para Plantio e Manejo ---
        plantio_html = planta[7] or ""
        soup = BeautifulSoup(plantio_html, "html.parser")

        # Extrair seções com base nas tags <h3>
        plantio_secoes = []
        atual_titulo = None
        conteudo = []

        for elem in soup.children:
            if elem.name == "h3":
                if atual_titulo and conteudo:
                    plantio_secoes.append((atual_titulo, "".join(str(e) for e in conteudo)))
                    conteudo = []
                atual_titulo = elem.get_text()
            elif atual_titulo:
                conteudo.append(elem)

        if atual_titulo and conteudo:
            plantio_secoes.append((atual_titulo, "".join(str(e) for e in conteudo)))

        # Mostrar as seções como expanders
        if plantio_secoes:
            st.markdown("### 🌾 Plantio e Manejo")
            for titulo, conteudo_html in plantio_secoes:
                with st.expander(titulo):
                    st.markdown(conteudo_html, unsafe_allow_html=True)

        # Exibir receitas vinculadas
        receitas = listar_receitas(planta[0])
        if receitas:
            st.markdown("### 🍴 Receitas")
            for _, titulo, descricao in receitas:
                with st.expander(f"📖 {titulo}"):
                    st.markdown(descricao, unsafe_allow_html=True)
        else:
            st.info("Nenhuma receita cadastrada para esta planta.")
else:
    st.info("Nenhuma planta cadastrada ainda.")