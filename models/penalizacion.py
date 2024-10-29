from datetime import datetime
import sqlite3
import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager

class Penalizacion:
    def __init__(self, usuario_id, monto, motivo):
        self.usuario_id = usuario_id
        self.monto = monto
        self.motivo = motivo

    def __str__(self):
        return (f"Penalización: Usuario ID: {self.usuario_id}, Monto: {self.monto}, "
                f"Motivo: {self.motivo}")

    def guardar(self):
        # Registrar la penalización en la base de datos
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                db_manager.conn.execute('''INSERT INTO penalizacion (usuario_id, monto, motivo)
                                           VALUES (?, ?, ?);''',
                                        (self.usuario_id, self.monto, self.motivo))
                print(f"Penalización registrada para el usuario con ID {self.usuario_id}. Motivo: {self.motivo}.")
        except sqlite3.Error as e:
            print(f"Error al registrar la penalización: {e}")