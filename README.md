# API REST de Gestión Bibliotecaria con FastAPI y MySQL

## Descripción y Funcionamiento de la API
La presente API REST constituye el núcleo (backend) de un sistema de gestión bibliotecaria. Está construida con el framework **FastAPI** (Python) y utiliza una base de datos relacional **MySQL** para la persistencia de los datos. 

El sistema opera bajo una arquitectura cliente-servidor, procesando peticiones HTTP estándar (GET, POST, PUT, DELETE) y comunicándose estrictamente mediante el formato de intercambio de datos **JSON**. Su funcionamiento se divide en dos dominios principales: la gestión del inventario (libros) y el control transaccional de los ejemplares (préstamos y devoluciones), garantizando en todo momento la integridad referencial de la base de datos.

---

## Endpoints de la API

### 1. Rutas Base y Documentación
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Devuelve un mensaje de bienvenida con enlaces HATEOAS. |
| GET | `/health` | Verifica el estado del servidor (Health check). |
| GET | `/docs` | Interfaz interactiva de documentación (Swagger UI). |
| GET | `/redoc` | Documentación estática de la API (ReDoc). |

### 2. Gestión del Catálogo (Libros)

#### Listar todos los libros (`GET /books/`)
El sistema consulta la base de datos y retorna el listado íntegro de los ejemplares registrados en el catálogo.
* **Cuerpo de la petición:** *(No requiere)*
* **Respuesta del servidor (200 OK):**
  ```json
  [
    {
      "titulo": "El Quijote",
      "autor": "Miguel de Cervantes",
      "editorial": "Editorial A",
      "publicadoEn": 1605,
      "categoria": "Ficción",
      "id": 1
    }
  ]
