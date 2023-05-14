class Actividad:
    def __init__(self, titulo, descripcion, hora, prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.hora = hora
        self.prioridad = prioridad
        
    def toDBCollection(self):
        return{
            'titulo': self.titulo,
            'descripcion' : self.descripcion,
            'hora': self.hora,
            'prioridad' : self.prioridad
        }