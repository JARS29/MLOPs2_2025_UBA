# Sesión 1 — Del modelo al servicio: despliegue y APIs REST productivas

Primera capa de la plataforma del curso: servimos el modelo por REST y aprendemos a hacerlo bien.
Clase **100% online**, ~90–120 min.

---

## Parte teórica (`teoria/`)

- Repaso del ciclo de vida de un proyecto de ML y puente de MLOps I a II.
- **Despliegue de modelos:** qué significa; patrones (estático, en el dispositivo, en el servidor, transmisión) y estrategias (único, silencioso/shadow, A/B, canary, bandidos).
- **Predicción online vs batch.** Dónde corre el servicio: máquina virtual, contenedores y serverless.
- **APIs, microservicios y REST:** el memo de Bezos, qué es una API, historia de protocolos (SOAP → REST → gRPC → GraphQL), monolito vs microservicios (SOA).
- **HTTP en detalle:** modelo cliente–servidor, métodos ↔ CRUD, códigos de estado, endpoints, OpenAPI.
- **Diseño productivo:** contratos y validación (Pydantic), versionado (API y modelo), estado/escalabilidad, qué monitorear.
- **Implementación en Python:** Flask/Django/**FastAPI**; consumir APIs con `requests`; interfaces rápidas con gradio/streamlit.

Material: `MLOPS II - Intro.pdf`, `clase1.pdf`. La presentación (`Sesion1_APIs_REST_2026.pptx`) y las guías del docente están fuera del repo, junto a los pptx.

## Parte práctica (`Practica/`) — cómo correr

Construimos una ML API desde un juguete hasta producción. El notebook **`API_MLOPS2.ipynb`** es el hilo: genera y prueba cada script. Todo corre de punta a punta.

**El curso usa [uv](https://docs.astral.sh/uv/)** como gestor de entornos y dependencias (más rápido que pip/Poetry). Preparación, parado **dentro de `Practica/`**:

```bash
uv venv                              # crea el entorno .venv
uv pip install -r requirements.txt   # instala fastapi, uvicorn, pydantic, requests
```

> **Para correr `API_MLOPS2.ipynb`.** Lo más simple es usar el entorno del curso (`uv sync` en la raíz, que ya trae Jupyter e ipykernel) y elegir su kernel. Si querés usar el entorno local de `Practica/`, agregale el kernel: `uv pip install ipykernel jupyter` y registralo con `uv run python -m ipykernel install --user --name mlops2 --display-name "Python (MLOps2 · uv)"`. Ver la sección **Puesta en marcha** del README del repo.

> **¿Todavía usás Poetry o pip?** Podés instalar las mismas dependencias con `pip install -r requirements.txt` dentro de tu entorno (o `poetry add fastapi uvicorn pydantic requests`) y reemplazar en los comandos de abajo `uv run uvicorn ...` por `python -m uvicorn ...` (con el entorno activado). El resto es idéntico.

| Paso | Archivo | Qué hace | Cómo correr |
|---|---|---|---|
| 1 | `simple_api.py` | API básica: `GET /usuarios` lee `datos_locales.json` | `uv run uvicorn simple_api:app --reload --port 8001` → ver `http://localhost:8001/docs` |
| 2 | `frontend_API.html` | Frontend que **falla** por la política CORS del navegador | abrir el `.html` con la API 8001 corriendo (F12 → Console) |
| 3 | `api_cors.py` + `frontend_API_cors.html` | Misma API **con CORS**: ahora el frontend funciona | `uv run uvicorn api_cors:app --reload --port 8002` y abrir el html |
| 4 | `api_ml_nivel1.py` | ML API nivel 1: `POST /predecir_basico` (features por query) | `uv run uvicorn api_ml_nivel1:app --reload --port 8003` |
| 5 | `api_ml_nivel2.py` | Nivel 2: validación **Pydantic** (entrada + salida), `/predecir_estructurado` | `uv run uvicorn api_ml_nivel2:app --reload --port 8004` |
| 6 | `api_ml_nivel3.py` | Nivel 3 (producción): **API Key** `X-API-KEY` + versionado `/v1` y `/v2` | `uv run uvicorn api_ml_nivel3:app --reload --port 8080` |

Consumo del Nivel 3 (con token):
```python
import requests
h = {"X-API-KEY": "token-secreto-123"}
p = {"feature_1": 12.5, "feature_2": 4.2}
print(requests.post("http://localhost:8080/v1/predecir", json=p, headers=h).json())
```

### Empaquetar en Docker (opcional, on-ramp al TP)

En `Practica/` hay un **`Dockerfile`** (que usa uv) y un **`requirements.txt`** que empaquetan la API de Nivel 3:

```bash
# desde Practica/
docker build -t mlapi-nivel3 .
docker run -p 8080:8080 mlapi-nivel3
# API en http://localhost:8080  (probar con el header X-API-KEY)
```

Qué hace el Dockerfile: parte de `python:3.11-slim`, copia el binario de **uv** desde su imagen oficial, instala las dependencias de `requirements.txt` con `uv pip install --system`, copia el código y arranca `uvicorn api_ml_nivel3:app` en el puerto 8080. `docker build` crea la imagen; `docker run -p 8080:8080` la ejecuta y publica el puerto. En Sesión 1 es opcional; se vuelve central en el TP integrador y en la Sesión 5 (nube/Data Lakes).

## Qué se debe entregar — Mini-TP 1 (individual, esta semana)

Serví **tu** modelo (el de Aprendizaje de Máquina, o uno simple) con FastAPI:

1. Contrato Pydantic con las **features reales** del modelo.
2. Endpoint `/v1/predict` (online) y `/health`.
3. La respuesta devuelve la predicción y la **versión del modelo**.
4. Un cliente que dispare un caso válido y uno inválido (mostrar el 422).

**Se evalúa:** que corra de punta a punta; que la validación rechace entradas malas; que el contrato coincida con las features del modelo; y que el código esté en el repo con un README de cómo ejecutarlo (con `uv`). Es el cimiento del TP integrador.
