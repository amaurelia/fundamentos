# Ingresa números hasta que hayas ingresado 10 pares

contador_pares = 0
while contador_pares < 10:
    numero = int(input("Ingresa un número: "))
    if numero % 2 == 0:
        contador_pares += 1
print("Has ingresado 10 números pares.")