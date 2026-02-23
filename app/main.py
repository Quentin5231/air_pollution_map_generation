from fastapi import FastAPI, Request, Form
from .routes import router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the directory "static" for the CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 for the HTML templates
templates = Jinja2Templates(directory="templates")

# Generate a HTML page in which the user can choose the polluant in a list and  define the maximum level to display in the map.
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
     polluants = ["CO","NO2","O3","PM1","PM10", "PM2.5", "RELATIVEHUMIDITY","SO2","TEMPERATURE","UM003"]
     return templates.TemplateResponse(
        "index.html",
        {"request": request, "polluants": polluants}
    )

app.include_router(router, prefix="/api/v1")
