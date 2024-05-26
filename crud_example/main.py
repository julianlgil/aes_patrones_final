from fastapi import FastAPI

from crud_example.database import init_db
from crud_example.routers import router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)
