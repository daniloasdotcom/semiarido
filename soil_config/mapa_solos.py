import folium
import os
from folium.plugins import Fullscreen
import streamlit as st

from .utils import adicionar_camada_solo, adicionar_camada_generica
from .config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS, CAMADAS_GEOMORFOLOGIA

@st.cache_data(show_spinner=False)
def gerar_mapa_solos(prefixo, todos_os_simbolos, camadas_geomorfologicas):
    mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True, tiles=None)
    Fullscreen(position="topright").add_to(mapa)

    # Base layers
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

    # Camada fixa: limites do semiárido
    adicionar_camada_generica(
        mapa,
        "Limites do Semiárido",
        os.path.join("dados", CAMADAS_DISPONIVEIS["Limites do Semiárido"]),
        show=True
    )

    # Camadas de solo (filtradas por prefixo)
    for simb in todos_os_simbolos:
        if simb.startswith(prefixo):
            caminho = os.path.join(CAMINHO_SHAPES, f"{simb}.shp")
            adicionar_camada_solo(mapa, simb, f"Solo {simb}", caminho)

    # Camadas adicionais (não-geomorfológicas)
    for nome, arquivo in CAMADAS_DISPONIVEIS.items():
        if nome != "Limites do Semiárido":
            adicionar_camada_generica(
                mapa,
                nome,
                os.path.join("dados", arquivo),
                show=False
            )

    # Camadas de geomorfologia selecionadas
    for nome in camadas_geomorfologicas:
        caminho = os.path.join("dados", CAMADAS_GEOMORFOLOGIA[nome])
        adicionar_camada_generica(mapa, nome, caminho, show=True)

    folium.LayerControl(collapsed=False).add_to(mapa)

    return mapa