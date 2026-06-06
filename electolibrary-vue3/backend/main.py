import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models import Book

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR.parent / "data" / "tasks.db"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="ElectoLibrary API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT DEFAULT '',
                year INTEGER NOT NULL,
                publisher TEXT NOT NULL,
                category TEXT NOT NULL,
                theme TEXT DEFAULT 'Общая',
                status TEXT NOT NULL DEFAULT 'available',
                favorite INTEGER NOT NULL DEFAULT 0,
                cover_url TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        count = connection.execute("SELECT COUNT(*) AS total FROM books").fetchone()["total"]
        if count == 0:
            created_at = now_iso()
            seed_books = [
                (
                    "Мастер и Маргарита",
                    "М. А. Булгаков",
                    "Роман о добре, зле, любви и свободе выбора.",
                    1967,
                    "Эксмо",
                    "16+",
                    "Классика",
                    "available",
                    1,
                    None,
                    created_at,
                    created_at,
                ),
                (
                    "Преступление и наказание",
                    "Ф. М. Достоевский",
                    "Психологический роман о моральном выборе героя.",
                    1866,
                    "АСТ",
                    "16+",
                    "Классика",
                    "reserved",
                    0,
                    None,
                    created_at,
                    created_at,
                ),
                (
                    "Чистый код",
                    "Роберт Мартин",
                    "Практическое руководство по качественной разработке программ.",
                    2008,
                    "Питер",
                    "12+",
                    "IT",
                    "available",
                    1,
                    None,
                    created_at,
                    created_at,
                ),
            ]
            connection.executemany(
                """
                INSERT INTO books
                (title, author, description, year, publisher, category, theme, status, favorite, cover_url, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                seed_books,
            )


def row_to_book(row: sqlite3.Row) -> Book:
    data = dict(row)
    data["favorite"] = bool(data["favorite"])
    return Book(**data)


def save_cover(cover: UploadFile | None) -> str | None:
    if cover is None or not cover.filename:
        return None

    suffix = Path(cover.filename).suffix.lower()
    if suffix not in {".jpg", ".jpeg"}:
        raise HTTPException(status_code=400, detail="Разрешена только обложка в формате JPG.")

    safe_name = f"{int(datetime.now().timestamp())}_{Path(cover.filename).name}"
    destination = UPLOAD_DIR / safe_name
    with destination.open("wb") as buffer:
        shutil.copyfileobj(cover.file, buffer)
    return f"/uploads/{safe_name}"


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/books", response_model=list[Book])
def get_books() -> list[Book]:
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM books ORDER BY created_at DESC").fetchall()
        return [row_to_book(row) for row in rows]


def find_book_or_404(book_id: int) -> Book:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Книга не найдена.")
        return row_to_book(row)


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> Book:
    return find_book_or_404(book_id)


# Alias for the typo in the assignment text: /api/boooks/{id}
@app.get("/api/boooks/{book_id}", response_model=Book)
def get_book_with_typo_path(book_id: int) -> Book:
    return find_book_or_404(book_id)


@app.post("/api/books", response_model=Book, status_code=201)
def create_book(
    title: Annotated[str, Form(min_length=2)],
    author: Annotated[str, Form(min_length=2)],
    year: Annotated[int, Form(ge=1500, le=2100)],
    publisher: Annotated[str, Form()],
    category: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    theme: Annotated[str, Form()] = "Общая",
    status: Annotated[str, Form()] = "available",
    favorite: Annotated[bool, Form()] = False,
    cover: Annotated[UploadFile | None, File()] = None,
) -> Book:
    cover_url = save_cover(cover)
    created_at = now_iso()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO books
            (title, author, description, year, publisher, category, theme, status, favorite, cover_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title.strip(),
                author.strip(),
                description.strip(),
                year,
                publisher,
                category,
                theme.strip() or "Общая",
                status,
                int(favorite),
                cover_url,
                created_at,
                created_at,
            ),
        )
        connection.commit()
        return find_book_or_404(cursor.lastrowid)


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    title: Annotated[str, Form(min_length=2)],
    author: Annotated[str, Form(min_length=2)],
    year: Annotated[int, Form(ge=1500, le=2100)],
    publisher: Annotated[str, Form()],
    category: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    theme: Annotated[str, Form()] = "Общая",
    status: Annotated[str, Form()] = "available",
    favorite: Annotated[bool, Form()] = False,
    cover: Annotated[UploadFile | None, File()] = None,
) -> Book:
    existing = find_book_or_404(book_id)
    cover_url = save_cover(cover) or existing.cover_url
    updated_at = now_iso()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE books
            SET title = ?, author = ?, description = ?, year = ?, publisher = ?, category = ?,
                theme = ?, status = ?, favorite = ?, cover_url = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                title.strip(),
                author.strip(),
                description.strip(),
                year,
                publisher,
                category,
                theme.strip() or "Общая",
                status,
                int(favorite),
                cover_url,
                updated_at,
                book_id,
            ),
        )
        connection.commit()
        return find_book_or_404(book_id)


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int) -> None:
    find_book_or_404(book_id)
    with get_connection() as connection:
        connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
        connection.commit()
