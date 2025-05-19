import geopandas as gpd

def carregar_geojson(caminho):
    try:
        return gpd.read_file(caminho)
    except Exception:
        return None

def calcular_area_por_tipo(gdf):
    try:
        gdf_proj = gdf.to_crs(epsg=5880)  # SIRGAS 2000 / Albers Equal Area
    except:
        gdf_proj = gdf.to_crs(gdf.estimate_utm_crs())

    gdf_proj["area_km2"] = gdf_proj["geometry"].area / 1_000_000

    df = gdf_proj.groupby(["cod_simbol", "legenda"]).agg(
        area_km2=("area_km2", "sum")
    ).reset_index()

    total = df["area_km2"].sum()
    df["percentual"] = (df["area_km2"] / total * 100).round(2)
    return df.sort_values(by="area_km2", ascending=False)