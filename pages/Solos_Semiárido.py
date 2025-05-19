import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

st.title("Visualização Interativa do Semiárido Brasileiro")

# === Checkbox para mostrar latossolos ===
mostrar_latossolos = st.checkbox("Mostrar Latossolos")

# Caminho para o shape do semiárido
caminho_shape_semiarido = os.path.join("dados", "limites_semiarido.shp")

# Lista dos nomes dos arquivos dos latossolos
nomes_latossolos = [
    "LAa", "LAd", "LAdf", "LAdx", "LAe", "LAw",
    "LVAa", "LVAd", "LVAe", "LVd", "LVdf", "LVe", "LVw"
]

# Pasta onde estão os shapes de solos
pasta_solos = os.path.join("dados", "solos_sab250")

# Carrega e exibe o shape do semiárido
if not os.path.exists(caminho_shape_semiarido):
    st.error("Arquivo 'limites_semiarido.shp' não encontrado na pasta 'dados'.")
else:
    try:
        gdf = gpd.read_file(caminho_shape_semiarido)
        geojson_semiarido = gdf.__geo_interface__

        bounds = gdf.total_bounds
        centro_lat = (bounds[1] + bounds[3]) / 2
        centro_lon = (bounds[0] + bounds[2]) / 2

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

        # === Adiciona os Latossolos se checkbox estiver marcada ===
        if mostrar_latossolos:
            for nome in nomes_latossolos:
                caminho_shp = os.path.join(pasta_solos, f"{nome}.shp")
                if os.path.exists(caminho_shp):
                    gdf_lato = gpd.read_file(caminho_shp)
                    geojson_lato = gdf_lato.__geo_interface__

                    folium.GeoJson(
                        geojson_lato,
                        name=f"Latossolo {nome}",
                        style_function=lambda feature: {
                            'fillColor': '#FF8C00',   # laranja suave
                            'color': '#FF4500',
                            'weight': 1,
                            'fillOpacity': 0.4
                        },
                        tooltip=folium.GeoJsonTooltip(fields=[],
                                                      aliases=[],
                                                      labels=False)
                    ).add_to(m)

        # Mostra o mapa ampliado
        st_folium(m, width=1000, height=1500)

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")