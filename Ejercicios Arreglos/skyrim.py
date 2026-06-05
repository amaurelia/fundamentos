inventario = [
    "Moneda de oro",
    "Manzana dulce",
    "Mapa mundial",
    "Pocion recuperativa",
    "Libro antiguo"
]

MAX_OBJETOS = 5

while True:
    print("\n=== Inventario de Skyrim ===")
    print("1) Ver inventario")
    print("2) Agregar objeto")
    print("3) Dejar objeto por numero")
    print("4) Eliminar objetos por palabra")
    print("5) Salir")

    opcion = input("Elige una opcion: ")

    if opcion == "1":
        if len(inventario) == 0:
            print("Tu inventario esta vacio.")
        else:
            print("Objetos actuales:")
            for i, obj in enumerate(inventario, start=1):
                print(f"{i}) {obj}")

    elif opcion == "2":
        if len(inventario) >= MAX_OBJETOS:
            print("Inventario lleno. No puedes agregar mas objetos.")
        else:
            nuevo = input("Objeto a agregar: ").strip()
            if nuevo == "":
                print("Debes ingresar un nombre valido.")
            else:
                inventario.append(nuevo)
                print(f"'{nuevo}' agregado al inventario.")

    elif opcion == "3":
        if len(inventario) == 0:
            print("No hay objetos para eliminar.")
            continue

        print("Selecciona el objeto a dejar:")
        for i, obj in enumerate(inventario, start=1):
            print(f"{i}) {obj}")

        try:
            indice = int(input("Numero de objeto: "))
            if 1 <= indice <= len(inventario):
                eliminado = inventario.pop(indice - 1)
                print(f"Eliminaste '{eliminado}'.")
            else:
                print("Numero fuera de rango.")
        except ValueError:
            print("Debes ingresar un numero valido.")

    elif opcion == "4":
        palabra = input("Ingresa palabra a buscar: ").strip().lower()
        if palabra == "":
            print("Debes ingresar una palabra.")
            continue

        antes = len(inventario)
        inventario = [obj for obj in inventario if palabra not in obj.lower()]
        eliminados = antes - len(inventario)
        print(f"Se eliminaron {eliminados} objeto(s).")

    elif opcion == "5":
        print("Saliendo del inventario.")
        break

    else:
        print("Opcion no valida.")
