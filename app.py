"""Rutas de Flask (la web)."""
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

from services.tutor_service import NIVELES, responder

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambia-esta-llave")


@app.route("/")
def inicio():
    if "sesion" not in session:
        session["sesion"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/preguntar", methods=["POST"])
def preguntar():
    datos = request.get_json(silent=True) or {}
    pregunta = (datos.get("pregunta") or "").strip()
    nivel = datos.get("nivel", "principiante")
    if not pregunta:
        return jsonify({"error": "Escribe una pregunta."}), 400
    if nivel not in NIVELES:
        nivel = "principiante"
    if "sesion" not in session:
        session["sesion"] = str(uuid.uuid4())
    try:
        return jsonify(responder(session["sesion"], pregunta, nivel))
    except Exception as e:  # muestra el error al alumno para depurar
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500


@app.route("/nueva", methods=["POST"])
def nueva_conversacion():
    session["sesion"] = str(uuid.uuid4())
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
