from datetime import datetime
import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager
import sqlite3

class Bajas:
    def __init__(self, libro_isbn, motivo, usuario_id=None):
        self.libro_isbn = libro_isbn
        self.motivo = motivo  # Debe ser "dañado" o "perdido"
        self.fecha_baja = datetime.now().strftime("%Y-%m-%d")
        self.usuario_id = usuario_id

    def __str__(self):
        return (f"Baja: ISBN Libro: {self.libro_isbn}, Motivo: {self.motivo}, "
                f"Fecha de Baja: {self.fecha_baja}, Usuario ID: {self.usuario_id}")

    def guardar(self):
        # Registrar la baja en la base de datos
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO bajas_libros (libro_isbn, motivo, fecha_baja, usuario_id)
                    VALUES (?, ?, ?, ?);
                ''', (self.libro_isbn, self.motivo, self.fecha_baja, self.usuario_id))
                print(f"Baja registrada para el libro con ISBN {self.libro_isbn}. Motivo: {self.motivo}.")
        except sqlite3.Error as e:
            print(f"Error al registrar la baja: {e}")
