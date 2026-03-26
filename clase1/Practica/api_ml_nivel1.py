from fastapi import FastAPI

app = FastAPI(title="ML API - Nivel 1")

def modelo_dummy(f1: float, f2: float) -> int:
    # Si la suma ponderada supera el umbral, clase 1 (Positivo), si no, 0 (Negativo)
    return 1 if (f1 * 0.5 + f2) > 10 else 0

@app.post("/predecir_basico")
def predecir_simple(feature_1: float, feature_2: float):
    prediccion = modelo_dummy(feature_1, feature_2)
    return {"prediccion": prediccion}
