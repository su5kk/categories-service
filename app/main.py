from fastapi import FastAPI

from app.controllers.category import router

app = FastAPI(title="Taxi Categories API")
app.include_router(router)
