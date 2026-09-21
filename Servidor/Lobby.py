class Lobby:
    def __init__(self):
        self.espera = []
        self.lock = threading.Lock()

    def agregar(self, cliente):
        with self.lock:
            self.espera.append(cliente)

    def emparejar(self):
        with self.lock:
            if len(self.espera) >= 2:
                return self.espera.pop(0), self.espera.pop(0)
            return None

def manejar_cliente(conn, addr, lobby):
    try:
        conn.sendall(b"Dime tu nombre: ")
        nombre = conn.recv(1024).decode().strip()
        cliente = Cliente(nombre, conn)
        lobby.agregar(cliente)

        while True:
            emp = lobby.emparejar()
            if emp:
                partida = Partida(*emp)
                partida.start()
                break
    except Exception as e:
        print(f"Error con cliente {addr}: {e}")
        conn.close()

def main():
    if len(sys.argv) < 4:
        print("Uso: python3 servidor.py <puerto> <max_partidas> <fichero_ranking>")
        return

    puerto = int(sys.argv[1])
    max_partidas = int(sys.argv[2])
    fichero_ranking = sys.argv[3]

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("", puerto))
    servidor.listen()
    print(f"Servidor escuchando en puerto {puerto}...")

    lobby = Lobby()

    try:
        while True:
            conn, addr = servidor.accept()
            print(f"Conexión desde {addr}")
            threading.Thread(target=manejar_cliente, args=(conn, addr, lobby)).start()
    except KeyboardInterrupt:
        print("\nApagando servidor...")
    finally:
        servidor.close()

if __name__ == '__main__':
    main()