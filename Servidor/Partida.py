class Partida(threading.Thread):
    def __init__(self, jugador1, jugador2):
        super().__init__()
        self.j1 = jugador1
        self.j2 = jugador2
        self.turnos = 0

    def run(self):
        try:
            self.j1.conn.sendall(f"Oponente: {self.j2.nombre}\n".encode())
            self.j2.conn.sendall(f"Oponente: {self.j1.nombre}\n".encode())

            primero = random.choice([self.j1, self.j2])
            segundo = self.j2 if primero == self.j1 else self.j1
            primero.conn.sendall(b"TURNO:1")
            segundo.conn.sendall(b"TURNO:0")

            # Esperar que ambos jugadores confirmen estar listos
            self.j1.conn.recv(1024)
            self.j2.conn.recv(1024)

            activo, pasivo = primero, segundo
            while True:
                self.turnos += 1
                activo.conn.sendall(b"ES_TURNO")
                codigo = activo.conn.recv(1024).decode()
                pasivo.conn.sendall(codigo.encode())
                respuesta = pasivo.conn.recv(2048)
                activo.conn.sendall(respuesta)

                if b"FIN" in respuesta:
                    break

                activo, pasivo = pasivo, activo

            activo.conn.sendall(b"VICTORIA")
            pasivo.conn.sendall(b"DERROTA")

        except Exception as e:
            print(f"Error en la partida: {e}")
        finally:
            self.j1.conn.close()
            self.j2.conn.close()
