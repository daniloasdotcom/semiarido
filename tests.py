import geopandas as gpd
import pandas as pd
import os

# Lista dos nomes dos arquivos de Latossolos
nomes_latossolos = [
    "LAa", "LAd", "LAdf", "LAdx", "LAe", "LAw",
    "LVAa", "LVAd", "LVAe", "LVd", "LVdf", "LVe", "LVw"
]

# Pasta onde estão os shapefiles
pasta = "dados/solos_sab250"

# Lista para guardar os GeoDataFrames
gdfs = []

# Tolerância de simplificação (ajuste conforme necessário)
tolerancia = 0.01  # Aproximadamente 1 km de simplificação

for nome in nomes_latossolos:
    caminho = os.path.join(pasta, f"{nome}.shp")
    if os.path.exists(caminho):
        gdf = gpd.read_file(caminho)
        gdf["origem"] = nome  # opcional: marca a origem
        gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerancia, preserve_topology=True)
        gdfs.append(gdf)

# Junta tudo em um único GeoDataFrame
gdf_final = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

# Exporta para GeoJSON
saida = "dados/latossolos_simplificado.geojson"
gdf_final.to_file(saida, driver="GeoJSON")

print("GeoJSON exportado com sucesso:", saida)