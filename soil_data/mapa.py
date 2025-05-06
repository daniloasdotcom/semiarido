import geopandas as gpd

def carregar_shapefile(caminho):
    gdf = gpd.read_file(caminho)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    return gdf