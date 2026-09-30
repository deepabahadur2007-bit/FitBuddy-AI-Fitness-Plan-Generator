from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import init_db
from .routes import router


BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title="FitBuddy – AI Fitness Plan Generator",

    description=(
        "AI-powered 7-day workout planning "
        "with feedback updates and nutrition tips."
    ),

    version="1.0.0",

    lifespan=lifespan,

)


app.mount(

    "/static",

    StaticFiles(
        directory=BASE_DIR / "static"
    ),

    name="static",

)


templates = Jinja2Templates(

    directory=BASE_DIR / "templates"

)


app.include_router(router)