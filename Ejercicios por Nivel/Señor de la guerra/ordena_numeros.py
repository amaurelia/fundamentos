# Ingresa 6 números y ordénalos de menor a mayor

numeros = []
for i in range(6):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    numeros.append(numero)
    numeros.sort()

print("Los números ordenados de menor a mayor son:", numeros)