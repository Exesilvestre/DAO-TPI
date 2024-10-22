import sqlite3

class DatabaseManager:
    def __init__(self, db_name="data/biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.crear_tablas()

    def crear_tablas(self):
        """Crea las tablas si no existen en la base de datos"""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS autores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    nacionalidad TEXT NOT NULL
                )
            ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS libros (
                    codigo_isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    anio_publicacion INTEGER NOT NULL,
                    autor_id INTEGER NOT NULL,
                    cantidad_disponible INTEGER NOT NULL,
                    FOREIGN KEY (autor_id) REFERENCES autores(id)
                )
            ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    tipo_usuario TEXT CHECK( tipo_usuario IN ('estudiante', 'profesor') ) NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
            ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    libro_isbn TEXT NOT NULL,
                    fecha_prestamo TEXT NOT NULL,
                    fecha_devolucion TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY (libro_isbn) REFERENCES libros(codigo_isbn)
                )
            ''')

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()