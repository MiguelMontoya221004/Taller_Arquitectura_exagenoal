"""
Excepciones del dominio.

Define excepciones específicas del negocio, no genéricas de Python.
"""


class DomainException(Exception):
    """Excepción base para excepciones del dominio."""
    pass


class ProductNotFoundException(DomainException):
    """Se lanza cuando un producto no es encontrado."""
    
    def __init__(self, product_id: int):
        super().__init__(f"Producto con ID {product_id} no encontrado")


class InsufficientStockException(DomainException):
    """Se lanza cuando no hay suficiente stock."""
    
    def __init__(self, product_id: int, requested: int, available: int):
        super().__init__(
            f"Stock insuficiente para producto {product_id}. "
            f"Solicitado: {requested}, Disponible: {available}"
        )


class InvalidProductException(DomainException):
    """Se lanza cuando los datos del producto son inválidos."""
    pass


class ChatSessionException(DomainException):
    """Se lanza cuando hay error en la sesión de chat."""
    pass