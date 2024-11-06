from db_management.db_manager import DatabaseManager
import tkinter as tk
from interfaz.biblioteca_app import BibliotecaApp
from models.Libro import Libro
def main():

    db_manager = DatabaseManager()
    

    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()

    db_manager.cerrar_conexion()


if __name__ == "__main__":
    main()
