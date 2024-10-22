from db_management.db_manager import DatabaseManager

def main():
    # Inicializar el manejador de base de datos
    db_manager = DatabaseManager()

    db_manager.cerrar_conexion()

if __name__ == "__main__":
    main()