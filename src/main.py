from fastapi import FastAPI

from src.controller.user import router as user_router

app = FastAPI()

app.include_router(user_router)
