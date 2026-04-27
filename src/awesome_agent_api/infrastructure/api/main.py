"""
Aplicación principal de FastAPI.

Configura e inicializa la API con todos sus componentes.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.awesome_agent_api.infrastructure.db.database import init_db
from src.awesome_agent_api.infrastructure.api.routes import products, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.

    Inicializa la base de datos al arrancar.
    """
    init_db()
    yield


app = FastAPI(
    title="Awesome Agent API",
    description="E-commerce de zapatos con chat inteligente potenciado por Google Gemini",
    version="1.0.0",
    lifespan=lifespan
)


# Registrar routers
app.include_router(products.router)
app.include_router(chat.router)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Verifica que la API está funcionando correctamente.

    Returns:
        Estado de la API
    """
    return {"status": "ok", "message": "Awesome Agent API funcionando"}