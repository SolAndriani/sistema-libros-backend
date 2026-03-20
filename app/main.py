from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import usuarios, libros

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Libros",
    description="API para gestionar libros con autenticación JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(libros.router)

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "OK"}