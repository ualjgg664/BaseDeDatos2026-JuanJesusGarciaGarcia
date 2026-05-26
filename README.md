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
Obtener un libro por ID (GET /books/{id})El sistema recibe el identificador único mediante la URL, ejecuta una consulta filtrada y devuelve los detalles del libro solicitado.Cuerpo de la petición: (No requiere)Respuesta del servidor (200 OK):JSON{
  "titulo": "1984",
  "autor": "George Orwell",
  "editorial": "Editorial C",
  "publicadoEn": 1949,
  "categoria": "Ciencia",
  "id": 3
}
Registrar un nuevo libro (POST /books/)El sistema recibe los datos de un nuevo volumen a través del cuerpo de la petición. Tras su validación, se inserta el registro y se retorna el objeto persistido con su ID autogenerado.Cuerpo de la petición (JSON):JSON{
  "titulo": "El Señor de los Anillos",
  "autor": "J.R.R. Tolkien",
  "editorial": "Minotauro",
  "publicadoEn": 1954,
  "categoria": "Fantasía"
}
Respuesta del servidor (201 Created):JSON{
  "titulo": "El Señor de los Anillos",
  "autor": "J.R.R. Tolkien",
  "editorial": "Minotauro",
  "publicadoEn": 1954,
  "categoria": "Fantasía",
  "id": 11
}
Actualizar un registro (PUT /books/{id})El sistema modifica los datos de un libro existente en el catálogo. Requiere el ID en la URL y los nuevos campos en el cuerpo de la petición.Cuerpo de la petición (JSON):JSON{
  "titulo": "1984 (Edición Revisada)",
  "autor": "George Orwell",
  "editorial": "Editorial C",
  "publicadoEn": 1950,
  "categoria": "Ciencia"
}
Respuesta del servidor (200 OK):JSON{
  "titulo": "1984 (Edición Revisada)",
  "autor": "George Orwell",
  "editorial": "Editorial C",
  "publicadoEn": 1950,
  "categoria": "Ciencia",
  "id": 3
}
Eliminar un libro (DELETE /books/{id})El sistema borra un registro del catálogo, verificando previamente que no existan restricciones de integridad referencial (como préstamos activos).Cuerpo de la petición: (No requiere)Respuesta del servidor (204 No Content): (Operación exitosa, no se devuelve cuerpo JSON)3. Gestión de PréstamosRegistrar un préstamo (POST /loans/)El sistema gestiona la salida de un ejemplar físico vinculándolo al ID de un usuario. Se registra una nueva entrada transaccional con la fecha actual del sistema.Cuerpo de la petición (JSON):JSON{
  "userId": 1,
  "inventoryNumber": "INV001"
}
Respuesta del servidor (200 OK):JSON{
  "message": "Préstamo creado con éxito"
}
Procesar una devolución (POST /loans/return)El sistema recibe los datos de un préstamo en curso y ejecuta la eliminación del registro correspondiente, liberando el ejemplar para su posterior uso.Cuerpo de la petición (JSON):JSON{
  "userId": 1,
  "inventoryNumber": "INV001"
}
Respuesta del servidor (200 OK):JSON{
  "message": "Ejemplar devuelto con éxito"
}
ArquitecturaFragmento de códigoflowchart LR

fastapi["🐍 FastAPI (8000)<br/>Uvicorn"]
mysql["🗄️ MySQL 8"]

fastapi -->|SQL| mysql
Dos servicios Docker:ServicioPuertoDescripciónmysql3306Base de datos MySQL 8.0 con persistencia localpython8000API FastAPI + UvicornEstructura del proyectoapi/
├── main.py              # Punto de entrada FastAPI
├── database.py          # Pool de conexiones MySQL
├── models.py            # Modelos de datos (Pydantic)
└── routes/
    ├── base.py          # GET / y GET /health
    ├── books.py         # Endpoints del catálogo de libros
    └── loans.py         # Endpoints de gestión de préstamos
setup-environment/
├── docker-compose.yml
├── .env                 # Variables de entorno configuradas
├── Dockerfile           # Imagen para la API
├── requirements.txt     # Dependencias de la API
data/
└── mysql-data/          # Volumen local MySQL (persistencia)
Puesta en marchaRequisitos previosDocker y Docker Compose1. Variables de entornoEl archivo setup-environment/.env incluye la configuración del acceso al motor de base de datos (con la instrucción de acceso sin credenciales para desarrollo local):Fragmento de códigoMYSQL_ALLOW_EMPTY_PASSWORD=true
MYSQL_DATABASE=PrestamosBiblioteca
MYSQL_USER=biblioteca
MYSQL_PASSWORD=biblioteca123
MYSQL_HOST=mysql
MYSQL_PORT=3306
2. Arrancar los serviciosBashcd setup-environment
docker-compose up --build -d
3. Verificar estadoBashdocker-compose ps
docker-compose logs -f python   # logs de la API
NOTAEl contenedor python contiene un servidor Uvicorn en modo de desarrollo, por lo que se reiniciará automáticamente al detectar cambios en el código fuente. Esto facilita el desarrollo iterativo sin necesidad de reconstruir la imagen cada vez.Comandos útilesBash# Parar servicios
docker-compose down --volumes --remove-orphans

# Reiniciar solo la API
docker-compose restart python

# Entrar al contenedor de la API
docker exec -it $(docker-compose ps -q python) /bin/sh

# Acceder a MySQL
docker exec -it mysql mysql -u root
Dependencias principalesAPI (requirements.txt):fastapi — framework webuvicorn — servidor ASGImysql-connector-python — driver MySQLdotenv — carga de variables de entornopydantic — validación de datospytz — manejo de zonas horariasLicenciaEste proyecto está licenciado bajo la Licencia CC BY-NC-ND 4.0.
