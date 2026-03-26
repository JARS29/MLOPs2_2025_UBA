import requests
import json
from typing import Optional

graphql_endpoint = "http://localhost:8000/graphql"

def execute_graphql_query(query: str, variables: Optional[dict] = None) -> dict:
    """Función para ejecutar consultas/mutaciones GraphQL."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = requests.post(graphql_endpoint, json=payload)
        response.raise_for_status() # Lanza un error para códigos 4xx/5xx
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. Asegúrate de que el contenedor Docker esté corriendo.")
        return {"errors": [{"message": "Connection error"}]}
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err} - {response.text}")
        return {"errors": [{"message": f"HTTP error: {http_err}"}]}
    except Exception as err:
        print(f"Ocurrió otro error: {err}")
        return {"errors": [{"message": f"An unexpected error occurred: {err}"}]}


print("--- Cliente Python para API GraphQL ---")

# --- Query de ejemplo: obtener todos los libros, solo título y autor ---
print("\n--- Consultando todos los libros (solo título y autor) ---")
all_books_query = """
query GetBooks {
  books {
    title
    author
  }
}
"""
result = execute_graphql_query(all_books_query)
if "data" in result:
    for book in result["data"]["books"]:
        print(f"- {book['title']} por {book['author']}")
elif "errors" in result:
    print(f"Errores: {result['errors']}")

# --- Mutation de ejemplo: crear un nuevo libro ---
print("\n--- Creando un nuevo libro ---")
create_book_mutation = """
mutation AddBook($title: String!, $author: String!, $year: Int) {
  createBook(data: {title: $title, author: $author, year: $year}) {
    id
    title
    author
    year
  }
}
"""
variables = {
    "title": "La sombra del viento",
    "author": "Carlos Ruiz Zafón",
    "year": 2001
}
result = execute_graphql_query(create_book_mutation, variables)
if "data" in result:
    new_book = result["data"]["createBook"]
    print(f"Libro creado: ID={new_book['id']}, Título='{new_book['title']}'")
elif "errors" in result:
    print(f"Errores: {result['errors']}")

# --- Query de verificación: obtener todos los libros de nuevo para ver el nuevo ---
print("\n--- Verificando todos los libros después de la creación ---")
result = execute_graphql_query(all_books_query)
if "data" in result:
    for book in result["data"]["books"]:
        print(f"- {book['title']} por {book['author']}")
elif "errors" in result:
    print(f"Errores: {result['errors']}")

# --- Mutation de ejemplo: eliminar un libro ---
print("\n--- Eliminando un libro (por ejemplo, el b1) ---")
delete_book_mutation = """
mutation RemoveBook($id: String!) {
  deleteBook(id: $id) {
    id
    title
  }
}
"""
variables = {"id": "b1"}
result = execute_graphql_query(delete_book_mutation, variables)
if "data" in result and result["data"]["deleteBook"]:
    deleted_book = result["data"]["deleteBook"]
    print(f"Libro eliminado: ID={deleted_book['id']}, Título='{deleted_book['title']}'")
elif "errors" in result:
    print(f"Errores: {result['errors']}")
else:
    print("No se encontró el libro para eliminar o ya fue eliminado.")


print("\n--- Fin del ejemplo de cliente GraphQL ---")
