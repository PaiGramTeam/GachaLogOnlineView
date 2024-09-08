from contextlib import asynccontextmanager

from fastapi import FastAPI
import flet.fastapi as flet_fastapi
from .endpoints.pb import router as pb_router
from .scheduler import scheduler


@asynccontextmanager
async def lifespan(_: FastAPI):
    await flet_fastapi.app_manager.start()
    if not scheduler.running:
        scheduler.start()
    yield
    await flet_fastapi.app_manager.shutdown()
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(pb_router)
