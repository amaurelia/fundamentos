# Crea el siguiente juego:
# Genera un mapa de 8x5, comienzas en la celda a1 y tu objetivo es llegar hasta la celda e8,
# para ello puedes moverte hacia arriba, abajo, derecha e izquierda pero:
# ● No puedes salir de los bordes ( el programa debe indicar que estás en el borde )
# ● No puedes pasar por las rocas ( estas son de color morado )
# a1 a2 a3 a4 a5 a6 a7 a8
# b1 b2 b3 b4 b5 b6 b7 b8
# c1 c2 c3 c4 c5 c6 c7 c8
# d1 d2 d3 d4 d5 d6 d7 d8
# e1 e2 e3 e4 e5 e6 e7 e8
# El programa debe mostrar el mapa después de cada movimiento, indicando tu posición actual y las rocas, el programa debe indicar si has ganado o perdido ( si te quedas sin movimientos )
# El programa debe permitir al jugador reiniciar el juego después de ganar o perder

import random

FILAS = ['a', 'b', 'c', 'd', 'e']
COLUMNAS = list(range(1, 9))
MAX_MOVIMIENTOS = 25


def hay_camino(rocas):
    """Verifica con BFS si existe un camino desde a1 hasta e8."""
    inicio = ('a', 1)
    meta = ('e', 8)
    visitados = {inicio}
    cola = [inicio]
    while cola:
        fila, col = cola.pop(0)
        if (fila, col) == meta:
            return True
        idx = FILAS.index(fila)
        vecinos = []
        if idx > 0:
            vecinos.append((FILAS[idx - 1], col))
        if idx < len(FILAS) - 1:
            vecinos.append((FILAS[idx + 1], col))
        if col > 1:
            vecinos.append((fila, col - 1))
        if col < COLUMNAS[-1]:
            vecinos.append((fila, col + 1))
        for v in vecinos:
            if v not in visitados and v not in rocas:
                visitados.add(v)
                cola.append(v)
    return False


def generar_rocas():
    """Genera rocas aleatorias garantizando que siempre exista un camino."""
    while True:
        rocas = set()
        protegidas = {('a', 1), ('e', 8)}
        for fila in FILAS:
            for col in COLUMNAS:
                if (fila, col) not in protegidas and random.random() < 0.20:
                    rocas.add((fila, col))
        if hay_camino(rocas):
            return rocas


def mostrar_mapa(pos_fila, pos_col, rocas):
    print()
    print("     " + "  ".join(str(c) for c in COLUMNAS))
    print("   +" + "---" * len(COLUMNAS) + "+")
    for fila in FILAS:
        print(f" {fila} |", end="")
        for col in COLUMNAS:
            if (fila, col) == (pos_fila, pos_col):
                print(" @ ", end="")
            elif (fila, col) == ('e', 8):
                print(" X ", end="")
            elif (fila, col) in rocas:
                print(" # ", end="")
            else:
                print(" . ", end="")
        print("|")
    print("   +" + "---" * len(COLUMNAS) + "+")
    print("  @ = tú   X = meta   # = roca\n")


def jugar():
    rocas = generar_rocas()
    pos_fila = 'a'
    pos_col = 1
    movimientos = MAX_MOVIMIENTOS

    print("=" * 40)
    print("       JUEGO DEL MAPA")
    print("=" * 40)
    print(f"Llega desde a1 hasta e8 en {MAX_MOVIMIENTOS} movimientos.")
    print("Comandos: w = arriba  s = abajo  d = derecha  a = izquierda\n")
    mostrar_mapa(pos_fila, pos_col, rocas)

    while True:
        print(f"Posición: {pos_fila}{pos_col}  |  Movimientos restantes: {movimientos}")
        comando = input("Movimiento (w/a/s/d): ").strip().lower()

        nueva_fila = pos_fila
        nuevo_col = pos_col

        if comando == "w":
            idx = FILAS.index(pos_fila)
            if idx == 0:
                print("¡Estás en el borde superior! No puedes ir más arriba.\n")
                continue
            nueva_fila = FILAS[idx - 1]
        elif comando == "s":
            idx = FILAS.index(pos_fila)
            if idx == len(FILAS) - 1:
                print("¡Estás en el borde inferior! No puedes ir más abajo.\n")
                continue
            nueva_fila = FILAS[idx + 1]
        elif comando == "d":
            if pos_col == COLUMNAS[-1]:
                print("¡Estás en el borde derecho! No puedes ir más a la derecha.\n")
                continue
            nuevo_col = pos_col + 1
        elif comando == "a":
            if pos_col == COLUMNAS[0]:
                print("¡Estás en el borde izquierdo! No puedes ir más a la izquierda.\n")
                continue
            nuevo_col = pos_col - 1
        else:
            print("Comando no válido. Usa: w = arriba  s = abajo  d = derecha  a = izquierda\n")
            continue

        if (nueva_fila, nuevo_col) in rocas:
            print("¡Hay una roca! No puedes pasar por ahí.\n")
            continue

        pos_fila = nueva_fila
        pos_col = nuevo_col
        movimientos -= 1

        mostrar_mapa(pos_fila, pos_col, rocas)

        if pos_fila == 'e' and pos_col == 8:
            print("¡¡GANASTE!! Has llegado a la meta.")
            break

        if movimientos == 0:
            print("¡PERDISTE! Te quedaste sin movimientos.")
            break

    respuesta = input("\n¿Quieres jugar de nuevo? (s/n): ").strip().lower()
    if respuesta == 's':
        jugar()


jugar()

