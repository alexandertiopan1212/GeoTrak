import streamlit as st
import zipfile
import os
import folium
import shutil
from shapely.geometry import Point
from streamlit_folium import st_folium
from utils.shapefile_utils import (
    list_shapefiles,
    read_shapefile,
    get_area_km2,
    detect_geometry_type
)

# --- Setup page
st.set_page_config(page_title="GeoTrak GIS Explorer", layout="wide")
st.title("🌍 GeoTrak: Multi-Layer Catchment GIS Explorer")

# --- Init session state
for k, v in {
    "gdf": None,
    "map_result": None,
    "shp_files": [],
    "selected_shp": None,
    "last_uploaded_file": None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Upload
uploaded_file = st.file_uploader("📁 Upload your Shapefile (.zip)", type=["zip"])

if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
    with st.spinner("🔄 Extracting files..."):
        extract_dir = "temp_shp"
        shutil.rmtree(extract_dir, ignore_errors=True)
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(uploaded_file, "r") as z:
            z.extractall(extract_dir)

        shp_files = list_shapefiles(extract_dir)
        if not shp_files:
            st.error("❌ No .shp file found in the ZIP.")
        else:
            st.session_state.shp_files = shp_files
            st.session_state.selected_shp = shp_files[0]
            st.session_state.last_uploaded_file = uploaded_file

# --- Select Shapefile Layer
if st.session_state.shp_files:
    selected = st.selectbox("🗂 Select layer to visualize:", st.session_state.shp_files, index=0)
    if selected != st.session_state.selected_shp or st.session_state.gdf is None:
        shp_path = os.path.join("temp_shp", selected)
        gdf = read_shapefile(shp_path)
        st.session_state.gdf = gdf
        st.session_state.selected_shp = selected

        geometry_type = detect_geometry_type(gdf)
        st.success(f"✅ {len(gdf)} features loaded from **{selected}**")
        st.info(f"📐 Geometry Type: **{geometry_type}**")

# --- Render map
if st.session_state.gdf is not None:
    gdf = st.session_state.gdf
    m = folium.Map(location=gdf.geometry.iloc[0].centroid.coords[0][::-1], zoom_start=6)

    folium.GeoJson(
        gdf,
        name="Layer",
        style_function=lambda x: {"fillOpacity": 0.4, "weight": 1},
        tooltip=folium.GeoJsonTooltip(fields=gdf.columns[:3].tolist()),
    ).add_to(m)

    st.session_state.map_result = st_folium(m, width=1000, height=600)

    # --- Handle click
    if st.session_state.map_result and st.session_state.map_result["last_clicked"] is not None:
        clicked = st.session_state.map_result["last_clicked"]
        st.info(f"🖱️ Clicked at: {clicked}")
        point = Point(clicked["lng"], clicked["lat"])

        match = gdf[gdf.geometry.intersects(point)]
        if match.empty:
            match = gdf[gdf.geometry.intersects(point.buffer(0.0001))]

        if not match.empty:
            st.write("📍 Feature Info:")
            st.dataframe(match)
            area_km2 = get_area_km2(match.geometry)
            st.metric("📐 Area (km²)", f"{area_km2:,.2f}")
        else:
            st.warning("⚠️ No polygon found at this location.")

# --- Clear session
if st.button("🧹 Clear Session & Temp Files"):
    for k in ["gdf", "map_result", "shp_files", "selected_shp", "last_uploaded_file"]:
        st.session_state[k] = None
    shutil.rmtree("temp_shp", ignore_errors=True)
    st.success("🧼 Session & temp files cleared.")
