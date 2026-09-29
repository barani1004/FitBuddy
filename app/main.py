from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from . import models
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBuddy")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)