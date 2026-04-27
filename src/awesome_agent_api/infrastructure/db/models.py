"""
Modelos ORM de SQLAlchemy.

Mapean las entidades del dominio a tablas de base de datos.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from src.awesome_agent_api.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM para productos.
    
    Mapea la tabla 'products' en la base de datos.
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    color = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.now)


class ChatMessageModel(Base):
    """
    Modelo ORM para mensajes de chat.
    
    Mapea la tabla 'chat_messages' en la base de datos.
    """
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" o "assistant"
    content = Column(String(4000), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, index=True)