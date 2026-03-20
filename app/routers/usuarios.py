from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import app.crud as crud
import app.security as security
from app.auth import get_db, get_current_user

router = APIRouter(tags=["Usuarios"])

@router.post("/register", response_model=schemas.UsuarioOut)
def register(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = crud.obtener_usuario_por_email(db, usuario.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.crear_usuario(db, usuario)

@router.post("/login", response_model=schemas.TokenResponse)
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

@router.get("/me", response_model=schemas.UsuarioOut)
def get_current_user_info(current_user: models.Usuario = Depends(get_current_user)):
    return current_user