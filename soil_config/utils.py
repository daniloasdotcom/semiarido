import geopandas as gpd
import folium
import os
from folium.features import GeoJson
from folium import LayerControl

from soil_config.config import CORES_SOLOS, CORES_GEOMORFOLOGIA  # ← Certifique-se de que esse dicionário está no config.py


def adicionar_camada_solo(mapa, nome, legenda, caminho):
    gdf = gpd.read_file(caminho)

    cor = CORES_SOLOS.get(nome, "#666666")  # nome = símbolo como "SXe", "SNz", etc.

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


def adicionar_camada_generica(mapa, nome, caminho, show=False):
    """
    Adiciona uma camada genérica ao mapa (ex: geomorfologia),
    com preenchimento colorido e contorno preto espesso.
    """
    gdf = gpd.read_file(caminho)

    # Simplificar geometria
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.005, preserve_topology=True)

    # Reprojetar se necessário
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    cor_preenchimento = CORES_GEOMORFOLOGIA.get(nome, "#808080")  # Cor padrão caso não esteja no dicionário

    estilo = lambda feature: {
        "fillColor": cor_preenchimento,
        "color": "#000000",           # contorno preto
        "weight": 2.5,                # espessura do contorno
        "fillOpacity": 0.2           # transparência do preenchimento
    }

    folium.GeoJson(
        gdf,
        name=nome,
        style_function=estilo,
        show=show
    ).add_to(mapa)