import geopandas as gpd
import folium
from soil_config.config import CORES_SOLOS, CORES_GEOMORFOLOGIA

def adicionar_camada_solo(mapa, nome, legenda, caminho):
    gdf = gpd.read_file(caminho)

    cor = CORES_SOLOS.get(nome, "#666666")

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
    gdf = gpd.read_file(caminho)

    gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.005, preserve_topology=True)

    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    cor_preenchimento = CORES_GEOMORFOLOGIA.get(nome, "#808080")

    estilo = lambda feature: {
        "fillColor": cor_preenchimento,
        "color": "#000000",
        "weight": 2.5,
        "fillOpacity": 0.2
    }

    folium.GeoJson(
        gdf,
        name=nome,
        style_function=estilo,
        show=show
    ).add_to(mapa)