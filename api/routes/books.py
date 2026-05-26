import logging
from fastapi import APIRouter, Depends, HTTPException, status
from mysql.connector.abstracts import MySQLConnectionAbstract
from database import get_db
from models import BookCreate, BookResponse

router = APIRouter()
logger = logging.getLogger("uvicorn")


# =============================================================================
# GET /books  — Lista todos los libros (COMPLETO)
# =============================================================================
@router.get("/", response_model=list[BookResponse])
async def list_books(conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titulo, autor, editorial, publicadoEn, categoria FROM Libro")
    return cursor.fetchall()


# =============================================================================
# GET /books/{book_id}  — Obtiene un libro por su ID (COMPLETO)
# =============================================================================
@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, titulo, autor, editorial, publicadoEn, categoria FROM Libro WHERE id = %s",
        (book_id,),
    )
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return row


# =============================================================================
# POST /books  — Crea un nuevo libro
# =============================================================================
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, conn: MySQLConnectionAbstract = Depends(get_db)):
    logger.info("POST /books - creating book '%s'", book.titulo)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Libro (titulo, autor, editorial, publicadoEn, categoria) VALUES (%s, %s, %s, %s, %s)",
            (book.titulo, book.autor, book.editorial, book.publicadoEn, book.categoria),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Categoría no válida")
        logger.exception("POST /books - unexpected error")
        raise
    new_id = cursor.lastrowid
    logger.info("POST /books - created book id=%d '%s'", new_id, book.titulo)
    return BookResponse(id=new_id, **book.model_dump())


# =============================================================================
# PUT /books/{book_id}  — Actualiza un libro existente (CORREGIDO)
# =============================================================================
@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book: BookCreate, conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM Libro WHERE id = %s", (book_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    try:
        cursor.execute(
            "UPDATE Libro SET titulo=%s, autor=%s, editorial=%s, publicadoEn=%s, categoria=%s WHERE id=%s",
            (book.titulo, book.autor, book.editorial, book.publicadoEn, book.categoria, book_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Categoría no válida")
        raise

    return BookResponse(id=book_id, **book.model_dump())


# =============================================================================
# DELETE /books/{book_id}  — Elimina un libro (CORREGIDO)
# =============================================================================
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Libro WHERE id = %s", (book_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    try:
        cursor.execute(
            "DELETE FROM Libro WHERE id = %s",
            (book_id,),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar: el libro tiene ejemplares o reseñas asociados",
            )
        raise