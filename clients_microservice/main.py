from fastapi import FastAPI

from .database import init_db
from .routers import router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)
