from fastapi import FastAPI
from routes.main import router

app = FastAPI()

app.include_router(router)