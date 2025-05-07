# pages/solos.py

import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import os

# Importações dos módulos customizados
from soil_config.config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS, CORES_SOLOS
from soil_config.descricao_solos import descricao_solos
from soil_config.utils import carregar_shapefile, adicionar_camada_solo, adicionar_camada_generica

# Configuração da página
st.set_page_config(layout="wide")

# Menu lateral
st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Visualize as camadas de solos ou explore um tipo específico.")

opcao_solo = st.sidebar.radio(
    "🔍 Visualizar por:",
    ["Todas as camadas", "Cambissolos (CX)", "Luvissolos (TC)", "Latossolos (LA, LV, LVA)"],
    key="selecao_solo"
)

# Título dinâmico
titulo = {
    "Cambissolos (CX)": "Cambissolos (CX) no Semiárido",
    "Luvissolos (TC)": "Luvissolos (TC) no Semiárido",
    "Latossolos (LA, LV, LVA)": "Latossolos no Semiárido"
}.get(opcao_solo, "Solos do Semiárido")

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center;'>{titulo}</h2>", unsafe_allow_html=True)

# Seletor de camadas adicionais
if opcao_solo == "Todas as camadas":
    with col2:
        st.markdown(
            "<label style='font-size:18px; font-weight:bold;'>🧩 Escolha e ordene as camadas adicionais:</label>",
            unsafe_allow_html=True
        )
        ordem_camadas = st.multiselect(
            "",
            options=list(CAMADAS_DISPONIVEIS.keys()),
            default=[],
            help="Arraste para definir a ordem de sobreposição"
        )
        exibir_todos = st.checkbox("Exibir todas as camadas de solo", value=True, key="exibir_solos_checkbox")

# Criação do mapa
mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True, tiles=None)
Fullscreen(position="topright").add_to(mapa)

# Camadas base
folium.TileLayer(
    tiles='https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
    name='Preto e Branco',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
).add_to(mapa)

folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    name='Claro',
    attr='© CartoDB'
).add_to(mapa)

# Obtenção dos arquivos de solo
arquivos_shape = sorted([
    f for f in os.listdir(CAMINHO_SHAPES)
    if f.startswith("COD_SIMBOL_") and f.endswith(".shp")
])

# Exibição de camadas
if opcao_solo == "Todas as camadas":
    for arquivo in arquivos_shape:
        simb = arquivo.replace("COD_SIMBOL_", "").replace(".shp", "")
        caminho = os.path.join(CAMINHO_SHAPES, arquivo)
        adicionar_camada_solo(mapa, simb, f"Solo {simb}", caminho)

    for camada in ordem_camadas:
        caminho = os.path.join(CAMINHO_SHAPES, CAMADAS_DISPONIVEIS[camada])
        adicionar_camada_generica(mapa, camada, caminho)

else:
    # Sempre ativa o limite do semiárido
    adicionar_camada_generica(
        mapa,
        "Limites do Semiárido",
        os.path.join(CAMINHO_SHAPES, CAMADAS_DISPONIVEIS["Limites do Semiárido"]),
        show=True
    )

    if opcao_solo == "Latossolos (LA, LV, LVA)":
        for simb in ["LA", "LV", "LVA"]:
            adicionar_camada_solo(mapa, simb, f"Latossolo {simb}", os.path.join(CAMINHO_SHAPES, f"COD_SIMBOL_{simb}.shp"))
    else:
        simb = "CX" if "CX" in opcao_solo else "TC"
        adicionar_camada_solo(mapa, simb, f"Solo {simb}", os.path.join(CAMINHO_SHAPES, f"COD_SIMBOL_{simb}.shp"))

    # As demais camadas são adicionadas, mas ocultas por padrão
    for nome, arquivo in CAMADAS_DISPONIVEIS.items():
        if nome != "Limites do Semiárido":
            adicionar_camada_generica(
                mapa,
                nome,
                os.path.join(CAMINHO_SHAPES, arquivo),
                show=False
            )

# Controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)

# Exibição do mapa
with col2:
    folium_static(mapa, height=1000, width=2000)

    # Descrição do solo (se aplicável)
    if opcao_solo in ["Cambissolos (CX)", "Luvissolos (TC)", "Latossolos (LA, LV, LVA)"]:
        chave = "LATOSSOLOS" if "Latossolos" in opcao_solo else "CX" if "CX" in opcao_solo else "TC"
        st.markdown(descricao_solos[chave], unsafe_allow_html=True)