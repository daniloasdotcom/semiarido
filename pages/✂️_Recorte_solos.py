import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import matplotlib.pyplot as plt
from io import BytesIO
import zipfile
import tempfile

st.set_page_config(layout="centered")

st.title("Mapa de Solos por Município - Com shapefile para downlaod")

# Descrição orientativa
st.markdown("""
<div style='font-size: 16px; line-height: 1.6;'>
<ul>
  <li>🗺️ <strong>Selecione um município</strong> para visualizar o recorte de solos disponíveis.</li>
  <li>📥 <strong>Para baixar o shapefile do recorte</strong>, role até o final da página e clique em <em>Baixar Recorte (.zip)</em>.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --- 1. Carregar municípios ---
gdf_municipios = gpd.read_file("dados/municipios/Municipios_caatinga.shp")
if gdf_municipios.crs is None:
    gdf_municipios.set_crs("EPSG:4674", inplace=True)

# --- 2. Carregar todos os shapefiles de solos da pasta ---
pasta_solos = "dados/solos_sab250"
arquivos = [f for f in os.listdir(pasta_solos) if f.endswith(".shp")]

todos_solos = []
arquivos_ignorados = []

for shp in arquivos:
    caminho = os.path.join(pasta_solos, shp)
    try:
        gdf = gpd.read_file(caminho)
        gdf.columns = [col.strip().upper() for col in gdf.columns]

        geom_cols = [col for col in gdf.columns if gdf[col].dtype.name == "geometry"]
        if not geom_cols:
            arquivos_ignorados.append(f"{shp} (nenhuma coluna de geometria encontrada)")
            continue
        gdf = gdf.set_geometry(geom_cols[0])

        if "COD_SIMBOL" not in gdf.columns and "LEGENDA" not in gdf.columns:
            arquivos_ignorados.append(f"{shp} (sem COD_SIMBOL nem LEGENDA)")
            continue

        if "COD_SIMBOL" not in gdf.columns:
            gdf["COD_SIMBOL"] = gdf["LEGENDA"]
        else:
            if "LEGENDA" in gdf.columns:
                gdf["COD_SIMBOL"] = gdf["COD_SIMBOL"].fillna(gdf["LEGENDA"])

        if gdf.crs is None:
            gdf.set_crs("EPSG:4674", inplace=True)
        if gdf.crs != gdf_municipios.crs:
            gdf = gdf.to_crs(gdf_municipios.crs)

        todos_solos.append(gdf)

    except Exception as e:
        arquivos_ignorados.append(f"{shp} (erro: {str(e)})")
        continue

if arquivos_ignorados:
    st.warning("Alguns arquivos foram ignorados:")
    for item in arquivos_ignorados:
        st.text(f" - {item}")

if not todos_solos:
    st.error("Nenhum shapefile de solo válido foi carregado.")
    st.stop()

gdf_solos = gpd.GeoDataFrame(pd.concat(todos_solos, ignore_index=True))

# --- Seleção de município ---
lista_municipios = sorted(gdf_municipios["NM_MUN"].unique())
municipio_nome = st.selectbox("Selecione um município", [""] + lista_municipios)

if not municipio_nome:
    st.warning("Por favor, selecione um município no menu acima.")
else:
    muni = gdf_municipios[gdf_municipios["NM_MUN"] == municipio_nome]

    def mostrar_resultados(muni):
        clipado = gpd.clip(gdf_solos, muni)
        if clipado.empty:
            st.warning("Nenhum solo encontrado com `clip()`. Tentando com `intersects()`...")
            clipado = gdf_solos[gdf_solos.geometry.intersects(muni.geometry.iloc[0])]

        clipado["area_ha"] = clipado.geometry.area / 10_000
        tipos_solo = clipado["COD_SIMBOL"].unique() if not clipado.empty else []
        cores = plt.cm.get_cmap('tab20', len(tipos_solo))
        mapa_cores = {
            solo: f'#{int(cores(i)[0]*255):02x}{int(cores(i)[1]*255):02x}{int(cores(i)[2]*255):02x}'
            for i, solo in enumerate(tipos_solo)
        }

        centro = muni.geometry.centroid.iloc[0].coords[0][::-1]
        m = folium.Map(location=centro, zoom_start=10, tiles=None)

        # Camadas de base
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            name="Satélite (Esri)",
            attr="Tiles © Esri & the GIS community"
        ).add_to(m)

        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            name="Mapa padrão (OSM)",
            attr="© OpenStreetMap contributors"
        ).add_to(m)

        folium.GeoJson(muni, name="Município", style_function=lambda x: {
            'fillColor': 'none', 'color': 'blue', 'weight': 2
        }).add_to(m)

        if not clipado.empty:
            if not clipado.empty:
                for solo_tipo in clipado["COD_SIMBOL"].unique():
                    camada = clipado[clipado["COD_SIMBOL"] == solo_tipo]
                    cor = mapa_cores.get(solo_tipo, "#aaaaaa")

                    folium.GeoJson(
                        camada,
                        name=solo_tipo,  # Apenas o símbolo
                        style_function=lambda feature, cor=cor: {
                            'fillColor': cor,
                            'color': 'black',
                            'weight': 1,
                            'fillOpacity': 0.6
                        },
                        tooltip=folium.GeoJsonTooltip(
                            fields=["COD_SIMBOL", "area_ha"],
                            aliases=["Código do Solo:", "Área (ha):"]
                        )
                    ).add_to(m)
        else:
            st.info("Nenhuma feição de solo encontrada.")

        folium.LayerControl().add_to(m)
        st_folium(m, width=1000, height=600)

        if not clipado.empty:
            st.subheader("Legenda de Cores por Tipo de Solo")

            area_total = clipado["area_ha"].sum()
            resumo = clipado.groupby(["COD_SIMBOL", "LEGENDA"])["area_ha"].sum().reset_index()
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

            st.subheader("Exportar Recorte como Shapefile")

            buffer = BytesIO()
            nome_base = municipio_nome.replace(" ", "_").lower()

            with tempfile.TemporaryDirectory() as temp_dir:
                shp_path = os.path.join(temp_dir, f"solo_{nome_base}.shp")
                clipado.to_file(shp_path)

                with zipfile.ZipFile(buffer, mode="w") as z:
                    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                        caminho = os.path.join(temp_dir, f"solo_{nome_base}{ext}")
                        if os.path.exists(caminho):
                            with open(caminho, "rb") as f:
                                z.writestr(f"solo_{nome_base}{ext}", f.read())

            buffer.seek(0)
            st.download_button(
                label="📦 Baixar Recorte (.zip)",
                data=buffer,
                file_name=f"solo_{nome_base}.zip",
                mime="application/zip"
            )

    # 👇 Executa o processamento completo
    mostrar_resultados(muni)