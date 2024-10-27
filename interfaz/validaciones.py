def validar_campos_vacios(*args):
    """Verifica que ninguno de los argumentos sea una cadena vacía."""
    return all(arg.strip() != "" for arg in args)
