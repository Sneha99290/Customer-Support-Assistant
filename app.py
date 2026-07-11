from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="ShopSphere Customer Support Assistant",
)

app.include_router(router)