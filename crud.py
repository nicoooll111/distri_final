from database import videojuegos_collection
from models import Videojuego

async def agregar_videojuego(videojuego: Videojuego):
    nuevo_videojuego = await videojuegos_collection.insert_one(videojuego.dict())
    return {"mensaje": "Videojuego agregado", "id": str(nuevo_videojuego.inserted_id)}
