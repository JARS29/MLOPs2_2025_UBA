from fastapi import FastAPI, HTTPException, Security, APIRouter
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field

app = FastAPI(title="ML API - Nivel 3 (Producción)")

# --- SEGURIDAD ---
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
CLIENTES_AUTORIZADOS = {"token-secreto-123": "Cliente_Alpha"}

def validar_token(api_key: str = Security(api_key_header)):
    if api_key not in CLIENTES_AUTORIZADOS:
        raise HTTPException(status_code=403, detail="Token inválido.")
    return CLIENTES_AUTORIZADOS[api_key]

# --- ESQUEMAS ---
class Caracteristicas(BaseModel):
    feature_1: float = Field(..., example=12.5)
    feature_2: float = Field(..., example=4.2)

# --- REGISTRO DE MODELOS (Simulado) ---
class ModeloV1:
    def predecir(self, f1: float, f2: float) -> int:
        return 1 if (f1 * 0.5 + f2) > 10 else 0  # Lógica antigua

class ModeloV2:
    def predecir(self, f1: float, f2: float) -> int:
        return 1 if (f1 * 0.8 + f2 ** 1.2) > 15 else 0 # Nueva lógica optimizada

modelos = {"v1": ModeloV1(), "v2": ModeloV2()}

# --- ENRUTAMIENTO VERSIONADO ---
router_v1 = APIRouter(prefix="/v1", tags=["Modelo V1"])
router_v2 = APIRouter(prefix="/v2", tags=["Modelo V2 (Beta)"])

@router_v1.post("/predecir")
def prediccion_v1(datos: Caracteristicas, cliente: str = Security(validar_token)):
    res = modelos["v1"].predecir(datos.feature_1, datos.feature_2)
    return {"version": "1.0", "prediccion": res}

@router_v2.post("/predecir")
def prediccion_v2(datos: Caracteristicas, cliente: str = Security(validar_token)):
    res = modelos["v2"].predecir(datos.feature_1, datos.feature_2)
    return {"version": "2.0", "prediccion": res}

app.include_router(router_v1)
app.include_router(router_v2)
