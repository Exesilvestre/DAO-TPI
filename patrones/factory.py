from abc import ABC, abstractmethod
from models.Autor import Autor
from models.Libro import Libro
from models.penalizacion import Penalizacion
from models.Prestamo import Prestamo
from models.Usuario import Usuario
from models.Reserva import Reserva
from models.baja import Baja
from models.donacion import Donacion

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
        libro = Libro(codigo_isbn, titulo, genero, anio, autor_id, cantidad_disponible)
        return libro


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

# Fábrica concreta para crear instancias de Baja
class BajasFactory(Factory):
    def factory_method(self, libro_isbn, motivo, usuario_id=None):
        return Baja(libro_isbn, motivo, usuario_id)

# Fábrica concreta para crear instancias de Penalizacion
class PenalizacionFactory(Factory):
    def factory_method(self, usuario_id, monto, motivo):
        return Penalizacion(usuario_id, monto, motivo)
    
# Fábrica concreta para crear instancias de Donacion
class DonacionFactory(Factory):
    def factory_method(self, tipo_donacion, nombre_institucion=None, usuario_id=None, codigo_isbn=None, cantidad=0):
        return Donacion(tipo_donacion, nombre_institucion, usuario_id, codigo_isbn, cantidad)