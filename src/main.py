from fastapi import FastAPI

from src.containers import Container
from src.controller.role import router as role_router
from src.controller.user import router as user_router

app = FastAPI()

container = Container()

container.wire(modules=['src.controller.user'])

app.container = container
app.include_router(user_router)
app.include_router(role_router)
