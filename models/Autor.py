class Autor():
    def __init__(self, id, nombre, apellido, nacionalidad):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad
        
    def __str__(self):
        return f"Autor: ID: {self.id}, Nombre: {self.nombre} {self.apellido}, Nacionalidad: {self.nacionalidad}"