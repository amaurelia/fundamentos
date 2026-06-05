inventario = []
equipados = []
MAX_EQUIPADOS = 4

while True:
    print("\n=== Inventario de Link ===")
    print("1) Agregar objeto al inventario")
    print("2) Equipar objeto")
    print("3) Ver estado de combate")
    print("4) Ver inventario")
    print("5) Ver objetos equipados")
    print("6) Salir")

    opcion = input("Elige una opcion: ")

    if opcion == "1":
        objeto = input("Objeto a agregar: ").strip()
        if objeto == "":
            print("Debes ingresar un nombre de objeto.")
        else:
            inventario.append(objeto)
            print(f"Se agrego '{objeto}' al inventario.")

    elif opcion == "2":
        if len(equipados) >= MAX_EQUIPADOS:
            print("Ya tienes el maximo de 4 objetos equipados.")
            continue

        if len(inventario) == 0:
            print("No tienes objetos en el inventario.")
            continue

        print("Objetos en inventario:")
        for i, objeto in enumerate(inventario, start=1):
            print(f"{i}) {objeto}")

        eleccion = input("Escribe el nombre del objeto a equipar: ").strip()

        if eleccion not in inventario:
            print("Ese objeto no esta en tu inventario.")
        elif eleccion in equipados:
            print("Ese objeto ya esta equipado.")
        else:
            equipados.append(eleccion)
            print(f"'{eleccion}' equipado correctamente.")

    elif opcion == "3":
        tiene_espada = any(obj.lower() == "espada" for obj in equipados)
        tiene_escudo = any(obj.lower() == "escudo" for obj in equipados)

        if tiene_espada and tiene_escudo:
            print("Link esta listo para pelear")
        else:
            print("Aun falta para enfrentar a Ganondorf")

    elif opcion == "4":
        print("\nInventario:")
        if len(inventario) == 0:
            print("(vacio)")
        else:
            for i, objeto in enumerate(inventario, start=1):
                print(f"{i}) {objeto}")

    elif opcion == "5":
        print("\nObjetos equipados:")
        if len(equipados) == 0:
            print("(ninguno)")
        else:
            for i, objeto in enumerate(equipados, start=1):
                print(f"{i}) {objeto}")

    elif opcion == "6":
        print("Hasta luego, heroe de Hyrule.")
        break

    else:
        print("Opcion no valida.")
