from fastapi import FastAPI
import json

app = FastAPI(title="API Básica")

@app.get("/usuarios")
def obtener_usuarios():
    try:
        with open("datos_locales.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Archivo no encontrado."}
