import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import os

# Configuração da página
st.set_page_config(layout="wide")

st.sidebar.title("🧱 Visualizador de Solos")
st.sidebar.markdown("Visualize todas as camadas de solos do semiárido com controle individual.")

st.markdown("## Solos do Semiárido - Todas as Camadas")

# Caminho dos arquivos .shp
CAMINHO_SHAPES = "dados"

# Dicionário de cores por tipo de solo
CORES_SOLOS = {
    "AR": "saddlebrown", "CX": "darkorange", "ES": "darkgoldenrod", "FF": "darkmagenta",
    "FX": "indigo", "GX": "slategray", "GZ": "lightseagreen", "LA": "seagreen",
    "LV": "darkgreen", "LVA": "limegreen", "MD": "orchid", "MT": "plum",
    "Magua0": "goldenrod", "Magua1": "khaki", "PA": "coral", "PAC": "tomato",
    "PV": "chocolate", "PVA": "burlywood", "RL": "peru", "RQ": "olive",
    "RR": "mediumseagreen", "RU": "crimson", "SG": "steelblue", "SN": "midnightblue",
    "SX": "teal", "TC": "cadetblue", "VC": "hotpink", "VE": "salmon"
}

# Lista de arquivos COD_SIMBOL_*.shp
arquivos_shape = sorted([
    f for f in os.listdir(CAMINHO_SHAPES)
    if f.startswith("COD_SIMBOL_") and f.endswith(".shp")
])

# Camadas adicionais e seus caminhos
camadas_disponiveis = {
    "Limites do Semiárido": "limites_semiarido.shp",
    "Estados do Semiárido": "Estados_Semiarido.shp"
}

# Interface: escolha da ordem das camadas adicionais
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    ordem_camadas = st.multiselect(
        "🧩 Escolha e ordene as camadas adicionais:",
        options=list(camadas_disponiveis.keys()),
        default=[],
        help="Arraste para definir a ordem de sobreposição"
    )

# Criar mapa base
mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True)
Fullscreen(position="topright").add_to(mapa)

# Camadas base
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(mapa)
folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    name='Claro',
    attr='© CartoDB'
).add_to(mapa)
folium.TileLayer(
    tiles='https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
    name='Preto e Branco',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
).add_to(mapa)

# Adicionar camadas de solo
for arquivo in arquivos_shape:
    nome_base = arquivo.replace("COD_SIMBOL_", "").replace(".shp", "")
    caminho = os.path.join(CAMINHO_SHAPES, arquivo)

    try:
        gdf = gpd.read_file(caminho)
        if gdf.crs is None:
            gdf.set_crs(epsg=4674, inplace=True)

        cor = CORES_SOLOS.get(nome_base, "gray")

        folium.GeoJson(
            gdf,
            name=f"Solo {nome_base}",
            style_function=lambda x, cor=cor: {
                "color": cor,
                "weight": 1,
                "fillOpacity": 0.4
            }
        ).add_to(mapa)

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar {arquivo}: {e}")

# Adicionar camadas adicionais na ordem selecionada
for nome_camada in ordem_camadas:
    caminho = os.path.join(CAMINHO_SHAPES, camadas_disponiveis[nome_camada])
    if os.path.exists(caminho):
        try:
            gdf = gpd.read_file(caminho)
            if gdf.crs is None:
                gdf.set_crs(epsg=4674, inplace=True)

            cor = "green" if "Limites" in nome_camada else "red"

            folium.GeoJson(
                gdf,
                name=nome_camada,
                style_function=lambda x, cor=cor: {
                    "color": cor,
                    "weight": 2 if cor == "green" else 1.5,
                    "fillOpacity": 0
                }
            ).add_to(mapa)
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar {nome_camada}: {e}")

# Controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)

# Exibir mapa com altura suficiente
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    folium_static(mapa, height=1000)