import tkinter as tk
from tkinter import PhotoImage
from tkcalendar import DateEntry 
from tkinter import ttk 
import sys
import os
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import messagebox
from patrones.factory import AutorFactory, LibroFactory, UsuarioFactory, PrestamoFactory, ReservaFactory
from interfaz.validaciones import validar_campos_vacios
from models.autor import Autor
from models.libro import Libro
from models.usuario import Usuario
from models.prestamo import Prestamo
from datetime import datetime


class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.state("zoomed")  # Ocupa la ventana completa pero no en pantalla completa

        # Frame principal para contener todos los elementos
        self.frame_inicial = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_inicial.pack(fill="both", expand=True)

        # Cargar y mostrar el logo
        logo_path = os.path.join("recursos", "logo.png")
        logo_image = PhotoImage(file=logo_path)
        self.logo_label = tk.Label(self.frame_inicial, image=logo_image, bg="#f0f0f0")
        self.logo_label.image = logo_image  # Mantener referencia
        self.logo_label.place(x=150, y=20)  # Posición del logo

        # Título principal en grande
        self.titulo_label = tk.Label(self.frame_inicial, text="Sistema de Gestión de Biblioteca", font=("Trebuchet MS", 24, "bold"), bg="#f0f0f0")
        self.titulo_label.place(x=150, y=520)  # Posición del título

        # Definir los botones con las funcionalidades y propiedades de estilo
        botones = [
            ("Registro de Autores", self.mostrar_registro_autores),
            ("Registro de Libros", self.mostrar_registro_libros),
            ("Registro de Usuarios", self.mostrar_registro_usuarios),
            ("Préstamo de Libros", self.mostrar_prestamo_libros),
            ("Devolución de Libros", self.mostrar_devolucion_libros),
            ("Consulta de Disponibilidad", self.mostrar_consulta_disponibilidad),
            ("Reserva de Libros", self.mostrar_reserva_libros),
            ("Reportes", self.mostrar_reportes)  # Añade el botón de Reportes
        ]

        # Posicionar los botones en una cuadrícula de 2 columnas a la derecha
        x_offset = 850  # Coordenada x para la columna de botones
        y_offset = 200   # Coordenada y inicial para el primer botón
        for i, (text, command) in enumerate(botones):
            boton = tk.Button(self.frame_inicial, text=text, width=25, height=2, font=("Trebuchet MS", 11), bg="orange", command=command)
            boton.place(x=x_offset + (i % 2) * 250, y=y_offset + (i // 2) * 70)

        # Botón de cerrar al centro de la zona de botones
        self.cerrar_boton = tk.Button(self.frame_inicial, text="Cerrar", width=20, height=2, font=("Trebuchet MS", 11), bg="maroon", fg="white", command=self.root.quit)
        self.cerrar_boton.place(x=1000, y=500)

    def ocultar_inicio(self):
        """Oculta el frame inicial y el botón de cerrar."""
        self.frame_inicial.pack_forget()  # Ocultar el frame inicial
        self.cerrar_boton.pack_forget()   # Ocultar el botón de cerrar

    def mostrar_registro_autores(self):
        """Muestra la interfaz de registro de autores y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de registro de autores
        self.frame_registro_autores = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_autores.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_registro_autores, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=450, y=20)

        # Título de la página de registro de autores
        titulo_label = tk.Label(
            self.frame_registro_autores, 
            text="Registro de Autores", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=570, y=50)


        # Campos de texto para el registro de autores, con etiquetas a la izquierda
        tk.Label(self.frame_registro_autores, text="Nombre:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=150)
        self.nombre_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.nombre_entry.place(x=620, y=150)

        tk.Label(self.frame_registro_autores, text="Apellido:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=190)
        self.apellido_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.apellido_entry.place(x=620, y=190)

        tk.Label(self.frame_registro_autores, text="Nacionalidad:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=500, y=230)
        self.nacionalidad_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.nacionalidad_entry.place(x=620, y=230)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_registro_autores, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=300)

        # Botón "Registrar" en marrón oscuro
        registrar_boton = tk.Button(
            self.frame_registro_autores, 
            text="Registrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="orange", 
            command=self.registrar_autor
        )
        registrar_boton.place(x=620, y=300)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_registro_autores, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=300)


    def mostrar_registro_libros(self):
        """Muestra la interfaz de registro de libros y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de registro de libros
        self.frame_registro_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_libros.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_registro_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la página de registro de libros
        titulo_label = tk.Label(
            self.frame_registro_libros, 
            text="Registro de Libros", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Campos de texto para el registro de libros, con etiquetas a la izquierda
        tk.Label(self.frame_registro_libros, text="Código ISBN:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=500, y=150)
        self.isbn_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.isbn_entry.place(x=620, y=150)

        tk.Label(self.frame_registro_libros, text="Título:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=545, y=190)
        self.titulo_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.titulo_entry.place(x=620, y=190)

        tk.Label(self.frame_registro_libros, text="Género:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=540, y=230)
        self.genero_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.genero_entry.place(x=620, y=230)

        # Año de publicación con Spinbox
        tk.Label(self.frame_registro_libros, text="Año de Publicación:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=465, y=270)
        self.anio_publicacion_entry = tk.Spinbox(self.frame_registro_libros, from_=1900, to=2100, font=("Trebuchet MS", 12), width=10)
        self.anio_publicacion_entry.config(validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.anio_publicacion_entry.place(x=620, y=270)

        # Combobox para seleccionar el autor existente
        tk.Label(self.frame_registro_libros, text="Selecciona el Autor:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=460, y=310)
        autores = Autor.listar_autores()  # Obtener lista de autores desde la base de datos
        self.autor_combobox = ttk.Combobox(self.frame_registro_libros, values=[f"{autor[0]} - {autor[1]}" for autor in autores], font=("Trebuchet MS", 12), width=22, state="readonly")
        self.autor_combobox.place(x=620, y=310)

        # Campo para ingresar la cantidad de libros
        tk.Label(self.frame_registro_libros, text="Cantidad de Libros:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=465, y=350)
        self.cantidad_libros_entry = tk.Entry(
            self.frame_registro_libros, 
            font=("Trebuchet MS", 12), 
            width=25, 
            validate="key", 
            validatecommand=(self.root.register(self.validar_numerico), "%P")
        )
        self.cantidad_libros_entry.place(x=620, y=350)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_registro_libros, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=420)

        # Botón "Registrar" en marrón oscuro
        registrar_boton = tk.Button(
            self.frame_registro_libros, 
            text="Registrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="orange", 
            command=self.registrar_libro
        )
        registrar_boton.place(x=620, y=420)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_registro_libros, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=420)


    def mostrar_registro_usuarios(self):
        """Muestra la interfaz de registro de usuarios y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de registro de usuarios
        self.frame_registro_usuarios = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_usuarios.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_registro_usuarios, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la página de registro de usuarios
        titulo_label = tk.Label(
            self.frame_registro_usuarios, 
            text="Registro de Usuarios", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Campos de texto para el registro de usuarios, con etiquetas a la izquierda
        tk.Label(self.frame_registro_usuarios, text="Nombre:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=150)
        self.nombre_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.nombre_entry.place(x=620, y=150)

        tk.Label(self.frame_registro_usuarios, text="Apellido:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=190)
        self.apellido_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.apellido_entry.place(x=620, y=190)

        # Combobox para seleccionar el tipo de usuario
        tk.Label(self.frame_registro_usuarios, text="Tipo de Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=475, y=230)
        self.tipo_usuario_combobox = ttk.Combobox(
            self.frame_registro_usuarios, 
            values=["Estudiante", "Profesor"], 
            font=("Trebuchet MS", 12), 
            width=22, 
            state="readonly"
        )
        self.tipo_usuario_combobox.place(x=620, y=230)

        # Campos de dirección y teléfono
        tk.Label(self.frame_registro_usuarios, text="Dirección:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=520, y=270)
        self.direccion_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.direccion_entry.place(x=620, y=270)

        tk.Label(self.frame_registro_usuarios, text="Teléfono:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=525, y=310)
        self.telefono_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25, validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.telefono_entry.place(x=620, y=310)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_registro_usuarios, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=380)

        # Botón "Registrar" en marrón oscuro
        registrar_boton = tk.Button(
            self.frame_registro_usuarios, 
            text="Registrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="orange", 
            command=self.registrar_usuario
        )
        registrar_boton.place(x=620, y=380)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_registro_usuarios, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=380)


    def mostrar_prestamo_libros(self):
        """Muestra la interfaz de préstamo de libros y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de préstamo de libros
        self.frame_prestamo_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_prestamo_libros.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_prestamo_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la página de préstamo de libros
        titulo_label = tk.Label(
            self.frame_prestamo_libros,
            text="Préstamo de Libros",
            font=("Trebuchet MS", 20, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Combobox para seleccionar el Usuario existente
        tk.Label(self.frame_prestamo_libros, text="Selecciona el Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=440, y=150)
        usuarios = Usuario.listar_usuarios()  # Obtener lista de usuarios desde la base de datos
        self.usuario_combobox = ttk.Combobox(
            self.frame_prestamo_libros,
            values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios],
            font=("Trebuchet MS", 12),
            width=35,
            state="readonly"
        )
        self.usuario_combobox.place(x=620, y=150)

        # Combobox para seleccionar el Libro disponible
        tk.Label(self.frame_prestamo_libros, text="Selecciona el Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=190)
        libros = Libro.listar_libros("disponibles")  # Obtener lista de libros disponibles desde la base de datos
        self.libro_combobox = ttk.Combobox(
            self.frame_prestamo_libros,
            values=[f"({libro[0]}) - {libro[1]}" for libro in libros],
            font=("Trebuchet MS", 12),
            width=35,
            state="readonly"
        )
        self.libro_combobox.place(x=620, y=190)

        # Campo de Fecha de Préstamo (automáticamente se establece la fecha actual)
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        tk.Label(self.frame_prestamo_libros, text="Fecha de Préstamo:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=230)
        self.fecha_prestamo_label = tk.Label(self.frame_prestamo_libros, text=fecha_actual, font=("Trebuchet MS", 12), width=35)
        self.fecha_prestamo_label.place(x=620, y=230)

        # Campo de Fecha de Devolución Estimada (con DateEntry)
        tk.Label(self.frame_prestamo_libros, text="Fecha de Devolución Estimada:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=370, y=270)
        self.fecha_devolucion_entry = DateEntry(
            self.frame_prestamo_libros,
            font=("Trebuchet MS", 12),
            width=35,
            date_pattern="yyyy-mm-dd",
            state="normal"
        )
        self.fecha_devolucion_entry.place(x=620, y=270)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_prestamo_libros,
            text="Volver",
            width=10,
            height=2,
            font=("Trebuchet MS", 12),
            bg="#E9F98B",
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=350)

        # Botón "Registrar" en naranja oscuro
        registrar_boton = tk.Button(
            self.frame_prestamo_libros,
            text="Registrar",
            width=10,
            height=2,
            font=("Trebuchet MS", 12),
            bg="orange",
            command=self.registrar_prestamo
        )
        registrar_boton.place(x=620, y=350)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_prestamo_libros,
            text="Cerrar",
            width=10,
            height=2,
            font=("Trebuchet MS", 12),
            bg="maroon",
            fg="white",
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=350)


    def mostrar_devolucion_libros(self):
        """Muestra la interfaz de devolución de libros con una tabla de préstamos activos."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de devolución de libros
        self.frame_devolucion_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_devolucion_libros.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_devolucion_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la página de devolución de libros
        titulo_label = tk.Label(
            self.frame_devolucion_libros, 
            text="Devolución de Libros", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Etiqueta de instrucción para la tabla
        instruccion_label = tk.Label(
            self.frame_devolucion_libros, 
            text="Seleccione un Préstamo Activo para Devolver", 
            font=("Trebuchet MS", 12), 
            bg="#f0f0f0"
        )
        instruccion_label.place(x=530, y=150)

        # Tabla de préstamos activos
        self.tabla_prestamos = ttk.Treeview(self.frame_devolucion_libros, columns=("ID", "Usuario", "Libro"), show="headings", height=10)
        self.tabla_prestamos.heading("ID", text="ID")
        self.tabla_prestamos.heading("Usuario", text="Nombre Persona")
        self.tabla_prestamos.heading("Libro", text="Nombre Libro")
        self.tabla_prestamos.column("ID", width=100, anchor="center")
        self.tabla_prestamos.column("Usuario", width=200, anchor="center")
        self.tabla_prestamos.column("Libro", width=200, anchor="center")
        self.tabla_prestamos.place(x=450, y=200)
        self.tabla_prestamos.place(x=450, y=200)

        # Rellenar la tabla con los préstamos activos
        prestamos_activos = Prestamo.listar_prestamos_activos()
        for prestamo in prestamos_activos:
            self.tabla_prestamos.insert("", tk.END, values=prestamo)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_devolucion_libros, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=500)

        # Botón "Devolver" en marrón oscuro
        devolver_boton = tk.Button(
            self.frame_devolucion_libros, 
            text="Devolver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="orange", 
            command=self.devolver_prestamo
        )
        devolver_boton.place(x=620, y=500)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_devolucion_libros, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=500)

    def mostrar_consulta_disponibilidad(self):
        """Muestra la interfaz de consulta de disponibilidad y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame de consulta de disponibilidad
        self.frame_consulta_disponibilidad = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_consulta_disponibilidad.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_consulta_disponibilidad, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=380, y=20)

        # Título de la página de consulta de disponibilidad
        titulo_label = tk.Label(
            self.frame_consulta_disponibilidad, 
            text="Consulta de Disponibilidad de Libros", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=520, y=50)

        # Etiqueta para seleccionar el libro
        tk.Label(
            self.frame_consulta_disponibilidad, 
            text="Selecciona el Libro:", 
            font=("Trebuchet MS", 12), 
            bg="#f0f0f0"
        ).place(x=450, y=150)

        # Combobox para seleccionar el libro
        libros = Libro.listar_libros()  # Obtener lista de todos los libros
        self.libro_combobox = ttk.Combobox(
            self.frame_consulta_disponibilidad,
            values=[f"{libro[0]} - {libro[1]}" for libro in libros],
            font=("Trebuchet MS", 12),
            width=40,
            state="readonly"
        )
        self.libro_combobox.place(x=630, y=150)

        # Botón para consultar la disponibilidad
        consultar_boton = tk.Button(
            self.frame_consulta_disponibilidad, 
            text="Consultar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="orange", 
            command=self.consultar_disponibilidad_libro
        )
        consultar_boton.place(x=620, y=350)

        # Etiqueta para mostrar el resultado de la consulta
        self.resultado_label = tk.Label(
            self.frame_consulta_disponibilidad, 
            text="", 
            font=("Trebuchet MS", 12), 
            bg="#f0f0f0"
        )
        self.resultado_label.place(x=550, y=250)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_consulta_disponibilidad, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=350)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_consulta_disponibilidad, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=350)

    def mostrar_reserva_libros(self):
        """Muestra la interfaz de reserva de libros y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame para la interfaz de reserva de libros
        self.frame_reserva_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_reserva_libros.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_reserva_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la página de reserva de libros
        titulo_label = tk.Label(
            self.frame_reserva_libros,
            text="Reserva de Libros",
            font=("Trebuchet MS", 20, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Obtener lista de libros no disponibles
        libros_no_disponibles = Libro.listar_libros("no_disponibles")

        if libros_no_disponibles:
            # Combobox para seleccionar el Usuario
            tk.Label(
                self.frame_reserva_libros, 
                text="Selecciona el Usuario:", 
                font=("Trebuchet MS", 12), 
                bg="#f0f0f0"
            ).place(x=450, y=150)
            usuarios = Usuario.listar_usuarios()  # Obtener lista de usuarios desde la base de datos
            self.usuario_combobox = ttk.Combobox(
                self.frame_reserva_libros,
                values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios],
                font=("Trebuchet MS", 12),
                width=30,
                state="readonly"
            )
            self.usuario_combobox.place(x=630, y=150)

            # Combobox para seleccionar el Libro no disponible
            tk.Label(
                self.frame_reserva_libros, 
                text="Selecciona el Libro:", 
                font=("Trebuchet MS", 12), 
                bg="#f0f0f0"
            ).place(x=450, y=190)
            self.libro_combobox = ttk.Combobox(
                self.frame_reserva_libros,
                values=[f"{libro[0]} - {libro[1]}" for libro in libros_no_disponibles],
                font=("Trebuchet MS", 12),
                width=30,
                state="readonly"
            )
            self.libro_combobox.place(x=630, y=190)

            # Botón para realizar la reserva
            self.reservar_boton = tk.Button(
                self.frame_reserva_libros, 
                text="Reservar", 
                width=10, 
                height=2, 
                font=("Trebuchet MS", 12), 
                bg="orange", 
                command=self.reservar_libro
            )
            self.reservar_boton.place(x=620, y=320)

        else:
            # Mostrar mensaje de todos los libros disponibles y desactivar opciones de reserva
            tk.Label(
                self.frame_reserva_libros,
                text="Todos los libros están disponibles. No se pueden realizar reservas.",
                font=("Trebuchet MS", 12, "italic"),
                bg="#f0f0f0"
            ).place(x=450, y=200)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_reserva_libros,
            text="Volver",
            width=10,
            height=2,
            font=("Trebuchet MS", 12),
            bg="#E9F98B",
            command=self.volver_inicio
        )
        volver_boton.place(x=500, y=320)

        # Botón "Cerrar" en su posición habitual
        cerrar_boton = tk.Button(
            self.frame_reserva_libros,
            text="Cerrar",
            width=10,
            height=2,
            font=("Trebuchet MS", 12),
            bg="maroon",
            fg="white",
            command=self.root.quit
        )
        cerrar_boton.place(x=740, y=320)

    def mostrar_reportes(self):
        """Muestra la interfaz de reportes y oculta los elementos anteriores."""
        self.ocultar_inicio()  # Ocultar los elementos del inicio

        # Frame para la interfaz de reportes
        self.frame_reportes = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_reportes.pack(fill="both", expand=True)

        # Logo pequeño en la esquina izquierda
        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)  # Redimensionar el logo
        self.logo_label_small = tk.Label(self.frame_reportes, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small  # Mantener referencia
        self.logo_label_small.place(x=480, y=20)

        # Título de la sección de reportes
        titulo_label = tk.Label(
            self.frame_reportes, 
            text="Reportes de Biblioteca", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        # Botones para cada reporte
        reportes = [
            ("Préstamos Vencidos", self.generar_reporte_prestamos_vencidos),
            ("Libros Más Prestados Último Mes", self.generar_reporte_libros_mas_prestados),
            ("Usuarios con Más Préstamos", self.generar_reporte_usuarios_mas_prestamos),
            ("Libros por Autor", self.generar_reporte_libros_por_autor),
            ("Usuarios con Penalizaciones", self.generar_reporte_usuarios_penalizados),
            ("Estadísticas de Donaciones", self.generar_reporte_donaciones)
        ]

        y_offset = 150  # Posición y inicial para el primer botón
        for i, (text, command) in enumerate(reportes):
            boton_reporte = tk.Button(
                self.frame_reportes, 
                text=text, 
                width=30, 
                height=2, 
                font=("Trebuchet MS", 12), 
                bg="orange", 
                command=command
            )
            boton_reporte.place(x=100, y=y_offset + i * 80)

        # Botón "Volver" en naranja
        volver_boton = tk.Button(
            self.frame_reportes, 
            text="Volver", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="#E9F98B", 
            command=self.volver_inicio
        )
        volver_boton.place(x=800, y=600)

        # Botón "Cerrar" en marrón oscuro
        cerrar_boton = tk.Button(
            self.frame_reportes, 
            text="Cerrar", 
            width=10, 
            height=2, 
            font=("Trebuchet MS", 12), 
            bg="maroon", 
            fg="white", 
            command=self.root.quit
        )
        cerrar_boton.place(x=950, y=600)

    def mostrar_area_reporte(self):
        """Crea o limpia el área de visualización del reporte sin afectar los botones de navegación."""
        if hasattr(self, 'frame_reporte'):
            # Si ya existe el frame, lo limpia
            for widget in self.frame_reporte.winfo_children():
                widget.destroy()
        else:
            # Crea el frame si no existe, en una posición fija dentro de frame_reportes
            self.frame_reporte = tk.Frame(self.frame_reportes, width=2000, height=400, bg="#f0f0f0")
            self.frame_reporte.place(x=400, y=150)  # Ubicación personalizada para el área de reportes con coordenadas x, y

    def generar_reporte_prestamos_vencidos(self):
        """Genera y muestra el reporte de préstamos vencidos en el área de reportes."""
        # Muestra o limpia el área del reporte
        self.mostrar_area_reporte()

        # Obtener la lista de préstamos vencidos
        prestamos_vencidos = Prestamo.obtener_prestamos_vencidos()  # Método de consulta en la clase Prestamo

        if not prestamos_vencidos:
            tk.Label(self.frame_reporte, text="No hay préstamos vencidos.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        # Título del reporte
        titulo_label = tk.Label(
            self.frame_reporte, 
            text="Reporte de Préstamos Vencidos", 
            font=("Trebuchet MS", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=350, y=10)

        # Crear un Treeview para mostrar los datos en formato tabular
        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Vencimiento"), show="headings")
        tabla_reporte.heading("ID", text="ID Préstamo")
        tabla_reporte.heading("Usuario", text="Usuario")
        tabla_reporte.heading("Libro", text="Libro")
        tabla_reporte.heading("Fecha Préstamo", text="Fecha Préstamo")
        tabla_reporte.heading("Fecha Vencimiento", text="Fecha Vencimiento")

        # Centrando las columnas y ajustando el ancho
        for col in ("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Vencimiento"):
            tabla_reporte.column(col, width=150, anchor="center")

        # Posicionar la tabla en coordenadas específicas dentro del área de reporte
        tabla_reporte.place(x=120, y=50, width=750, height=300)

        # Agregar scroll vertical al Treeview
        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=870, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview


        # Insertar datos en la tabla (ajuste para acceder por índice)
        for prestamo in prestamos_vencidos:
            tabla_reporte.insert("", tk.END, values=(prestamo[0], prestamo[1], prestamo[2], prestamo[3], prestamo[4]))


    def generar_reporte_libros_mas_prestados(self):
        """Genera y muestra el reporte de libros más prestados en el área de reportes."""
        # Muestra o limpia el área del reporte
        self.mostrar_area_reporte()

        # Obtener la lista de libros más prestados del último mes
        libros_mas_prestados = Prestamo.obtener_libros_mas_prestados()  # Método de consulta en la clase Prestamo

        if not libros_mas_prestados:
            tk.Label(self.frame_reporte, text="No hay préstamos en el último mes.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        # Título del reporte
        titulo_label = tk.Label(
            self.frame_reporte, 
            text="Reporte de Libros Más Prestados en el Último Mes", 
            font=("Trebuchet MS", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=300, y=10)

        # Crear un Treeview para mostrar los datos en formato tabular
        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Título", "Total Préstamos"), show="headings")
        tabla_reporte.heading("ID", text="ID Libro")
        tabla_reporte.heading("Título", text="Título")
        tabla_reporte.heading("Total Préstamos", text="Total Préstamos")

        # Centrando las columnas y ajustando el ancho
        for col in ("ID", "Título", "Total Préstamos"):
            tabla_reporte.column(col, width=200, anchor="center")

        # Posicionar la tabla en coordenadas específicas dentro del área de reporte
        tabla_reporte.place(x=120, y=50, width=650, height=300)

        # Agregar scroll vertical al Treeview
        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=770, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview

        # Insertar datos en la tabla (ajuste para acceder por índice)
        for libro in libros_mas_prestados:
            tabla_reporte.insert("", tk.END, values=(libro[0], libro[1], libro[2]))
            
    def generar_reporte_usuarios_mas_prestamos(self):
        """Genera y muestra el reporte de usuarios con más préstamos en el área de reportes."""
        # Muestra o limpia el área del reporte
        self.mostrar_area_reporte()

        # Obtener la lista de usuarios con más préstamos del último mes
        usuarios_mas_prestamos = Prestamo.obtener_usuarios_mas_prestamos()  # Método de consulta en la clase Prestamo

        if not usuarios_mas_prestamos:
            tk.Label(self.frame_reporte, text="No hay usuarios con préstamos en el último mes.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        # Título del reporte
        titulo_label = tk.Label(
            self.frame_reporte, 
            text="Reporte de Usuarios con Más Préstamos en el Último Mes", 
            font=("Trebuchet MS", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=300, y=10)

        # Crear un Treeview para mostrar los datos en formato tabular
        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Nombre", "Apellido", "Total Préstamos"), show="headings")
        tabla_reporte.heading("ID", text="ID Usuario")
        tabla_reporte.heading("Nombre", text="Nombre")
        tabla_reporte.heading("Apellido", text="Apellido")
        tabla_reporte.heading("Total Préstamos", text="Total Préstamos")

        # Centrando las columnas y ajustando el ancho
        for col in ("ID", "Nombre", "Apellido", "Total Préstamos"):
            tabla_reporte.column(col, width=150, anchor="center")

        # Posicionar la tabla en coordenadas específicas dentro del área de reporte
        tabla_reporte.place(x=120, y=50, width=650, height=300)

        # Agregar scroll vertical al Treeview
        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=770, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview

        # Insertar datos en la tabla
        for usuario in usuarios_mas_prestamos:
            tabla_reporte.insert("", tk.END, values=(usuario[0], usuario[1], usuario[2], usuario[3]))

    def generar_reporte_libros_por_autor(self):
        """Genera y muestra el reporte de libros por autor en el área de reportes."""
        # Muestra o limpia el área del reporte
        self.mostrar_area_reporte()

        # Obtener la lista de libros por autor
        libros_por_autor = Libro.obtener_libros_por_autor()  # Método de consulta en la clase Libro

        if not libros_por_autor:
            tk.Label(self.frame_reporte, text="No hay libros disponibles.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        # Título del reporte
        titulo_label = tk.Label(
            self.frame_reporte, 
            text="Reporte de Libros por Autor", 
            font=("Trebuchet MS", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=300, y=10)

        # Crear un Treeview para mostrar los datos en formato tabular
        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("Autor", "Cantidad Libros", "Total Disponibles"), show="headings")
        tabla_reporte.heading("Autor", text="Autor")
        tabla_reporte.heading("Cantidad Libros", text="Cantidad de Libros")
        tabla_reporte.heading("Total Disponibles", text="Total Disponibles")

        # Centrando las columnas y ajustando el ancho
        for col in ("Autor", "Cantidad Libros", "Total Disponibles"):
            tabla_reporte.column(col, width=200, anchor="center")

        # Posicionar la tabla en coordenadas específicas dentro del área de reporte
        tabla_reporte.place(x=120, y=50, width=650, height=300)

        # Agregar scroll vertical al Treeview
        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=770, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview

        # Insertar datos en la tabla
        for autor in libros_por_autor:
            tabla_reporte.insert("", tk.END, values=(autor[0], autor[1], autor[2]))

    def generar_reporte_usuarios_penalizados(self):
        """Genera y muestra el reporte de usuarios con penalizaciones."""
        # Muestra o limpia el área del reporte
        self.mostrar_area_reporte()

        # Obtener la lista de usuarios con penalizaciones
        penalizaciones = Usuario.obtener_usuarios_con_penalizaciones()

        if not penalizaciones:
            tk.Label(self.frame_reporte, text="No hay usuarios con penalizaciones.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        # Título del reporte
        titulo_label = tk.Label(
            self.frame_reporte, 
            text="Reporte de Usuarios con Penalizaciones", 
            font=("Trebuchet MS", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo_label.place(x=300, y=10)

        # Crear un Treeview para mostrar los datos en formato tabular
        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("Nombre", "Apellido", "Monto", "Motivo"), show="headings")
        tabla_reporte.heading("Nombre", text="Nombre")
        tabla_reporte.heading("Apellido", text="Apellido")
        tabla_reporte.heading("Monto", text="Monto")
        tabla_reporte.heading("Motivo", text="Motivo")

        # Centrando las columnas y ajustando el ancho
        for col in ("Nombre", "Apellido", "Monto", "Motivo"):
            tabla_reporte.column(col, width=200, anchor="center")

        # Posicionar la tabla en coordenadas específicas dentro del área de reporte
        tabla_reporte.place(x=120, y=50, width=650, height=300)

        # Agregar scroll vertical al Treeview
        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=770, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview

        # Insertar datos en la tabla
        for penalizacion in penalizaciones:
            tabla_reporte.insert("", tk.END, values=(penalizacion[0], penalizacion[1], penalizacion[2], penalizacion[3]))  # Asegúrate de que los índices coincidan con los datos obtenidos

            # Obtener la lista de usuarios con penalizaciones
            penalizaciones_activas = Usuario.obtener_usuarios_penalizaciones()

            if not penalizaciones_activas:
                tk.Label(self.frame_reporte, text="No hay usuarios con penalizaciones activas.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
                return

            # Título del reporte
            titulo_label = tk.Label(
                self.frame_reporte, 
                text="Reporte de Usuarios con Penalizaciones", 
                font=("Trebuchet MS", 16, "bold"),
                bg="#f0f0f0"
            )
            titulo_label.place(x=300, y=10)

            # Crear un Treeview para mostrar los datos en formato tabular
            tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("Usuario ID", "Monto", "Motivo"), show="headings")
            tabla_reporte.heading("Usuario ID", text="Usuario ID")
            tabla_reporte.heading("Monto", text="Monto")
            tabla_reporte.heading("Motivo", text="Motivo")

            # Centrando las columnas y ajustando el ancho
            for col in ("Usuario ID", "Monto", "Motivo"):
                tabla_reporte.column(col, width=200, anchor="center")

            # Posicionar la tabla en coordenadas específicas dentro del área de reporte
            tabla_reporte.place(x=120, y=50, width=650, height=300)

            # Agregar scroll vertical al Treeview
            scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
            tabla_reporte.configure(yscrollcommand=scroll_y.set)
            scroll_y.place(x=770, y=50, height=300)  # Ajusta 'x' y 'y' según el ancho y la posición del Treeview

            # Insertar datos en la tabla
            for penalizacion in penalizaciones_activas:
                tabla_reporte.insert("", tk.END, values=(penalizacion[0], penalizacion[1], penalizacion[2]))  # Asegúrate de que los índices coincidan con los datos obtenidos

    def generar_reporte_donaciones(self):
        # Lógica para obtener y mostrar el reporte de donaciones
        messagebox.showinfo("Reporte", "Generando reporte de donaciones.")

    def consultar_disponibilidad_libro(self):
        """Consulta y muestra la disponibilidad de un libro seleccionado."""
        libro_seleccionado = self.libro_combobox.get()

        # Validación de selección
        if not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un libro para consultar su disponibilidad.")
            return

        # Extraer ISBN del libro seleccionado
        codigo_isbn = libro_seleccionado.split(" - ")[0]

        # Consultar la disponibilidad usando el método de la clase Libro
        cantidad_disponible = Libro.consultar_disponibilidad(codigo_isbn)
        self.resultado_label.config(text=f"Disponibilidad: {cantidad_disponible} ejemplares.")


    def crear_campo(self, frame, label_text, validate=None, vcmd=None):
        """Crea un campo de texto con una etiqueta en el frame proporcionado."""
        label = tk.Label(frame, text=label_text, font=("Helvetica", 12))
        label.pack(pady=5)
        
        entry = tk.Entry(frame, font=("Helvetica", 12), width=30, validate=validate, validatecommand=vcmd)
        entry.pack(pady=5)
        
        return entry

    def validar_numerico(self, texto):
        """Permite solo entrada numérica."""
        return texto.isdigit() or texto == ""

    def registrar_autor(self):
        """Registra un nuevo autor en el sistema verificando los campos."""
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        nacionalidad = self.nacionalidad_entry.get()
    

        # Validación de campos vacíos
        if not validar_campos_vacios(nombre, apellido, nacionalidad):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Crear una instancia de Autor usando AutorFactory y guardar en la base de datos
        autor_factory = AutorFactory()
        autor = autor_factory.factory_method(nombre, apellido, nacionalidad)
        
        try:
            autor.guardar()  # Llama al método guardar de la instancia de Autor
            messagebox.showinfo("Registro", "Autor registrado correctamente.")
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.nacionalidad_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el autor: {e}")

    def registrar_usuario(self):
        """Registra un nuevo usuario en el sistema verificando los campos."""
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        tipo_usuario = self.tipo_usuario_combobox.get().lower()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()

        # Validación de campos vacíos
        if not validar_campos_vacios(nombre, apellido, tipo_usuario, direccion, telefono):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Crear una instancia de Usuario usando UsuarioFactory y guardar en la base de datos
        usuario_factory = UsuarioFactory()
        usuario = usuario_factory.factory_method(nombre, apellido, tipo_usuario, direccion, telefono)
        
        try:
            usuario.guardar()  # Llama al método guardar de la instancia de Usuario
            messagebox.showinfo("Registro", "Usuario registrado correctamente.")
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.tipo_usuario_combobox.set('')
            self.direccion_entry.delete(0, tk.END)
            self.telefono_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    def registrar_prestamo(self):
        """Registra un nuevo préstamo en el sistema verificando los campos."""
        usuario_seleccionado = self.usuario_combobox.get()
        libro_seleccionado = self.libro_combobox.get()
        fecha_devolucion = self.fecha_devolucion_entry.get_date().strftime("%Y-%m-%d")

        # Validación de selección en combobox
        if not usuario_seleccionado or not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        # Extraer IDs de usuario y libro seleccionados
        usuario_id = int(usuario_seleccionado.split(" - ")[0])
        # Extraer los caracteres del 1 al 13 para obtener el ISBN
        codigo_isbn = libro_seleccionado[1:18]

        # Crear una instancia de Préstamo usando PrestamoFactory y guardar en la base de datos
        prestamo_factory = PrestamoFactory()
        prestamo = prestamo_factory.factory_method(usuario_id, codigo_isbn, fecha_devolucion)
        
        try:
            prestamo.guardar()  # Llama al método guardar de la instancia de Préstamo
            messagebox.showinfo("Registro", "Préstamo registrado correctamente.")
            self.usuario_combobox.set('')
            self.libro_combobox.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo: {e}")

    def volver_inicio(self):
        """Vuelve a la pantalla de inicio y oculta cualquier frame de registro o funcionalidad."""

        # Ocultar frames específicos solo si existen
        if hasattr(self, 'frame_registro_autores'):
            self.frame_registro_autores.pack_forget()
        if hasattr(self, 'frame_registro_libros'):
            self.frame_registro_libros.pack_forget()
        if hasattr(self, 'frame_registro_usuarios'):
            self.frame_registro_usuarios.pack_forget()
        if hasattr(self, 'frame_prestamo_libros'):
            self.frame_prestamo_libros.pack_forget()
        if hasattr(self, 'frame_devolucion_libros'):
            self.frame_devolucion_libros.pack_forget()
        if hasattr(self, 'frame_consulta_disponibilidad'):
            self.frame_consulta_disponibilidad.pack_forget()
        if hasattr(self, 'frame_reserva_libros'):
            self.frame_reserva_libros.pack_forget()
        if hasattr(self, 'frame_reportes'):
            self.frame_reportes.pack_forget()

        # Volver a mostrar el frame inicial y sus elementos usando coordenadas
        self.frame_inicial.place(x=0, y=0, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        
        # Volver a mostrar el botón de cerrar con la misma posición y estilo
        self.cerrar_boton.place(x=1000, y=500)

    # Funciones de otras funcionalidades
    def registrar_libro(self):
        """Registra un nuevo libro en el sistema verificando los campos."""
        codigo_isbn = self.isbn_entry.get()
        titulo = self.titulo_entry.get()
        genero = self.genero_entry.get()
        anio_publicacion = self.anio_publicacion_entry.get()
        autor_seleccionado = self.autor_combobox.get()
        cantidad = self.cantidad_libros_entry.get()

        # Validación de campos vacíos
        if not validar_campos_vacios(codigo_isbn, titulo, genero, anio_publicacion, autor_seleccionado, cantidad):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Obtener autor_id de la selección
            autor_id = int(autor_seleccionado.split(" - ")[0])
            
            # Crear y guardar el libro usando el Factory
            libro_factory = LibroFactory()
            print(autor_id)
            libro = libro_factory.factory_method(codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad)
            libro.guardar()  # Método guardar en clase Libro

            messagebox.showinfo("Registro", "Libro registrado correctamente.")
            self.isbn_entry.delete(0, tk.END)
            self.titulo_entry.delete(0, tk.END)
            self.genero_entry.delete(0, tk.END)
            self.anio_publicacion_entry.delete(0, tk.END)
            self.autor_combobox.set('')
            self.cantidad_libros_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el libro: {e}")

    def registrar_devolucion(self):
        """Registra la devolución del libro en el sistema verificando las condiciones."""
        usuario_seleccionado = self.usuario_combobox.get()
        libro_seleccionado = self.libro_combobox.get()
        en_condiciones = self.condiciones_var.get()

        # Validación de selección en combobox
        if not usuario_seleccionado or not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        # Extraer IDs de usuario y libro seleccionados
        usuario_id = int(usuario_seleccionado.split(" - ")[0])
        codigo_isbn = libro_seleccionado.split(" - ")[0]

        try:
            # Llama al método de clase para registrar la devolución
            Prestamo.registrar_devolucion(usuario_id, codigo_isbn, en_condiciones)
            messagebox.showinfo("Devolución", "Devolución registrada correctamente.")
            
            # Reiniciar los campos
            self.usuario_combobox.set('')
            self.libro_combobox.set('')
            self.condiciones_var.set(False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución: {e}")

    def devolver_prestamo(self):
        """Marca el préstamo seleccionado como devuelto (estado 'Finalizado')."""
        selected_item = self.tabla_prestamos.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un préstamo para devolver.")
            return

        # Obtener el ID del préstamo seleccionado
        prestamo_id = self.tabla_prestamos.item(selected_item)["values"][0]

        try:
            Prestamo.finalizar_prestamo(prestamo_id)  # Finalizar el préstamo
            messagebox.showinfo("Devolución", "Préstamo devuelto correctamente.")

            # Actualizar la tabla eliminando el préstamo devuelto
            self.tabla_prestamos.delete(selected_item)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución: {e}")

        messagebox.showinfo("Funcionalidad", "Consulta de Disponibilidad: Consultar la disponibilidad de un libro.")

    def reservar_libro(self):
        """Registra una reserva de libro en el sistema verificando los campos."""
        usuario_seleccionado = self.usuario_combobox.get()
        libro_seleccionado = self.libro_combobox.get()

        # Validación de selección en combobox
        if not usuario_seleccionado or not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        # Extraer IDs de usuario y libro seleccionados
        usuario_id = int(usuario_seleccionado.split(" - ")[0])
        codigo_isbn = libro_seleccionado.split(" - ")[0]

        # Crear una instancia de Reserva usando ReservaFactory y guardar en la base de datos
        reserva_factory = ReservaFactory()
        reserva = reserva_factory.factory_method(usuario_id, codigo_isbn)

        try:
            reserva.guardar()  # Llama al método guardar de la instancia de Reserva
            messagebox.showinfo("Reserva", "Reserva registrada correctamente.")
            self.usuario_combobox.set('')
            self.libro_combobox.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la reserva: {e}")

# Inicializar la aplicación
def crear_interfaz():
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()