impresoras = [
    {"id": 1, "marca": "HP",    "modelo": "LaserJet 1020", "estado": "activo"},
    {"id": 2, "marca": "Canon", "modelo": "Pixma G2020",   "estado": "inactivo"}
]

def buscar_por_id(id_buscado):
    for imp in impresoras:
        if imp["id"] == id_buscado:
            return imp
    return None

while True:
    print("\n=== PrintCorp - Gestion de Impresoras ===")
    print("1) POST   - Agregar impresora")
    print("2) GET    - Mostrar todas las impresoras")
    print("3) PUT    - Actualizar estado")
    print("4) DELETE - Eliminar impresora")
    print("5) GET    - Buscar impresora por id")
    print("6) Salir")

    opcion = input("Elige una opcion: ")

    if opcion == "1":
        try:
            id_nuevo = int(input("ID: "))
        except ValueError:
            print("El ID debe ser un numero.")
            continue

        if buscar_por_id(id_nuevo):
            print("Ya existe una impresora con ese ID.")
            continue

        marca  = input("Marca: ").strip()
        modelo = input("Modelo: ").strip()
        estado = input("Estado (activo / inactivo / en reparacion): ").strip()

        impresoras.append({"id": id_nuevo, "marca": marca, "modelo": modelo, "estado": estado})
        print("Impresora agregada correctamente.")

    elif opcion == "2":
        if len(impresoras) == 0:
            print("No hay impresoras registradas.")
        else:
            print("\n--- Impresoras ---")
            for imp in impresoras:
                print(f"  ID {imp['id']} | {imp['marca']} {imp['modelo']} | Estado: {imp['estado']}")

    elif opcion == "3":
        try:
            id_upd = int(input("ID de la impresora a actualizar: "))
        except ValueError:
            print("Debes ingresar un numero.")
            continue

        impresora = buscar_por_id(id_upd)
        if impresora is None:
            print("No se encontro una impresora con ese ID.")
        else:
            nuevo_estado = input("Nuevo estado: ").strip()
            impresora["estado"] = nuevo_estado
            print(f"Estado actualizado a '{nuevo_estado}'.")

    elif opcion == "4":
        try:
            id_del = int(input("ID de la impresora a eliminar: "))
        except ValueError:
            print("Debes ingresar un numero.")
            continue

        impresora = buscar_por_id(id_del)
        if impresora is None:
            print("No se encontro una impresora con ese ID.")
        else:
            impresoras.remove(impresora)
            print("Impresora eliminada.")

    elif opcion == "5":
        try:
            id_busq = int(input("ID a buscar: "))
        except ValueError:
            print("Debes ingresar un numero.")
            continue

        impresora = buscar_por_id(id_busq)
        if impresora is None:
            print("No se encontro una impresora con ese ID.")
        else:
            print(f"  ID {impresora['id']} | {impresora['marca']} {impresora['modelo']} | Estado: {impresora['estado']}")

    elif opcion == "6":
        print("Hasta luego.")
        break

    else:
        print("Opcion no valida.")
