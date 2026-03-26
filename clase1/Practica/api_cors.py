from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="API básica con CORS")

# Configuramos el Middleware para permitir conexiones externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, reemplazar '*' por los dominios de tu Frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/usuarios")
def obtener_usuarios():
    try:
        with open("datos_locales.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Archivo no encontrado."}
