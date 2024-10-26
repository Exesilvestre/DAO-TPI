import sqlite3
from datetime import datetime

class DatabaseManager:
    _instance = None

    def __new__(cls, db_name="data/biblioteca.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize_connection(db_name)
        return cls._instance

    def _initialize_connection(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.crear_tablas()

    def crear_tablas(self):
        with self.conn:
            # Crear tabla de autores
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS autores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    nacionalidad TEXT NOT NULL
                )
            ''')
            print("Tabla autores creada o ya existente.")
            self.agregar_registros_autores()

            # Crear tabla de libros
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
            print("Tabla libros creada o ya existente.")
            self.agregar_registros_libros()

            # Crear tabla de usuarios
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
            print("Tabla usuarios creada o ya existente.")
            self.agregar_registros_usuarios()

            # Crear tabla de préstamos
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
            print("Tabla préstamos creada o ya existente.")

            # Crear tabla de reservas
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    libro_isbn TEXT NOT NULL,
                    fecha_reserva TEXT NOT NULL,
                    estado TEXT CHECK( estado IN ('pendiente', 'notificado') ) NOT NULL DEFAULT 'pendiente',
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY (libro_isbn) REFERENCES libros(codigo_isbn)
                )
            ''')
            print("Tabla reservas creada o ya existente.")

    def agregar_registros_autores(self):
        autores = [
            ("Gabriel", "García Márquez", "Colombiana"),
            ("Julio", "Cortázar", "Argentina"),
            ("Isabel", "Allende", "Chilena"),
            ("Mario", "Vargas Llosa", "Peruana"),
            ("Jorge", "Luis Borges", "Argentina"),
            ("Pablo", "Neruda", "Chilena"),
            ("Octavio", "Paz", "Mexicana"),
            ("Laura", "Esquivel", "Mexicana"),
            ("Carlos", "Fuentes", "Mexicana"),
            ("Miguel", "de Cervantes", "Española")
        ]
        with self.conn:
            self.conn.executemany('''
                INSERT INTO autores (nombre, apellido, nacionalidad)
                VALUES (?, ?, ?)
            ''', autores)
        print("Registros de autores agregados.")

    def agregar_registros_libros(self):
        libros = [
            ("978-1-2345-6780-1", "Cien Años de Soledad", "Novela", 1967, 1, 5),
            ("978-1-2345-6780-2", "Rayuela", "Novela", 1963, 2, 4),
            ("978-1-2345-6780-3", "La Casa de los Espíritus", "Novela", 1982, 3, 6),
            ("978-1-2345-6780-4", "La Ciudad y los Perros", "Novela", 1963, 4, 5),
            ("978-1-2345-6780-5", "Ficciones", "Cuentos", 1944, 5, 3),
            ("978-1-2345-6780-6", "Canto General", "Poesía", 1950, 6, 7),
            ("978-1-2345-6780-7", "El Laberinto de la Soledad", "Ensayo", 1950, 7, 2),
            ("978-1-2345-6780-8", "Como Agua para Chocolate", "Novela", 1989, 8, 4),
            ("978-1-2345-6780-9", "La Muerte de Artemio Cruz", "Novela", 1962, 9, 5),
            ("978-1-2345-6781-0", "Don Quijote de la Mancha", "Novela", 1605, 10, 8)
        ]
        with self.conn:
            self.conn.executemany('''
                INSERT INTO libros (codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', libros)
        print("Registros de libros agregados.")

    def agregar_registros_usuarios(self):
        usuarios = [
            ("Juan", "Pérez", "estudiante", "Av. Siempre Viva 123", "1234567890"),
            ("María", "González", "profesor", "Calle Falsa 456", "2345678901"),
            ("Carlos", "López", "estudiante", "Av. Las Flores 789", "3456789012"),
            ("Ana", "Ramírez", "profesor", "Calle Principal 321", "4567890123"),
            ("Luis", "Martínez", "estudiante", "Av. San Martín 111", "5678901234"),
            ("Laura", "García", "profesor", "Calle Central 222", "6789012345"),
            ("Pedro", "Fernández", "estudiante", "Av. Libertad 333", "7890123456"),
            ("Sofía", "Rodríguez", "profesor", "Calle Secundaria 444", "8901234567"),
            ("José", "Hernández", "estudiante", "Av. Los Álamos 555", "9012345678"),
            ("Elena", "Díaz", "profesor", "Calle Tercera 666", "0123456789")
        ]
        with self.conn:
            self.conn.executemany('''
                INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
                VALUES (?, ?, ?, ?, ?)
            ''', usuarios)
        print("Registros de usuarios agregados.")

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Conexión cerrada")

# Crear instancia para ejecutar la creación de tablas e inserción de datos
db_manager = DatabaseManager()
