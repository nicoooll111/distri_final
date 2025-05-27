# models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Usuario(BaseModel):
    nombre: str
    email: str
    password: str
    fecha_registro: datetime = datetime.utcnow()

class Videojuego(BaseModel):
    titulo: str
    genero: List[str]
    plataformas: List[str]
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[datetime]

# Renombrada sin “ñ” para evitar problemas de codificación
class Resena(BaseModel):
    usuario_id: str  
    videojuego_id: str  
    calificacion: int  
    comentario: str
    fecha_creacion: datetime = datetime.utcnow()
