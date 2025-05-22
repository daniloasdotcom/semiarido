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
st.sidebar.image("images/logo_geosab.webp")

st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
        Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

col_esq, col_centro, col_dir = st.columns([1, 6, 1])

with col_centro:
    st.title("Visualização Interativa do Semiárido Brasileiro")

    # 1. Dropdown
    tipo_solo = st.selectbox(
        "Selecione o tipo de solo para visualizar:",
        ["Nenhum", "Latossolo", "Cambissolo", "Luvissolo", "Argissolo"]
    )

    cores_solos = {
        "Latossolo": {
            "LAa": "#eb4d1c", "LAd": "#e31239", "LAdf": "#0000ff", "LAdx": "#8ce8c3", "LAe": "#c28ee8",
            "LAw": "#0fd3f3", "LVAa": "#0000ff", "LVAd": "#f44336", "LVAe": "#de8782", "LVd": "#5e71cf",
            "LVdf": "#0e00ff", "LVe": "#09f745", "LVw": "#99dc3c"
        },
        "Cambissolo": {
            "CXa": "#ff00ff", "CXbd": "#c0d904", "CXbe": "#6f7fc7", "CXk": "#c0d904", "CXve": "#b50057", "CYbe": "#6f7fc7"
        },
        "Luvissolo": {
            "TCk": "#00ef32", "TCo": "#dada48", "TCp": "#cc8a73", "TXp": "#e6cd69"
        },
        "Argissolo": {
            "PACd": "#3a00a6", "PAd": "#3f92bf", "PAdx": "#ff00ff", "PAe": "#07d928",
            "PVa": "#6aff5d", "PVAd": "#d673d8", "PVAe": "#4dff98", "PVd": "#87c3ea", "PVe": "#66c8cf"
        }
    }

    geojson_solos = {
        "Latossolo": os.path.join("dados", "latossolos_simplificado.geojson"),
        "Cambissolo": os.path.join("dados", "cambissolos_simplificado.geojson"),
        "Luvissolo": os.path.join("dados", "luvissolos_simplificado.geojson"),
        "Argissolo": os.path.join("dados", "argissolos_simplificado.geojson")
    }

    # Overlay de carregamento
    loading_overlay = st.empty()
    loading_overlay.markdown("""
    <div id="overlay-loading">
        <div class="loader-text">🔄 Carregando dados...</div>
    </div>
    <style>
    #overlay-loading {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(255,255,255,0.85);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .loader-text {
        font-size: 2rem;
        color: #333;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        selecionados = []
        gdf_solo = None

        # 2. Grid de subtipos
        if tipo_solo != "Nenhum":
            caminho = geojson_solos.get(tipo_solo)
            gdf_solo = carregar_geojson(caminho)

            if gdf_solo is not None and "cod_simbol" in gdf_solo.columns:
                cores = cores_solos.get(tipo_solo, {})
                subtipos = sorted(gdf_solo["cod_simbol"].unique())
                col1, col2, col3 = st.columns(3)
                for i, subtipo in enumerate(subtipos):
                    col = [col1, col2, col3][i % 3]
                    if col.checkbox(subtipo, key=f"chk_{subtipo}"):
                        selecionados.append(subtipo)

        # 3. Camadas adicionais
        st.markdown("### Camadas adicionais")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.checkbox("Estados do Semiárido", key="opt_estados")
        with c2:
            st.checkbox("Caatinga", key="opt_caatinga")
        with c3:
            st.checkbox("MATOPIBA", key="opt_matopiba")

        # 4. Mapa
        m = folium.Map(location=[-9.5, -40.5], zoom_start=6, tiles=None, control_scale=True)
        folium.TileLayer("CartoDB positron", name="Mapa Base Claro", control=True).add_to(m)
        Fullscreen(position="topright").add_to(m)

        # ✅ Camada: Limite do Semiárido (sempre visível)
        caminho_limite = os.path.join("dados", "limites_semiarido.shp")
        if os.path.exists(caminho_limite):
            gdf_limite = gpd.read_file(caminho_limite)
            folium.GeoJson(
                gdf_limite.__geo_interface__,
                name="Limite do Semiárido",
                style_function=lambda _: {
                    'fillColor': 'none',
                    'color': 'red',
                    'weight': 2.5,
                    'dashArray': '5, 5'
                }
            ).add_to(m)

        # Outras camadas adicionais
        if st.session_state.get("opt_estados"):
            caminho = os.path.join("dados", "estados", "Estados_Semiarido.shp")
            if os.path.exists(caminho):
                gdf = gpd.read_file(caminho)
                folium.GeoJson(gdf.__geo_interface__, name="Estados do Semiárido",
                    style_function=lambda _: {"fillColor": "none", "color": "black", "weight": 3}
                ).add_to(m)

        if st.session_state.get("opt_caatinga"):
            caminho = os.path.join("dados", "caatinga", "Caatinga.shp")
            if os.path.exists(caminho):
                gdf = gpd.read_file(caminho)
                folium.GeoJson(gdf.__geo_interface__, name="Caatinga",
                    style_function=lambda _: {"fillColor": "none", "color": "black", "weight": 3}
                ).add_to(m)

        if st.session_state.get("opt_matopiba"):
            caminho = os.path.join("dados", "sab_matopiba", "sab_matopiba.shp")
            if os.path.exists(caminho):
                gdf = gpd.read_file(caminho)
                folium.GeoJson(gdf.__geo_interface__, name="MATOPIBA",
                    style_function=lambda _: {"fillColor": "none", "color": "black", "weight": 3}
                ).add_to(m)

        # Solo selecionado
        if tipo_solo != "Nenhum" and gdf_solo is not None:
            for tipo in selecionados:
                geojson_tipo = gdf_solo[gdf_solo["cod_simbol"] == tipo].__geo_interface__
                cor = cores.get(tipo, "#888888")
                folium.GeoJson(
                    geojson_tipo,
                    name=f"{tipo_solo} - {tipo}",
                    style_function=lambda feature, cor=cor: {
                        'fillColor': cor,
                        'color': cor,
                        'weight': 1,
                        'fillOpacity': 0.5
                    }
                ).add_to(m)

        folium.LayerControl(collapsed=False, position="topright").add_to(m)
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        st_folium(m, height=800, use_container_width=True)

        # 5. Legenda
        if tipo_solo != "Nenhum" and selecionados and gdf_solo is not None:
            df_legenda = calcular_area_por_tipo(gdf_solo[gdf_solo["cod_simbol"].isin(selecionados)])
            st.markdown(f"### Legenda dos {tipo_solo}s selecionados")
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
                    f"</div>", unsafe_allow_html=True
                )

        # 6. Descrição
        if tipo_solo != "Nenhum":
            chave = {
                "Latossolo": "LATOSSOLOS",
                "Cambissolo": "CAMBISSOLOS",
                "Luvissolo": "LUVISSOLOS",
                "Argissolo": "ARGISSOLOS"
            }.get(tipo_solo)
            if chave and chave in descricao_solos:
                st.markdown(f"### Sobre {tipo_solo}s")
                st.markdown(descricao_solos[chave], unsafe_allow_html=True)

        loading_overlay.empty()

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

    except Exception as e:
        loading_overlay.empty()
        st.error(f"Erro ao processar os dados: {e}")