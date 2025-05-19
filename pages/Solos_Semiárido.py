import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

st.title("Visualização Interativa do Semiárido Brasileiro")

# Checkbox para ativar a visualização dos Latossolos
mostrar_latossolos = st.checkbox("Mostrar Latossolos")

# Caminho para os arquivos
caminho_shape_semiarido = os.path.join("dados", "limites_semiarido.shp")
caminho_geojson_latossolos = os.path.join("dados", "latossolos_simplificado.geojson")

# Verifica se o shape do semiárido existe
if not os.path.exists(caminho_shape_semiarido):
    st.error("Arquivo 'limites_semiarido.shp' não encontrado.")
else:
    try:
        # Carrega o shapefile do semiárido
        gdf = gpd.read_file(caminho_shape_semiarido)
        geojson_semiarido = gdf.__geo_interface__

        # Centraliza no centro da geometria
        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
        centro_lat = (bounds[1] + bounds[3]) / 2
        centro_lon = (bounds[0] + bounds[2]) / 2

        # Cria o mapa
        m = folium.Map(location=[centro_lat, centro_lon], zoom_start=6, tiles="CartoDB positron")

        # Adiciona o contorno do semiárido
        folium.GeoJson(
            geojson_semiarido,
            name="Limites do Semiárido",
            style_function=lambda feature: {
                'fillColor': 'none',
                'color': 'black',
                'weight': 3
            }
        ).add_to(m)

        # Se a checkbox estiver marcada, carrega o GeoJSON dos Latossolos
        if mostrar_latossolos:
            if os.path.exists(caminho_geojson_latossolos):
                gdf_lato = gpd.read_file(caminho_geojson_latossolos)
                geojson_lato = gdf_lato.__geo_interface__

                folium.GeoJson(
                    geojson_lato,
                    name="Latossolos",
                    style_function=lambda feature: {
                        'fillColor': '#FF8C00',    # Laranja suave
                        'color': '#FF4500',
                        'weight': 1,
                        'fillOpacity': 0.4
                    }
                ).add_to(m)
            else:
                st.warning("Arquivo 'latossolos_simplificado.geojson' não encontrado.")

        # Exibe o mapa
        st_folium(m, width=1000, height=1500)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")