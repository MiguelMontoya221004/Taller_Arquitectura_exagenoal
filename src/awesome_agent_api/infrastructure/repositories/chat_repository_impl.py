"""
Implementación del repositorio de chat.

Persistencia de mensajes en SQLite.
"""

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from src.awesome_agent_api.domain.repositories.chat_repository import ChatRepository
from src.awesome_agent_api.domain.entities.chat_message import ChatMessage, MessageRole
from src.awesome_agent_api.infrastructure.db.models import ChatMessageModel


class ChatRepositoryImpl(ChatRepository):
    """
    Implementación del repositorio de chat en SQLite.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    async def save(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            message: Entidad ChatMessage
            
        Returns:
            Mensaje guardado con ID
        """
        model = ChatMessageModel(
            session_id=message.session_id,
            role=message.role.value,
            content=message.content,
            timestamp=message.timestamp or datetime.now()
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return self._model_to_entity(model)
    
    async def get_history(self, session_id: str, limit: int = 6) -> List[ChatMessage]:
        """
        Obtiene el historial de una sesión.
        
        Args:
            session_id: ID de la sesión
            limit: Número máximo de mensajes
            
        Returns:
            Lista de mensajes ordenados
        """
        models = self.db.query(ChatMessageModel).filter(
            ChatMessageModel.session_id == session_id
        ).order_by(
            ChatMessageModel.timestamp.desc()
        ).limit(limit).all()
        
        # Invertir para obtener orden cronológico
        return [self._model_to_entity(m) for m in reversed(models)]
    
    async def clear_history(self, session_id: str) -> None:
        """
        Borra el historial de una sesión.
        
        Args:
            session_id: ID de la sesión
        """
        self.db.query(ChatMessageModel).filter(
            ChatMessageModel.session_id == session_id
        ).delete()
        self.db.commit()
    
    def _model_to_entity(self, model: ChatMessageModel) -> ChatMessage:
        """
        Convierte modelo ORM a entidad.
        
        Args:
            model: Modelo ChatMessageModel
            
        Returns:
            Entidad ChatMessage
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=MessageRole(model.role),
            content=model.content,
            timestamp=model.timestamp
        )