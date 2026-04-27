"""
Entidad ChatMessage - Representa un mensaje en la conversación.

Mantiene el historial de interacciones usuario-asistente.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Roles posibles en una conversación."""
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """
    Representa un mensaje en el chat.
    
    Attributes:
        id: Identificador único del mensaje
        session_id: ID de la sesión/usuario
        role: Rol del que envía el mensaje (user o assistant)
        content: Contenido del mensaje
        timestamp: Hora del mensaje
    """
    id: int
    session_id: str
    role: MessageRole
    content: str
    timestamp: datetime = None
    
    def __post_init__(self):
        """Validaciones después de la inicialización."""
        if not self.session_id or not self.session_id.strip():
            raise ValueError("session_id no puede estar vacío")
        if not self.content or not self.content.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío")
        if self.timestamp is None:
            self.timestamp = datetime.now()