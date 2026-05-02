# Ingresa 5 números, suma los pares y los impares por separado

suma_pares = 0
suma_impares = 0
for i in range(5):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    if numero % 2 == 0:
        suma_pares += numero
    else:
        suma_impares += numero

print("La suma de los números pares es:", suma_pares)
print("La suma de los números impares es:", suma_impares)