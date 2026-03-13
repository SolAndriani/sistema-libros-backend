from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import engine, Base
from app.auth import get_db, get_current_user
import app.crud as crud
import app.security as security

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Libros",
    description="API para gestionar libros con autenticación JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://sistema-libros-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UsuarioOut, tags=["Usuarios"])
def register(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = crud.obtener_usuario_por_email(db, usuario.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    new_user = crud.crear_usuario(db, usuario)
    return new_user

@app.post("/login", response_model=schemas.TokenResponse, tags=["Usuarios"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.obtener_usuario_por_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UsuarioOut, tags=["Usuarios"])
def get_current_user_info(current_user: models.Usuario = Depends(get_current_user)):
    return current_user

@app.get("/books", response_model=List[schemas.LibroOut], tags=["Libros"])
def get_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    books = crud.obtener_libros_por_usuario(db, current_user.id, skip=skip, limit=limit)
    return books

@app.get("/books/count", tags=["Libros"])
def count_books(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    total = crud.contar_libros_por_usuario(db, current_user.id)
    return {"total": total}

@app.get("/books/{book_id}", response_model=schemas.LibroOut, tags=["Libros"])
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    book = crud.obtener_libro_por_id(db, book_id)
    if not book or book.propietario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@app.post("/books", response_model=schemas.LibroOut, tags=["Libros"])
def create_book(
    book: schemas.LibroCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    new_book = crud.crear_libro(db, book, current_user.id)
    return new_book

@app.put("/books/{book_id}", response_model=schemas.LibroOut, tags=["Libros"])
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

@app.delete("/books/{book_id}", tags=["Libros"])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    if not crud.eliminar_libro(db, book_id, current_user.id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"message": "Libro eliminado correctamente"}

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "OK"}