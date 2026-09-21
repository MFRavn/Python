import socket
import threading
import sys
import random

class Cliente:
    def __init__(self, nombre, conn):
        self.nombre = nombre
        self.conn = conn