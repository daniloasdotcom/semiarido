import geopandas as gpd
import folium
import os
import streamlit as st

from folium.features import GeoJson
from soil_config.config import CORES_SOLOS, CORES_GEOMORFOLOGIA

# -------------------- Função cacheada para leitura de shapefile --------------------
@st.cache_data(show_spinner=False)
def carregar_shapefile(caminho, simplificar=False):
    gdf = gpd.read_file(caminho)

    # Reprojetar para WGS84 se necessário
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    # Simplificar geometria, se solicitado
    if simplificar:
        gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.005, preserve_topology=True)

    return gdf

# -------------------- Camada de solo --------------------
def adicionar_camada_solo(mapa, nome, legenda, caminho):
    gdf = carregar_shapefile(caminho)

    cor = CORES_SOLOS.get(nome, "#666666")  # fallback cinza

    estilo = lambda feature: {
        "fillColor": cor,
        "color": cor,
        "weight": 1,
        "fillOpacity": 0.6
    }

    legenda_html = f"<span style='display:inline-block; width:14px; height:14px; background-color:{cor}; margin-right:6px;'></span>{legenda}"

    folium.GeoJson(
        gdf,
        name=legenda_html,
        style_function=estilo,
        show=True
    ).add_to(mapa)

# -------------------- Camada genérica (ex: geomorfologia) --------------------
def adicionar_camada_generica(mapa, nome, caminho, show=False):
    gdf = carregar_shapefile(caminho, simplificar=True)

    cor_preenchimento = CORES_GEOMORFOLOGIA.get(nome, "#808080")

    estilo = lambda feature: {
        "fillColor": cor_preenchimento,
        "color": "#000000",      # contorno preto
        "weight": 2.5,
        "fillOpacity": 0.2
    }

    folium.GeoJson(
        gdf,
        name=nome,
        style_function=estilo,
        show=show
    ).add_to(mapa)