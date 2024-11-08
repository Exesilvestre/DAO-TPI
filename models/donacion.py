import sys
import os
from datetime import datetime
import sqlite3
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager
from models.libro import Libro

class Donacion:
    def __init__(self, tipo_donacion, nombre_institucion=None, usuario_id=None, codigo_isbn=None, cantidad=0, fecha=None):
        self.tipo_donacion = tipo_donacion
        self.nombre_institucion = nombre_institucion if tipo_donacion == "Institución" else None
        self.usuario_id = usuario_id if tipo_donacion == "Usuario" else None
        self.codigo_isbn = codigo_isbn
        self.cantidad = cantidad
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"Donacion: Tipo: {self.tipo_donacion}, Institución: {self.nombre_institucion}, Usuario ID: {self.usuario_id}, Libro ISBN: {self.codigo_isbn}, Cantidad: {self.cantidad}, Fecha: {self.fecha}"

    # Guarda la donación y actualiza la cantidad de libros donados en la base de datos
    def guardar(self):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO donaciones (fecha, nombre_institucion, usuario_id, codigo_isbn, cantidad_donada)
                    VALUES (?, ?, ?, ?, ?);
                ''', (self.fecha, self.nombre_institucion, self.usuario_id, self.codigo_isbn, self.cantidad))

                if Libro.existe_libro_con_isbn(self.codigo_isbn):
                    libro_existente = Libro.obtener_libro_por_isbn(self.codigo_isbn)
                    libro_existente.cantidad_disponible += self.cantidad
                    with db_manager.conn:
                        db_manager.conn.execute('''
                            UPDATE libros SET cantidad_disponible = ? WHERE codigo_isbn = ?;
                        ''', (libro_existente.cantidad_disponible, self.codigo_isbn))
                    print(f"Libro existente actualizado: ISBN {self.codigo_isbn}, Nueva cantidad: {libro_existente.cantidad_disponible}")
                else:
                    print(f"No se encontró el libro con ISBN {self.codigo_isbn}. La donación no afectará el inventario.")

            db_manager.conn.commit()
            print(f"Donación guardada en la base de datos: {self}")
        except sqlite3.Error as e:
            print(f"Error al guardar la donación: {e}")

    # Obtiene las donaciones realizadas en un periodo determinado
    @classmethod
    def obtener_donaciones_por_periodo(cls, fecha_desde, fecha_hasta):
        db_manager = DatabaseManager()
        consulta = """
            SELECT id, nombre_institucion, usuario_id, codigo_isbn, fecha, cantidad_donada
            FROM donaciones
            WHERE fecha BETWEEN ? AND ?
        """
        try:
            with db_manager.conn:
                resultado = db_manager.conn.execute(consulta, (fecha_desde, fecha_hasta)).fetchall()
            return resultado
        except sqlite3.Error as e:
            print(f"Error al obtener donaciones por periodo: {e}")
            return []
        
    # Añadir el método en la clase Donacion para obtener las donaciones de los últimos 12 meses
    @classmethod
    def obtener_donaciones_por_mes(cls):
        db_manager = DatabaseManager()
        consulta = """
            SELECT strftime('%Y-%m', fecha) AS mes, SUM(cantidad_donada) AS total_donaciones
            FROM donaciones
            WHERE fecha >= date('now', '-12 months')
            GROUP BY mes
            ORDER BY mes
        """
        try:
            with db_manager.conn:
                resultado = db_manager.conn.execute(consulta).fetchall()
            # Separar el resultado en dos listas: una para los meses y otra para la cantidad de donaciones
            meses = [row[0] for row in resultado]
            cantidad_donaciones = [row[1] for row in resultado]
            return meses, cantidad_donaciones
        except sqlite3.Error as e:
            print(f"Error al obtener donaciones mensuales: {e}")
            return [], []
