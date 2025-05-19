import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
import pandas as pd

# Modo wide
st.set_page_config(layout="wide")
st.title("Visualização Interativa do Semiárido Brasileiro")

# Dropdown do tipo de solo
tipo_solo = st.selectbox("Selecione o tipo de solo para visualizar:", ["Nenhum", "Latossolo", "Cambissolo"])

# Caminhos
caminho_shape_semiarido = os.path.join("dados", "limites_semiarido.shp")
geojson_solos = {
    "Latossolo": os.path.join("dados", "latossolos_simplificado.geojson"),
    "Cambissolo": os.path.join("dados", "cambissolos_simplificado.geojson")
}

# Cores
cores_latossolo = {
    "LAa": "#eb4d1c", "LAd": "#e31239", "LAdf": "#0000ff", "LAdx": "#8ce8c3", "LAe": "#c28ee8",
    "LAw": "#0fd3f3", "LVAa": "#0000ff", "LVAd": "#f44336", "LVAe": "#de8782", "LVd": "#5e71cf",
    "LVdf": "#0e00ff", "LVe": "#09f745", "LVw": "#99dc3c"
}

cores_cambissolo = {
    "CXa": "#ff00ff", "CXbd": "#c0d904", "CXbe": "#6f7fc7",
    "CXk": "#c0d904", "CXve": "#b50057", "CYbe": "#6f7fc7"
}

# Verifica o shapefile do semiárido
if not os.path.exists(caminho_shape_semiarido):
    st.error("Arquivo 'limites_semiarido.shp' não encontrado.")
else:
    try:
        gdf = gpd.read_file(caminho_shape_semiarido)
        geojson_semiarido = gdf.__geo_interface__

        bounds = gdf.total_bounds
        centro_lat = (bounds[1] + bounds[3]) / 2
        centro_lon = (bounds[0] + bounds[2]) / 2

        m = folium.Map(location=[centro_lat, centro_lon], zoom_start=6, tiles="CartoDB positron")

        # Contorno do semiárido
        folium.GeoJson(
            geojson_semiarido,
            name="Limites do Semiárido",
            style_function=lambda feature: {
                'fillColor': 'none',
                'color': 'black',
                'weight': 3
            }
        ).add_to(m)

        # Adiciona os solos se selecionado
        if tipo_solo in ["Latossolo", "Cambissolo"]:
            caminho_geojson = geojson_solos[tipo_solo]
            if os.path.exists(caminho_geojson):
                gdf_solo = gpd.read_file(caminho_geojson)

                if "cod_simbol" in gdf_solo.columns and "legenda" in gdf_solo.columns:
                    tipos_unicos = gdf_solo["cod_simbol"].unique()
                    cores = cores_latossolo if tipo_solo == "Latossolo" else cores_cambissolo

                    # Adiciona camadas ao mapa
                    for tipo in tipos_unicos:
                        gdf_tipo = gdf_solo[gdf_solo["cod_simbol"] == tipo]
                        geojson_tipo = gdf_tipo.__geo_interface__
                        cor = cores.get(tipo, "#888888")

                        folium.GeoJson(
                            geojson_tipo,
                            name=f"{tipo_solo} {tipo}",
                            style_function=lambda feature, cor=cor: {
                                'fillColor': cor,
                                'color': cor,
                                'weight': 1,
                                'fillOpacity': 0.5
                            }
                        ).add_to(m)

                    # LEGENDAS COM ÁREA E PORCENTAGEM
                    try:
                        gdf_area = gdf_solo.to_crs(epsg=5880)
                    except:
                        gdf_area = gdf_solo.to_crs(gdf_solo.estimate_utm_crs())

                    gdf_area["area_km2"] = gdf_area["geometry"].area / 1_000_000

                    df_legenda = gdf_area.groupby(["cod_simbol", "legenda"]).agg(
                        area_km2=("area_km2", "sum")
                    ).reset_index()

                    area_total = df_legenda["area_km2"].sum()
                    df_legenda["percentual"] = (df_legenda["area_km2"] / area_total * 100).round(2)
                    df_legenda = df_legenda.sort_values(by="area_km2", ascending=False)

                    st.markdown(f"### Legenda dos {tipo_solo}s")

                    for _, row in df_legenda.iterrows():
                        tipo = row["cod_simbol"]
                        desc = row["legenda"]
                        cor = cores.get(tipo, "#888888")
                        area = row["area_km2"]
                        perc = row["percentual"]

                        st.markdown(
                            f"<div style='display: flex; align-items: center; gap: 0.5rem;'>"
                            f"<div style='width: 18px; height: 18px; background-color: {cor}; border: 1px solid #000;'></div>"
                            f"<span><strong>{tipo}</strong>: {desc} — {area:,.1f} km² ({perc}%)</span>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("Colunas 'cod_simbol' ou 'legenda' não encontradas no GeoJSON.")
            else:
                st.warning(f"Arquivo '{caminho_geojson}' não encontrado.")

        folium.LayerControl(collapsed=False).add_to(m)
        st_folium(m, width=1000, height=1200)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")