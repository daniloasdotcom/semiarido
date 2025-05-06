import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import os

st.set_page_config(layout="wide")

# Menu lateral
st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Visualize as camadas de solos ou explore um tipo específico.")

opcao_solo = st.sidebar.radio(
    "🔍 Visualizar por:",
    ["Todas as camadas", "Cambissolos (CX)", "Luvissolos (TC)", "Latossolos (LA, LV, LVA)"],
    key="selecao_solo"
)

# Título dinâmico
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    if opcao_solo == "Cambissolos (CX)":
        titulo = "Cambissolos (CX) no Semiárido"
    elif opcao_solo == "Luvissolos (TC)":
        titulo = "Luvissolos (TC) no Semiárido"
    elif opcao_solo == "Latossolos (LA, LV, LVA)":
        titulo = "Latossolos no Semiárido"
    else:
        titulo = "Solos do Semiárido"
    st.markdown(f"<h2 style='text-align: center;'>{titulo}</h2>", unsafe_allow_html=True)

CAMINHO_SHAPES = "dados"

# Cores baseadas no SiBCS 2018
CORES_SOLOS = {
    "AR": "#a0522d",
    "CX": "#d7c5a5",
    "ES": "#cebec6",
    "FF": "#edadcb",
    "FX": "#dabecc",
    "GX": "#b6d8ee",
    "GZ": "#5eb4e6",
    "LA": "#fecc5c",
    "LV": "#f4b980",
    "LVA": "#f8d1a6",
    "MD": "#8e6856",
    "MT": "#9c4a4e",
    "PA": "#f1ccc8",
    "PAC": "#fdf1f0",
    "PV": "#f07f7f",
    "PVA": "#ffa77f",
    "RL": "#969595",
    "RQ": "#fffe73",
    "RR": "#cfcece",
    "RU": "#dc143c",
    "SG": "#4682b4",
    "SN": "#89cac7",
    "SX": "#b5d6ae",
    "TC": "#d49616",
    "VC": "#ff69b4",
    "VE": "#868f72"
}

camadas_disponiveis = {
    "Limites do Semiárido": "limites_semiarido.shp",
    "Estados do Semiárido": "Estados_Semiarido.shp",
    "Caatinga": "caatinga/caatinga.shp",
    "Matopiba": "sab_matopiba/sab_matopiba.shp"
}

descricao_solos = {
    "CX": """
    <p style="text-align: justify;">
    Os <strong>Cambissolos (CX)</strong> são solos jovens, com horizonte B incipiente. 
    São moderadamente profundos, com fertilidade variável, e ocorrem em relevos movimentados. 
    Embora limitantes à mecanização, podem ser produtivos com manejo adequado.
    </p>
    """,
    "TC": """
    <p style="text-align: justify;">
    Os <strong>Luvissolos (TC)</strong> são solos argilosos com horizonte B textural, 
    alta fertilidade natural e presença de argilas do tipo 2:1. 
    São muito utilizados na agricultura do semiárido, porém demandam manejo para evitar erosão.
    </p>
    """,
    "LATOSSOLOS": """
    <p style="text-align: justify;">
    Os <strong>Latossolos</strong> compreendem:
    <ul>
      <li><strong>Latossolo Amarelo (LA)</strong></li>
      <li><strong>Latossolo Vermelho (LV)</strong></li>
      <li><strong>Latossolo Vermelho-Amarelo (LVA)</strong></li>
    </ul>
    São solos profundos, bem drenados, com estrutura granular e textura média a argilosa.
    </p>
    """
}

@st.cache_data(show_spinner=False)
def carregar_shapefile(caminho):
    gdf = gpd.read_file(caminho)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    return gdf

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    if opcao_solo == "Todas as camadas":
        st.markdown(
            "<label style='font-size:18px; font-weight:bold;'>🧩 Escolha e ordene as camadas adicionais:</label>",
            unsafe_allow_html=True
        )

        ordem_camadas = st.multiselect(
            "",
            options=list(camadas_disponiveis.keys()),
            default=[],
            help="Arraste para definir a ordem de sobreposição",
            placeholder="Escolha as camadas de visualização"
        )

        exibir_todos = st.checkbox("Exibir todas as camadas de solo", value=True, key="exibir_solos_checkbox")

