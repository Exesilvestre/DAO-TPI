class Prestamo():
    def __init__(self, usuario, libro, fecha_prestamo, fecha_devolucion):
        self.id = id
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def __str__(self):
        devolucion_info = f", Fecha de devolución: {self.fecha_devolucion}" if self.fecha_devolucion else ""
        return (f"Préstamo: ID: {self.id}, Usuario: {self.usuario.nombre} {self.usuario.apellido}, "
                f"Libro: {self.libro.titulo}, Fecha de préstamo: {self.fecha_prestamo}{devolucion_info}")