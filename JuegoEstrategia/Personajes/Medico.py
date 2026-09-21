class Medico(Personaje):
    def __init__(self, posicion, equipo):
        super().__init__('Medico', 1, 0, posicion, equipo)

    def habilidad(self):
        vivos = [p for p in self.equipo if p.vida_actual > 0 and p.vida_actual < p.vida_maxima]
        if not vivos:
            print("No hay compañeros a curar.")
            return None
        for i, p in enumerate(vivos):
            print(f"{i+1}: {p.nombre} [{p.vida_actual}/{p.vida_maxima}]")
        idx = int(input("Selecciona el personaje a curar: ")) - 1
        vivos[idx].vida_actual = vivos[idx].vida_maxima
        return None