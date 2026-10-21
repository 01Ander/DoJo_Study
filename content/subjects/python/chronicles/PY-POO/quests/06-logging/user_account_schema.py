"""
Módulo user_account_schema.py — Quest 06-03: De Dataclass a Pydantic BaseModel

Tu tarea es sustituir la dataclass por un modelo Pydantic V2 que garantice
la integridad de los datos en tiempo de ejecución.
"""

from pydantic import BaseModel, Field


class UserAccount(BaseModel):
    """
    Modelo de cuenta de usuario con validación en tiempo de ejecución.

    Campos requeridos:
    - username: str (longitud mínima de 3 caracteres)
    - age: int (mayor o igual a 18 años, ge=18)
    - balance: float (mayor o igual a 0.0, ge=0.0)
    - is_active: bool (valor por defecto True)
    """
    # TODO: Define los campos requeridos utilizando Field con sus restricciones declarativas
    username: str = Field(min_length=3)
    age: int = Field(ge=18)
    balance: float = Field(ge=0.0)
    is_active: bool = True