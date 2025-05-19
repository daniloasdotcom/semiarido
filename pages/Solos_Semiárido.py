import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium
import os
from utils.solos import carregar_geojson, calcular_area_por_tipo
from utils.descricao_solos import descricao_solos

# Layout wide
st.set_page_config(layout="wide")

# Colunas para centralização
col_esq, col_centro, col_dir = st.columns([1, 6, 1])

with col_centro:
    st.title("Visualização Interativa do Semiárido Brasileiro")

    tipo_solo = st.selectbox("Selecione o tipo de solo para visualizar:", ["Nenhum", "Latossolo", "Cambissolo"])

    # Caminhos e cores
    caminho_shape_semiarido = os.path.join("dados", "limites_semiarido.shp")
    geojson_solos = {
        "Latossolo": os.path.join("dados", "latossolos_simplificado.geojson"),
        "Cambissolo": os.path.join("dados", "cambissolos_simplificado.geojson")
    }

    cores_latossolo = {
        "LAa": "#eb4d1c", "LAd": "#e31239", "LAdf": "#0000ff", "LAdx": "#8ce8c3", "LAe": "#c28ee8",
        "LAw": "#0fd3f3", "LVAa": "#0000ff", "LVAd": "#f44336", "LVAe": "#de8782", "LVd": "#5e71cf",
        "LVdf": "#0e00ff", "LVe": "#09f745", "LVw": "#99dc3c"
    }

    cores_cambissolo = {
        "CXa": "#ff00ff", "CXbd": "#c0d904", "CXbe": "#6f7fc7",
        "CXk": "#c0d904", "CXve": "#b50057", "CYbe": "#6f7fc7"
    }

    if not os.path.exists(caminho_shape_semiarido):
        st.error("Arquivo 'limites_semiarido.shp' não encontrado.")
    else:
        try:
            gdf = gpd.read_file(caminho_shape_semiarido)
            bounds = gdf.total_bounds
            centro_lat = (bounds[1] + bounds[3]) / 2
            centro_lon = (bounds[0] + bounds[2]) / 2

            # Mapa base com tela cheia e controle reposicionado
            m = folium.Map(location=[centro_lat, centro_lon], zoom_start=6, tiles="CartoDB positron", control_scale=True)
            Fullscreen(position="topright", title="Tela cheia", title_cancel="Sair da tela cheia").add_to(m)

            # Contorno do semiárido
            folium.GeoJson(
                gdf.__geo_interface__,
                name="Limites do Semiárido",
                style_function=lambda feature: {
                    'fillColor': 'none',
                    'color': 'black',
                    'weight': 3
                }
            ).add_to(m)

            if tipo_solo in geojson_solos:
                caminho = geojson_solos[tipo_solo]
                gdf_solo = carregar_geojson(caminho)

                if gdf_solo is not None and "cod_simbol" in gdf_solo.columns and "legenda" in gdf_solo.columns:
                    cores = cores_latossolo if tipo_solo == "Latossolo" else cores_cambissolo

                    for tipo in gdf_solo["cod_simbol"].unique():
                        geojson_tipo = gdf_solo[gdf_solo["cod_simbol"] == tipo].__geo_interface__
                        cor = cores.get(tipo, "#888888")

                        folium.GeoJson(
                            geojson_tipo,
                            name=tipo,  # Apenas o código no LayerControl
                            style_function=lambda feature, cor=cor: {
                                'fillColor': cor,
                                'color': cor,
                                'weight': 1,
                                'fillOpacity': 0.5
                            }
                        ).add_to(m)

                    # Legenda com cor, área e % em HTML
                    df_legenda = calcular_area_por_tipo(gdf_solo)
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
                    st.warning("GeoJSON inválido ou sem colunas 'cod_simbol' e 'legenda'.")
            else:
                st.warning(f"Arquivo do solo '{tipo_solo}' não encontrado.")

            # Controles de mapa
            folium.LayerControl(collapsed=False, position="topleft").add_to(m)

            # Espaço e exibição do mapa
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            st_folium(m, width=1000, height=1000)

            # Descrição abaixo do mapa
            st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
            chave = "LATOSSOLOS" if tipo_solo == "Latossolo" else "CX" if tipo_solo == "Cambissolo" else None
            if chave and chave in descricao_solos:
                st.markdown("### Sobre este tipo de solo")
                st.markdown(descricao_solos[chave], unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")