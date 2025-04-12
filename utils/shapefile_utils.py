import geopandas as gpd
import os

def list_shapefiles(folder: str):
    return [f for f in os.listdir(folder) if f.lower().endswith(".shp")]

def read_shapefile(path: str, to_epsg=4326):
    gdf = gpd.read_file(path)
    return gdf.to_crs(epsg=to_epsg)

def get_area_km2(geo_series, epsg=3857):
    return geo_series.to_crs(epsg=epsg).area.sum() / 1e6

def detect_geometry_type(gdf):
    types = gdf.geometry.geom_type.unique()
    return types[0] if len(types) == 1 else f"Mixed: {', '.join(types)}"
