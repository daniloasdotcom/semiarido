import streamlit as st
st.set_page_config(layout="wide")

import os
from streamlit_folium import folium_static
from soil_config.config import CAMINHO_SHAPES, CAMADAS_DISPONIVEIS, CAMADAS_GEOMORFOLOGIA, CORES_SOLOS
from soil_config.descricao_solos import descricao_solos
from soil_config.mapa_solos import gerar_mapa_solos

# CSS para centralizar o spinner
st.markdown("""
    <style>
    .css-1v0mbdj {
        display: flex;
        justify-content: center;
    }

    .stSpinner {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Menu lateral
st.sidebar.title("🧱 GeoSAB - Solos")
st.sidebar.markdown("Selecione uma classe de solo para visualizar com outras camadas")

opcao_solo = st.sidebar.radio(
    "🔍 Visualizar grupo de solos:",
    [
        "Selecionar...",
        "Cambissolos", "Luvissolos", "Latossolos", "Planossolos",
        "Neossolos", "Argissolos", "Vertissolos", "Gleissolos",
        "Chernossolos", "Plintossolos", "Nitossolos"
    ],
    key="selecao_solo"
)

# Camadas adicionais
st.sidebar.markdown("---")
camadas_geomorfologia = st.sidebar.multiselect(
    "🗺️ Camadas geomorfológicas (opcional):",
    options=list(CAMADAS_GEOMORFOLOGIA.keys())
)

col1, col2, col3 = st.columns([1, 5, 1])

if opcao_solo == "Selecionar...":
    with col2:
        st.markdown("<h2 style='text-align: center;'>Bem-vindo ao GeoSAB - Solos</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align: center; font-size: 18px;'>
            Utilize o menu lateral para visualizar os grupos de solos presentes no Semiárido brasileiro.<br>
            Ao selecionar um grupo, o mapa correspondente será carregado aqui.
        </p>
        """, unsafe_allow_html=True)

else:
    titulo = f"{opcao_solo} no Semiárido"
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{titulo}</h2>", unsafe_allow_html=True)

    arquivos_shape = sorted([
        f for f in os.listdir(CAMINHO_SHAPES) if f.endswith(".shp")
    ])
    todos_os_simbolos = [arquivo.replace(".shp", "") for arquivo in arquivos_shape]

    grupo_para_prefixo = {
        "Cambissolos": ("C", "CX"),
        "Luvissolos": ("T", "TC"),
        "Latossolos": ("L", "LATOSSOLOS"),
        "Planossolos": ("S", None),
        "Neossolos": ("R", None),
        "Argissolos": ("P", None),
        "Vertissolos": ("V", None),
        "Gleissolos": ("G", None),
        "Chernossolos": ("M", None),
        "Plintossolos": ("F", None),
        "Nitossolos": ("N", None)
    }

    prefixo, chave_desc = grupo_para_prefixo.get(opcao_solo, ("", None))

    with col2:
        with st.spinner("🔄 Carregando dados do solo e gerando o mapa..."):
            mapa, gdf_clipado = gerar_mapa_solos(prefixo, todos_os_simbolos, camadas_geomorfologia)
            folium_static(mapa, width=1200, height=800)

        if not gdf_clipado.empty and "COD_SIMBOL" in gdf_clipado.columns:
            st.subheader("Legenda de Cores por Tipo de Solo")
            tipos_solo = gdf_clipado["COD_SIMBOL"].unique()
            mapa_cores = {solo: CORES_SOLOS.get(solo, "#aaaaaa") for solo in tipos_solo}

            gdf_clipado["area_ha"] = gdf_clipado.geometry.area / 10_000
            area_total = gdf_clipado["area_ha"].sum()
            resumo = gdf_clipado.groupby(["COD_SIMBOL", "LEGENDA"])["area_ha"].sum().reset_index()
            resumo["percent"] = (resumo["area_ha"] / area_total * 100).round(2)
            resumo = resumo.sort_values(by="area_ha", ascending=False)

            for _, row in resumo.iterrows():
                simbolo = row["COD_SIMBOL"]
                descricao = row["LEGENDA"]
                cor = mapa_cores.get(simbolo, "#aaaaaa")
                perc = f"{row['percent']}%"

                st.markdown(
                    f"""
                    <div style='display: flex; align-items: center; margin-bottom: 6px;'>
                        <div style='width: 25px; height: 20px; background-color:{cor}; border:1px solid #333; margin-right: 10px;'></div>
                        <span style='font-size: 16px;'><strong>{simbolo}</strong> — {perc} — {descricao}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if chave_desc and chave_desc in descricao_solos:
            st.markdown(descricao_solos[chave_desc], unsafe_allow_html=True)