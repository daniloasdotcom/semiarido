import streamlit as st
st.set_page_config(layout="wide")

import os
from soil_config.config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS, CAMADAS_GEOMORFOLOGIA
from soil_config.descricao_solos import descricao_solos
from soil_config.mapa_solos import gerar_mapa_solos
from streamlit_folium import folium_static

# ----------------- CSS: Spinner centralizado -----------------
st.markdown("""
    <style>
    .css-1v0mbdj {
        display: flex;
        justify-content: center;
    }
    .stSpinner {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Sidebar -----------------
st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Selecione uma classe de solo para visualizar com outras camadas")

opcao_solo = st.sidebar.radio(
    "🔍 Visualizar grupo de solos:",
    [
        "Selecionar...",
        "Cambissolos",
        "Luvissolos",
        "Latossolos",
        "Planossolos",
        "Neossolos",
        "Argissolos",
        "Vertissolos",
        "Gleissolos",
        "Chernossolos",
        "Plintossolos",
        "Nitossolos"
    ],
    key="selecao_solo"
)

st.sidebar.markdown("---")
camadas_geomorfologia = st.sidebar.multiselect(
    "🗺️ Camadas geomorfológicas (opcional):",
    options=list(CAMADAS_GEOMORFOLOGIA.keys())
)

# ----------------- Cache: Listagem dos shapefiles disponíveis -----------------
@st.cache_data
def listar_simbolos_disponiveis():
    arquivos = sorted([f for f in os.listdir(CAMINHO_SHAPES) if f.endswith(".shp")])
    return [arquivo.replace(".shp", "") for arquivo in arquivos]

todos_os_simbolos = listar_simbolos_disponiveis()

# ----------------- Mapeamento de prefixos -----------------
grupo_para_prefixo = {
    "Cambissolos": ("C", "CX"),
    "Luvissolos": ("T", "TC"),
    "Latossolos": ("L", "LATOSSOLOS"),
    "Planossolos": ("S", None),
    "Neossolos": ("R", None),
    "Argissolos": ("P", None),
    "Vertissolos": ("V", None),
    "Gleissolos": ("G", None),
    "Chernossolos": ("M", None),
    "Plintossolos": ("F", None),
    "Nitossolos": ("N", None)
}

# ----------------- Layout central -----------------
col1, col2, col3 = st.columns([1, 5, 1])

# ----------------- Página inicial -----------------
if opcao_solo == "Selecionar...":
    with col2:
        st.markdown("<h2 style='text-align: center;'>Bem-vindo ao GeoSAB - Solos</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align: center; font-size: 18px;'>
            Utilize o menu lateral para visualizar os grupos de solos presentes no Semiárido brasileiro.<br>
            Ao selecionar um grupo, o mapa correspondente será carregado aqui.
        </p>
        """, unsafe_allow_html=True)

# ----------------- Quando um solo é selecionado -----------------
else:
    titulo = f"{opcao_solo} no Semiárido"
    prefixo, chave_desc = grupo_para_prefixo.get(opcao_solo, ("", None))

    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{titulo}</h2>", unsafe_allow_html=True)

    # Cache para evitar recarregamento desnecessário
    if "ultimo_solo" not in st.session_state or st.session_state.ultimo_solo != opcao_solo or \
       st.session_state.get("camadas_geomorfologia") != camadas_geomorfologia:

        with col2:
            with st.spinner("🔄 Carregando dados e gerando o mapa..."):
                mapa = gerar_mapa_solos(prefixo, todos_os_simbolos, camadas_geomorfologia)
                st.session_state["mapa"] = mapa
                st.session_state["ultimo_solo"] = opcao_solo
                st.session_state["camadas_geomorfologia"] = camadas_geomorfologia

    # Renderiza mapa já salvo em sessão
    with col2:
        if "mapa" in st.session_state:
            folium_static(st.session_state["mapa"], height=1000, width=2000)

    # Adiciona descrição, se houver
    if chave_desc and chave_desc in descricao_solos:
        with col2:
            st.markdown(descricao_solos[chave_desc], unsafe_allow_html=True)