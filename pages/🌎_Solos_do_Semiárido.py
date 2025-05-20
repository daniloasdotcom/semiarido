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

# Centralização com colunas
col_esq, col_centro, col_dir = st.columns([1, 6, 1])

with col_centro:
    st.markdown("""
        <script>
            const body = window.parent.document.body;
            const spinner = document.createElement("div");
            spinner.id = "global-spinner";
            spinner.innerHTML = '<div style="position:fixed; top:1rem; right:1rem; background:#f0f0f0; padding:10px 20px; border:1px solid #ccc; border-radius:5px; z-index:9999; box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-family:sans-serif;">🔄 Carregando...</div>';
            if (!body.querySelector("#global-spinner")) {
                body.appendChild(spinner);
            }
            const observer = new MutationObserver(() => {
                const status = body.querySelector('[data-testid="stStatusWidget"]');
                if (status && status.style.display === "none") {
                    const existing = body.querySelector("#global-spinner");
                    if (existing) existing.remove();
                }
            });
            observer.observe(body, { childList: true, subtree: true });
        </script>
    """, unsafe_allow_html=True)
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
            with st.spinner("🔄 Carregando dados e montando o mapa..."):
                gdf = gpd.read_file(caminho_shape_semiarido)
                bounds = gdf.total_bounds
                centro_lat = (bounds[1] + bounds[3]) / 2
                centro_lon = (bounds[0] + bounds[2]) / 2

                # Criação do mapa base ...

            # Criação do mapa base sem camada padrão
            m = folium.Map(location=[centro_lat, centro_lon], zoom_start=6, tiles=None, control_scale=True)

            # Adiciona camada base nomeada
            folium.TileLayer(
                tiles="CartoDB positron",
                name="Mapa Base Claro",
                control=True
            ).add_to(m)

            # Botão de tela cheia
            Fullscreen(position="topright").add_to(m)

            # Limites do semiárido
            folium.GeoJson(
                gdf.__geo_interface__,
                name="Limites do Semiárido",
                style_function=lambda feature: {
                    'fillColor': 'none',
                    'color': 'black',
                    'weight': 3
                }
            ).add_to(m)

            # Solo selecionado
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
                            name=tipo,
                            style_function=lambda feature, cor=cor: {
                                'fillColor': cor,
                                'color': cor,
                                'weight': 1,
                                'fillOpacity': 0.5
                            }
                        ).add_to(m)

                    # Legenda
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

            # Checkboxes centralizados entre legenda e mapa
            st.markdown("### Camadas adicionais")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.checkbox("Estados do Semiárido", key="opt_estados")
            with c2:
                st.checkbox("Caatinga", key="opt_caatinga")

            # Camada de Estados do Semiárido (opção 1)
            # Camada de Estados do Semiárido
            if st.session_state.get("opt_estados"):
                caminho_estados = os.path.join("dados", "estados", "Estados_Semiarido.shp")
                if os.path.exists(caminho_estados):
                    gdf_estados = gpd.read_file(caminho_estados)
                    folium.GeoJson(
                        gdf_estados.__geo_interface__,
                        name="Estados do Semiárido",
                        style_function=lambda feature: {
                            'fillColor': 'none',
                            'color': 'black',
                            'weight': 3
                        }
                    ).add_to(m)

            # Camada da Caatinga
            if st.session_state.get("opt_caatinga"):
                caminho_caatinga = os.path.join("dados", "caatinga", "Caatinga.shp")
                if os.path.exists(caminho_caatinga):
                    gdf_caatinga = gpd.read_file(caminho_caatinga)
                    folium.GeoJson(
                        gdf_caatinga.__geo_interface__,
                        name="Caatinga",
                        style_function=lambda feature: {
                            'fillColor': 'none',
                            'color': 'black',
                            'weight': 3
                        }
                    ).add_to(m)

            # Layer control e exibição do mapa
            folium.LayerControl(collapsed=False, position="topright").add_to(m)

            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            st_folium(m, height=1000, use_container_width=True)

            # Estilo para LayerControl
            st.markdown("""
            <style>
            .leaflet-control-layers {
                max-height: 300px !important;
                max-width: 200px !important;
                overflow-y: auto !important;
                font-size: 13px;
                padding: 5px;
            }
            </style>
            """, unsafe_allow_html=True)

            # Descrição do solo
            st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
            chave = "LATOSSOLOS" if tipo_solo == "Latossolo" else "CAMBISSOLOS" if tipo_solo == "Cambissolo" else None
            if chave and chave in descricao_solos:
                st.markdown("### Sobre este tipo de solo")
                st.markdown(descricao_solos[chave], unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")