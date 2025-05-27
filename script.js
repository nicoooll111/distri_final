document.addEventListener('DOMContentLoaded', () => {
    // URL base de tu API de FastAPI.
    // **IMPORTANTE**: Cuando lo despliegues, esta URL cambiará a la de tu servicio en Render/Railway, etc.
    // Por ahora, si estás ejecutando FastAPI localmente, usa esta:
    const API_BASE_URL = 'http://127.0.0.1:8000'; // O la URL donde corra tu backend

    const videojuegosContainer = document.getElementById('videojuegos-container');

    async function obtenerVideojuegos() {
        try {
            videojuegosContainer.innerHTML = '<p>Cargando videojuegos...</p>'; // Mensaje de carga

            const response = await fetch(`${API_BASE_URL}/videojuegos/`);
            if (!response.ok) {
                // Manejar errores HTTP (ej. 404, 500)
                const errorData = await response.json();
                throw new Error(`Error HTTP: ${response.status} - ${errorData.detail || 'Error desconocido'}`);
            }
            let videojuegos = await response.json();

            // Si la API devuelve un mensaje de "No hay videojuegos", lo manejamos
            if (videojuegos.mensaje && videojuegos.mensaje.includes("No hay videojuegos")) {
                videojuegosContainer.innerHTML = '<p>No se encontraron videojuegos.</p>';
                return;
            }

            // Asegurarse de que `videojuegos` sea un array
            if (!Array.isArray(videojuegos)) {
                console.error("La respuesta de la API no es un array:", videojuegos);
                videojuegosContainer.innerHTML = '<p>Error al cargar los videojuegos: formato de datos inesperado.</p>';
                return;
            }

            videojuegosContainer.innerHTML = ''; // Limpiar el mensaje de carga

            videojuegos.forEach(videojuego => {
                const card = document.createElement('div');
                card.classList.add('videojuego-card');

                card.innerHTML = `
                    <h3>${videojuego.titulo}</h3>
                    <p>${videojuego.descripcion || 'Sin descripción.'}</p>
                    <p class="genero">Género: ${videojuego.genero ? videojuego.genero.join(', ') : 'N/A'}</p>
                    <p class="plataformas">Plataformas: ${videojuego.plataformas ? videojuego.plataformas.join(', ') : 'N/A'}</p>
                    <p>Fecha de lanzamiento: ${videojuego.fecha_lanzamiento ? new Date(videojuego.fecha_lanzamiento).toLocaleDateString() : 'N/A'}</p>
                    `;
                videojuegosContainer.appendChild(card);
            });

        } catch (error) {
            console.error('Error al obtener los videojuegos:', error);
            videojuegosContainer.innerHTML = `<p>Error al cargar los videojuegos: ${error.message}. Asegúrate de que tu API esté corriendo.</p>`;
        }
    }

    // Llamar a la función cuando la página cargue
    obtenerVideojuegos();
});