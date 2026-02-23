import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

def load_data(filepath: str,datatimeKey : str) -> gpd.GeoDataFrame:
    """Load and prepare the data."""
    df = pd.read_csv(filepath,sep=";",parse_dates=[datatimeKey])
    df["Last_Updated"]=pd.to_datetime(df[datatimeKey],utc=True)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Coordinates"].str.split(',').str.get(0), df["Coordinates"].str.split(',').str.get(1)))
    return gdf

def filter_data(gdf: gpd.GeoDataFrame, polluant: str = None, max_level: float = None) -> gpd.GeoDataFrame:
    """Filter data by polluant and/or pollution level."""
    if polluant:
        gdf = gdf[gdf.Pollutant == polluant]
    if max_level:
        gdf = gdf[gdf.Value <= max_level]
    return gdf

def generate_map(gdf: gpd.GeoDataFrame, center: list = [48.8566, 2.3522], zoom: int = 10) -> str:
    """Generates Folium map et returns HTML code."""
    m = folium.Map(location=center, zoom_start=zoom)
    for idx, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.x, row.geometry.y],
            radius=row.Value/ 20,
            color="red" if row.Value > 40 else "orange",
            popup=f"{row.Pollutant}: {row.Value} µg/m³ \n Date : {row.Last_Updated.day}/{row.Last_Updated.month}/{row.Last_Updated.year}"
        ).add_to(m)
    return m._repr_html_()  # Return HTML map

if __name__=="__main__" :
    DATA_PATH = "data/qualite-de-lair-france.csv"
    DATATIME_KEY="Last Updated"
    gdf=load_data(DATA_PATH,DATATIME_KEY)
    filtered_gdf = filter_data(gdf, "CO", 100000000)
    print(filtered_gdf)

    #rint(filtered_gdf.drop(columns="geometry").to_dict(orient="records"))
    m=generate_map(filtered_gdf)
    #m.save("carte_pollution_test.html")
