"""
Entidad Product - Representa un zapato en el inventario.

Esta entidad encapsula las reglas de negocio relacionadas con productos.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Representa un producto (zapato) en el sistema.
    
    Attributes:
        id: Identificador único del producto
        name: Nombre del zapato (ej: "Air Zoom Pegasus")
        brand: Marca (ej: "Nike", "Adidas")
        category: Categoría (ej: "Running", "Casual")
        size: Talla disponible
        color: Color del zapato
        price: Precio en USD (debe ser > 0)
        stock: Cantidad disponible (no puede ser negativa)
        description: Descripción del producto
        created_at: Fecha de creación
    """
    id: int
    name: str
    brand: str
    category: str
    size: int
    color: str
    price: float
    stock: int
    description: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        """Validaciones de la entidad después de la inicialización."""
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
    
    def is_available(self) -> bool:
        """
        Verifica si el producto está disponible.
        
        Returns:
            bool: True si hay stock disponible
        """
        return self.stock > 0
    
    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto.
        
        Args:
            quantity: Cantidad a reducir
            
        Raises:
            ValueError: Si la cantidad es mayor al stock disponible
        """
        if quantity > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= quantity