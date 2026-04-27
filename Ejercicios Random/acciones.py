import random

print("=== Generador de Acción Aleatoria ===")
num_personaje = random.randint(1, 5)
num_verbo = random.randint(1, 4)
num_lugar = random.randint(1, 5)

if num_personaje == 1:
    personaje = "Nina"
elif num_personaje == 2:
    personaje = "Luna"
elif num_personaje == 3:
    personaje = "Alis"
elif num_personaje == 4:
    personaje = "Jack"
else:
    personaje = "Cris"

if num_verbo == 1:
    verbo = "estudiando"
elif num_verbo == 2:
    verbo = "cantando"
elif num_verbo == 3:
    verbo = "bailando"
else:
    verbo = "saltando"

if num_lugar == 1:
    lugar = "la biblioteca"
elif num_lugar == 2:
    lugar = "la cordillera"
elif num_lugar == 3:
    lugar = "el patio"
elif num_lugar == 4:
    lugar = "el lago"
else:
    lugar = "la sede"

print(f"{personaje} está {verbo} en {lugar}")
