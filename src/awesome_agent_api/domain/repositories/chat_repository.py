"""
Interfaz para acceso a datos de chat.

Define el contrato para persistencia de mensajes de chat.
"""

from abc import ABC, abstractmethod
from typing import List
from src.awesome_agent_api.domain.entities.chat_message import ChatMessage


class ChatRepository(ABC):
    """Interfaz de repositorio para mensajes de chat."""
    
    @abstractmethod
    async def save(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            message: Mensaje a guardar
            
        Returns:
            Mensaje guardado con ID
        """
        pass
    
    @abstractmethod
    async def get_history(self, session_id: str, limit: int = 6) -> List[ChatMessage]:
        """
        Obtiene el historial de una sesión.
        
        Args:
            session_id: ID de la sesión
            limit: Número máximo de mensajes a retornar
            
        Returns:
            Lista de mensajes ordenados por timestamp
        """
        pass
    
    @abstractmethod
    async def clear_history(self, session_id: str) -> None:
        """
        Borra el historial de una sesión.
        
        Args:
            session_id: ID de la sesión a limpiar
        """
        pass