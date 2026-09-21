import socket
import sys
from jugador import Jugador

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 cliente.py <ip_servidor> <puerto>")
        return

    ip = sys.argv[1]
    puerto = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))

    msg = s.recv(1024).decode()
    nombre = input(msg)
    s.sendall(nombre.encode())

    oponente = s.recv(1024).decode()
    print(oponente)

    turno_msg = s.recv(1024).decode()
    es_turno = turno_msg.endswith("1")

    jugador = Jugador()
    s.sendall(b"LISTO")

    fin = False
    while not fin:
        if es_turno:
            print("Es tu turno!")
            fin = jugador.turno_remoto(s)
        else:
            print("Turno del oponente. Espera...")
            codigo = s.recv(1024).decode()
            resultado = jugador.recibir_accion(codigo)
            mensaje = resultado['informe']
            if resultado['fin']:
                mensaje += "\nFIN"
                fin = True
            s.sendall(mensaje.encode())
        es_turno = not es_turno

    print(s.recv(1024).decode())
    s.close()

if __name__ == '__main__':
    main()
