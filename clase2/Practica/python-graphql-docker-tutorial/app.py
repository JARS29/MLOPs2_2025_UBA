import strawberry
from fastapi import FastAPI
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
# --- Datos simulados en memoria ---
class BookData:
    def __init__(self, id: str, title: str, author: str, year: Optional[int] = None):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

mock_books = [
    BookData("b1", "El principito", "Antoine de Saint-Exupéry", 1943),
    BookData("b2", "Cien años de soledad", "Gabriel García Márquez", 1967),
    BookData("b3", "1984", "George Orwell", 1949),
]
next_book_id = len(mock_books) + 1

# --- Definición del Esquema GraphQL ---
@strawberry.type
class Book:
    id: str
    title: str
    author: str
    year: Optional[int] = None

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "¡Hola desde tu API GraphQL en Docker!"

    @strawberry.field
    def books(self) -> List[Book]:
        return mock_books

    @strawberry.field
    def book(self, id: str) -> Optional[Book]:
        for book in mock_books:
            if book.id == id:
                return book
        return None

@strawberry.input
class CreateBookInput:
    title: str
    author: str
    year: Optional[int] = None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, data: CreateBookInput) -> Book:
        global next_book_id
        new_id = f"b{next_book_id}"
        next_book_id += 1
        new_book = BookData(new_id, data.title, data.author, data.year)
        mock_books.append(new_book)
        return new_book

    @strawberry.mutation
    def delete_book(self, id: str) -> Optional[Book]:
        global mock_books
        original_len = len(mock_books)
        mock_books = [book for book in mock_books if book.id != id]
        if len(mock_books) < original_len:
            return BookData(id, "Eliminado", "N/A") 
        return None

schema = strawberry.Schema(query=Query, mutation=Mutation)

#  Integrar GraphQL con FastAPI
app = FastAPI(
    title="Mi API GraphQL de Libros",
    description="Una API GraphQL de ejemplo en Docker.",
    version="1.0.0",
)

#  Crea el router con tu esquema
graphql_app = GraphQLRouter(schema)

# Incluye el router en la aplicación FastAPI
app.include_router(graphql_app, prefix="/graphql")

@app.get("/status")
async def get_status() -> dict:
    return {"status": "running", "api_type": "GraphQL & REST (Hybrid)"}
