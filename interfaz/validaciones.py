import os
import sys
# Añadir el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def validar_campos_vacios(*args):
    """Verifica que ninguno de los argumentos sea una cadena vacía."""
    return all(arg.strip() != "" for arg in args)
