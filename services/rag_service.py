"""Etapa 4: RAG. Busca en los apuntes los fragmentos más parecidos a la pregunta."""
import os
from langchain_openai import OpenAIEmbeddings
from db import obtener_cliente

UMBRAL_SIMILITUD = 0.30


def obtener_embeddings():
    modelo = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=modelo)


def buscar_fragmentos(pregunta, cantidad=3):
    """Devuelve una lista de fragmentos (dict) relevantes para la pregunta."""
    vector = obtener_embeddings().embed_query(pregunta)
    res = obtener_cliente().rpc(
        "buscar_apuntes", {"query_embedding": vector, "cantidad": cantidad}
    ).execute()
    return [f for f in (res.data or []) if f["similitud"] >= UMBRAL_SIMILITUD]
