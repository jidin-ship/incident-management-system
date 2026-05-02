from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.signal import router as signal_router
from app.db.postgres import engine
from app.models.work_item import Base
from app.routes.work_item import router as work_item_router

import time

app = FastAPI()

@app.on_event("startup")
def startup():
    # Wait for DB to be ready
    time.sleep(5)
    Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(signal_router)
app.include_router(work_item_router)
