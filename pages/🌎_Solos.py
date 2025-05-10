# pages/solos.py (Atualizado com download do .zip do Google Drive)

import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import os
import gdown
import zipfile

# Importações dos módulos customizados
from soil_config.config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS
from soil_config.descricao_solos import descricao_solos
from soil_config.utils import adicionar_camada_solo, adicionar_camada_generica

# Configuração da página
st.set_page_config(layout="wide")

# Verifica se os geojsons já estão extraídos
if not os.path.exists(os.path.join(CAMINHO_SHAPES, "CXa.geojson")):
    file_id = "1io9L-rBGI8haOtVJW_TCPqUwHY8MMHUz"
    output = "dados/solos.zip"

    # Baixa o .zip do Google Drive
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

    # Extrai os arquivos para a pasta correta
    with zipfile.ZipFile(output, "r") as zip_ref:
        zip_ref.extractall(CAMINHO_SHAPES)

    os.remove(output)

# Menu lateral
st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Visualize os solos do Semiárido por grupo principal.")

opcao_solo = st.sidebar.radio(
    "🔍 Visualizar grupo de solos:",
    [
        "Cambissolos",
        "Luvissolos",
        "Latossolos",
        "Planossolos",
        "Neossolos",
        "Argissolos"
    ],
    key="selecao_solo"
)

# Título dinâmico
titulo = {
    "Cambissolos": "Cambissolos no Semiárido",
    "Luvissolos": "Luvissolos no Semiárido",
    "Latossolos": "Latossolos no Semiárido",
    "Planossolos": "Planossolos no Semiárido",
    "Neossolos": "Neossolos no Semiárido",
    "Argissolos": "Argissolos no Semiárido"
}[opcao_solo]

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center;'>{titulo}</h2>", unsafe_allow_html=True)

# Obtenção dos arquivos geojson
arquivos_shape = sorted([
    f for f in os.listdir(CAMINHO_SHAPES)
    if f.endswith(".geojson")
])
todos_os_simbolos = [arquivo.replace(".geojson", "") for arquivo in arquivos_shape]

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

# Ativa sempre os limites do semiárido
adicionar_camada_generica(
    mapa,
    "Limites do Semiárido",
    os.path.join("dados", CAMADAS_DISPONIVEIS["Limites do Semiárido"]),
    show=True
)

# Mapeia o grupo para prefixo e descrição
grupo_para_prefixo = {
    "Cambissolos": ("C", "CX"),
    "Luvissolos": ("T", "TC"),
    "Latossolos": ("L", "LATOSSOLOS"),
    "Planossolos": ("S", None),
    "Neossolos": ("R", None),
    "Argissolos": ("P", None)
}

prefixo, chave_desc = grupo_para_prefixo.get(opcao_solo, ("", None))

# Adiciona os solos que começam com o prefixo
for simb in todos_os_simbolos:
    if simb.startswith(prefixo):
        caminho = os.path.join(CAMINHO_SHAPES, f"{simb}.geojson")
        adicionar_camada_solo(mapa, simb, f"Solo {simb}", caminho)

# Adiciona demais camadas (ocultas por padrão)
for nome, arquivo in CAMADAS_DISPONIVEIS.items():
    if nome != "Limites do Semiárido":
        adicionar_camada_generica(
            mapa,
            nome,
            os.path.join("dados", arquivo),
            show=False
        )

# Controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)

# Exibição do mapa
with col2:
    folium_static(mapa, height=1000, width=2000)

    if chave_desc and chave_desc in descricao_solos:
        st.markdown(descricao_solos[chave_desc], unsafe_allow_html=True)