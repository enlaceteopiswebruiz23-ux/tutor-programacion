"""Etapa 6: evaluación del tutor con preguntas de prueba y una rúbrica.
Uso:  python -m scripts.evaluar
Rúbrica (4 puntos por pregunta):
  1) Detecta el tema correcto.
  2) Menciona al menos una palabra clave esperada.
  3) Se apoyó en los apuntes (uso_apuntes = True).
  4) Incluye un ejemplo de código.
"""
import uuid
from services.tutor_service import responder

PRUEBAS = [
    ("¿Qué es una variable en Python?", "variables", ["variable", "valor", "nombre"]),
    ("¿Cómo guardo mi edad en una variable?", "variables", ["=", "edad"]),
    ("¿Para qué sirve if y else?", "condicionales", ["if", "else", "condición"]),
    ("¿Qué hace elif?", "condicionales", ["elif", "condición"]),
    ("¿Cómo repito algo 5 veces?", "bucles", ["for", "range"]),
    ("¿Cuál es la diferencia entre for y while?", "bucles", ["for", "while"]),
    ("¿Cómo creo una función que sume dos números?", "funciones", ["def", "return"]),
    ("¿Qué son los parámetros de una función?", "funciones", ["parámetro", "argumento", "def"]),
]


def calificar(esperado_tema, palabras, r):
    texto = r["respuesta"].lower()
    puntos = [
        r["tema"] == esperado_tema,
        any(p.lower() in texto for p in palabras),
        r["uso_apuntes"],
        "```" in r["respuesta"] or "    " in r["respuesta"] or "print(" in texto or "def " in texto,
    ]
    return sum(puntos)


def main():
    total = 0
    lineas = ["# Resultados de la evaluación", "", "| Pregunta | Tema | Puntos (de 4) |", "|---|---|---|"]
    for pregunta, tema, palabras in PRUEBAS:
        r = responder(str(uuid.uuid4()), pregunta, "principiante")  # sesión nueva por pregunta
        p = calificar(tema, palabras, r)
        total += p
        print(f"[{p}/4] {pregunta} -> tema detectado: {r['tema']}")
        lineas.append(f"| {pregunta} | {r['tema']} | {p} |")
    maximo = 4 * len(PRUEBAS)
    resumen = f"Puntaje total: {total}/{maximo} ({round(100 * total / maximo)}%)"
    print(resumen)
    lineas += ["", f"**{resumen}**"]
    with open("evaluacion_resultados.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")


if __name__ == "__main__":
    main()
