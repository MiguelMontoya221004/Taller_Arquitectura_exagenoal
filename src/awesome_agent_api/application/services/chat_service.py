"""
ChatService - Casos de uso para chat.

Orquesta el flujo completo de una conversación con IA.
"""

from typing import List, Optional
from datetime import datetime
from src.awesome_agent_api.domain.repositories.chat_repository import ChatRepository
from src.awesome_agent_api.domain.repositories.product_repository import ProductRepository
from src.awesome_agent_api.domain.entities.chat_message import ChatMessage, MessageRole
from src.awesome_agent_api.domain.exceptions import ChatSessionException
from src.awesome_agent_api.infrastructure.llm_providers.gemini_service import GeminiService
from src.awesome_agent_api.application.services.product_service import ProductService
from src.awesome_agent_api.application.dtos.chat_dto import ChatMessageResponseDTO


class ChatService:
    """
    Servicio de aplicación para chat inteligente.
    
    Orquesta la obtención de contexto, llamada a IA, y persistencia.
    """
    
    def __init__(
        self,
        chat_repository: ChatRepository,
        product_repository: ProductRepository,
        gemini_service: GeminiService
    ):
        """
        Inicializa el servicio.
        
        Args:
            chat_repository: Repositorio de mensajes
            product_repository: Repositorio de productos
            gemini_service: Cliente de Google Gemini
        """
        self.chat_repository = chat_repository
        self.product_service = ProductService(product_repository)
        self.gemini_service = gemini_service
    
    async def process_message(
        self,
        session_id: str,
        user_message: str
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera respuesta con IA.
        
        Args:
            session_id: ID único del usuario
            user_message: Mensaje del usuario
            
        Returns:
            DTO con la respuesta del asistente
            
        Raises:
            ChatSessionException: Si hay error en el procesamiento
        """
        try:
            # 1. Guardar mensaje del usuario
            user_msg_entity = ChatMessage(
                id=None,
                session_id=session_id,
                role=MessageRole.USER,
                content=user_message,
                timestamp=datetime.now()
            )
            saved_user_msg = await self.chat_repository.save(user_msg_entity)
            
            # 2. Obtener contexto (productos disponibles)
            products_context = await self.product_service.format_products_for_context()
            
            # 3. Obtener historial anterior
            history = await self.chat_repository.get_history(session_id, limit=5)
            conversation_history = self._format_history(history)
            
            # 4. Llamar a Gemini con contexto
            assistant_response = await self.gemini_service.generate_response(
                user_message=user_message,
                products_context=products_context,
                conversation_history=conversation_history,
                system_prompt=self._get_system_prompt()
            )
            
            # 5. Guardar respuesta del asistente
            assistant_msg_entity = ChatMessage(
                id=None,
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=assistant_response,
                timestamp=datetime.now()
            )
            saved_assistant_msg = await self.chat_repository.save(assistant_msg_entity)
            
            # 6. Retornar DTO
            return ChatMessageResponseDTO(
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_response,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            raise ChatSessionException(f"Error procesando mensaje: {str(e)}")
    
    async def get_chat_history(self, session_id: str) -> List[dict]:
        """
        Obtiene el historial de chat de una sesión.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Lista de mensajes
        """
        messages = await self.chat_repository.get_history(session_id, limit=50)
        return [
            {
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    
    def _format_history(self, messages: List[ChatMessage]) -> str:
        """
        Formatea el historial para enviar a Gemini.
        
        Args:
            messages: Lista de mensajes
            
        Returns:
            String formateado
        """
        if not messages:
            return "Esta es la primera pregunta del usuario."
        
        formatted = "## Historial de conversación:\n\n"
        for msg in messages:
            role_label = "Usuario" if msg.role == MessageRole.USER else "Asistente"
            formatted += f"**{role_label}:** {msg.content}\n\n"
        return formatted
    
    def _get_system_prompt(self) -> str:
        """
        Retorna el prompt del sistema para Gemini.
        
        Returns:
            String con instrucciones para la IA
        """
        return """Eres un asistente amable y experto en zapatos de una tienda online.
Tu objetivo es ayudar a los clientes a encontrar el zapato perfecto.

Sigue estas reglas:
1. Sé amable y profesional
2. Basate en los productos disponibles listados
3. Haz recomendaciones personalizadas
4. Si el cliente pregunta sobre un producto específico, proporciona todos los detalles
5. Sugiere alternativas cuando sea apropiado
6. Nunca inventes productos que no estén en la lista

Responde siempre en español."""