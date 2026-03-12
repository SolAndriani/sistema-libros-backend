from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import app.security as security

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """Crear un nuevo usuario"""
    hashed_password = security.hash_password(usuario.password)
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario_por_email(db: Session, email: str) -> models.Usuario:
    """Obtener usuario por email"""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def obtener_usuario_por_id(db: Session, usuario_id: int) -> models.Usuario:
    """Obtener usuario por ID"""
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def crear_libro(db: Session, libro: schemas.LibroCreate, propietario_id: int) -> models.Libro:
    """Crear un nuevo libro"""
    db_libro = models.Libro(
        nombre=libro.nombre,
        descripcion=libro.descripcion,
        propietario_id=propietario_id
    )
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def obtener_libros_por_usuario(db: Session, propietario_id: int, skip: int = 0, limit: int = 10):
    """Obtener libros de un usuario con paginación"""
    return db.query(models.Libro).filter(
        models.Libro.propietario_id == propietario_id
    ).offset(skip).limit(limit).all()

def contar_libros_por_usuario(db: Session, propietario_id: int) -> int:
    """Contar total de libros de un usuario"""
    return db.query(models.Libro).filter(
        models.Libro.propietario_id == propietario_id
    ).count()

def obtener_libro_por_id(db: Session, libro_id: int) -> models.Libro:
    """Obtener un libro por ID"""
    return db.query(models.Libro).filter(models.Libro.id == libro_id).first()

def actualizar_libro(db: Session, libro_id: int, libro_data: schemas.LibroCreate, propietario_id: int) -> models.Libro:
    """Actualizar un libro"""
    libro = db.query(models.Libro).filter(
        models.Libro.id == libro_id,
        models.Libro.propietario_id == propietario_id
    ).first()
    if libro:
        libro.nombre = libro_data.nombre
        libro.descripcion = libro_data.descripcion
        db.commit()
        db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int, propietario_id: int) -> bool:
    """Eliminar un libro"""
    libro = db.query(models.Libro).filter(
        models.Libro.id == libro_id,
        models.Libro.propietario_id == propietario_id
    ).first()
    if libro:
        db.delete(libro)
        db.commit()
        return True
    return False