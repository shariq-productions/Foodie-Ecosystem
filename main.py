from fastapi import FastAPI
from app.routes import router
from contextlib import asynccontextmanager
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router)


@app.get("/", tags=["Health"])
async def read_root():
    return {"Hello": "World"}
