print("=== Verificador de Edad ===")
print()

try:
    edad = int(input("Ingresa tu edad: "))
except ValueError:
    print("Error: debes ingresar un número entero, no un texto.")
else:
    if edad >= 18:
        print("Eres mayor de edad.")
    else:
        print("Eres menor de edad.")
finally:
    print()
    print("Programa finalizado.")
