from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
import app.crud as crud
from app.auth import get_db, get_current_user

router = APIRouter(prefix="/books", tags=["Libros"])

@router.get("", response_model=List[schemas.LibroOut])
def get_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    return crud.obtener_libros_por_usuario(db, current_user.id, skip=skip, limit=limit)

@router.get("/count")
def count_books(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    total = crud.contar_libros_por_usuario(db, current_user.id)
    return {"total": total}

@router.get("/{book_id}", response_model=schemas.LibroOut)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    book = crud.obtener_libro_por_id(db, book_id)
    if not book or book.propietario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@router.post("", response_model=schemas.LibroOut)
def create_book(
    book: schemas.LibroCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    return crud.crear_libro(db, book, current_user.id)

@router.put("/{book_id}", response_model=schemas.LibroOut)
def update_book(
    book_id: int,
    book: schemas.LibroCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    updated_book = crud.actualizar_libro(db, book_id, book, current_user.id)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return updated_book

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    if not crud.eliminar_libro(db, book_id, current_user.id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"message": "Libro eliminado correctamente"}