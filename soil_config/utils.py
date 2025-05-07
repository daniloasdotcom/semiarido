# soil_config/utils.py

import geopandas as gpd
import folium
import streamlit as st
from soil_config.config import CORES_SOLOS

@st.cache_data(show_spinner=False)
def carregar_shapefile(caminho):
    gdf = gpd.read_file(caminho)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    return gdf

def adicionar_camada_solo(mapa, simbolo, nome, caminho):
    try:
        gdf = carregar_shapefile(caminho)
        cor = CORES_SOLOS.get(simbolo, "gray")
        folium.GeoJson(
            gdf,
            name=nome,
            style_function=lambda x, cor=cor: {
                "color": cor,
                "weight": 1,
                "fillOpacity": 0.4
            }
        ).add_to(mapa)
    except Exception as e:
        st.warning(f"Erro ao carregar solo {simbolo}: {e}")

def adicionar_camada_generica(mapa, nome, caminho, show=True):
    try:
        gdf = carregar_shapefile(caminho)
        folium.GeoJson(
            gdf,
            name=nome,
            show=show,
            style_function=lambda x: {
                "color": "black",
                "weight": 3,
                "fillOpacity": 0
            }
        ).add_to(mapa)
    except Exception as e:
        st.warning(f"Erro ao carregar camada '{nome}': {e}")