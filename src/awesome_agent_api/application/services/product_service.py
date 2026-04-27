"""
ProductService - Casos de uso para productos.

Orquesta la obtención y validación de productos.
"""

from typing import List, Optional
from src.awesome_agent_api.domain.repositories.product_repository import ProductRepository
from src.awesome_agent_api.domain.entities.product import Product
from src.awesome_agent_api.domain.exceptions import ProductNotFoundException
from src.awesome_agent_api.application.dtos.product_dto import (
    ProductResponseDTO,
    ProductListResponseDTO
)


class ProductService:
    """
    Servicio de aplicación para productos.
    
    Implementa los casos de uso relacionados con productos.
    """
    
    def __init__(self, product_repository: ProductRepository):
        """
        Inicializa el servicio.
        
        Args:
            product_repository: Implementación del repositorio de productos
        """
        self.product_repository = product_repository
    
    async def get_all_products(self) -> ProductListResponseDTO:
        """
        Obtiene todos los productos disponibles.
        
        Returns:
            DTO con lista de productos
        """
        products = await self.product_repository.get_all()
        return ProductListResponseDTO(
            total=len(products),
            products=[
                ProductResponseDTO(
                    **product.__dict__,
                    is_available=product.is_available()
                ) for product in products
            ]
        )
    
    async def get_product(self, product_id: int) -> ProductResponseDTO:
        """
        Obtiene un producto por ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            DTO del producto
            
        Raises:
            ProductNotFoundException: Si el producto no existe
        """
        product = await self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(product_id)
        return ProductResponseDTO(
            **product.__dict__,
            is_available=product.is_available()
        )
    
    async def get_available_products(self) -> ProductListResponseDTO:
        """
        Obtiene solo los productos con stock disponible.
        
        Returns:
            DTO con productos disponibles
        """
        products = await self.product_repository.get_available()
        return ProductListResponseDTO(
            total=len(products),
            products=[
                ProductResponseDTO(
                    **product.__dict__,
                    is_available=product.is_available()
                ) for product in products
            ]
        )
    
    async def format_products_for_context(self) -> str:
        """
        Formatea los productos para usar como contexto en la IA.
        
        Returns:
            String con descripción de productos para Gemini
        """
        products = await self.product_repository.get_available()
        
        if not products:
            return "No hay productos disponibles en este momento."
        
        formatted = "## Productos Disponibles:\n\n"
        for p in products:
            formatted += (
                f"- **{p.name}** (ID: {p.id})\n"
                f"  Marca: {p.brand}\n"
                f"  Categoría: {p.category}\n"
                f"  Talla: {p.size}\n"
                f"  Color: {p.color}\n"
                f"  Precio: ${p.price}\n"
                f"  Stock: {p.stock} unidades\n\n"
            )
        return formatted