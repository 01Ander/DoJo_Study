"""
Módulo transaction_schema.py — Quest 06-03: Validación de Esquemas con Pydantic

Completa la excepción personalizada, el modelo TransactionPayload y la función de validación
siguiendo las especificaciones de Lore 06 §5 y el contrato de la quest.
"""

from pydantic import BaseModel, Field, field_validator, ValidationError


class InvalidTransactionDataError(Exception):
    """Excepción de dominio lanzada cuando una carga útil de transacción no es válida."""
    pass


class TransactionPayload(BaseModel):
    """
    Modelo de validación para transacciones financieras.

    Campos requeridos:
    - transaction_id: str (longitud mínima de 3 caracteres)
    - account_id: int (estrictamente positivo, gt=0)
    - amount: float (estrictamente positivo, gt=0.0)
    - currency: str (valor por defecto "USD")

    Validador personalizado para 'currency':
    - Debe convertir el valor recibido a mayúsculas.
    - Debe verificar que pertenezca a: {"USD", "EUR", "GBP", "COP"}.
    - Si no pertenece, debe levantar un ValueError con un mensaje explicativo.
    """
    # TODO: Define los campos transaction_id, account_id, amount y currency con sus restricciones
    pass

    # TODO: Implementa el validador @field_validator("currency") con @classmethod
    # pass


def validate_and_create_transaction(data: dict) -> TransactionPayload:
    """
    Parsea y valida un diccionario crudo en una instancia de TransactionPayload.

    - Intenta instanciar TransactionPayload(**data).
    - Si se produce un ValidationError de Pydantic, captura la excepción y levanta
      un InvalidTransactionDataError conteniendo información del fallo.
    - Si la validación es exitosa, retorna la instancia de TransactionPayload.
    """
    # TODO: Implementar try/except capturando ValidationError y levantando InvalidTransactionDataError
    pass
