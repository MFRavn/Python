class Artillero(Personaje):
    def __init__(self, posicion, equipo):
        super().__init__('Artillero', 2, 1, posicion, equipo)

    def habilidad(self):
        celda = input("Indica coordenadas (esquina sup. izq. del área 2x2): ").lower()
        if not validar_celda(celda):
            print("Coordenadas inválidas.")
            return None
        return f"A{celda}"