"""
Data Transfer Objects para productos.

Los DTOs son modelos Pydantic para validación y serialización.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreateDTO(BaseModel):
    """DTO para crear un producto."""
    name: str = Field(..., min_length=1, description="Nombre del producto")
    brand: str = Field(..., min_length=1, description="Marca")
    category: str = Field(..., min_length=1, description="Categoría")
    size: int = Field(..., gt=0, description="Talla")
    color: str = Field(..., min_length=1, description="Color")
    price: float = Field(..., gt=0, description="Precio")
    stock: int = Field(..., ge=0, description="Stock inicial")
    description: Optional[str] = None


class ProductResponseDTO(BaseModel):
    """DTO para respuesta de producto."""
    id: int
    name: str
    brand: str
    category: str
    size: int
    color: str
    price: float
    stock: int
    description: Optional[str] = None
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponseDTO(BaseModel):
    """DTO para lista de productos."""
    total: int
    products: list[ProductResponseDTO]