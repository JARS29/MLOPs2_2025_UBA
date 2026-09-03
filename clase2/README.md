# Sesión 2 — GraphQL en MLOps + grafos de linaje

Segunda capa de la plataforma: consultar metadatos y relaciones (linaje) con flexibilidad, cuando REST se queda corto.

---

## Parte teórica (`Teoria/`)

- **Grafos y su importancia:** nodos y aristas (con tipo y dirección); por qué en muchos problemas la relación *es* el dato; recorridos multi-hop; casos (redes, recomendación, fraude, conocimiento, **linaje**).
- **Bases de datos de grafos:** Neo4j (property graph) y **Cypher**; SQL vs Cypher en la consulta multi-hop; cuándo conviene grafo y cuándo relacional.
- **Grafos de linaje en MLOps:** dato → feature → experimento → modelo → despliegue como grafo; trazabilidad, análisis de impacto y auditoría/gobernanza.
- **GraphQL y sus ventajas frente a REST:** over/under-fetching; esquema/SDL, queries, mutations, subscriptions, resolvers; GraphQL vs REST (ventajas y costos); GraphQL en MLOps (metadatos de MLflow, agregación de servicios).

Material: `CL2-grafos_neo4j_graphQL.pdf`. Presentación: `Sesion2_GraphQL_Grafos_2026.pptx` (fuera del repo, junto a los pptx).

## Parte práctica (`Practica/`) — cómo correr

El curso usa **[uv](https://docs.astral.sh/uv/)** y **Docker**. Preparación (una vez, desde la raíz del repo): `uv sync`. O, dentro de `Practica/`: `uv venv && uv pip install strawberry-graphql fastapi "uvicorn[standard]" requests neo4j`.

> Strawberry requiere **Python ≥ 3.11**. Para correr los notebooks, registra el kernel de uv (ver *Puesta en marcha* del README raíz).

| Paso | Archivo | Qué hace | Cómo correr |
|---|---|---|---|
| 1 | `neo4j_sql.ipynb` | Neo4j con Docker + Cypher; **SQL vs grafo** en la consulta multi-hop (actores/películas) | levantar Neo4j (abajo) y correr el notebook con el kernel de uv |
| 2 | `GraphQL.ipynb` | Tutorial GraphQL con **FastAPI + Strawberry** (libros): esquema, queries, mutations, GraphiQL | seguir el notebook; usa `python-graphql-docker-tutorial/` |
| 3 | `python-graphql-docker-tutorial/` | La API GraphQL dockerizada (`app.py`, `client.py`) | `docker build -t graphql-app . && docker run -p 8000:8000 graphql-app` → `/graphql` |
| 4 | `rest_vs_graphql.ipynb` | **REST vs GraphQL con código:** la misma data servida por ambos; mide **llamadas y bytes** para armar una vista (muestra over-fetching y N+1). Autocontenido: corre en un hilo, sin Docker. (`GraphQL_REST_API.ipynb` es la versión original.) | correr el notebook |
| 5 | `graphql_neo4j_lineage.ipynb` | **GraphQL sobre una base de grafos:** notebook-tutorial que escribe `graphql_neo4j_lineage.py` (un resolver que lee el **linaje** desde Neo4j) y lo consulta | ver abajo |
| + | `docker_tutorial.ipynb` | **Docker paso a paso:** contenerizar la API GraphQL (imagen/contenedor, Dockerfile con uv, build/run/logs/stop) | seguir el notebook |
| + | `mini_tp2_actividad.ipynb` | **Actividad del Mini-TP 2** (starter para completar y entregar) | completar el notebook |

**Levantar Neo4j (para pasos 1 y 5):**
```bash
docker run --name neo4j-tp -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/testpass neo4j:latest
# UI: http://localhost:7474   ·   driver bolt: 7687   ·   user/pass: neo4j/testpass
```

**GraphQL sobre Neo4j (paso 5):** sigue el notebook `graphql_neo4j_lineage.ipynb` (escribe el `.py`, siembra el grafo y lo consulta). Los comandos que usa:
```bash
# con Neo4j corriendo (el notebook siembra el grafo con seed()):
uv run uvicorn graphql_neo4j_lineage:app --reload --port 8000
# GraphiQL en http://localhost:8000/graphql, probar:
#   query { model(name:"churn@3") { name lineage { name kind } } }
```
El resolver `lineage` corre Cypher (`MATCH (a)-[:DERIVES*]->(:Model)`) y devuelve el linaje del modelo por una query GraphQL. GraphQL es la **puerta flexible**; Neo4j, el **motor de relaciones**.

## Qué se debe entregar — Mini-TP 2 (individual, esta semana)

Expón los **metadatos de tu modelo** por GraphQL:

1. Esquema GraphQL (Strawberry) con un tipo `Model` (`name`, `version`, `metrics`).
2. Una query que devuelva las métricas/experimentos (de MLflow local o simulados).
3. Pruébalo desde **GraphiQL** y desde un **cliente Python**.
4. Compara la **misma lectura** contra tu endpoint REST de la Sesión 1 y anota la diferencia en el README.

Tienes un **starter** listo para completar: **`mini_tp2_actividad.ipynb`** (con la consigna y las celdas con `# TODO`).

**Se evalúa:** que corra de punta a punta; que el esquema tipe entrada y salida; que la query pida solo lo necesario; y la reflexión REST vs GraphQL.
**Opcional (+):** que el resolver lea el linaje desde Neo4j (`graphql_neo4j_lineage.ipynb` como base).
