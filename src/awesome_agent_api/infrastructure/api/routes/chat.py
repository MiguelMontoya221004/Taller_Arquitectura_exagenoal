"""
Endpoints para chat con IA.

Define las rutas REST para interactuar con el asistente inteligente.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.awesome_agent_api.infrastructure.db.database import get_db
from src.awesome_agent_api.infrastructure.repositories.chat_repository_impl import ChatRepositoryImpl
from src.awesome_agent_api.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from src.awesome_agent_api.infrastructure.llm_providers.gemini_service import GeminiService
from src.awesome_agent_api.application.services.chat_service import ChatService
from src.awesome_agent_api.application.dtos.chat_dto import (
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryResponseDTO
)
from src.awesome_agent_api.domain.exceptions import ChatSessionException

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    """
    Crea el servicio de chat con inyección de dependencias.

    Args:
        db: Sesión de base de datos

    Returns:
        Instancia de ChatService
    """
    chat_repository = ChatRepositoryImpl(db)
    product_repository = ProductRepositoryImpl(db)
    gemini_service = GeminiService()
    return ChatService(chat_repository, product_repository, gemini_service)


@router.post("/", response_model=ChatMessageResponseDTO)
async def send_message(
    request: ChatMessageRequestDTO,
    service: ChatService = Depends(get_chat_service)
):
    """
    Envía un mensaje al asistente y recibe respuesta IA.

    Args:
        request: Mensaje del usuario con session_id

    Returns:
        Respuesta del asistente

    Raises:
        HTTPException 500: Si hay error en el procesamiento
    """
    try:
        return await service.process_message(
            session_id=request.session_id,
            user_message=request.message
        )
    except ChatSessionException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=ChatHistoryResponseDTO)
async def get_chat_history(
    session_id: str,
    service: ChatService = Depends(get_chat_service)
):
    """
    Obtiene el historial de conversación de una sesión.

    Args:
        session_id: ID de la sesión

    Returns:
        Historial de mensajes
    """
    messages = await service.get_chat_history(session_id)
    return ChatHistoryResponseDTO(
        session_id=session_id,
        messages=messages,
        total_messages=len(messages)
    )