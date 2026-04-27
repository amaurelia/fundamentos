print("=== Bienvenido al sistema de registro de viajes ===")

bencina = 0
kilometraje = 0
opcion = 0
while opcion!=4:
    opcion = int(input("Ingrese una opción (1:Registrar viaje | 2:Ver consumo | 3:Ver kilometraje | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Registrar viaje ***")
            bencina_consumida = float(input("\nIngrese la cantidad de bencina consumida en litros: "))
            kilometraje_recorrido = float(input("\nIngrese el kilometraje recorrido en kilómetros: "))
            bencina += bencina_consumida
            kilometraje += kilometraje_recorrido
            print("Viaje registrado")
        case 2:
            print("\n *** Ver consumo ***")
            if kilometraje == 0:
                print("No hay viajes registrados")
            else:
                consumo = bencina / kilometraje
                print(f"El consumo de bencina es: {consumo} litros por kilómetro")
        case 3:
            print("\n *** Ver kilometraje ***")
            print(f"El kilometraje total recorrido es: {kilometraje} kilómetros")
        case 4:
            print("\n *** Salir ***")
            
