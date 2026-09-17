from fastapi import FastAPI

from app.controllers.category import router
from app.models.category import initialize_database

initialize_database()
app = FastAPI(title="Taxi Categories API")
app.include_router(router)
