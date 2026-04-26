# El menú es una estructura de control que permite al usuario elegir entre varias opciones
# En python, el menú se puede implementar con un ciclo while y un match para evaluar la opción elegida por el usuario

opcion = 0
while opcion!=4:
    opcion = int(input("Ingrese una opción (1:Registrar | 2:Ver | 3:Buscar | 4:Salir): "))
    match opcion:
        case 1:
            print("Registrar")
        case 2:
            print("Ver")
        case 3:
            print("Buscar")
        case 4:
            print("Salir")