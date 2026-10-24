# Tutor de Programación Básica con IA

Chat web (Flask) que explica variables, condicionales, bucles y funciones.
Usa prompt de sistema, memoria de conversación (Supabase), RAG con pgvector,
respuesta estructurada (Pydantic) y un script de evaluación.

## Puesta en marcha
1. `python -m venv .venv` y activarlo; luego `pip install -r requirements.txt`
2. Copia `.env.example` a `.env` y llena las 5 variables (nunca subas `.env`).
3. En Supabase (SQL Editor) ejecuta todo el contenido de `schema.sql`.
4. Carga los apuntes: `python -m scripts.cargar_apuntes`
5. Ejecuta: `python app.py` y abre http://127.0.0.1:5000
6. Evaluación: `python -m scripts.evaluar` (genera `evaluacion_resultados.md`)

## Despliegue en Render
- Web Service conectado a este repositorio de GitHub.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Variables de entorno (panel Environment): las 5 del `.env.example`.
