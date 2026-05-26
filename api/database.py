import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno heredadas de Docker
_DB_HOST = os.environ.get('MYSQL_HOST')
_DB_PORT = int(os.getenv("MYSQL_PORT", 3306))
_DB_USER = os.environ.get('MYSQL_USER')
_DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
_DB_NAME = os.environ.get('MYSQL_DATABASE', 'mydatabase')

_pool = None

def _get_pool():
    """Inicializa el pool de conexiones de forma segura solo cuando se necesita"""
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="main_pool",
            pool_size=5,
            host=_DB_HOST,
            port=_DB_PORT,
            user=_DB_USER,
            password=_DB_PASSWORD,
            database=_DB_NAME,
        )
    return _pool

def get_connection():
    return _get_pool().get_connection()

def get_db():
    """Proveedor de conexión seguro para los endpoints de FastAPI"""
    pool = _get_pool()
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()