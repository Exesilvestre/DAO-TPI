from db_management.db_manager import DatabaseManager
import sqlite3
from patrones.observer import Reserva, Subject
from models import Autor

class Libro(Subject):
    def __init__(self, codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        self.codigo_isbn = codigo_isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad_disponible = cantidad_disponible

    def __str__(self):
        return (f"Libro: ISBN: {self.codigo_isbn}, Título: {self.titulo}, Género: {self.genero}, "
                f"Año: {self.anio_publicacion}, Autor ID: {self.autor_id}, "
                f"Cantidad disponible: {self.cantidad_disponible}")

    def guardar(self):
        db_manager = DatabaseManager()

        try:
            # Verificar que el autor con el autor_id existe
            if not Autor.existe_autor_con_id(self.autor_id):
                print(f"Error: No se encontró un autor con ID {self.autor_id}")
                return

            with db_manager.conn:
                # Intentar insertar el libro en la base de datos
                db_manager.conn.execute('''
                    INSERT INTO libros (codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
                    VALUES (?, ?, ?, ?, ?, ?);
                ''', (self.codigo_isbn, self.titulo, self.genero, self.anio_publicacion, self.autor_id, self.cantidad_disponible))
                
                print(f"Libro guardado en la base de datos: {self}")
        except sqlite3.IntegrityError:
            print(f"Error: ISBN '{self.codigo_isbn}' ya está registrado (clave primaria duplicada).")
        except sqlite3.Error as e:
            print(f"Error al guardar el libro: {e}")
    
    @classmethod
    def existe_libro_con_isbn(cls, codigo_isbn):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT codigo_isbn FROM libros WHERE codigo_isbn = ?;", (codigo_isbn,)
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error al verificar el libro: {e}")
            return False

    @classmethod
    def consultar_disponibilidad(cls, codigo_isbn):
        """Consulta y devuelve la cantidad disponible de un libro con un ISBN dado."""
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT cantidad_disponible FROM libros WHERE codigo_isbn = ?;", (codigo_isbn,)
                )
                result = cursor.fetchone()
                if result:
                    cantidad_disponible = result[0]
                    print(f"El libro con ISBN {codigo_isbn} tiene {cantidad_disponible} ejemplares disponibles.")
                    return cantidad_disponible
                else:
                    print(f"No se encontró un libro con ISBN {codigo_isbn}.")
                    return 0
        except sqlite3.Error as e:
            print(f"Error al consultar la disponibilidad del libro: {e}")
            return 0

    def reservar(self, usuario_id):
        """Permite a un usuario reservar el libro si no está disponible"""
        if not self.consultar_disponibilidad() > 0:
            reserva = Reserva(usuario_id, self.codigo_isbn)
            reserva.guardar()
            self.attach(reserva)
            print(f"Reserva realizada para el usuario {usuario_id} porque el libro no está disponible.")
        else:
            print(f"El libro con ISBN {self.codigo_isbn} está disponible, no es necesario reservarlo.")

    def notificar_disponibilidad(self):
        """Notifica a los observadores cuando el libro esté disponible"""
        if self.consultar_disponibilidad() > 0:
            print(f"El libro con ISBN {self.codigo_isbn} está disponible. Notificando a los usuarios en la lista de reservas...")
            self.notify()
            self._observers = []
