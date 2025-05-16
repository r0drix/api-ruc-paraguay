import sqlite3
from sqlite3 import Error

DATABASE_PATH = "DB/rucpy.db"

def get_database_connection():
    """Establece y retorna una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Permite acceso tipo diccionario
        print("Conexión a la base de datos exitosa!")
        return conn
    except Error as e:
        print(f"Error al conectar a SQLite: {e}")
        raise  # Relanza la excepción para manejo externo
