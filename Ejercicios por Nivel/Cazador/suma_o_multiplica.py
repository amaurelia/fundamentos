# Ingresa 2 números, si ambos son pares súmalos, caso contrario multiplícalos

num1 = int(input("Ingresa el primer número: "))
num2 = int(input("Ingresa el segundo número: "))
if num1 % 2 == 0 and num2 % 2 == 0:
    resultado = num1 + num2
    print("Ambos números son pares. La suma es:", resultado)
else:
    resultado = num1 * num2
    print("Al menos uno de los números no es par. La multiplicación es:", resultado)
