import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static
import os
import time

# Configuração da página
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("🛰️ Visualizador Geográfico")
st.sidebar.markdown("Explore os municípios da Caatinga, os limites do Semiárido e os estados abrangidos.")

# Título centralizado
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown("## Visualizador Interativo - Caatinga e Semiárido")

# Caminhos dos shapefiles
path_caatinga = os.path.join("dados", "Municipios_caatinga.shp")
path_semiarido = os.path.join("dados", "limites_semiarido.shp")
path_estados = os.path.join("dados", "Estados_Semiarido.shp")

# Spinner com mensagem centralizada
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    with st.spinner("🗺️ **Carregando o mapa, por favor aguarde...**"):
        time.sleep(0.5)

        # Mapa com localização e zoom fixos
        mapa = folium.Map(location=[-13, -40], zoom_start=5, control_scale=True)

        # Tela cheia
        Fullscreen(position="topright").add_to(mapa)

        # Camadas base
        folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(mapa)

        folium.TileLayer(
            tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
            name='Terreno',
            attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
        ).add_to(mapa)

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

        # Estilo das camadas vetoriais
        def estilo(cor):
            return lambda x: {
                "color": cor,
                "weight": 1,
                "fillOpacity": 0.2,
            }

        # Camada 1: Municípios da Caatinga
        if os.path.exists(path_caatinga):
            gdf1 = gpd.read_file(path_caatinga)
            folium.GeoJson(
                gdf1,
                name="Municípios Caatinga",
                style_function=estilo("blue")
            ).add_to(mapa)

        # Camada 2: Limites do Semiárido
        if os.path.exists(path_semiarido):
            gdf2 = gpd.read_file(path_semiarido)
            folium.GeoJson(
                gdf2,
                name="Limites do Semiárido",
                style_function=estilo("green")
            ).add_to(mapa)

        # Camada 3: Estados no Semiárido
        if os.path.exists(path_estados):
            gdf3 = gpd.read_file(path_estados)
            if not gdf3.empty:
                folium.GeoJson(
                    gdf3,
                    name="Estados no Semiárido",
                    style_function=estilo("red")
                ).add_to(mapa)
            else:
                st.warning("⚠️ Shapefile 'Estados_Semiarido' está vazio.")
        else:
            st.error("❌ Shapefile 'Estados_Semiarido' não encontrado.")

        # Controle de camadas
        folium.LayerControl(collapsed=False).add_to(mapa)

        # Renderiza o mapa centralizado
        with col2:
            folium_static(mapa, height=600)

# Mensagem de sucesso temporária
mensagem = st.empty()
with mensagem.container():
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.success("✅ Mapa carregado com sucesso.")
time.sleep(3)
mensagem.empty()