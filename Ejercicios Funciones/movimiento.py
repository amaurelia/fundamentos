def validar_posicion(x, y):
    return 0 <= x <= 5 and 0 <= y <= 5


def mover_derecha(posicion):
    x, y = posicion
    nuevo_x, nuevo_y = x, y + 1
    if validar_posicion(nuevo_x, nuevo_y):
        return [nuevo_x, nuevo_y]
    print("No puedes salir del mapa.")
    return posicion


def mover_izquierda(posicion):
    x, y = posicion
    nuevo_x, nuevo_y = x, y - 1
    if validar_posicion(nuevo_x, nuevo_y):
        return [nuevo_x, nuevo_y]
    print("No puedes salir del mapa.")
    return posicion


def mover_arriba(posicion):
    x, y = posicion
    nuevo_x, nuevo_y = x - 1, y
    if validar_posicion(nuevo_x, nuevo_y):
        return [nuevo_x, nuevo_y]
    print("No puedes salir del mapa.")
    return posicion


def mover_abajo(posicion):
    x, y = posicion
    nuevo_x, nuevo_y = x + 1, y
    if validar_posicion(nuevo_x, nuevo_y):
        return [nuevo_x, nuevo_y]
    print("No puedes salir del mapa.")
    return posicion


def mostrar_mapa(posicion):
    x, y = posicion
    print("\nMapa actual:")
    for fila in range(6):
        linea = ""
        for col in range(6):
            if fila == x and col == y:
                linea += "x"
            else:
                linea += "."
        print(linea)


def menu():
    posicion = [3, 3]

    while True:
        mostrar_mapa(posicion)
        print("\nControles: w(arriba), s(abajo), a(izquierda), d(derecha), q(salir)")
        tecla = input("Movimiento: ").strip().lower()

        if tecla == "w":
            posicion = mover_arriba(posicion)
        elif tecla == "s":
            posicion = mover_abajo(posicion)
        elif tecla == "a":
            posicion = mover_izquierda(posicion)
        elif tecla == "d":
            posicion = mover_derecha(posicion)
        elif tecla == "q":
            print("Saliendo del juego.")
            break
        else:
            print("Tecla no valida.")


menu()
