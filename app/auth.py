from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models as models
import app.security as security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Se abre al inicio del request y se cierra al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.Usuario:
    """
    Dependencia que valida el JWT y retorna el usuario autenticado.
    Lanza 401 si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = security.decode_token(token)
    if email is None:
        raise credentials_exception

    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if user is None:
        raise credentials_exception

    return user