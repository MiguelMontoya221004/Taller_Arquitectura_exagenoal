"""
Servicio de integración con Google Gemini API.

Maneja la comunicación con el modelo de lenguaje.
"""

import os
from google import genai
from typing import Optional


class GeminiService:
    """
    Cliente para interactuar con Google Gemini.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Gemini.

        Args:
            api_key: Clave API de Google (usa variable de entorno si no se proporciona)
        """
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY no configurada")

        self.client = genai.Client(api_key=key)

    async def generate_response(
        self,
        user_message: str,
        products_context: str,
        conversation_history: str,
        system_prompt: str
    ) -> str:
        """
        Genera una respuesta usando Gemini.

        Args:
            user_message: Mensaje del usuario
            products_context: Descripción de productos disponibles
            conversation_history: Historial de conversación
            system_prompt: Instrucciones para el modelo

        Returns:
            Respuesta generada por el modelo
        """
        full_prompt = f"""{system_prompt}

{conversation_history}

{products_context}

Mensaje del usuario: {user_message}

Por favor, responde de manera amable y útil."""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )
        return response.text