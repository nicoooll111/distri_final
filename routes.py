from fastapi import APIRouter, HTTPException
from models import Videojuego, Resena
from database import videojuegos_collection, usuarios_collection, resenas_collection
from bson import ObjectId, errors
from datetime import datetime

router = APIRouter()

# Crear un videojuego
@router.post("/videojuegos/")
async def crear_videojuego(videojuego: Videojuego):
    nuevo_videojuego = await videojuegos_collection.insert_one(videojuego.dict())
    return {"mensaje": "Videojuego agregado", "id": str(nuevo_videojuego.inserted_id)}

# Obtener todos los videojuegos
@router.get("/videojuegos/")
async def obtener_videojuegos():
    try:
        videojuegos_cursor = videojuegos_collection.find()
        videojuegos = await videojuegos_cursor.to_list(length=100)
        for v in videojuegos:
            v["_id"] = str(v["_id"])
        return videojuegos if videojuegos else {"mensaje": "No hay videojuegos registrados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Obtener un videojuego por ID
@router.get("/videojuegos/{id}")
async def obtener_videojuego(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="ID no válido")
        videojuego = await videojuegos_collection.find_one({"_id": ObjectId(id)})
        if not videojuego:
            raise HTTPException(status_code=404, detail="Videojuego no encontrado")
        videojuego["_id"] = str(videojuego["_id"])
        return videojuego
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener videojuego: {str(e)}")

# Actualizar un videojuego
@router.put("/videojuegos/{id}")
async def actualizar_videojuego(id: str, videojuego: Videojuego):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    resultado = await videojuegos_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": videojuego.dict()}
    )
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado o sin cambios")
    return {"mensaje": "Videojuego actualizado"}

# Eliminar un videojuego
@router.delete("/videojuegos/{id}")
async def eliminar_videojuego(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    resultado = await videojuegos_collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return {"mensaje": "Videojuego eliminado"}

@router.post("/resenas/")
async def crear_resena(resena: Resena):
    # Validar existencia del usuario
    if not ObjectId.is_valid(resena.usuario_id):
        raise HTTPException(status_code=400, detail="usuario_id no válido")
    usuario = await usuarios_collection.find_one({"_id": ObjectId(resena.usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar existencia del videojuego
    if not ObjectId.is_valid(resena.videojuego_id):
        raise HTTPException(status_code=400, detail="videojuego_id no válido")
    videojuego = await videojuegos_collection.find_one({"_id": ObjectId(resena.videojuego_id)})
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")

    # Insertar la reseña
    nueva_resena = resena.dict()
    nueva_resena["fecha"] = nueva_resena.get("fecha") or datetime.utcnow()

    resultado = await resenas_collection.insert_one(nueva_resena)
    return {"mensaje": "Reseña agregada", "id": str(resultado.inserted_id)}

@router.get("/resenas/videojuego/{videojuego_id}")
async def obtener_resenas_por_videojuego(videojuego_id: str):
    if not ObjectId.is_valid(videojuego_id):
        raise HTTPException(status_code=400, detail="ID de videojuego no válido")

    resenas_cursor = resenas_collection.find({"videojuego_id": ObjectId(videojuego_id)})
    resenas = await resenas_cursor.to_list(length=100)

    for r in resenas:
        r["_id"] = str(r["_id"])
    
    return resenas if resenas else {"mensaje": "Este videojuego no tiene reseñas"}