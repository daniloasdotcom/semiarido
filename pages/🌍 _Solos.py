import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import os

st.set_page_config(layout="wide")

st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Visualize todas as camadas de solos do semiárido brasileiro com controle individual e cores associadas.")

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown("<h2 style='text-align: center;'>Solos do Semiárido - Todas as Camadas</h2>", unsafe_allow_html=True)

CAMINHO_SHAPES = "dados"

CORES_SOLOS = {
    "AR": "saddlebrown", "CX": "darkorange", "ES": "darkgoldenrod", "FF": "darkmagenta",
    "FX": "indigo", "GX": "slategray", "GZ": "lightseagreen", "LA": "seagreen",
    "LV": "darkgreen", "LVA": "limegreen", "MD": "orchid", "MT": "plum",
    "Magua0": "goldenrod", "Magua1": "khaki", "PA": "coral", "PAC": "tomato",
    "PV": "chocolate", "PVA": "burlywood", "RL": "peru", "RQ": "olive",
    "RR": "mediumseagreen", "RU": "crimson", "SG": "steelblue", "SN": "midnightblue",
    "SX": "teal", "TC": "cadetblue", "VC": "hotpink", "VE": "salmon"
}

camadas_disponiveis = {
    "Limites do Semiárido": "limites_semiarido.shp",
    "Estados do Semiárido": "Estados_Semiarido.shp",
    "Caatinga": "caatinga/caatinga.shp",
    "Matopiba": "sab_matopiba/sab_matopiba.shp"
}

@st.cache_data(show_spinner=False)
def carregar_shapefile(caminho):
    gdf = gpd.read_file(caminho)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    return gdf

# Interface lateral
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown(
        "<label style='font-size:18px; font-weight:bold; margin-bottom:0;'>🧩 Escolha e ordene as camadas adicionais:</label>",
        unsafe_allow_html=True
    )

    ordem_camadas = st.multiselect(
        "",  # Label vazio, já usamos o markdown acima
        options=list(camadas_disponiveis.keys()),
        default=[],
        help="Arraste para definir a ordem de sobreposição",
        placeholder="Escolha as camadas de visualização"
    )

    exibir_todos = st.checkbox("Exibir todas as camadas de solo", value=True, key="exibir_solos_checkbox")

# Criação do mapa sem camada base padrão
mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True, tiles=None)
Fullscreen(position="topright").add_to(mapa)

# Camadas base
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

# Camadas de solo SEMPRE adicionadas, mas show depende do checkbox
arquivos_shape = sorted([
    f for f in os.listdir(CAMINHO_SHAPES)
    if f.startswith("COD_SIMBOL_") and f.endswith(".shp")
])

for arquivo in arquivos_shape:
    nome_base = arquivo.replace("COD_SIMBOL_", "").replace(".shp", "")
    caminho = os.path.join(CAMINHO_SHAPES, arquivo)

    try:
        gdf = carregar_shapefile(caminho)
        cor = CORES_SOLOS.get(nome_base, "gray")
        label_colorida = f"<span style='background:{cor};padding:2px 6px;margin-right:4px;border-radius:2px;'>&nbsp;</span>Solo {nome_base}"

        folium.GeoJson(
            gdf,
            name=label_colorida,
            show=exibir_todos,
            style_function=lambda x, cor=cor: {
                "color": cor,
                "weight": 1,
                "fillOpacity": 0.4
            }
        ).add_to(mapa)

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar {arquivo}: {e}")

# Camadas adicionais selecionadas
for nome_camada in ordem_camadas:
    caminho = os.path.join(CAMINHO_SHAPES, camadas_disponiveis[nome_camada])
    if os.path.exists(caminho):
        try:
            gdf = carregar_shapefile(caminho)
            if "Limites" in nome_camada:
                estilo = lambda x: {
                    "color": "black",
                    "weight":3,
                    "fillOpacity": 0  # sem preenchimento
                }
            elif "Estados" in nome_camada:
                estilo = lambda x: {
                    "color": "red",
                    "weight": 3,
                    "fillOpacity": 0
                }
            elif "Matopiba" in nome_camada:
                estilo = lambda x: {
                    "color": "brown",
                    "weight": 3,
                    "fillOpacity": 0
                }
            else:
                estilo = lambda x: {
                    "color": "blue",
                    "weight": 3,
                    "fillOpacity": 0
                }

            folium.GeoJson(
                gdf,
                name=nome_camada,
                style_function=estilo
            ).add_to(mapa)
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar {nome_camada}: {e}")

folium.LayerControl(collapsed=False).add_to(mapa)

# Exibe o mapa centralizado

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    folium_static(mapa, height=1000, width=2000)
