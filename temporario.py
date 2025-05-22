import geopandas as gpd

gdf = gpd.read_file("dados/municipios/municipios_semiarido_2022.shp")

# Junta todos os polígonos em uma única geometria
gdf_union = gdf.unary_union

# Extrai a borda (fronteira externa)
borda_total = gpd.GeoDataFrame(geometry=[gdf_union.boundary], crs=gdf.crs)

# Salva o resultado
borda_total.to_file("limites_semiarido.shp")