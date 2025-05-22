import geopandas as gpd
import pandas as pd

# Caminhos dos arquivos
shapefile_path = 'BR_Municipios_2024/BR_Municipios_2024.shp'
xlsx_path = 'lista_municipios_Semiarido_2022.xlsx'

# Carrega os dados
gdf_municipios = gpd.read_file(shapefile_path)
df_semiarido = pd.read_excel(xlsx_path)

# Normaliza os códigos para string com 7 dígitos (pode ter int misturado)
gdf_municipios['CD_MUN'] = gdf_municipios['CD_MUN'].astype(str).str.zfill(7)
df_semiarido['CD_MUN'] = df_semiarido['CD_MUN'].astype(str).str.zfill(7)

# Faz o filtro seguro pelo código IBGE
gdf_semiarido = gdf_municipios[gdf_municipios['CD_MUN'].isin(df_semiarido['CD_MUN'])]

# Conta os registros
print(f"Total de municípios no shapefile: {len(gdf_municipios)}")
print(f"Total de municípios do semiárido encontrados: {len(gdf_semiarido)}")

# Exporta o shapefile filtrado
gdf_semiarido.to_file('municipios_semiarido_2022.shp', encoding='utf-8')
print("✅ Shapefile 'municipios_semiarido_2022.shp' criado com sucesso.")