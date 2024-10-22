class Usuario():
    TIPOS_VALIDOS = ['estudiante', 'profesor']
    def __init__(self, id, nombre, apellido, tipo, direccion, telefono):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de usuario inválido: {tipo}. Debe ser 'estudiante' o 'profesor'.")
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.tipo = tipo
        self.direccion = direccion
        self.telefono = telefono
        
    def __str__(self):
        return (f"Usuario: ID: {self.id}, Nombre: {self.nombre} {self.apellido}, Tipo: {self.tipo_usuario}, "
                f"Dirección: {self.direccion}, Teléfono: {self.telefono}")
        