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

            # Crear tabla de préstamos con estado
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    libro_isbn TEXT NOT NULL,
                    fecha_prestamo TEXT NOT NULL,
                    fecha_devolucion TEXT,
                    estado TEXT CHECK(estado IN ('Activo', 'Finalizado')) DEFAULT 'Activo',
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY (libro_isbn) REFERENCES libros(codigo_isbn)
                )
            ''')
            print("Tabla préstamos creada o ya existente.")
            self.agregar_registros_prestamos()

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

            # Crear tabla de bajas de libros
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS bajas_libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    libro_isbn TEXT NOT NULL,
                    motivo TEXT CHECK(motivo IN ('dañado', 'perdido')) NOT NULL,
                    fecha_baja TEXT NOT NULL,
                    usuario_id INTEGER,
                    FOREIGN KEY (libro_isbn) REFERENCES libros(codigo_isbn),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            print("Tabla bajas creada o ya existente.")
            
             # Crear tabla de penalizaciones
            self.conn.execute('''CREATE TABLE IF NOT EXISTS penalizacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                motivo TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )''')
            print("Tabla penalizacion creada o ya existente.")

            # Crear tabla de donaciones
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS donaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    nombre_institucion TEXT,
                    usuario_id INTEGER,
                    codigo_isbn TEXT NOT NULL,
                    cantidad_donada INTEGER NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY (codigo_isbn) REFERENCES libros(codigo_isbn)
                )
            ''')
            print("Tabla donaciones creada o ya existente.")


    def _tabla_tiene_datos(self, tabla):
        cursor = self.conn.execute(f'SELECT COUNT(*) FROM {tabla}')
        return cursor.fetchone()[0] > 0

    def agregar_registros_autores(self):
        if not self._tabla_tiene_datos('autores'):
            autores = [
                ("Gabriel", "García Márquez", "Colombia"),
                ("Julio", "Cortázar", "Argentina"),
                ("Isabel", "Allende", "Chile"),
                ("Mario", "Vargas Llosa", "Peru"),
                ("Jorge", "Luis Borges", "Argentina"),
                ("Pablo", "Neruda", "Chile"),
                ("Octavio", "Paz", "Mexico"),
                ("Laura", "Esquivel", "Mexico"),
                ("Carlos", "Fuentes", "Mexico"),
                ("Miguel", "de Cervantes", "España")
            ]
            with self.conn:
                self.conn.executemany('''
                    INSERT INTO autores (nombre, apellido, nacionalidad)
                    VALUES (?, ?, ?)
                ''', autores)
            print("Registros de autores agregados.")
        else:
            print("La tabla de autores ya tiene registros.")

    def agregar_registros_libros(self):
        if not self._tabla_tiene_datos('libros'):
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
        else:
            print("La tabla de libros ya tiene registros.")

    def agregar_registros_usuarios(self):
        if not self._tabla_tiene_datos('usuarios'):
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
        else:
            print("La tabla de usuarios ya tiene registros.")

    def agregar_registros_prestamos(self):
        if not self._tabla_tiene_datos('prestamos'):
            prestamos = [
                (2, "978-1-2345-6780-1", "2024-11-01", "2024-11-05", 'Activo'),
                (2, "978-1-2345-6780-2", "2024-11-01", "2024-11-05", 'Activo')
            ]
            with self.conn:
                self.conn.executemany('''
                    INSERT INTO prestamos (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion, estado)
                    VALUES (?, ?, ?, ?, ?);
                ''', prestamos)
            print("Registros de préstamos agregados.")
        else:
            print("La tabla de préstamos ya tiene registros.")

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Conexión cerrada")

# Crear instancia para ejecutar la creación de tablas e inserción de datos
db_manager = DatabaseManager()
