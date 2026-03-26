from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="ML API - Nivel 2 (Con Pydantic)")

# 1. ESQUEMA DE ENTRADA ESTRICTO
class Caracteristicas(BaseModel):
    feature_1: float = Field(..., description="Medida en cm", example=12.5)
    feature_2: float = Field(..., description="Peso en kg", example=4.2)

# 2. ESQUEMA DE SALIDA
class Resultado(BaseModel):
    clase_predicha: int
    etiqueta: str

def modelo_dummy(f1: float, f2: float) -> int:
    return 1 if (f1 * 0.5 + f2) > 10 else 0

@app.post("/predecir_estructurado", response_model=Resultado)
def predecir_mejorado(datos: Caracteristicas):
    pred = modelo_dummy(datos.feature_1, datos.feature_2)
    etiqueta = "Aprobado" if pred == 1 else "Rechazado"
    
    return Resultado(clase_predicha=pred, etiqueta=etiqueta)
