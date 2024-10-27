import tkinter as tk

from tkinter import messagebox
from validaciones import validar_campos_vacios

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("600x400")  # Tamaño de la ventana más grande

        # Título principal
        self.titulo_label = tk.Label(self.root, text="Sistema de Gestión de Biblioteca", font=("Helvetica", 18))
        self.titulo_label.pack(pady=20)

        # Frame inicial con botones
        self.frame_inicial = tk.Frame(self.root)
        self.frame_inicial.pack()

        # Definir los botones con las funcionalidades y propiedades de estilo
        botones = [
            ("Registro de Autores", self.mostrar_registro_autores),
            ("Registro de Libros", self.registro_libros),
            ("Registro de Usuarios", self.registro_usuarios),
            ("Préstamo de Libros", self.prestamo_libros),
            ("Devolución de Libros", self.devolucion_libros),
            ("Consulta de Disponibilidad", self.consulta_disponibilidad),
            ("Reserva de Libros", self.reserva_libros)
        ]

        # Crear botones en una cuadrícula de 3 columnas en el frame inicial
        for i, (text, command) in enumerate(botones):
            boton = tk.Button(self.frame_inicial, text=text, width=20, height=3, bg="orange", command=command)
            boton.grid(row=i//3, column=i%3, padx=10, pady=10)

        # Botón de cerrar centrado al final de la ventana
        self.cerrar_boton = tk.Button(self.root, text="Cerrar", width=20, height=3, bg="maroon", fg="white", command=self.root.quit)
        self.cerrar_boton.pack(pady=10)

    def mostrar_registro_autores(self):
        """Muestra la interfaz de registro de autores y oculta los elementos anteriores."""
        self.frame_inicial.pack_forget()  # Ocultar el frame inicial
        self.cerrar_boton.pack_forget()   # Ocultar el botón de cerrar

        # Frame de registro de autores
        self.frame_registro_autores = tk.Frame(self.root)
        self.frame_registro_autores.pack()

        # Campos de texto para el registro de autores
        self.nombre_entry = self.crear_campo(self.frame_registro_autores, "Nombre")
        self.apellido_entry = self.crear_campo(self.frame_registro_autores, "Apellido")
        self.nacionalidad_entry = self.crear_campo(self.frame_registro_autores, "Nacionalidad")

        # Botón de volver, registrar y cerrar dentro del frame de registro de autores, usando pack
        volver_boton = tk.Button(self.frame_registro_autores, text="Volver", width=10, height=2, command=self.volver_inicio)
        volver_boton.pack(side="left", padx=10, pady=10)

        registrar_boton = tk.Button(self.frame_registro_autores, text="Registrar", width=10, height=2, command=self.registrar_autor)
        registrar_boton.pack(side="left", padx=10, pady=10)

        cerrar_boton = tk.Button(self.frame_registro_autores, text="Cerrar", width=10, height=2, bg="maroon", fg="white", command=self.root.quit)
        cerrar_boton.pack(side="left", padx=10, pady=10)


    def crear_campo(self, frame, label_text):
        """Crea un campo de texto con una etiqueta en el frame proporcionado."""
        label = tk.Label(frame, text=label_text, font=("Helvetica", 12))
        label.pack(pady=5)
        
        entry = tk.Entry(frame, font=("Helvetica", 12), width=30)
        entry.pack(pady=5)
        
        return entry


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
        autor = autor_factory.factory_method(None, nombre, apellido, nacionalidad)
        
        try:
            autor.guardar()  # Llama al método guardar de la instancia de Autor
            messagebox.showinfo("Registro", "Autor registrado correctamente.")
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.nacionalidad_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el autor: {e}")

    def volver_inicio(self):
        """Vuelve a la pantalla de inicio y oculta el formulario de registro de autores."""
        self.frame_registro_autores.pack_forget()  # Ocultar el frame de registro de autores

        # Volver a mostrar el frame inicial y el botón de cerrar
        self.frame_inicial.pack()
        self.cerrar_boton.pack(pady=10)

    # Funciones de otras funcionalidades
    def registro_libros(self):
        messagebox.showinfo("Funcionalidad", "Registro de Libros: Permitir el registro de nuevos libros y asignarlos a un autor.")

    def registro_usuarios(self):
        messagebox.showinfo("Funcionalidad", "Registro de Usuarios: Permitir el registro de nuevos usuarios.")

    def prestamo_libros(self):
        messagebox.showinfo("Funcionalidad", "Préstamo de Libros: Asignar un libro a un usuario con la fecha de préstamo y una fecha de devolución estimada.")

    def devolucion_libros(self):
        messagebox.showinfo("Funcionalidad", "Devolución de Libros: Permitir registrar la devolución de un libro y verificar si está en condiciones.")

    def consulta_disponibilidad(self):
        messagebox.showinfo("Funcionalidad", "Consulta de Disponibilidad: Consultar la disponibilidad de un libro.")

    def reserva_libros(self):
        messagebox.showinfo("Funcionalidad", "Reserva de Libros: Permitir que los usuarios puedan reservar libros que actualmente no están disponibles y notificarlos cuando el libro esté disponible.")

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
