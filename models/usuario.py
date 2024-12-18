import sqlite3
import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_management.db_manager import DatabaseManager


class Usuario():
    TIPOS_VALIDOS = ['estudiante', 'profesor']
    
    def __init__(self, nombre, apellido, tipo, direccion, telefono, id=None):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de usuario inválido: {tipo}. Debe ser 'estudiante' o 'profesor'.")
        self.nombre = nombre
        self.apellido = apellido
        self.tipo = tipo
        self.direccion = direccion
        self.telefono = telefono
        self.libros_prestados = []
        self.id = id


    def __str__(self):
        return (f"Usuario: Nombre: {self.nombre} {self.apellido}, Tipo: {self.tipo}, "
                f"Dirección: {self.direccion}, Teléfono: {self.telefono}")

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def prestar_libro(self, libro):
        max_libros = 3 if self.tipo == 'estudiante' else 5
        if len(self.libros_prestados) < max_libros and libro.prestar():
            self.libros_prestados.append(libro)
            return True
        return False

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            libro.devolver()
            self.libros_prestados.remove(libro)
            return True
        return False

    def cambiar_direccion(self, nueva_direccion):
        self.direccion = nueva_direccion

    def cambiar_telefono(self, nuevo_telefono):
        self.telefono = nuevo_telefono

    def guardar(self):
        db_manager = DatabaseManager()

        try:
            with db_manager.conn:
                db_manager.conn.execute('''
                    INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
                    VALUES (?, ?, ?, ?, ?);
                ''', (self.nombre, self.apellido, self.tipo, self.direccion, self.telefono))
            print(f"Usuario guardado en la base de datos: {self}")
        except sqlite3.Error as e:
            print(f"Error al guardar el usuario: {e}")

    @classmethod
    def existe_usuario_con_id(cls, usuario_id):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT id FROM usuarios WHERE id = ?;", (usuario_id,)
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error al verificar el usuario: {e}")
            return False

    @classmethod
    def puede_prestar_libro(cls, usuario_id):
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute(
                    "SELECT tipo_usuario, COUNT(*) as prestamos_activos FROM usuarios "
                    "JOIN prestamos ON usuarios.id = prestamos.usuario_id "
                    "WHERE usuarios.id = ? AND prestamos.fecha_devolucion IS NULL;", (usuario_id,)
                )
                result = cursor.fetchone()
                if result:
                    tipo_usuario, prestamos_activos = result
                    max_prestamos = 3 if tipo_usuario == 'estudiante' else 5
                    return prestamos_activos <= max_prestamos
                return False
        except sqlite3.Error as e:
            print(f"Error al verificar el límite de préstamos: {e}")
            return False
    
    @classmethod
    def listar_usuarios(self):
        """Obtiene una lista de usuarios desde la base de datos."""
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute("SELECT id, nombre, apellido FROM usuarios;")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar usuarios: {e}")
            return []
        
    @classmethod
    def obtener_usuarios_con_penalizaciones(cls):
        """Obtiene una lista de usuarios con penalizaciones desde la base de datos."""
        db_manager = DatabaseManager()
        try:
            with db_manager.conn:
                cursor = db_manager.conn.execute('''
                    SELECT u.nombre, u.apellido, p.monto, p.motivo 
                    FROM usuarios u
                    JOIN penalizacion p ON u.id = p.usuario_id;
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar usuarios con penalizaciones: {e}")
            return []
