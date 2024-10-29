from abc import ABC, abstractmethod
from models.autor import Autor
from models.libro import Libro
from models.penalizacion import Penalizacion
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
    def factory_method(self, nombre, apellido, nacionalidad, id=None):
        return Autor(nombre, apellido, nacionalidad, id)

# Fábrica concreta para crear instancias de Libro
class LibroFactory(Factory):
    def factory_method(self, codigo_isbn, titulo, genero, anio, autor_id, cantidad_disponible = None):
        return Libro(codigo_isbn, titulo, genero, anio, autor_id, cantidad_disponible)


# Fábrica concreta para crear instancias de Prestamo
class PrestamoFactory(Factory):
    def factory_method(self, usuario, libro, fecha_devolucion=None, id=None):
        return Prestamo(usuario, libro, fecha_devolucion, id)


# Fábrica concreta para crear instancias de Usuario
class UsuarioFactory(Factory):
    def factory_method(self, nombre, apellido, tipo, direccion, telefono, id=None):
        return Usuario(nombre, apellido, tipo, direccion, telefono, id)

# Fábrica concreta para crear instancias de Reserva
class ReservaFactory(Factory):
    def factory_method(self, usuario_id, codigo_isbn, estado="pendiente"):
        return Reserva(usuario_id, codigo_isbn, estado)

        # Fábrica concreta para crear instancias de Bajas
class BajasFactory(Factory):
    def factory_method(self, libro_isbn, motivo, usuario_id=None):
        return Bajas(libro_isbn, motivo, usuario_id)

# Fábrica concreta para crear instancias de Penalizacion
class PenalizacionFactory(Factory):
    def factory_method(self, usuario_id, monto, motivo):
        return Penalizacion(usuario_id, monto, motivo)