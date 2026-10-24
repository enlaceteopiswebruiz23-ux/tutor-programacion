"""Conexión a Supabase y funciones para guardar/leer mensajes."""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_cliente = None


def obtener_cliente():
    """Crea el cliente de Supabase una sola vez."""
    global _cliente
    if _cliente is None:
        _cliente = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    return _cliente


def guardar_mensaje(sesion, rol, contenido):
    """Guarda un mensaje ('user' o 'assistant') en la tabla mensajes."""
    obtener_cliente().table("mensajes").insert(
        {"sesion": sesion, "rol": rol, "contenido": contenido}
    ).execute()


def obtener_historial(sesion, limite=10):
    """Devuelve los últimos mensajes de la sesión, del más viejo al más nuevo."""
    res = (
        obtener_cliente()
        .table("mensajes")
        .select("rol, contenido")
        .eq("sesion", sesion)
        .order("id", desc=True)
        .limit(limite)
        .execute()
    )
    return list(reversed(res.data))
