import random

print("=== Lanzamiento de Dados ===")
print()

dado1 = random.randint(1, 6)
dado2 = random.randint(1, 6)
dado3 = random.randint(1, 6)

print(f"Dado 1: {dado1}")
print(f"Dado 2: {dado2}")
print(f"Dado 3: {dado3}")
print()

resultado = (dado1 * dado2) - dado3

print(f"Resultado: ({dado1} × {dado2}) - {dado3} = {resultado}")
print()

if resultado < 10:
    print("Resultado bajo")
elif resultado <= 20:
    print("Resultado intermedio")
else:
    print("Resultado alto")
