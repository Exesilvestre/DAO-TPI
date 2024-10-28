from db_management.db_manager import DatabaseManager
from interfaz.biblioteca_app import crear_interfaz

def main():
    # Inicializar el manejador de base de datos
    db_manager = DatabaseManager()

    crear_interfaz()
    db_manager.cerrar_conexion()

if __name__ == "__main__":
    main()