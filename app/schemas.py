from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True} 

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class LibroBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int
    propietario_id: int
    created_at: datetime

    model_config = {"from_attributes": True}  

class LibroWithPropietario(LibroOut):
    propietario: UsuarioOut

class TokenResponse(BaseModel):
    access_token: str
    token_type: str