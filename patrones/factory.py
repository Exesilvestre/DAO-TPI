from abc import ABC, abstractmethod
from models.autor import Autor
from models.libro import Libro
from models.prestamo import Prestamo
from models.usuario import Usuario
from models.reserva import Reserva
from models.bajas import Bajas
# Clase abstracta Factory
class Factory(ABC):
    @abstractmethod
    def factory_method(self, *args, **kwargs):
        pass


# Fábrica concreta para crear instancias de Autor
class AutorFactory(Factory):
    def factory_method(self, id, nombre, apellido, nacionalidad):
        return Autor(nombre, apellido, nacionalidad) 

# Fábrica concreta para crear instancias de Libro
class LibroFactory(Factory):
    def factory_method(self, codigo_isbn, titulo, genero, anio, autor, cantidad_disponible):
        return Libro(codigo_isbn, titulo, genero, anio, autor, cantidad_disponible)


# Fábrica concreta para crear instancias de Prestamo
class PrestamoFactory(Factory):
    def factory_method(self, id, usuario, libro, fecha_prestamo, fecha_devolucion=None):
        return Prestamo(id, usuario, libro, fecha_prestamo, fecha_devolucion)


# Fábrica concreta para crear instancias de Usuario
class UsuarioFactory(Factory):
    def factory_method(self, id, nombre, apellido, tipo, direccion, telefono):
        return Usuario(id, nombre, apellido, tipo, direccion, telefono)

# Fábrica concreta para crear instancias de Reserva
class ReservaFactory(Factory):
    def factory_method(self, usuario_id, codigo_isbn, estado="pendiente"):
        return Reserva(usuario_id, codigo_isbn, estado)

        # Fábrica concreta para crear instancias de Bajas
class BajasFactory(Factory):
    def factory_method(self, libro_isbn, motivo, usuario_id=None):
        return Bajas(libro_isbn, motivo, usuario_id)