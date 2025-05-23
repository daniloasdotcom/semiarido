import geopandas as gpd
import pandas as pd
import os

# Lista dos códigos de Argissolos
argissolos = ["PACd", "PAd", "PAdx", "PAe", "PVa", "PVAd", "PVAe", "PVd", "PVe"]

# Caminho base
pasta = "dados/solos_sab250"

# Tolerância de simplificação (ajuste conforme necessário)
tolerancia = 0.01  # ~1km de simplificação

gdfs = []

for nome in argissolos:
    caminho = os.path.join(pasta, f"{nome}.shp")
    if os.path.exists(caminho):
        print(f"Lendo {nome}...")
        gdf = gpd.read_file(caminho)

        # Verificação mínima
        if "cod_simbol" not in gdf.columns:
            gdf["cod_simbol"] = nome  # se não existir, cria

        if "legenda" not in gdf.columns:
            gdf["legenda"] = nome  # ou insira descrições mais detalhadas aqui se desejar

        # Simplificação da geometria
        gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerancia, preserve_topology=True)

        gdfs.append(gdf)
    else:
        print(f"Arquivo não encontrado: {caminho}")

# Junta todos os tipos
if gdfs:
    gdf_final = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

    # Salva como GeoJSON
    saida = "dados/argissolos_simplificado.geojson"
    gdf_final.to_file(saida, driver="GeoJSON")
    print(f"Arquivo exportado para {saida}")
else:
    print("Nenhum arquivo de Argissolo foi carregado.")