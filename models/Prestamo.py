import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager
from models.usuario import Usuario
from models.libro import Libro
from datetime import datetime, timedelta
import sqlite3

class Prestamo:
    def __init__(self, usuario_id, codigo_isbn, fecha_devolucion_estimada, id=None):
        self.usuario_id = usuario_id
        self.codigo_isbn = codigo_isbn
        self.fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
        self.fecha_devolucion_estimada = fecha_devolucion_estimada
        self.id = id

    def __str__(self):
        return (f"Préstamo: Usuario ID: {self.usuario_id}, ISBN Libro: {self.codigo_isbn}, "
                f"Fecha de Préstamo: {self.fecha_prestamo}, Fecha de Devolución Estimada: {self.fecha_devolucion_estimada}")

    def guardar(self):
        db_manager = DatabaseManager()

        try:
            # Verificar que el usuario existe y puede realizar el préstamo
            if not Usuario.existe_usuario_con_id(self.usuario_id):
                print(f"Error: No se encontró un usuario con ID {self.usuario_id}")
                return

            if not Usuario.puede_prestar_libro(self.usuario_id):
                print(f"Error: El usuario con ID {self.usuario_id} ha alcanzado el límite de préstamos permitidos.")
                return

            # Verificar que el libro existe y está disponible
            if not Libro.existe_libro_con_isbn(self.codigo_isbn):
                print(f"Error: No se encontró un libro con ISBN {self.codigo_isbn}")
                return

            if not Libro.consultar_disponibilidad(self.codigo_isbn) > 0:
                print(f"Error: No hay ejemplares disponibles del libro con ISBN {self.codigo_isbn}")
                return

            # Registrar el préstamo y actualizar la disponibilidad del libro
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO prestamos (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion)
                    VALUES (?, ?, ?, ?);
                ''', (self.usuario_id, self.codigo_isbn, self.fecha_prestamo, self.fecha_devolucion_estimada))

                db_manager.conn.execute('''
                    UPDATE libros SET cantidad_disponible = cantidad_disponible - 1 WHERE codigo_isbn = ?;
                ''', (self.codigo_isbn,))

                print(f"Préstamo registrado exitosamente: {self}")
        except sqlite3.Error as e:
            print(f"Error al registrar el préstamo: {e}")
    
    @classmethod
    def registrar_devolucion(cls, usuario_id, codigo_isbn, en_condiciones=True):
        db_manager = DatabaseManager()

        try:
            with db_manager.conn:
                # Verificar si el préstamo existe y está pendiente de devolución
                cursor = db_manager.conn.execute('''
                    SELECT id, fecha_devolucion FROM prestamos
                    WHERE usuario_id = ? AND libro_isbn = ?;
                ''', (usuario_id, codigo_isbn))
                prestamo = cursor.fetchone()
                
                if not prestamo:
                    print(f"No se encontró un préstamo para el usuario {usuario_id} y libro {codigo_isbn}.")
                    return

                prestamo_id, fecha_devolucion_estimada = prestamo

                # Verificar si el libro está en condiciones
                if not en_condiciones:
                    print(f"El libro con ISBN {codigo_isbn} ha sido devuelto en malas condiciones.")
                    return

                # Actualizar la fecha de devolución
                fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
                db_manager.conn.execute('''
                    UPDATE prestamos
                    SET fecha_devolucion = ?
                    WHERE id = ?;
                ''', (fecha_devolucion, prestamo_id)    )

                # Incrementar la cantidad disponible del libro
                db_manager.conn.execute('''
                    UPDATE libros
                    SET cantidad_disponible = cantidad_disponible + 1
                    WHERE codigo_isbn = ?;
                ''', (codigo_isbn,))

                # Calcular multa si hay retraso
                fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
                fecha_devolucion_estimada_dt = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d")
                dias_retraso = (fecha_devolucion_dt - fecha_devolucion_estimada_dt).days

                if dias_retraso > 0:
                    multa = dias_retraso * 100
                    print(f"Devolución registrada con retraso de {dias_retraso} días. Multa: {multa}.")
                else:
                    print("Devolución registrada a tiempo. No hay multa.")

                # Notificar la disponibilidad a los usuarios en la lista de reservas
                Libro(codigo_isbn).notificar_disponibilidad()

        except sqlite3.Error as e:
            print(f"Error al registrar la devolución: {e}")

    def calcular_multa(self, fecha_devolucion, fecha_devolucion_estimada):
        """Calcula la multa en función de los días de retraso."""
        # Convertir las fechas a objetos datetime
        fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
        fecha_devolucion_estimada_dt = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d")

        # Calcular los días de retraso
        dias_retraso = (fecha_devolucion_dt - fecha_devolucion_estimada_dt).days
        if dias_retraso > 0:
            multa = dias_retraso * 100
            return multa
        else:
            return 0
        
    @classmethod
    def listar_prestamos_activos(cls):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute('''
                    SELECT p.id, u.nombre || ' ' || u.apellido AS usuario_nombre, l.titulo AS libro_titulo
                    FROM prestamos p
                    JOIN usuarios u ON p.usuario_id = u.id
                    JOIN libros l ON p.libro_isbn = l.codigo_isbn
                    WHERE p.estado = 'Activo';
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar los préstamos activos: {e}")
            return []
        
    @classmethod
    def finalizar_prestamo(cls, prestamo_id):
        """Marca un préstamo como 'Finalizado' y actualiza la disponibilidad del libro."""
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                # Cambiar estado a 'Finalizado'
                db_manager.conn.execute('''
                    UPDATE prestamos
                    SET estado = 'Finalizado'
                    WHERE id = ?;
                ''', (prestamo_id,))

                # Recuperar el código ISBN del libro y actualizar disponibilidad
                cursor = db_manager.conn.execute('''
                    SELECT libro_isbn FROM prestamos WHERE id = ?;
                ''', (prestamo_id,))
                libro_isbn = cursor.fetchone()[0]

                # Incrementar la cantidad disponible del libro
                db_manager.conn.execute('''
                    UPDATE libros
                    SET cantidad_disponible = cantidad_disponible + 1
                    WHERE codigo_isbn = ?;
                ''', (libro_isbn,))

            print(f"Préstamo con ID {prestamo_id} finalizado y disponibilidad de libro actualizada.")
        except sqlite3.Error as e:
            print(f"Error al finalizar el préstamo: {e}")
            raise e
