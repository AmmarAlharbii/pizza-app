from fastapi import FastAPI
from .routes import auth_routes, order_routes
from fastapi_jwt_auth import AuthJWT
from app.schemas.settings import Settings
from fastapi.openapi.utils import get_openapi

app = FastAPI()


# For JWT token in Swagger UI

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pizza",
        version="1.0.0",
        description="JWT Authentication and Authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_routes.auth_router)
app.include_router(order_routes.order_router)
