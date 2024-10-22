

class Libro():
    def __init__(self, codigo, titulo, anio, autor, cantidad):
        self.codigo = codigo
        self.titulo = titulo
        self.anio = anio
        self.autor = autor
        self.cantidad = cantidad

    def __str__(self):
        return (f"Libro: ISBN: {self.codigo_isbn}, Título: {self.titulo}, Género: {self.genero}, "
                f"Año: {self.anio}, Autor: {self.autor.nombre} {self.autor.apellido}, "
                f"Cantidad disponible: {self.cantidad_disponible}")