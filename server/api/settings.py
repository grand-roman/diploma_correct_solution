from contextlib import asynccontextmanager
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from .bll.base import engine, init_models

    await init_models()

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
