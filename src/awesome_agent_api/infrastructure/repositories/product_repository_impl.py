"""
Implementación del repositorio de productos.

Acceso a datos de productos en SQLite.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.awesome_agent_api.domain.repositories.product_repository import ProductRepository
from src.awesome_agent_api.domain.entities.product import Product
from src.awesome_agent_api.infrastructure.db.models import ProductModel


class ProductRepositoryImpl(ProductRepository):
    """
    Implementación del repositorio de productos en SQLite.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    async def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos.
        
        Returns:
            Lista de entidades Product
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Entidad Product o None
        """
        model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        return self._model_to_entity(model) if model else None
    
    async def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos por marca.
        
        Args:
            brand: Nombre de la marca
            
        Returns:
            Lista de productos
        """
        models = self.db.query(ProductModel).filter(
            ProductModel.brand.ilike(f"%{brand}%")
        ).all()
        return [self._model_to_entity(m) for m in models]
    
    async def get_available(self) -> List[Product]:
        """
        Obtiene productos con stock > 0.
        
        Returns:
            Lista de productos disponibles
        """
        models = self.db.query(ProductModel).filter(
            ProductModel.stock > 0
        ).all()
        return [self._model_to_entity(m) for m in models]
    
    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM a entidad del dominio.
        
        Args:
            model: Modelo ProductModel
            
        Returns:
            Entidad Product
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
            created_at=model.created_at
        )