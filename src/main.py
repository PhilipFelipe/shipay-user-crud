from fastapi import FastAPI

from src.controller.role import router as role_router
from src.controller.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)
