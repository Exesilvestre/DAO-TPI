import tkinter as tk
from tkinter import PhotoImage
from tkcalendar import DateEntry 
from tkinter import ttk 
import sys
import re
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import messagebox
from patrones.factory import AutorFactory, LibroFactory, UsuarioFactory, PrestamoFactory, ReservaFactory, DonacionFactory
from models.Autor import Autor
from models.Libro import Libro
from models.Usuario import Usuario
from models.Prestamo import Prestamo
from models.donacion import Donacion
from datetime import datetime

class BibliotecaApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.state("zoomed")  

        self.frame_inicial = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_inicial.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image = PhotoImage(file=logo_path)
        self.logo_label = tk.Label(self.frame_inicial, image=logo_image, bg="#f0f0f0")
        self.logo_label.image = logo_image  
        self.logo_label.place(x=150, y=20) 

        self.titulo_label = tk.Label(self.frame_inicial, text="Sistema de Gestión de Biblioteca", font=("Trebuchet MS", 24, "bold"), bg="#f0f0f0")
        self.titulo_label.place(x=150, y=520)  # Posición del título

        botones = [
            ("Registrar Autores", self.mostrar_registro_autores),
            ("Registrar Libros", self.mostrar_registro_libros),
            ("Registrar Usuarios", self.mostrar_registro_usuarios),
            ("Registrar Préstamos", self.mostrar_prestamo_libros),
            ("Devolver Libros", self.mostrar_devolucion_libros),
            ("Consultar Disponibilidad", self.mostrar_consulta_disponibilidad),
            ("Reservar Libros", self.mostrar_reserva_libros),
            ("Bajar Libros", self.mostrar_baja_libros),
            ("Registrar Donación", self.mostrar_registro_donaciones),
            ("Reportes", self.mostrar_reportes)  
        ]

        x_offset = 850
        y_offset = 150  
        for i, (text, command) in enumerate(botones):
            boton = tk.Button(self.frame_inicial, text=text, width=25, height=2, font=("Trebuchet MS", 11), bg="orange", command=command)
            boton.place(x=x_offset + (i % 2) * 250, y=y_offset + (i // 2) * 70)

        self.cerrar_boton = tk.Button(self.frame_inicial, text="Cerrar", width=20, height=2, font=("Trebuchet MS", 11), bg="maroon", fg="white", command=self.root.quit)
        self.cerrar_boton.place(x=1000, y=550)  

    # Vuelve a la pantalla de inicio y oculta cualquier frame de registro o funcionalidad
    def volver_inicio(self):

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
        if hasattr(self, 'frame_baja_libros'):
            self.frame_baja_libros.pack_forget()
        if hasattr(self, 'frame_reportes'):
            self.frame_reportes.pack_forget()
        if hasattr(self, 'frame_donaciones'):
            self.frame_donaciones.pack_forget()

        self.frame_inicial.place(x=0, y=0, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        
        self.cerrar_boton.place(x=1000, y=550)

    # Oculta el frame inicial y el botón de cerrar
    def ocultar_inicio(self):
        self.frame_inicial.pack_forget()  # Ocultar el frame inicial
        self.cerrar_boton.pack_forget()   # Ocultar el botón de cerrar

    # Muestra la interfaz de registro de autores 
    def mostrar_registro_autores(self):
        self.ocultar_inicio()  

        self.frame_registro_autores = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_autores.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5) 
        self.logo_label_small = tk.Label(self.frame_registro_autores, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small 
        self.logo_label_small.place(x=450, y=20)

        titulo_label = tk.Label(self.frame_registro_autores, text="Registro de Autores", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=570, y=50)

        tk.Label(self.frame_registro_autores, text="Nombre:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=150)
        self.nombre_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.nombre_entry.place(x=620, y=150)

        tk.Label(self.frame_registro_autores, text="Apellido:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=190)
        self.apellido_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.apellido_entry.place(x=620, y=190)

        tk.Label(self.frame_registro_autores, text="Nacionalidad:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=500, y=230)
        self.nacionalidad_entry = tk.Entry(self.frame_registro_autores, font=("Trebuchet MS", 12), width=25)
        self.nacionalidad_entry.place(x=620, y=230)

        volver_boton = tk.Button(self.frame_registro_autores, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=300)

        registrar_boton = tk.Button(self.frame_registro_autores, text="Registrar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.registrar_autor)
        registrar_boton.place(x=620, y=300)

        cerrar_boton = tk.Button(self.frame_registro_autores, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=300)

    # Registra un nuevo autor en el sistema
    def registrar_autor(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        nacionalidad = self.nacionalidad_entry.get()
    
        if not nombre or not apellido or not nacionalidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        autor_factory = AutorFactory()
        autor = autor_factory.factory_method(nombre, apellido, nacionalidad)
        
        try:
            autor.guardar()
            messagebox.showinfo("Registro", "Autor registrado correctamente.")
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.nacionalidad_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el autor: {e}")

    # Muestra la interfaz de registro de libros
    def mostrar_registro_libros(self):
        self.ocultar_inicio()

        self.frame_registro_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_libros.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_registro_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(
            self.frame_registro_libros, 
            text="Registro de Libros", 
            font=("Trebuchet MS", 20, "bold"), 
            bg="#f0f0f0"
        )
        titulo_label.place(x=600, y=50)

        tk.Label(self.frame_registro_libros, text="Código ISBN:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=500, y=150)
        self.isbn_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.isbn_entry.place(x=620, y=150)
        # Metodo para verificar que el ISBN existe y autocompletar los datos
        self.isbn_entry.bind('<FocusOut>', self.verificar_isbn_existente)


        tk.Label(self.frame_registro_libros, text="Título:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=545, y=190)
        self.titulo_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.titulo_entry.place(x=620, y=190)

        tk.Label(self.frame_registro_libros, text="Género:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=540, y=230)
        self.genero_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12), width=25)
        self.genero_entry.place(x=620, y=230)

        tk.Label(self.frame_registro_libros, text="Año de Publicación:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=465, y=270)
        self.anio_publicacion_entry = tk.Spinbox(self.frame_registro_libros, from_=1900, to=2100, font=("Trebuchet MS", 12), width=10)
        self.anio_publicacion_entry.config(validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.anio_publicacion_entry.place(x=620, y=270)

        tk.Label(self.frame_registro_libros, text="Selecciona el Autor:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=460, y=310)
        autores = Autor.listar_autores()
        self.autor_combobox = ttk.Combobox(self.frame_registro_libros, values=[f"{autor[0]} - {autor[1]}" for autor in autores], font=("Trebuchet MS", 12), width=22, state="readonly")
        self.autor_combobox.place(x=620, y=310)

        tk.Label(self.frame_registro_libros, text="Cantidad de Libros:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=465, y=350)
        self.cantidad_libros_entry = tk.Entry(self.frame_registro_libros, font=("Trebuchet MS", 12),  width=15, validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.cantidad_libros_entry.place(x=620, y=350)

        volver_boton = tk.Button(self.frame_registro_libros, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=420)

        registrar_boton = tk.Button(self.frame_registro_libros, text="Registrar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.registrar_libro)
        registrar_boton.place(x=620, y=420)

        cerrar_boton = tk.Button(self.frame_registro_libros, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=420)

    # Registra un nuevo libro en el sistema
    def registrar_libro(self):
        codigo_isbn = self.isbn_entry.get()
        titulo = self.titulo_entry.get()
        genero = self.genero_entry.get()
        anio_publicacion = self.anio_publicacion_entry.get()
        autor_seleccionado = self.autor_combobox.get()
        cantidad = self.cantidad_libros_entry.get()

        if not self.validar_isbn(codigo_isbn):
            messagebox.showerror("Error de Validación", "El ISBN ingresado no es válido. Debe seguir el formato xxx-x-xx-xxxxxx-x.")
            return

        if not codigo_isbn or not titulo or not genero or not anio_publicacion or not autor_seleccionado or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            autor_id = int(autor_seleccionado.split(" - ")[0])
            
            libro_factory = LibroFactory()
            print(autor_id)
            libro = libro_factory.factory_method(codigo_isbn, titulo, genero, anio_publicacion, autor_id, cantidad)
            libro.guardar()

            messagebox.showinfo("Registro", "Libro registrado correctamente.")
            self.isbn_entry.delete(0, tk.END)
            self.titulo_entry.delete(0, tk.END)
            self.genero_entry.delete(0, tk.END)
            self.anio_publicacion_entry.delete(0, tk.END)
            self.autor_combobox.set('')
            self.cantidad_libros_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el libro: {e}")

    # Muestra la interfaz de registro de usuarios
    def mostrar_registro_usuarios(self):
        self.ocultar_inicio()

        self.frame_registro_usuarios = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_registro_usuarios.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_registro_usuarios, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_registro_usuarios, text="Registro de Usuarios", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=600, y=50)

        tk.Label(self.frame_registro_usuarios, text="Nombre:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=150)
        self.nombre_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.nombre_entry.place(x=620, y=150)

        tk.Label(self.frame_registro_usuarios, text="Apellido:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=530, y=190)
        self.apellido_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.apellido_entry.place(x=620, y=190)

        tk.Label(self.frame_registro_usuarios, text="Tipo de Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=475, y=230)
        self.tipo_usuario_combobox = ttk.Combobox(self.frame_registro_usuarios, values=["Estudiante", "Profesor"], font=("Trebuchet MS", 12), width=22, state="readonly")
        self.tipo_usuario_combobox.place(x=620, y=230)

        tk.Label(self.frame_registro_usuarios, text="Dirección:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=520, y=270)
        self.direccion_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25)
        self.direccion_entry.place(x=620, y=270)

        tk.Label(self.frame_registro_usuarios, text="Teléfono:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=525, y=310)
        self.telefono_entry = tk.Entry(self.frame_registro_usuarios, font=("Trebuchet MS", 12), width=25, validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.telefono_entry.place(x=620, y=310)

        volver_boton = tk.Button(self.frame_registro_usuarios, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=380)

        registrar_boton = tk.Button(self.frame_registro_usuarios, text="Registrar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.registrar_usuario)
        registrar_boton.place(x=620, y=380)

        cerrar_boton = tk.Button(self.frame_registro_usuarios, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=380)

    # Registra un nuevo usuario en el sistema
    def registrar_usuario(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        tipo_usuario = self.tipo_usuario_combobox.get().lower()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()

        if not nombre or not apellido or not tipo_usuario or not direccion or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuario_factory = UsuarioFactory()
        usuario = usuario_factory.factory_method(nombre, apellido, tipo_usuario, direccion, telefono)
        
        try:
            usuario.guardar()
            messagebox.showinfo("Registro", "Usuario registrado correctamente.")
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.tipo_usuario_combobox.set('')
            self.direccion_entry.delete(0, tk.END)
            self.telefono_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    # Muestra la interfaz de préstamo de libros
    def mostrar_prestamo_libros(self):
        self.ocultar_inicio() 

        self.frame_prestamo_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_prestamo_libros.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_prestamo_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small 
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_prestamo_libros,text="Préstamo de Libros",font=("Trebuchet MS", 20, "bold"),bg="#f0f0f0")
        titulo_label.place(x=600, y=50)

        tk.Label(self.frame_prestamo_libros, text="Selecciona el Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=440, y=150)
        usuarios = Usuario.listar_usuarios() 
        self.usuario_combobox = ttk.Combobox(self.frame_prestamo_libros,values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios],font=("Trebuchet MS", 12),width=35,state="readonly")
        self.usuario_combobox.place(x=620, y=150)

        tk.Label(self.frame_prestamo_libros, text="Selecciona el Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=190)
        libros = Libro.listar_libros("disponibles")
        self.libro_combobox = ttk.Combobox(self.frame_prestamo_libros,values=[f"({libro[0]}) - {libro[1]}" for libro in libros],font=("Trebuchet MS", 12),width=35,state="readonly")
        self.libro_combobox.place(x=620, y=190)

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        tk.Label(self.frame_prestamo_libros, text="Fecha de Préstamo:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=230)
        self.fecha_prestamo_label = tk.Label(self.frame_prestamo_libros, text=fecha_actual, font=("Trebuchet MS", 12), width=35)
        self.fecha_prestamo_label.place(x=620, y=230)

        tk.Label(self.frame_prestamo_libros, text="Fecha de Devolución Estimada:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=370, y=270)
        self.fecha_devolucion_entry = DateEntry(self.frame_prestamo_libros,font=("Trebuchet MS", 12),width=35,date_pattern="yyyy-mm-dd",state="normal")
        self.fecha_devolucion_entry.place(x=620, y=270)

        volver_boton = tk.Button(self.frame_prestamo_libros,text="Volver",width=10,height=2,font=("Trebuchet MS", 12),bg="#E9F98B",command=self.volver_inicio)
        volver_boton.place(x=500, y=350)

        registrar_boton = tk.Button(self.frame_prestamo_libros,text="Registrar",width=10,height=2,font=("Trebuchet MS", 12),bg="orange",command=self.registrar_prestamo)
        registrar_boton.place(x=620, y=350)

        cerrar_boton = tk.Button(self.frame_prestamo_libros,text="Cerrar",width=10,height=2,font=("Trebuchet MS", 12),bg="maroon",fg="white",command=self.root.quit)
        cerrar_boton.place(x=740, y=350)

    # Registra un nuevo préstamo en el sistema
    def registrar_prestamo(self):
        usuario_seleccionado = self.usuario_combobox.get()
        libro_seleccionado = self.libro_combobox.get()
        fecha_devolucion = self.fecha_devolucion_entry.get_date().strftime("%Y-%m-%d")

        if not usuario_seleccionado or not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        usuario_id = int(usuario_seleccionado.split(" - ")[0])
        codigo_isbn = libro_seleccionado[1:18]

        prestamo_factory = PrestamoFactory()
        prestamo = prestamo_factory.factory_method(usuario_id, codigo_isbn, fecha_devolucion)
        
        try:
            prestamo.guardar()
            messagebox.showinfo("Registro", "Préstamo registrado correctamente.")
            self.usuario_combobox.set('')
            self.libro_combobox.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo: {e}")

    # Muestra la interfaz de devolución de libros
    def mostrar_devolucion_libros(self):
        self.ocultar_inicio()

        self.frame_devolucion_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_devolucion_libros.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_devolucion_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_devolucion_libros, text="Devolución de Libros", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0" )
        titulo_label.place(x=600, y=50)

        instruccion_label = tk.Label(self.frame_devolucion_libros, text="Seleccione un Préstamo Activo para Devolver", font=("Trebuchet MS", 12), bg="#f0f0f0")
        instruccion_label.place(x=530, y=150)

        self.tabla_prestamos = ttk.Treeview(self.frame_devolucion_libros, columns=("ID", "Usuario", "Libro"), show="headings", height=10)
        self.tabla_prestamos.heading("ID", text="ID")
        self.tabla_prestamos.heading("Usuario", text="Nombre Persona")
        self.tabla_prestamos.heading("Libro", text="Nombre Libro")
        self.tabla_prestamos.column("ID", width=100, anchor="center")
        self.tabla_prestamos.column("Usuario", width=200, anchor="center")
        self.tabla_prestamos.column("Libro", width=200, anchor="center")
        self.tabla_prestamos.place(x=450, y=200)
        self.tabla_prestamos.place(x=450, y=200)

        prestamos_activos = Prestamo.listar_prestamos_activos()
        for prestamo in prestamos_activos:
            self.tabla_prestamos.insert("", tk.END, values=prestamo)

        volver_boton = tk.Button(self.frame_devolucion_libros, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=500)

        devolver_boton = tk.Button(self.frame_devolucion_libros, text="Devolver", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.devolver_prestamo)
        devolver_boton.place(x=620, y=500)

        cerrar_boton = tk.Button(self.frame_devolucion_libros, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=500)

    # Registra la devolución del libro en el sistema
    def devolver_prestamo(self):
        """ (estado 'Finalizado')."""
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

    # Muestra la interfaz de consulta de disponibilidad
    def mostrar_consulta_disponibilidad(self):
        self.ocultar_inicio()

        self.frame_consulta_disponibilidad = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_consulta_disponibilidad.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_consulta_disponibilidad, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=380, y=20)

        titulo_label = tk.Label(self.frame_consulta_disponibilidad, text="Consulta de Disponibilidad de Libros", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=520, y=50)

        tk.Label(self.frame_consulta_disponibilidad, text="Selecciona el Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=150)

        libros = Libro.listar_libros()
        self.libro_combobox = ttk.Combobox(self.frame_consulta_disponibilidad,values=[f"{libro[0]} - {libro[1]}" for libro in libros],font=("Trebuchet MS", 12),width=40,state="readonly")
        self.libro_combobox.place(x=630, y=150)

        consultar_boton = tk.Button(self.frame_consulta_disponibilidad, text="Consultar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.consultar_disponibilidad_libro)
        consultar_boton.place(x=620, y=350)

        self.resultado_label = tk.Label(self.frame_consulta_disponibilidad, text="", font=("Trebuchet MS", 12), bg="#f0f0f0")
        self.resultado_label.place(x=550, y=250)

        volver_boton = tk.Button(self.frame_consulta_disponibilidad, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=350)

        cerrar_boton = tk.Button(self.frame_consulta_disponibilidad, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=350)

    # Consulta y muestra la disponibilidad de un libro seleccionado
    def consultar_disponibilidad_libro(self):
        libro_seleccionado = self.libro_combobox.get()

        if not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un libro para consultar su disponibilidad.")
            return

        codigo_isbn = libro_seleccionado.split(" - ")[0]

        cantidad_disponible = Libro.consultar_disponibilidad(codigo_isbn)
        self.resultado_label.config(text=f"Disponibilidad: {cantidad_disponible} ejemplares.")

    # Muestra la interfaz de reserva de libros
    def mostrar_reserva_libros(self):
        self.ocultar_inicio() 

        self.frame_reserva_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_reserva_libros.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5) 
        self.logo_label_small = tk.Label(self.frame_reserva_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small 
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_reserva_libros,text="Reserva de Libros",font=("Trebuchet MS", 20, "bold"),bg="#f0f0f0")
        titulo_label.place(x=600, y=50)

        libros_no_disponibles = Libro.listar_libros("no_disponibles")

        if libros_no_disponibles:
            tk.Label(self.frame_reserva_libros, text="Selecciona el Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=150)
            usuarios = Usuario.listar_usuarios()
            self.usuario_combobox = ttk.Combobox(self.frame_reserva_libros,values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios],font=("Trebuchet MS", 12),width=30,state="readonly")
            self.usuario_combobox.place(x=630, y=150)

            tk.Label(self.frame_reserva_libros, text="Selecciona el Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=450, y=190)
            self.libro_combobox = ttk.Combobox(self.frame_reserva_libros,values=[f"{libro[0]} - {libro[1]}" for libro in libros_no_disponibles],font=("Trebuchet MS", 12),width=30,state="readonly")
            self.libro_combobox.place(x=630, y=190)

            self.reservar_boton = tk.Button(self.frame_reserva_libros, text="Reservar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.reservar_libro)
            self.reservar_boton.place(x=620, y=320)

        else:
            tk.Label(self.frame_reserva_libros,text="Todos los libros están disponibles. No se pueden realizar reservas.", font=("Trebuchet MS", 12, "italic"),bg="#f0f0f0").place(x=450, y=200)

        volver_boton = tk.Button(self.frame_reserva_libros,text="Volver",width=10,height=2,font=("Trebuchet MS", 12),bg="#E9F98B",command=self.volver_inicio)
        volver_boton.place(x=500, y=320)

        cerrar_boton = tk.Button(self.frame_reserva_libros,text="Cerrar",width=10,height=2,font=("Trebuchet MS", 12),bg="maroon",fg="white",command=self.root.quit)
        cerrar_boton.place(x=740, y=320)
    
    # Registra una reserva de libro en el sistema
    def reservar_libro(self):
        usuario_seleccionado = self.usuario_combobox.get()
        libro_seleccionado = self.libro_combobox.get()

        if not usuario_seleccionado or not libro_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        usuario_id = int(usuario_seleccionado.split(" - ")[0])
        codigo_isbn = libro_seleccionado.split(" - ")[0]

        reserva_factory = ReservaFactory()
        reserva = reserva_factory.factory_method(usuario_id, codigo_isbn)

        try:
            reserva.guardar() 
            messagebox.showinfo("Reserva", "Reserva registrada correctamente.")
            self.usuario_combobox.set('')
            self.libro_combobox.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la reserva: {e}")

    # Muestra la interfaz de baja de libros
    def mostrar_baja_libros(self):
        self.ocultar_inicio()

        self.frame_baja_libros = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_baja_libros.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_baja_libros, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small 
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_baja_libros, text="Baja de Libros", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=600, y=50)

        tk.Label(self.frame_baja_libros, text="Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=565, y=150)
        # Modified: Only get books with available copies
        libros = [libro for libro in Libro.listar_libros() if Libro.consultar_disponibilidad(libro[0]) > 0]
        if not libros:
            mensaje_label = tk.Label(self.frame_baja_libros, 
                                text="No hay libros disponibles para dar de baja", 
                                font=("Trebuchet MS", 12, "italic"), 
                                bg="#f0f0f0")
            mensaje_label.place(x=650, y=150)
        else:
            self.libro_combobox = ttk.Combobox(
                self.frame_baja_libros,
                values=[f"({libro[0]}) - {libro[1]}" for libro in libros],
                font=("Trebuchet MS", 12),
                width=35,
                state="readonly"
            )
            self.libro_combobox.place(x=650, y=150)

        tk.Label(self.frame_baja_libros, text="Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=550, y=190)
        usuarios = Usuario.listar_usuarios()
        self.usuario_combobox = ttk.Combobox(self.frame_baja_libros,values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios],font=("Trebuchet MS", 12),width=22,state="readonly")
        self.usuario_combobox.place(x=650, y=190)

        tk.Label(self.frame_baja_libros, text="Motivo de la Baja:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=475, y=230)
        self.motivo_combobox = ttk.Combobox(self.frame_baja_libros,values=["Dañado", "Perdido"],font=("Trebuchet MS", 12),width=22,state="readonly")
        self.motivo_combobox.place(x=650, y=230)

        fecha_baja = datetime.now().strftime("%Y-%m-%d")
        tk.Label(self.frame_baja_libros, text="Fecha de Baja:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=500, y=270)
        fecha_baja_label = tk.Label(self.frame_baja_libros, text=fecha_baja, font=("Trebuchet MS", 12), bg="#f0f0f0")
        fecha_baja_label.place(x=650, y=270)

        volver_boton = tk.Button(self.frame_baja_libros, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=350)

        registrar_boton = tk.Button(self.frame_baja_libros, text="Registrar", width=10, height=2, font=("Trebuchet MS", 12), bg="orange", command=self.registrar_baja)
        registrar_boton.place(x=620, y=350)

        cerrar_boton = tk.Button(self.frame_baja_libros, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=740, y=350)

    # Registrar la baja de un libro en el sistema
    def registrar_baja(self):
        libro_seleccionado = self.libro_combobox.get()
        usuario_seleccionado = self.usuario_combobox.get()
        motivo_seleccionado = self.motivo_combobox.get().lower()

        if not libro_seleccionado or not motivo_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos obligatorios.")
            return

        libro_isbn = libro_seleccionado.split(" ")[0].strip("()") 
        usuario_id = usuario_seleccionado.split(" - ")[0] if usuario_seleccionado else None

        libro = Libro.obtener_libro_por_isbn(libro_isbn)

        if libro is not None:
            libro.dar_de_baja(motivo_seleccionado, usuario_id)
            messagebox.showinfo("Éxito", "La baja del libro se ha registrado correctamente.")

            self.libro_combobox.set('')
            self.usuario_combobox.set('')
            self.motivo_combobox.set('')
        else:
            messagebox.showerror("Error", "No se pudo encontrar el libro para dar de baja.")

    # Muestra la interfaz de registro de donaciones
    def mostrar_registro_donaciones(self):
        self.ocultar_inicio()

        self.frame_donaciones = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_donaciones.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5)
        self.logo_label_small = tk.Label(self.frame_donaciones, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=450, y=20)

        titulo_label = tk.Label(self.frame_donaciones, text="Registro de Donación", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=570, y=50)

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        tk.Label(self.frame_donaciones, text="Fecha:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=563, y=140)
        tk.Label(self.frame_donaciones, text=fecha_actual, font=("Trebuchet MS", 12), bg="#f0f0f0", fg="black").place(x=650, y=140)

        tk.Label(self.frame_donaciones, text="Tipo de Donación:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=480, y=260)
        self.tipo_donacion_combobox = ttk.Combobox(self.frame_donaciones, values=["Usuario", "Institución"], font=("Trebuchet MS", 12), width=22, state="readonly")
        self.tipo_donacion_combobox.place(x=650, y=260)
        self.tipo_donacion_combobox.bind("<<ComboboxSelected>>", self.mostrar_campo_donante)

        self.nombre_institucion_entry = tk.Entry(self.frame_donaciones, font=("Trebuchet MS", 12), width=25)
        self.institucion_label = tk.Label(self.frame_donaciones, text="Nombre Institución:", font=("Trebuchet MS", 12), bg="#f0f0f0")

        usuarios = Usuario.listar_usuarios()
        self.usuario_combobox = ttk.Combobox(self.frame_donaciones, values=[f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios], font=("Trebuchet MS", 12), width=22, state="readonly")
        self.usuarios_label = tk.Label(self.frame_donaciones, text="Usuario:", font=("Trebuchet MS", 12), bg="#f0f0f0")

        tk.Label(self.frame_donaciones, text="Libro:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=565, y=180)
        libros = Libro.listar_libros()
        self.libro_combobox = ttk.Combobox(self.frame_donaciones, values=[f"{libro[0]} - {libro[1]}" for libro in libros], font=("Trebuchet MS", 12), width=35, state="readonly")
        self.libro_combobox.place(x=650, y=180)

        tk.Label(self.frame_donaciones, text="Cantidad Donada:", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=485, y=220)
        self.cantidad_entry = tk.Entry(self.frame_donaciones, font=("Trebuchet MS", 12), width=15, validate="key", validatecommand=(self.root.register(self.validar_numerico), "%P"))
        self.cantidad_entry.place(x=650, y=220)

        guardar_boton = tk.Button(self.frame_donaciones, text="Registrar Donación", width=15, height=2, font=("Trebuchet MS", 12), bg="orange", command=lambda: self.registrar_donacion())
        guardar_boton.place(x=620, y=360)

        volver_boton = tk.Button(self.frame_donaciones, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=500, y=360)

        cerrar_boton = tk.Button(self.frame_donaciones, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=780, y=360)

    # Muestra los campos según el tipo de donación
    def mostrar_campo_donante(self, event=None):
        if self.tipo_donacion_combobox.get() == "Institución":
            self.institucion_label.place(x=470, y=300)
            self.nombre_institucion_entry.place(x=650, y=300)
            self.usuarios_label.place_forget()
            self.usuario_combobox.place_forget()
        else:
            self.usuarios_label.place(x=550, y=300)
            self.usuario_combobox.place(x=650, y=300)
            self.institucion_label.place_forget()
            self.nombre_institucion_entry.place_forget()

    # Registra una donación en el sistema
    def registrar_donacion(self):
        tipo_donacion = self.tipo_donacion_combobox.get()
        nombre_institucion = self.nombre_institucion_entry.get() if tipo_donacion == "Institución" else None
        usuario = self.usuario_combobox.get() if tipo_donacion == "Usuario" else None
        libro = self.libro_combobox.get()
        cantidad = self.cantidad_entry.get()

        if not tipo_donacion or not libro or not cantidad or (not usuario and not nombre_institucion):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuario_id = int(usuario.split(" - ")[0]) if usuario else None
        codigo_isbn = libro.split(" - ")[0] if libro else None

        donacion_factory = DonacionFactory()
        donacion = donacion_factory.factory_method(tipo_donacion, nombre_institucion, usuario_id, codigo_isbn, int(cantidad))

        donacion.guardar()
        messagebox.showinfo("Éxito", "Donación registrada correctamente.")

        self.tipo_donacion_combobox.set('')
        self.nombre_institucion_entry.delete(0, tk.END)
        self.usuario_combobox.set('')
        self.libro_combobox.set('')
        self.cantidad_entry.delete(0, tk.END)

    # Muestra la interfaz de reportes
    def mostrar_reportes(self):
        self.ocultar_inicio()

        self.frame_reportes = tk.Frame(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg="#f0f0f0")
        self.frame_reportes.pack(fill="both", expand=True)

        logo_path = os.path.join("recursos", "logo.png")
        logo_image_small = PhotoImage(file=logo_path).subsample(5) 
        self.logo_label_small = tk.Label(self.frame_reportes, image=logo_image_small, bg="#f0f0f0")
        self.logo_label_small.image = logo_image_small
        self.logo_label_small.place(x=480, y=20)

        titulo_label = tk.Label(self.frame_reportes, text="Reportes de Biblioteca", font=("Trebuchet MS", 20, "bold"), bg="#f0f0f0")
        titulo_label.place(x=600, y=50)

        reportes = [
            ("Préstamos Vencidos", self.generar_reporte_prestamos_vencidos),
            ("Libros Más Prestados Último Mes", self.generar_reporte_libros_mas_prestados),
            ("Usuarios con Más Préstamos", self.generar_reporte_usuarios_mas_prestamos),
            ("Libros por Autor", self.generar_reporte_libros_por_autor),
            ("Usuarios con Penalizaciones", self.generar_reporte_usuarios_penalizados),
            ("Estadísticas de Donaciones", self.mostrar_reporte_donaciones)
        ]

        y_offset = 150 
        for i, (text, command) in enumerate(reportes):
            boton_reporte = tk.Button(self.frame_reportes, text=text, width=30, height=2, font=("Trebuchet MS", 12), bg="orange", command=command)
            boton_reporte.place(x=100, y=y_offset + i * 80)

        volver_boton = tk.Button(self.frame_reportes, text="Volver", width=10, height=2, font=("Trebuchet MS", 12), bg="#E9F98B", command=self.volver_inicio)
        volver_boton.place(x=700, y=600)

        self.boton_grafico = tk.Button(self.frame_reportes, text="Grafico", width=10, height=2, font=("Trebuchet MS", 12), bg="orange")

        cerrar_boton = tk.Button(self.frame_reportes, text="Cerrar", width=10, height=2, font=("Trebuchet MS", 12), bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.place(x=1000, y=600)

    # Crea o limpia el área de visualización del reporte
    def mostrar_area_reporte(self):
        if hasattr(self, 'frame_reporte'):
            for widget in self.frame_reporte.winfo_children():
                widget.destroy()
        else:
            self.frame_reporte = tk.Frame(self.frame_reportes, width=2000, height=400, bg="#f0f0f0")
            self.frame_reporte.place(x=400, y=150)

    # Genera y muestra el reporte de préstamos vencidos
    def generar_reporte_prestamos_vencidos(self):
        self.mostrar_area_reporte()
        self.boton_grafico.place_forget()

        prestamos_vencidos = Prestamo.obtener_prestamos_vencidos()

        if not prestamos_vencidos:
            tk.Label(self.frame_reporte, text="No hay préstamos vencidos.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Préstamos Vencidos", font=("Trebuchet MS", 16, "bold"),bg="#f0f0f0")
        titulo_label.place(x=350, y=10)

        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Vencimiento"), show="headings")
        tabla_reporte.heading("ID", text="ID Préstamo")
        tabla_reporte.heading("Usuario", text="Usuario")
        tabla_reporte.heading("Libro", text="Libro")
        tabla_reporte.heading("Fecha Préstamo", text="Fecha Préstamo")
        tabla_reporte.heading("Fecha Vencimiento", text="Fecha Vencimiento")

        for col in ("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Vencimiento"):
            tabla_reporte.column(col, width=150, anchor="center")

        tabla_reporte.place(x=120, y=50, width=750, height=300)

        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=870, y=50, height=300) 

        for prestamo in prestamos_vencidos:
            tabla_reporte.insert("", tk.END, values=(prestamo[0], prestamo[1], prestamo[2], prestamo[3], prestamo[4]))

    # Genera y muestra el reporte de libros más prestados
    def generar_reporte_libros_mas_prestados(self):
        self.mostrar_area_reporte()
        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Libros Más Prestados en el Último Mes", font=("Trebuchet MS", 16, "bold"), bg="#f0f0f0")
        titulo_label.place(x=250, y=10)

        libros_mas_prestados = Prestamo.obtener_libros_mas_prestados()
        if not libros_mas_prestados:
            tk.Label(self.frame_reporte, text="No hay préstamos en el último mes.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        self.tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Título", "Total Préstamos"), show="headings")
        self.tabla_reporte.heading("ID", text="ID Libro")
        self.tabla_reporte.heading("Título", text="Título")
        self.tabla_reporte.heading("Total Préstamos", text="Total Préstamos")
        for col in ("ID", "Título", "Total Préstamos"):
            self.tabla_reporte.column(col, width=250, anchor="center")
        self.tabla_reporte.place(x=120, y=50, width=750, height=300)
        self.scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=self.tabla_reporte.yview)
        self.tabla_reporte.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(x=870, y=50, height=300)

        for libro in libros_mas_prestados:
            self.tabla_reporte.insert("", tk.END, values=(libro[0], libro[1], libro[2]))

        self.boton_grafico .config(text="Grafico", command=lambda: self.alternar_reporte_libros_mas_prestados(libros_mas_prestados))
        self.boton_grafico.place(x=850, y=600)

    # Alternar entre la tabla y el gráfico
    def alternar_reporte_libros_mas_prestados(self, libros_mas_prestados):
        
        if self.boton_grafico["text"] == "Grafico":
            self.tabla_reporte.place_forget()
            self.scroll_y.place_forget()
            self.boton_grafico.config(text="Tabla")
            
            titulos = [libro[1] for libro in libros_mas_prestados]
            total_prestamos = [libro[2] for libro in libros_mas_prestados]
            
            fig, ax = plt.subplots()
            fig.set_size_inches(10, 4)
            ax.bar(titulos, total_prestamos)
            ax.set_ylabel("Total Préstamos")
            plt.xticks(rotation=45, ha="right", fontsize=8)
            fig.subplots_adjust(bottom=0.4)
            
            # Canvas para el gráfico en Tkinter
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_reporte)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(x=120, y=50, width=750, height=350)
        else:
            # Volver a mostrar la tabla y ocultar gráfico
            self.canvas.get_tk_widget().place_forget()
            self.tabla_reporte.place(x=120, y=50, width=750, height=300)
            self.boton_grafico.config(text="Grafico")

    # Genera y muestra el reporte de usuarios con más préstamos
    def generar_reporte_usuarios_mas_prestamos(self):
        self.mostrar_area_reporte()
        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Usuarios con Más Préstamos en el Último Mes", font=("Trebuchet MS", 16, "bold"), bg="#f0f0f0")
        titulo_label.place(x=230, y=10)

        usuarios_mas_prestamos = Prestamo.obtener_usuarios_mas_prestamos()
        if not usuarios_mas_prestamos:
            tk.Label(self.frame_reporte, text="No hay usuarios con préstamos en el último mes.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        self.tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("ID", "Nombre", "Apellido", "Total Préstamos"), show="headings")
        self.tabla_reporte.heading("ID", text="ID Usuario")
        self.tabla_reporte.heading("Nombre", text="Nombre")
        self.tabla_reporte.heading("Apellido", text="Apellido")
        self.tabla_reporte.heading("Total Préstamos", text="Total Préstamos")

        for col in ("ID", "Nombre", "Apellido", "Total Préstamos"):
            self.tabla_reporte.column(col, width=175, anchor="center")

        self.tabla_reporte.place(x=120, y=50, width=750, height=300)
        self.scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=self.tabla_reporte.yview)
        self.tabla_reporte.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(x=870, y=50, height=300)

        for usuario in usuarios_mas_prestamos:
            self.tabla_reporte.insert("", tk.END, values=(usuario[0], usuario[1], usuario[2], usuario[3]))

        self.boton_grafico.config(text="Grafico", command=lambda: self.alternar_reporte_usuarios_mas_prestamos(usuarios_mas_prestamos))
        self.boton_grafico.place(x=850, y=600)

    # Alternar entre tabla y gráfico
    def alternar_reporte_usuarios_mas_prestamos(self, usuarios_mas_prestamos):
        if self.boton_grafico["text"] == "Grafico":
            self.tabla_reporte.place_forget()
            self.scroll_y.place_forget()
            self.boton_grafico.config(text="Tabla")

            nombres_completos = [f"{usuario[1]} {usuario[2]}" for usuario in usuarios_mas_prestamos]
            total_prestamos = [usuario[3] for usuario in usuarios_mas_prestamos]

            fig, ax = plt.subplots()
            fig.set_size_inches(10, 4)
            ax.bar(nombres_completos, total_prestamos)
            ax.set_ylabel("Total Préstamos")
            plt.xticks(rotation=45, ha="right", fontsize=8)
            fig.subplots_adjust(bottom=0.4)

            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_reporte)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(x=120, y=50, width=750, height=350)
        else:
            self.canvas.get_tk_widget().place_forget()
            self.tabla_reporte.place(x=120, y=50, width=750, height=300)
            self.scroll_y.place(x=870, y=50, height=300)
            self.boton_grafico.config(text="Grafico")

    # Genera y muestra el reporte de libros por autor
    def generar_reporte_libros_por_autor(self):

        self.mostrar_area_reporte()
        self.boton_grafico.place_forget()

        libros_por_autor = Libro.obtener_libros_por_autor() 

        if not libros_por_autor:
            tk.Label(self.frame_reporte, text="No hay libros disponibles.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Libros por Autor", font=("Trebuchet MS", 16, "bold"),bg="#f0f0f0")
        titulo_label.place(x=320, y=10)

        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("Autor", "Cantidad Libros", "Total Disponibles"), show="headings")
        tabla_reporte.heading("Autor", text="Autor")
        tabla_reporte.heading("Cantidad Libros", text="Cantidad de Libros")
        tabla_reporte.heading("Total Disponibles", text="Total Disponibles")

        for col in ("Autor", "Cantidad Libros", "Total Disponibles"):
            tabla_reporte.column(col, width=250, anchor="center")

        tabla_reporte.place(x=120, y=50, width=750, height=300)

        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=870, y=50, height=300)

        for autor in libros_por_autor:
            tabla_reporte.insert("", tk.END, values=(autor[0], autor[1], autor[2]))

    # Genera y muestra el reporte de usuarios con penalizaciones
    def generar_reporte_usuarios_penalizados(self):

        self.mostrar_area_reporte()
        self.boton_grafico.place_forget()

        penalizaciones = Usuario.obtener_usuarios_con_penalizaciones()

        if not penalizaciones:
            tk.Label(self.frame_reporte, text="No hay usuarios con penalizaciones.", font=("Trebuchet MS", 12), bg="#f0f0f0").place(x=10, y=10)
            return

        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Usuarios con Penalizaciones", font=("Trebuchet MS", 16, "bold"),bg="#f0f0f0")
        titulo_label.place(x=300, y=10)

        tabla_reporte = ttk.Treeview(self.frame_reporte, columns=("Nombre", "Apellido", "Monto", "Motivo"), show="headings")
        tabla_reporte.heading("Nombre", text="Nombre")
        tabla_reporte.heading("Apellido", text="Apellido")
        tabla_reporte.heading("Monto", text="Monto")
        tabla_reporte.heading("Motivo", text="Motivo")

        tabla_reporte.column("Nombre", width=175, anchor="center")
        tabla_reporte.column("Apellido", width=175, anchor="center")
        tabla_reporte.column("Monto", width=125, anchor="center")
        tabla_reporte.column("Motivo", width=225, anchor="center")

        tabla_reporte.place(x=120, y=50, width=750, height=300)

        scroll_y = tk.Scrollbar(self.frame_reporte, orient="vertical", command=tabla_reporte.yview)
        tabla_reporte.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=870, y=50, height=300) 

        for penalizacion in penalizaciones:
            tabla_reporte.insert("", tk.END, values=(penalizacion[0], penalizacion[1], penalizacion[2], penalizacion[3]))

    # Muestra la interfaz del reporte de donaciones
    def mostrar_reporte_donaciones(self):
        self.tabla_donaciones = False
        self.mostrar_area_reporte()

        titulo_label = tk.Label(self.frame_reporte, text="Reporte de Donaciones en el Periodo", font=("Trebuchet MS", 16, "bold"), bg="#f0f0f0")
        titulo_label.place(x=275, y=10)

        self.fecha_desde_label = tk.Label(self.frame_reporte, text="Fecha Desde:", font=("Trebuchet MS", 12), bg="#f0f0f0")
        self.fecha_desde_label.place(x=150, y=60)
        self.fecha_desde_entry = DateEntry(self.frame_reporte, width=12, font=("Trebuchet MS", 12), date_pattern="yyyy-mm-dd")
        self.fecha_desde_entry.place(x=250, y=60)

        self.fecha_hasta_label = tk.Label(self.frame_reporte, text="Fecha Hasta:", font=("Trebuchet MS", 12), bg="#f0f0f0")
        self.fecha_hasta_label.place(x=400, y=60)
        self.fecha_hasta_entry = DateEntry(self.frame_reporte, width=12, font=("Trebuchet MS", 12), date_pattern="yyyy-mm-dd")
        self.fecha_hasta_entry.place(x=500, y=60)

        self.boton_generar_don = tk.Button(self.frame_reporte, text="Generar Reporte", command=self.generar_reporte_donacion, font=("Trebuchet MS", 12), bg="#988152")
        self.boton_generar_don.place(x=650, y=55)

        self.boton_grafico.config(text="Grafico", command=self.alternar_reporte_donaciones)
        self.boton_grafico.place(x=850, y=600)

    # Genera el reporte de donaciones y muestra la tabla
    def generar_reporte_donacion(self):
        fecha_desde = self.fecha_desde_entry.get_date().strftime("%Y-%m-%d")
        fecha_hasta = self.fecha_hasta_entry.get_date().strftime("%Y-%m-%d")

        self.donaciones = Donacion.obtener_donaciones_por_periodo(fecha_desde, fecha_hasta)

        if not self.donaciones:
            messagebox.showinfo("Reporte de Donaciones", "No se encontraron donaciones en el periodo seleccionado.")
            return

        columnas = ("ID", "Institución/Usuario", "ISBN", "Fecha", "Cantidad")
        self.tabla_reporte_donaciones = ttk.Treeview(self.frame_reporte, columns=columnas, show="headings")

        for col in columnas:
            self.tabla_reporte_donaciones.heading(col, text=col)
            self.tabla_reporte_donaciones.column(col, width=150, anchor="center")

        self.tabla_reporte_donaciones.place(x=120, y=120, width=750, height=280)

        self.scroll_y_donaciones = tk.Scrollbar(self.frame_reporte, orient="vertical", command=self.tabla_reporte_donaciones.yview)
        self.tabla_reporte_donaciones.configure(yscrollcommand=self.scroll_y_donaciones.set)
        self.scroll_y_donaciones.place(x=870, y=120, height=280)

        for donacion in self.donaciones:
            self.tabla_reporte_donaciones.insert("", "end", values=(donacion[0], donacion[1] if donacion[1] else donacion[2], donacion[3], donacion[4], donacion[5]))
        
        self.tabla_donaciones = True

    # Alterna entre la vista de tabla y gráfico para el reporte de donaciones
    def alternar_reporte_donaciones(self):
        if self.boton_grafico["text"] == "Grafico":
            if self.tabla_donaciones:
                self.tabla_reporte_donaciones.place_forget()
                self.scroll_y_donaciones.place_forget()
            self.fecha_desde_label.place_forget()
            self.fecha_desde_entry.place_forget()
            self.fecha_hasta_label.place_forget()
            self.fecha_hasta_entry.place_forget()
            self.boton_generar_don.place_forget()
            self.boton_grafico.config(text="Tabla")

            meses, cantidad_donaciones = Donacion.obtener_donaciones_por_mes()

            if not meses or not cantidad_donaciones:
                messagebox.showinfo("Error", "No hay datos de donaciones para mostrar en el gráfico.")
                self.boton_grafico.config(text="Grafico")
                return

            fig, ax = plt.subplots()
            fig.set_size_inches(10, 7) 
            ax.plot(meses, cantidad_donaciones, marker="o", linestyle="-")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Cantidad de Donaciones")
            ax.set_title("Donaciones en los Últimos 12 Meses")
            
            plt.xticks(rotation=45, ha="right", fontsize=8)
            
            fig.subplots_adjust(bottom=0.4)

            max_donaciones = max(cantidad_donaciones) if cantidad_donaciones else 0
            ax.set_ylim(0, max_donaciones * 1.2)

            for i, txt in enumerate(cantidad_donaciones):
                ax.annotate(txt, (meses[i], cantidad_donaciones[i]), textcoords="offset points", xytext=(0,5), ha="center", fontsize=8)

            self.canvas_donaciones = FigureCanvasTkAgg(fig, master=self.frame_reporte)
            self.canvas_donaciones.draw()
            self.canvas_donaciones.get_tk_widget().place(x=120, y=80, width=750, height=400)
        else:
            if hasattr(self, "canvas_donaciones"):
                self.canvas_donaciones.get_tk_widget().place_forget()
            if self.tabla_donaciones:
                self.tabla_reporte_donaciones.place(x=120, y=120, width=750, height=280)
                self.scroll_y_donaciones.place(x=870, y=120, height=280)
            self.fecha_desde_label.place(x=150, y=60)
            self.fecha_desde_entry.place(x=250, y=60)
            self.fecha_hasta_label.place(x=400, y=60)
            self.fecha_hasta_entry.place(x=500, y=60)
            self.boton_generar_don.place(x=650, y=55)
            self.boton_grafico.config(text="Grafico")

    # Permite solo entrada numérica
    def validar_numerico(self, texto):
        return texto.isdigit() or texto == ""
    
    # Valida que el ISBN cumpla con el formato ISBN-13 con guiones
    def validar_isbn(self, isbn):
        pattern = r"^\d{3}-\d-\d{2}-\d{6}-\d$"
        return bool(re.match(pattern, isbn))
    
    def verificar_isbn_existente(self, event):
        isbn = self.isbn_entry.get()
        
        if Libro.existe_libro_con_isbn(isbn):
            libro = Libro.obtener_libro_por_isbn(isbn)
            if libro:
                self.titulo_entry.delete(0, tk.END)
                self.titulo_entry.insert(0, libro.titulo)
                
                self.genero_entry.delete(0, tk.END)
                self.genero_entry.insert(0, libro.genero)
                
                self.anio_publicacion_entry.delete(0, tk.END)
                self.anio_publicacion_entry.insert(0, libro.anio_publicacion)
                
                # Find and select the correct author in combobox
                autores = Autor.listar_autores()
                for i, autor in enumerate(autores):
                    if autor[0] == libro.autor_id:
                        self.autor_combobox.current(i)
                        break
                
                messagebox.showinfo("ISBN Existente", 
                                "Este libro ya existe en la base de datos. Los campos han sido autocompletados.")
