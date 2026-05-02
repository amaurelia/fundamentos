# Para obtener un número aleatorio entre 0 y 1
import random
numero_aleatorio = random.random()
print(f"Número aleatorio entre 0 y 1: {numero_aleatorio}")

# Para obtener un número entero aleatorio entre a y b (inclusive)
a = 1
b = 10
numero_entero = random.randint(a, b)
print(f"Número entero aleatorio entre {a} y {b}: {numero_entero}")

# Para obtener un número flotante aleatorio entre a y b
a = 5.0
b = 15.0
numero_flotante = random.uniform(a, b)
print(f"Número flotante aleatorio entre {a} y {b}: {numero_flotante}")
