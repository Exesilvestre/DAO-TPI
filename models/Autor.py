import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager
import sqlite3

class Autor:
    def __init__(self, nombre, apellido, nacionalidad):
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad
        self.id = None 

    def __str__(self):
        return f"Autor: Nombre: {self.nombre} {self.apellido}, Nacionalidad: {self.nacionalidad}"

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def update_name(self, nuevo_nombre, nuevo_apellido):
        self.nombre = nuevo_nombre
        self.apellido = nuevo_apellido

    def update_nacionalidad(self, nueva_nacionalidad):
        self.nacionalidad = nueva_nacionalidad

    def guardar(self):
        db_manager = DatabaseManager()

        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO autores (nombre, apellido, nacionalidad)
                    VALUES (?, ?, ?);
                ''', (self.nombre, self.apellido, self.nacionalidad))
            print(f"Autor guardado en la base de datos: {self}")
        except sqlite3.Error as e:
            print(f"Error al guardar el autor: {e}")

    @classmethod
    def existe_autor_con_id(cls, autor_id):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT 1 FROM autores WHERE id = ?;", (autor_id,)
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error al verificar la existencia del autor: {e}")
            return False
