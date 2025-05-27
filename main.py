from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importa CORSMiddleware
from routes import router as videojuegos_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:8000",  # Si tu frontend se sirve en este puerto local
    "http://127.0.0.1:8000",
    "http://localhost:5500",  # Común si usas Live Server de VS Code
    "http://127.0.0.1:5500",
    # Cuando despliegues, añade la URL de tu frontend aquí, por ejemplo:
    # "https://tu-dominio-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(videojuegos_router)