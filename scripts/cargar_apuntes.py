"""Sube los apuntes de la carpeta apuntes/ a Supabase con su embedding.
Uso (desde la raíz del proyecto):  python -m scripts.cargar_apuntes
"""
from pathlib import Path
from db import obtener_cliente
from services.rag_service import obtener_embeddings


def dividir_en_fragmentos(texto):
    """Corta el archivo en secciones que empiezan con '## '."""
    partes = [p.strip() for p in texto.split("\n## ")]
    return [p if i == 0 else "## " + p for i, p in enumerate(partes) if p]


def main():
    cliente = obtener_cliente()
    embeddings = obtener_embeddings()

    cliente.table("apuntes").delete().neq("id", 0).execute()  # evita duplicados

    total = 0
    for archivo in sorted(Path("apuntes").glob("*.md")):
        fragmentos = dividir_en_fragmentos(archivo.read_text(encoding="utf-8"))
        vectores = embeddings.embed_documents(fragmentos)
        filas = [
            {"archivo": archivo.name, "contenido": f, "embedding": v}
            for f, v in zip(fragmentos, vectores)
        ]
        cliente.table("apuntes").insert(filas).execute()
        total += len(filas)
        print(f"{archivo.name}: {len(filas)} fragmentos")
    print(f"Listo: {total} fragmentos guardados.")


if __name__ == "__main__":
    main()
