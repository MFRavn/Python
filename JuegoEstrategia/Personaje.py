# personaje.py
class Personaje:
    def __init__(self, nombre, vida_maxima, danyo, posicion, equipo):
        self.nombre = nombre
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima
        self.danyo = danyo
        self.posicion = posicion
        self.enfriamiento_restante = 0
        self.equipo = equipo

    def mover(self, nueva_pos):
        if validar_celda_contigua(self.posicion, nueva_pos) and comprobar_celda_disponible(nueva_pos, self.equipo):
            self.posicion = nueva_pos
        else:
            print("Movimiento inválido.")

    def habilidad(self):
        raise NotImplementedError



