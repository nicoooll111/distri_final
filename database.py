from motor.motor_asyncio import AsyncIOMotorClient

# URI de conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://lnrv2003:Lau123@cluster0.xt1sd.mongodb.net/?retryWrites=true&w=majority"

# Conectar con MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Base de datos y colecciones
db = client.biblioteca_videojuegos
usuarios_collection = db.usuarios
videojuegos_collection = db.videojuegos
resenas_collection = db.resenas

