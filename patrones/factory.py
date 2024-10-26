from abc import ABC, abstractmethod
from models import Autor, Libro, Prestamo, Usuario

# Clase abstracta Factory
class Factory(ABC):
    @abstractmethod
    def factory_method(self, *args, **kwargs):
        pass


# Fábrica concreta para crear instancias de Autor
class AutorFactory(Factory):
    def factory_method(self, id, nombre, apellido, nacionalidad):
        return Autor(id, nombre, apellido, nacionalidad)

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