print("=== Bienvenido al sistema de registro de notas ===")

total = 0
cantidad_notas = 0
opcion = 0
while opcion!=4:
    opcion = int(input("\nIngrese una opción (1:Registrar nota | 2:Ver promedio | 3:Ver cantidad de notas | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Registrar nota ***")
            nota = float(input("\nIngrese la nota: "))
            total += nota
            cantidad_notas += 1
            print("Nota registrada")
        case 2:
            print("\n *** Ver promedio ***")
            if cantidad_notas == 0:
                print("No hay notas registradas")
            else:
                promedio = total / cantidad_notas
                print(f"El promedio de las notas es: {promedio}")
        case 3:
            print("\n *** Ver cantidad de notas ***")
            print(f"La cantidad de notas registradas es: {cantidad_notas}")
        case 4:
            print("\n *** Salir ***")