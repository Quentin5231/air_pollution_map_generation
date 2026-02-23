from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from .utils import load_data, filter_data, generate_map
import geopandas as gpd

router = APIRouter()

DATA_PATH = "data/qualite-de-lair-france.csv"
DATATIME_KEY="Last Updated"

@router.get("/data/", response_model=dict)
async def get_data(
    polluant: str = Query(None, description="Filter by polluant (ex: NO₂, PM10)"),
    max_level: float = Query(None, description="Maximum pollution level")
):
    """Returns filtered data of pollution level according to polluant and max level chosen"""
    gdf = load_data(DATA_PATH,DATATIME_KEY)
    filtered_gdf = filter_data(gdf, polluant, max_level)
    return filtered_gdf.drop(columns="geometry").to_dict(orient="records")

@router.get("/map/", response_class=HTMLResponse)
async def get_map(
    polluant: str = Query(None, description="Filter by polluant (ex: NO₂, PM10)"),
    max_level: float = Query(None, description="Maximum pollution level")
):
    """Generates and returns a HTML map."""
    gdf = load_data(DATA_PATH,DATATIME_KEY)
    filtered_gdf = filter_data(gdf, polluant, max_level)
    map_html = generate_map(filtered_gdf)
    return HTMLResponse(content=map_html, status_code=200)