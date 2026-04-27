"""
Interfaz para acceso a datos de productos.

Define el contrato que debe cumplir cualquier implementación de repositorio.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.awesome_agent_api.domain.entities.product import Product


class ProductRepository(ABC):
    """
    Interfaz de repositorio para productos.
    
    Define los métodos que debe implementar cualquier repositorio de productos.
    """
    
    @abstractmethod
    async def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos disponibles.
        
        Returns:
            Lista de productos
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Producto encontrado o None
        """
        pass
    
    @abstractmethod
    async def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos por marca.
        
        Args:
            brand: Nombre de la marca
            
        Returns:
            Lista de productos de esa marca
        """
        pass
    
    @abstractmethod
    async def get_available(self) -> List[Product]:
        """
        Obtiene productos con stock disponible.
        
        Returns:
            Lista de productos disponibles
        """
        pass