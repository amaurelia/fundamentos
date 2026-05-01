import random

print("=== Golpe crítico ===")

# Simular un golpe: 10% para crítico, 20% para fallo, 70% para golpe normal
aleatorio = random.randint(1, 100)
if aleatorio <= 10:
    rojo  = "\033[31m"
    texto = "¡Golpe crítico! Daño x2"
    reset = "\033[0m"
    print(rojo + texto + reset)
elif aleatorio <= 30:
    azul  = "\033[34m"
    texto = "¡Fallo! No se inflige daño"
    reset = "\033[0m"
    print(azul + texto + reset)
else:
    verde = "\033[32m"
    texto = "Golpe normal. Daño x1"
    reset = "\033[0m"
    print(verde + texto + reset)