mapa = folium.Map(location=[-13, -40], zoom_start=6, control_scale=True, tiles=None)
Fullscreen(position="topright").add_to(mapa)

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

arquivos_shape = sorted([
    f for f in os.listdir(CAMINHO_SHAPES)
    if f.startswith("COD_SIMBOL_") and f.endswith(".shp")
])

if opcao_solo == "Todas as camadas":
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

    for camada in ordem_camadas:
        try:
            caminho = os.path.join(CAMINHO_SHAPES, camadas_disponiveis[camada])
            gdf_camada = carregar_shapefile(caminho)
            folium.GeoJson(
                gdf_camada,
                name=camada,
                style_function=lambda x: {
                    "color": "gray",
                    "weight": 1.5,
                    "fillOpacity": 0
                }
            ).add_to(mapa)
        except Exception as e:
            st.warning(f"Erro ao carregar camada '{camada}': {e}")

else:
    shape_limite = os.path.join(CAMINHO_SHAPES, "limites_semiarido.shp")
    try:
        gdf_limite = carregar_shapefile(shape_limite)
        folium.GeoJson(
            gdf_limite,
            name="Limite do Semiárido",
            style_function=lambda x: {
                "color": "black",
                "weight": 3,
                "fillOpacity": 0
            }
        ).add_to(mapa)
    except Exception as e:
        st.warning(f"Erro ao carregar limite do semiárido: {e}")

    if opcao_solo == "Latossolos (LA, LV, LVA)":
        for simb, nome_exib in [("LA", "Latossolo Amarelo"), ("LV", "Latossolo Vermelho"), ("LVA", "Latossolo Vermelho-Amarelo")]:
            try:
                gdf = carregar_shapefile(os.path.join(CAMINHO_SHAPES, f"COD_SIMBOL_{simb}.shp"))
                cor = CORES_SOLOS.get(simb, "gray")
                folium.GeoJson(
                    gdf,
                    name=nome_exib,
                    style_function=lambda x, cor=cor: {
                        "color": cor,
                        "weight": 1,
                        "fillOpacity": 0.4
                    }
                ).add_to(mapa)
            except Exception as e:
                st.warning(f"Erro ao carregar solo {simb}: {e}")
    else:
        simbolo = "CX" if "CX" in opcao_solo else "TC"
        shape_solo = os.path.join(CAMINHO_SHAPES, f"COD_SIMBOL_{simbolo}.shp")
        try:
            gdf_solo = carregar_shapefile(shape_solo)
            cor = CORES_SOLOS.get(simbolo, "gray")
            folium.GeoJson(
                gdf_solo,
                name="Cambissolo" if simbolo == "CX" else "Luvissolo",
                style_function=lambda x, cor=cor: {
                    "color": cor,
                    "weight": 1,
                    "fillOpacity": 0.4
                }
            ).add_to(mapa)
        except Exception as e:
            st.warning(f"Erro ao carregar solo {simbolo}: {e}")
    for nome, arquivo in camadas_disponiveis.items():
        if nome == "Limites do Semiárido":
            continue
        try:
            gdf_camada = carregar_shapefile(os.path.join(CAMINHO_SHAPES, arquivo))
            folium.GeoJson(
                gdf_camada,
                name=nome,
                show=False,
                style_function=lambda x: {
                    "color": "black",
                    "weight": 3,
                    "fillOpacity": 0
                }
            ).add_to(mapa)
        except Exception as e:
            st.warning(f"Erro ao carregar camada '{nome}': {e}")

folium.LayerControl(collapsed=False).add_to(mapa)

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    folium_static(mapa, height=1000, width=2000)

    if opcao_solo in ["Cambissolos (CX)", "Luvissolos (TC)", "Latossolos (LA, LV, LVA)"]:
        chave = "LATOSSOLOS" if "Latossolos" in opcao_solo else "CX" if "CX" in opcao_solo else "TC"
        st.markdown(descricao_solos[chave], unsafe_allow_html=True)