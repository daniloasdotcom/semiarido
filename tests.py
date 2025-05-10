import geopandas as gpd
from shapely.geometry import mapping, shape

gdf = gpd.read_file("dados/geomorfologia_caatinga/south_4326.shp")

# Remove Z (transforma cada geometria em 2D)
gdf["geometry"] = gdf["geometry"].apply(lambda geom: shape(mapping(geom)))

gdf.to_file("dados/geomorfologia_caatinga/south_final.shp")