"""
Endpoints para productos.

Define las rutas REST para consultar el catálogo de zapatos.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.awesome_agent_api.infrastructure.db.database import get_db
from src.awesome_agent_api.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from src.awesome_agent_api.application.services.product_service import ProductService
from src.awesome_agent_api.application.dtos.product_dto import ProductResponseDTO, ProductListResponseDTO
from src.awesome_agent_api.domain.exceptions import ProductNotFoundException

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """
    Crea el servicio de productos con inyección de dependencias.

    Args:
        db: Sesión de base de datos

    Returns:
        Instancia de ProductService
    """
    repository = ProductRepositoryImpl(db)
    return ProductService(repository)


@router.get("/", response_model=ProductListResponseDTO)
async def get_all_products(
    service: ProductService = Depends(get_product_service)
):
    """
    Obtiene todos los productos del catálogo.

    Returns:
        Lista completa de productos
    """
    return await service.get_all_products()


@router.get("/available", response_model=ProductListResponseDTO)
async def get_available_products(
    service: ProductService = Depends(get_product_service)
):
    """
    Obtiene solo los productos con stock disponible.

    Returns:
        Lista de productos disponibles
    """
    return await service.get_available_products()


@router.get("/{product_id}", response_model=ProductResponseDTO)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """
    Obtiene un producto específico por ID.

    Args:
        product_id: ID del producto

    Returns:
        Producto encontrado

    Raises:
        HTTPException 404: Si el producto no existe
    """
    try:
        return await service.get_product(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))