import folium
import os
import geopandas as gpd
import pandas as pd
from folium.plugins import Fullscreen
import streamlit as st
from matplotlib import cm

from .utils import adicionar_camada_solo, adicionar_camada_generica
from .config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS, CAMADAS_GEOMORFOLOGIA, CORES_SOLOS

def gerar_mapa_solos(prefixo, todos_os_simbolos, camadas_geomorfologicas):
    with st.spinner('🔄 Carregando dados do solo e gerando o mapa...'):
        mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True, tiles=None)
        Fullscreen(position="topright").add_to(mapa)

        folium.TileLayer(
            tiles='https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
            name='Preto e Branco',
            attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
        ).add_to(mapa)

        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            name="Satélite (Esri)",
            attr="Tiles © Esri & the GIS community"
        ).add_to(mapa)

        folium.TileLayer(
            tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            name='Claro',
            attr='© CartoDB'
        ).add_to(mapa)

        adicionar_camada_generica(
            mapa,
            "Limites do Semiárido",
            os.path.join("dados", CAMADAS_DISPONIVEIS["Limites do Semiárido"]),
            show=True
        )

        gdfs = []
        simbolos_filtrados = [s for s in todos_os_simbolos if s.startswith(prefixo)]

        # Gerar cores únicas e atualizar dicionário global
        cores_cmap = cm.get_cmap('tab20', len(simbolos_filtrados))
        CORES_SOLOS.clear()
        CORES_SOLOS.update({
            simb: f'#{int(cores_cmap(i)[0]*255):02x}{int(cores_cmap(i)[1]*255):02x}{int(cores_cmap(i)[2]*255):02x}'
            for i, simb in enumerate(simbolos_filtrados)
        })

        for simb in simbolos_filtrados:
            caminho = os.path.join(CAMINHO_SHAPES, f"{simb}.gpkg")
            try:
                gdf = gpd.read_file(caminho, layer=simb)
                gdf["COD_SIMBOL"] = simb
                if "LEGENDA" not in gdf.columns:
                    gdf["LEGENDA"] = gdf.get("legenda", simb)
                gdfs.append(gdf)

                # Atualize aqui se a função também precisa receber .gpkg
                adicionar_camada_solo(mapa, simb, f"Solo {simb}", caminho, layer=simb)
            except Exception as e:
                st.warning(f"Erro ao carregar {simb}: {e}")

        if gdfs:
            gdf_clipado = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
            gdf_clipado.set_crs("EPSG:4674", inplace=True, allow_override=True)
        else:
            gdf_clipado = gpd.GeoDataFrame()

        for nome, arquivo in CAMADAS_DISPONIVEIS.items():
            if nome != "Limites do Semiárido":
                adicionar_camada_generica(mapa, nome, os.path.join("dados", arquivo), show=False)

        for nome in camadas_geomorfologicas:
            caminho = os.path.join("dados", CAMADAS_GEOMORFOLOGIA[nome])
            adicionar_camada_generica(mapa, nome, caminho, show=True)

        folium.LayerControl(collapsed=False).add_to(mapa)

        return mapa, gdf_clipado