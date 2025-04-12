# 🌍 GeoTrak: Multi-Layer Catchment GIS Explorer

GeoTrak is an interactive web application built with Streamlit that allows users to upload, visualize, and explore multi-layer GIS shapefiles. The app is ideal for exploring UK catchment layers and supports drill-down, area calculation, and feature inspection.

## 🚀 Features

- 📁 Upload shapefile ZIPs (must include `.shp`, `.shx`, `.dbf`, `.prj`)
- 🗂 Select from multiple shapefile layers within a ZIP
- 🗺️ Interactive map rendering using Folium
- 👆 Click on a map to view intersecting feature details
- 📐 Area calculation in square kilometers (for polygon layers)
- 🧹 Clear session and temp files easily

## 📦 Tech Stack

- Streamlit
- GeoPandas
- Folium
- Shapely
- Streamlit-Folium

## 🧑‍💻 How to Run

```bash
# Create and activate conda environment
conda create -n geotrak python=3.10 -y
conda activate geotrak

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🖼️ Screenshot

![GeoTrak Demo](screenshots/demo.png)

## 📁 Folder Structure

```
GeoTrak/
├── app.py
├── requirements.txt
├── utils/
│   └── shapefile_utils.py
├── temp_shp/                # auto-generated
└── .streamlit/
    └── config.toml
```

## 📜 License

Open source under the MIT License.