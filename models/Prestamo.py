from db_management.db_manager import DatabaseManager
from models import Usuario
from models import Libro
from datetime import datetime, timedelta
import sqlite3

class Prestamo:
    def __init__(self, usuario_id, codigo_isbn, fecha_prestamo=None, fecha_devolucion_estimada=None):
        self.usuario_id = usuario_id
        self.codigo_isbn = codigo_isbn
        self.fecha_prestamo = fecha_prestamo or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fecha_devolucion_estimada = fecha_devolucion_estimada or (self.fecha_prestamo + timedelta(days=14))

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
                    INSERT INTO prestamos (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion_estimada)
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
                    SELECT id, fecha_devolucion_estimada FROM prestamos
                    WHERE usuario_id = ? AND libro_isbn = ? AND fecha_devolucion IS NULL;
                ''', (usuario_id, codigo_isbn))
                prestamo = cursor.fetchone()
                
                if not prestamo:
                    print(f"No se encontró un préstamo activo para el usuario {usuario_id} y libro {codigo_isbn}.")
                    return

                prestamo_id, fecha_devolucion_estimada = prestamo

                # Verificar si el libro está en condiciones
                if not en_condiciones:
                    print(f"El libro con ISBN {codigo_isbn} ha sido devuelto en malas condiciones.")
                    return

                # Actualizar la fecha de devolución
                fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db_manager.conn.execute('''
                    UPDATE prestamos
                    SET fecha_devolucion = ?
                    WHERE id = ?;
                ''', (fecha_devolucion, prestamo_id))

                # Incrementar la cantidad disponible del libro
                db_manager.conn.execute('''
                    UPDATE libros
                    SET cantidad_disponible = cantidad_disponible + 1
                    WHERE codigo_isbn = ?;
                ''', (codigo_isbn,))

                # Calcular multa si hay retraso
                fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d %H:%M:%S")
                fecha_devolucion_estimada_dt = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d %H:%M:%S")
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
        fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d %H:%M:%S")
        fecha_devolucion_estimada_dt = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d %H:%M:%S")

        # Calcular los días de retraso
        dias_retraso = (fecha_devolucion_dt - fecha_devolucion_estimada_dt).days
        if dias_retraso > 0:
            multa = dias_retraso * 100
            return multa
        else:
            return 0
