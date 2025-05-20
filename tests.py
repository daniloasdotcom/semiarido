import geopandas as gpd
import pandas as pd
import os

# --- CONFIGURAÇÕES ---
# Códigos dos Luvissolos
luvissoos = ["TCk", "TCo", "TCp", "TXp"]

# Caminhos
pasta_entrada = "dados/solos_sab250"
saida_geojson = "dados/luvissolos_simplificado.geojson"

# Tolerância para simplificação de geometria (aprox. 1 km)
tolerancia = 0.01

# --- PROCESSAMENTO ---
gdfs = []

for nome in luvissoos:
    caminho = os.path.join(pasta_entrada, f"{nome}.shp")

    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        continue

    print(f"✅ Lendo {nome}...")
    gdf = gpd.read_file(caminho)

    # Garantir colunas essenciais
    gdf["cod_simbol"] = gdf.get("cod_simbol", pd.Series([nome] * len(gdf)))
    gdf["legenda"] = gdf.get("legenda", pd.Series([nome] * len(gdf)))

    # Simplifica a geometria
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerancia, preserve_topology=True)

    gdfs.append(gdf)

# --- EXPORTAÇÃO ---
if gdfs:
    gdf_final = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)
    gdf_final.to_file(saida_geojson, driver="GeoJSON")
    print(f"✅ GeoJSON exportado com sucesso: {saida_geojson}")
else:
    print("⚠️ Nenhum shapefile de Luvissolo foi processado.")