# jugador.py
from personaje import Medico, Artillero, Francotirador, Inteligencia
from utils import validar_celda, comprobar_celda_disponible, limpiar_terminal

class Jugador:
    def __init__(self):
        self.equipo = []
        self.oponente = None
        self.informe = ""
        self.crear_equipo()
        self.posicionar_equipo()

    def set_oponente(self, enemigo):
        self.oponente = enemigo

    def crear_equipo(self):
        self.equipo = [
            Medico("", self.equipo),
            Artillero("", self.equipo),
            Francotirador("", self.equipo),
            Inteligencia("", self.equipo),
        ]

    def posicionar_equipo(self):
        print("Vamos a posicionar a nuestros personajes en el tablero!")
        for personaje in self.equipo:
            while True:
                celda = input(f"Indica la celda (A-D, 1-4. p.ej: B2) para {personaje.nombre}: ").lower()
                if not validar_celda(celda):
                    print("Ups... valor de celda incorrecto.")
                elif not comprobar_celda_disponible(celda, self.equipo):
                    print("Ups... la celda ya está ocupada!")
                else:
                    personaje.posicion = celda
                    break
        print("Posicionamiento terminado")

    def turno(self):
        if self.oponente.informe:
            print("---- INFORME ----")
            print(self.oponente.informe)

        print("\n---- SITUACION DEL EQUIPO ----")
        vivos = [p for p in self.equipo if p.vida_actual > 0]
        for p in vivos:
            print(f"{p.nombre} está en {p.posicion.upper()} [Vida {p.vida_actual}/{p.vida_maxima}]")

        opciones = []
        for i, p in enumerate(vivos):
            opciones.append((p, 'mover'))
            if p.enfriamiento_restante == 0:
                opciones.append((p, 'habilidad'))

        for i, (p, acc) in enumerate(opciones):
            if acc == 'mover':
                print(f"{i+1}: Mover ({p.nombre})")
            elif acc == 'habilidad':
                desc = p.habilidad.__doc__ or "Usar habilidad"
                print(f"{i+1}: {desc.strip()} ({p.nombre})")

        idx = int(input("Selecciona la acción de este turno: ")) - 1
        personaje, accion = opciones[idx]
        if accion == 'mover':
            nueva = input(f"Indica la celda a la que mover a {personaje.nombre} (Posición actual: {personaje.posicion.upper()}): ").lower()
            personaje.mover(nueva)
            return False
        elif accion == 'habilidad':
            codigo = personaje.habilidad()
            personaje.enfriamiento_restante = 1
            resultado = self.oponente.recibir_accion(codigo)
            self.informe = resultado['informe'] if resultado else "Nada que reportar"
            return resultado['fin'] if resultado else False

    def recibir_accion(self, codigo):
        if not codigo:
            return None
        inicial, celda = codigo[0], codigo[1:]
        afectados = []

        if inicial == 'I':
            col = ord(celda[0]) - ord('a')
            row = int(celda[1]) - 1
            for p in self.equipo:
                if p.vida_actual > 0:
                    c = p.posicion
                    c_col = ord(c[0]) - ord('a')
                    c_row = int(c[1]) - 1
                    if col <= c_col < col+2 and row <= c_row < row+2:
                        afectados.append(f"{p.nombre} ha sido avistado en {p.posicion.upper()}")
            return {'informe': '\n'.join(afectados) or "Ningún personaje ha sido revelado", 'fin': False}

        elif inicial in ['A', 'F']:
            if inicial == 'A':
                col = ord(celda[0]) - ord('a')
                row = int(celda[1]) - 1
                for p in self.equipo:
                    if p.vida_actual > 0:
                        c = p.posicion
                        c_col = ord(c[0]) - ord('a')
                        c_row = int(c[1]) - 1
                        if col <= c_col < col+2 and row <= c_row < row+2:
                            p.vida_actual -= 1
                            texto = f"{p.nombre} ha sido herido en {p.posicion.upper()} [Vida restante: {p.vida_actual}]"
                            if p.vida_actual <= 0:
                                texto = f"{p.nombre} ha sido eliminado"
                            afectados.append(texto)
            else:
                for p in self.equipo:
                    if p.posicion == celda and p.vida_actual > 0:
                        p.vida_actual = 0
                        afectados.append(f"{p.nombre} ha sido eliminado")

            vivos = [p for p in self.equipo if p.vida_actual > 0 and p.nombre in ["Francotirador", "Artillero"]]
            fin = len(vivos) == 0
            return {'informe': '\n'.join(afectados) or "Ningún personaje ha sido herido", 'fin': fin}