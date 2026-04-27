"""DTOs para chat."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessageRequestDTO(BaseModel):
    """DTO para enviar mensaje."""
    session_id: str = Field(..., description="ID único del usuario/sesión")
    message: str = Field(..., min_length=1, description="Contenido del mensaje")


class ChatMessageResponseDTO(BaseModel):
    """DTO para respuesta del chat."""
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime
    

class ChatHistoryResponseDTO(BaseModel):
    """DTO para historial de chat."""
    session_id: str
    messages: list[dict]
    total_messages: int