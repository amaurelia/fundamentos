import random

print("=== Generador de Personaje — Calabozos y Dragones ===")
print()

nombre = input("Ingrese el nombre de su personaje: ")

ataque = random.randint(10, 40)
defensa = random.randint(5, 20)
inteligencia = random.randint(0, 30)

clase = "Novato"
arma = "Sin arma"
hechizo = "Sin hechizo"

if defensa > 30:
    clase = "Paladín"

if ataque > 35:
    arma = "Espada Excalibur"

if inteligencia > 15:
    hechizo = "Bola de Fuego"

print()
print("=== Ficha de Personaje ===")
print(f"Nombre:       {nombre}")
print(f"Clase:        {clase}")
print(f"Ataque:       {ataque}")
print(f"Defensa:      {defensa}")
print(f"Inteligencia: {inteligencia}")
print(f"Arma:         {arma}")
print(f"Hechizo:      {hechizo}")
