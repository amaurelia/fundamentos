print("=== Verificador de Edad ===")
print()

while True:
    try:
        edad = int(input("Ingresa tu edad: "))
    except ValueError:
        print("Error: debes ingresar un número entero, no un texto.")
    else:
        if edad >= 18:
            print("Eres mayor de edad.")
        else:
            print("Eres menor de edad.")
        break

print()
print("Programa finalizado.")
