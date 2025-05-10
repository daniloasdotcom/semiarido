import geopandas as gpd
import folium
import os
from folium.features import GeoJson
from folium import LayerControl

from soil_config.config import CORES_SOLOS # ← Certifique-se de que esse dicionário está no config.py


def adicionar_camada_solo(mapa, nome, legenda, caminho):
    import geopandas as gpd
    import folium
    from soil_config.config import CORES_SOLOS  # ← nome correto agora

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
    Adiciona uma camada genérica ao mapa (ex: limites, vegetação).
    """
    gdf = gpd.read_file(caminho)

    estilo = lambda feature: {
        "fillColor": "#00000000",
        "color": "#000000",
        "weight": 2,
        "fillOpacity": 0.0
    }

    folium.GeoJson(
        gdf,
        name=nome,
        style_function=estilo,
        show=show
    ).add_to(mapa)