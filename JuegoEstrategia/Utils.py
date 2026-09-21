# utils.py
import os
import string

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_celda(celda, max_col=4, max_row=4):
    if len(celda) != 2:
        return False
    col, row = celda[0].upper(), celda[1]
    return col in string.ascii_uppercase[:max_col] and row.isdigit() and 1 <= int(row) <= max_row

def comprobar_celda_disponible(celda, equipo):
    return all(p.posicion != celda for p in equipo if p.vida_actual > 0)

def validar_celda_contigua(c1, c2):
    col1, row1 = ord(c1[0].upper()), int(c1[1])
    col2, row2 = ord(c2[0].upper()), int(c2[1])
    return abs(col1 - col2) + abs(row1 - row2) == 1

