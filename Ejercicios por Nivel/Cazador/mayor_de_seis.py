# Ingresa 6 números y encuentra el mayor

for i in range(6):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    if i == 0:
        mayor = numero
    elif numero > mayor:
        mayor = numero

print("El número mayor es:", mayor)