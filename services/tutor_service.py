"""Etapas 1-5: prompt de sistema, memoria, RAG y respuesta estructurada."""
import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from db import guardar_mensaje, obtener_historial
from schemas import RespuestaTutor
from services.rag_service import buscar_fragmentos

load_dotenv()

# ---- Etapa 2: prompt de sistema con rol y nivel ----
PROMPT_SISTEMA = """Eres un tutor de programación básica en Python, paciente y amable.
Tus temas son: variables, condicionales, bucles y funciones.
Reglas:
- Responde siempre en español, con lenguaje sencillo.
- Da una explicación corta y un ejemplo de código pequeño.
- No hagas la tarea completa del alumno: guíalo con pistas.
- Si la pregunta no es de programación básica, di con amabilidad que solo ayudas con ese tema.
- Si hay apuntes de la clase, apóyate en ellos y no inventes cosas que contradigan los apuntes.
"""

NIVELES = {
    "principiante": "El alumno es PRINCIPIANTE: usa analogías cotidianas, evita tecnicismos y avanza despacio.",
    "intermedio": "El alumno es INTERMEDIO: puedes usar términos técnicos y mencionar buenas prácticas.",
}


def crear_modelo():
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"), temperature=0.3)
    # ---- Etapa 5: salida con campos definidos ----
    return llm.with_structured_output(RespuestaTutor)


def armar_prompt_sistema(nivel, fragmentos):
    texto = PROMPT_SISTEMA + "\n" + NIVELES.get(nivel, NIVELES["principiante"])
    if fragmentos:
        apuntes = "\n---\n".join(f["contenido"] for f in fragmentos)
        texto += f"\n\nAPUNTES DE LA CLASE (úsalos como base):\n{apuntes}"
    else:
        texto += "\n\nNo se encontraron apuntes relacionados; responde con tu conocimiento general."
    return texto


def responder(sesion, pregunta, nivel="principiante"):
    """Responde una duda. Devuelve un dict con tema, dificultad, uso_apuntes y respuesta."""
    # ---- Etapa 3: memoria. Se reenvía el historial guardado en cada turno ----
    historial = obtener_historial(sesion)

    # ---- Etapa 4: RAG ----
    fragmentos = buscar_fragmentos(pregunta)

    mensajes = [SystemMessage(content=armar_prompt_sistema(nivel, fragmentos))]
    for m in historial:
        clase = HumanMessage if m["rol"] == "user" else AIMessage
        mensajes.append(clase(content=m["contenido"]))
    mensajes.append(HumanMessage(content=pregunta))

    resultado = crear_modelo().invoke(mensajes)
    datos = resultado.model_dump()
    datos["uso_apuntes"] = bool(fragmentos)  # dato real, no la opinión del modelo

    guardar_mensaje(sesion, "user", pregunta)
    guardar_mensaje(sesion, "assistant", datos["respuesta"])
    return datos
