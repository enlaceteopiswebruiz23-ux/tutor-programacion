"""Etapa 5: esquema de la respuesta estructurada (structured output)."""
from typing import Literal
from pydantic import BaseModel, Field


class RespuestaTutor(BaseModel):
    tema: Literal["variables", "condicionales", "bucles", "funciones", "otro"] = Field(
        description="Tema principal de la duda del alumno."
    )
    dificultad: Literal["basica", "intermedia", "avanzada"] = Field(
        description="Dificultad de la pregunta."
    )
    uso_apuntes: bool = Field(
        description="True si la respuesta se apoyó en los apuntes de la clase."
    )
    respuesta: str = Field(
        description="Explicación para el alumno, en español, con un ejemplo corto."
    )
