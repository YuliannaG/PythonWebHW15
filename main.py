from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.config import BASE_DIR
from src.router import news


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/source", StaticFiles(directory=BASE_DIR / "templates/source"), name="source")
app.include_router(news.router)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "News APP"})


@app.get("/test")
async def root():
    return {"message": "Hello World"}