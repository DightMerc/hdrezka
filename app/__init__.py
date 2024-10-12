from fastapi import FastAPI

from app.api.routers.proxy_router.router import router as auth_router


def create_app():
    app = FastAPI(title="HDRezka Proxy Backend")

    # Подключение маршрутов
    app.include_router(router=auth_router, prefix="/api/v1")

    return app
