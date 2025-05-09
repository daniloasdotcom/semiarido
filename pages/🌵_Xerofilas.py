import streamlit as st
from plant_datum.plant_database import (
    criar_tabela,
    criar_tabela_receitas,
    listar_plantas,
    listar_receitas
)
from plant_datum.initial_data import dados_iniciais

st.set_page_config(page_title="Xerófitas", page_icon="🌿", layout="centered")
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

        # Exibir informações da planta com os novos campos
        st.markdown(f"""
            <div style="background-color: {bg_color}; color: {text_color};
                        padding: 1rem; border-radius: 10px; border: 1px solid {border_color};">
                <p><strong>🌿 Nome popular:</strong> {planta[2]}</p>
                <p><strong>🔬 Nome científico:</strong> <em>{planta[1]}</em></p>
                <p><strong>🌍 Origem:</strong> {planta[3]}</p>
                <p><strong>🍽️ Uso:</strong><br>{planta[4]}</p>
                <p><strong>💧 Características adaptativas:</strong><br>{planta[5]}</p>
                <p><strong>📝 Observações:</strong><br>{planta[6]}</p>
                <p><strong>🌾 Plantio e manejo:</strong><br>{planta[7] or ""}</p>
                <p><strong>🌳 Aplicações em SAFs:</strong><br>{planta[8] or ""}</p>
            </div>
        """, unsafe_allow_html=True)

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