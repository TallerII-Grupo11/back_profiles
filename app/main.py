import uvicorn

import logging.config

from app.adapters import listeners_controller
from app.adapters import artists_controller
from app.conf.config import Settings
from fastapi import FastAPI
from app.db import db

logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

settings = Settings()

app = FastAPI(version=settings.version, title=settings.title)

app.include_router(listeners_controller.router)
app.include_router(artists_controller.router)


@app.on_event("startup")
async def startup():
    await db.connect_to_database(path=settings.db_path)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=settings.port,  reload=True)
