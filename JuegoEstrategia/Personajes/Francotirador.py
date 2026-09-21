class Francotirador(Personaje):
    def __init__(self, posicion, equipo):
        super().__init__('Francotirador', 3, 3, posicion, equipo)

    def habilidad(self):
        celda = input("Indica coordenadas de la celda a disparar: ").lower()
        if not validar_celda(celda):
            print("Coordenadas inválidas.")
            return None
        return f"F{celda}"