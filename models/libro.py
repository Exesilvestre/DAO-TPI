import sys
import os

from models.baja import Baja
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager
import sqlite3
from patrones.observer import Subject
from models.autor import Autor
from models.reserva import Reserva
from datetime import datetime


class Libro(Subject):
    def __init__(self, codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        super().__init__()
        self.codigo_isbn = codigo_isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad_disponible = int(cantidad_disponible)
        self.cargar_reservas_pendientes()

    def __str__(self):
        return (f"Libro: ISBN: {self.codigo_isbn}, Título: {self.titulo}, Género: {self.genero}, "
                f"Año: {self.anio_publicacion}, Autor ID: {self.autor_id}, "
                f"Cantidad disponible: {self.cantidad_disponible}")
    
    #Metodo para cargar las reservas pendientes como observer del libro

    def guardar(self):
        db_manager = DatabaseManager()

        try:
            # Verificar que el autor con el autor_id existe
            if not Autor.existe_autor_con_id(self.autor_id):
                print(f"Error: No se encontró un autor con ID {self.autor_id}")
                return

            with db_manager.conn:
                # Verificar si ya existe un libro con el mismo ISBN
                cursor = db_manager.conn.execute(
                    "SELECT cantidad_disponible FROM libros WHERE codigo_isbn = ?;", (self.codigo_isbn,)
                )
                result = cursor.fetchone()

                if result:
                    # Si el libro ya existe, actualizar la cantidad disponible
                    nueva_cantidad = result[0] + self.cantidad_disponible
                    db_manager.conn.execute(
                        "UPDATE libros SET cantidad_disponible = ? WHERE codigo_isbn = ?;",
                        (nueva_cantidad, self.codigo_isbn)
                    )
                    print(f"Cantidad del libro con ISBN '{self.codigo_isbn}' actualizada a {nueva_cantidad}.")
                    # Notificar a los observadores que la disponibilidad del libro ha cambiado
                    print(f"Longitud de lista de observadores: {len(self._observers)}")
                    
                    self.notificar_disponibilidad()
                else:
                    # Si el libro no existe, crear un nuevo registro
                    db_manager.conn.execute('''
                        INSERT INTO libros (codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
                        VALUES (?, ?, ?, ?, ?, ?);
                    ''', (self.codigo_isbn, self.titulo, self.genero, self.anio_publicacion, self.autor_id, self.cantidad_disponible))
                    print(f"Nuevo libro guardado en la base de datos: {self}")
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
                result = cursor.fetchone()
                print(f"Consulta ISBN '{codigo_isbn}', Resultado:", result)
                return result is not None
        except sqlite3.Error as e:
            print(f"Error al verificar el libro: {e}")
            return False

    # Consulta y devuelve la cantidad disponible de un libro con un ISBN dado
    @classmethod
    def consultar_disponibilidad(cls, codigo_isbn):
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

    # Permite a un usuario reservar el libro si no está disponible
    def reservar(self, usuario_id):
        if not self.consultar_disponibilidad() > 0:
            reserva = Reserva(usuario_id, self.codigo_isbn)
            reserva.guardar()
            self.attach(reserva)
            print(f"Reserva realizada para el usuario {usuario_id} porque el libro no está disponible.")
        else:
            print(f"El libro con ISBN {self.codigo_isbn} está disponible, no es necesario reservarlo.")

    def notificar_disponibilidad(self):
        """Notifica a los observadores cuando el libro esté disponible"""
        if self.consultar_disponibilidad(self.codigo_isbn) > 0 and len(self._observers) > 0:
            print(f"El libro con ISBN {self.codigo_isbn} está disponible. Notificando a los usuarios en la lista de reservas...")
            self.notify()
            print("Longitud de observadores:", len(self._observers))
            self._observers = []

    # Carga las reservas pendientes como observers del libro
    def cargar_reservas_pendientes(self):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute('''
                    SELECT usuario_id, libro_isbn, estado 
                    FROM reservas 
                    WHERE libro_isbn = ? AND estado = 'pendiente';
                ''', (self.codigo_isbn,))
                
                reservas_pendientes = cursor.fetchall()
                
                for reserva in reservas_pendientes:
                    usuario_id, libro_isbn, estado = reserva
                    reserva_obj = Reserva(usuario_id, libro_isbn, estado)
                    self.attach(reserva_obj)
                    
        except sqlite3.Error as e:
            print(f"Error al cargar reservas pendientes: {e}")

    # Obtiene un objeto Libro a partir de su ISBN
    @classmethod
    def obtener_libro_por_isbn(cls, codigo_isbn):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible FROM libros WHERE codigo_isbn = ?;", (codigo_isbn,)
                )
                result = cursor.fetchone()
                if result:
                    codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible = result
                    return cls(codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
                else:
                    print(f"No se encontró un libro con ISBN {codigo_isbn}.")
                    return None
        except sqlite3.Error as e:
            print(f"Error al obtener el libro: {e}")
            return None
        
    # Dar de baja el libro y registrar la baja en la tabla de bajas_libros si está disponible
    def dar_de_baja(self, motivo, usuario_id=None):
        # Consultar la disponibilidad antes de proceder con la baja
        cantidad_disponible = self.consultar_disponibilidad(self.codigo_isbn)
        
        if cantidad_disponible > 0:
            # Crear una instancia de Bajas
            baja = Baja(libro_isbn=self.codigo_isbn, motivo=motivo, usuario_id=usuario_id)

            # Guardar la baja en la base de datos
            baja.guardar()

            # Reducir la cantidad disponible del libro
            nueva_cantidad = cantidad_disponible - 1
            db_manager = DatabaseManager()
            try:
                with db_manager.conn:
                    db_manager.conn.execute(''' 
                        UPDATE libros SET cantidad_disponible = ? WHERE codigo_isbn = ?;
                    ''', (nueva_cantidad, self.codigo_isbn))
                    print(f"Libro con ISBN {self.codigo_isbn} dado de baja como {motivo}. Cantidad disponible actualizada a {nueva_cantidad}.")
            except sqlite3.Error as e:
                print(f"Error al actualizar la cantidad del libro: {e}")
        else:
            print(f"No hay ejemplares disponibles para dar de baja el libro con ISBN {self.codigo_isbn}.")


    @classmethod
    def listar_libros(cls, disponibilidad='todos'):

        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                if disponibilidad == 'disponibles':
                    cursor = db_manager.conn.execute(
                        "SELECT codigo_isbn, titulo FROM libros WHERE cantidad_disponible > 0;"
                    )
                elif disponibilidad == 'no_disponibles':
                    cursor = db_manager.conn.execute(
                        "SELECT codigo_isbn, titulo FROM libros WHERE cantidad_disponible = 0;"
                    )
                else:  # 'todos'
                    cursor = db_manager.conn.execute(
                        "SELECT codigo_isbn, titulo FROM libros;"
                    )
                libros = cursor.fetchall()
                return libros
        except sqlite3.Error as e:
            print(f"Error al listar los libros: {e}")
            return []

    # Obtiene una lista de libros por autor con un resumen de la cantidad de libros disponibles por autor 
    @classmethod
    def obtener_libros_por_autor(cls):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute('''
                    SELECT a.nombre || ' ' || a.apellido AS autor, 
                        COUNT(l.codigo_isbn) AS cantidad_libros, 
                        SUM(l.cantidad_disponible) AS total_disponibles
                    FROM libros l
                    JOIN autores a ON l.autor_id = a.id
                    GROUP BY a.id
                    ORDER BY a.nombre, a.apellido ASC;
                ''')
                
                libros_por_autor = cursor.fetchall()

            print("Libros por autor obtenidos correctamente.")
            return libros_por_autor
        except sqlite3.Error as e:
            print(f"Error al obtener los libros por autor: {e}")
            return []
