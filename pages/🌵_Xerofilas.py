import streamlit as st
from plant_datum.plant_database import criar_tabela, listar_plantas
from plant_datum.initial_data import dados_iniciais

st.set_page_config(page_title="Xerófitas", page_icon="🌿", layout="centered")
st.subheader("🔎 Buscar Planta por Nome")

criar_tabela()
dados_iniciais()

plantas = listar_plantas()

if plantas:
    criterio = st.radio("Buscar por:", ["Nome popular", "Nome científico"], horizontal=True)

    if criterio == "Nome popular":
        opcoes = {p[2]: p for p in plantas}  # nome popular → planta
        termos_ordenados = sorted(opcoes.keys())
        termos_ordenados.insert(0, "")  # Adiciona um item vazio no topo

    else:
        opcoes = {p[1]: p for p in plantas}  # nome científico → planta
        termos_ordenados = sorted(opcoes.keys())
        termos_ordenados.insert(0, "")  # Adiciona um item vazio no topo

    termo = st.selectbox("Digite ou selecione uma planta:", options=termos_ordenados, index=0, placeholder="Digite aqui...")

    if termo:
        planta = opcoes[termo]

        st.markdown(
            f"""
            <div style="
                background-color: rgba(240, 240, 240, 0.05); 
                padding: 1rem; 
                border-radius: 0.75rem; 
                border: 1px solid rgba(150,150,150,0.2);
            ">
                <p style="font-size:16px;"><strong>🌿 Nome popular:</strong> {planta[2]}</p>
                <p style="font-size:15px;"><strong>🔬 Nome científico:</strong> <em>{planta[1]}</em></p>
                <p style="font-size:15px;"><strong>🌍 Origem:</strong> {planta[3]}</p>
                <p style="font-size:15px;"><strong>🍽️ Uso:</strong> {planta[4]}</p>
                <p style="font-size:15px;"><strong>💧 Características adaptativas:</strong> {planta[5]}</p>
                <p style="font-size:15px;"><strong>📝 Observações:</strong> {planta[6]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Nenhuma planta cadastrada ainda.")