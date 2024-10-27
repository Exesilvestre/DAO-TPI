import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from patrones.observer import Observer
from db_management.db_manager import DatabaseManager
import sqlite3
import sys
sys.path.append("..")

class Reserva(Observer):
    def __init__(self, usuario_id, codigo_isbn, estado="pendiente"):
        self.usuario_id = usuario_id
        self.codigo_isbn = codigo_isbn
        self.fecha_reserva = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = estado

    def __str__(self):
        return (f"Reserva: Usuario ID: {self.usuario_id}, ISBN Libro: {self.codigo_isbn}, "
                f"Fecha de Reserva: {self.fecha_reserva}, Estado: {self.estado}")

    def guardar(self):
        # Registrar la reserva en la base de datos
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO reservas (usuario_id, libro_isbn, fecha_reserva, estado)
                    VALUES (?, ?, ?, ?);
                ''', (self.usuario_id, self.codigo_isbn, self.fecha_reserva, self.estado))
                print(f"Reserva registrada para el usuario {self.usuario_id} y el libro con ISBN {self.codigo_isbn}.")
        except sqlite3.Error as e:
            print(f"Error al registrar la reserva: {e}")

    def update(self):
        # Método llamado cuando el libro está disponible. Notifica al usuario.
        print(f"Notificación al usuario {self.usuario_id}: El libro con ISBN {self.codigo_isbn} ahora está disponible.")
        # Actualizar el estado de la reserva a 'notificado' en la base de datos
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    UPDATE reservas
                    SET estado = 'notificado'
                    WHERE usuario_id = ? AND libro_isbn = ? AND estado = 'pendiente';
                ''', (self.usuario_id, self.codigo_isbn))
                print(f"Estado de la reserva actualizado a 'notificado' para el usuario {self.usuario_id}.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el estado de la reserva: {e}")
