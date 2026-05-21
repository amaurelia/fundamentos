print("=== Bienvenido al Hotel Paradise ===")
print()

# Inicializar 3 habitaciones disponibles
habitaciones = [None] * 3  # None significa que la habitación está disponible
TOTAL_HABITACIONES = 3

while True:
    print()
    print("--- MENÚ ---")
    print("1. Tomar habitación")
    print("2. Habitaciones disponibles")
    print("3. Ver huéspedes")
    print("4. Devolver habitación")
    print("5. Salir")
    print()

    opcion = input("Selecciona una opción (1-5): ").strip()

    if opcion == "1":
        # Tomar una habitación
        disponibles = habitaciones.count(None)
        if disponibles == 0:
            print("Lo sentimos, el hotel está completo. No hay habitaciones disponibles.")
        else:
            nombre = input("¿Cuál es tu nombre? ").strip()
            if not nombre:
                print("Error: debes ingresar un nombre.")
            else:
                # Buscar la primera habitación disponible
                for i in range(TOTAL_HABITACIONES):
                    if habitaciones[i] is None:
                        habitaciones[i] = nombre
                        num_habitacion = i + 1
                        print(f"¡Bienvenido {nombre}! Se te ha asignado la habitación {num_habitacion}.")
                        break

    elif opcion == "2":
        # Ver habitaciones disponibles
        disponibles = habitaciones.count(None)
        print(f"Habitaciones disponibles: {disponibles}/{TOTAL_HABITACIONES}")

    elif opcion == "3":
        # Ver huéspedes
        huespedes = [(i + 1, nombre) for i, nombre in enumerate(habitaciones) if nombre is not None]
        if not huespedes:
            print("No hay huéspedes en el hotel.")
        else:
            print("Huéspedes actuales:")
            for num_hab, nombre in huespedes:
                print(f"  Habitación {num_hab}: {nombre}")

    elif opcion == "4":
        # Devolver habitación
        huespedes = [(i, nombre) for i, nombre in enumerate(habitaciones) if nombre is not None]
        if not huespedes:
            print("No hay huéspedes en el hotel.")
        else:
            nombre = input("Ingresa tu nombre para devolver la habitación: ").strip()
            encontrado = False
            for i, huesped in huespedes:
                if huesped.lower() == nombre.lower():
                    habitaciones[i] = None
                    print(f"Habitación {i + 1} liberada. ¡Hasta pronto, {huesped}!")
                    encontrado = True
                    break
            if not encontrado:
                print(f"No se encontró ningún huésped con el nombre \"{nombre}\".")

    elif opcion == "5":
        print("¡Gracias por visitarnos! Hasta pronto.")
        break

    else:
        print("Opción no válida. Por favor, selecciona entre 1 y 5.")
