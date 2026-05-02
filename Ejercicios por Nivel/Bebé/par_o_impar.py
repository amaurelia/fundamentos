# Ingresa un número y verifica si es par o impar ( n es par si n%2 = 0 )

numero = int(input("Ingresa un número: "))
if numero % 2 == 0:
    print("El número", numero, "es par")
else:
    print("El número", numero, "es impar")