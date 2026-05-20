import random

aleatorio = random.randint(1, 3)
match aleatorio:
    case 1:
        puertas = ["Auto", "Gato", "Gato"]
    case 2:
        puertas = ["Gato", "Auto", "Gato"]
    case 3:
        puertas = ["Gato", "Gato", "Auto"]

print("Hay 3 puertas: detrás de una hay un auto y detrás de las otras dos hay un gato.")

puerta_escogida = int(input("Elige una puerta (1, 2 o 3): "))
print(f"Has elegido la puerta {puerta_escogida}.")

for i in range(3):
    if i != puerta_escogida - 1 and puertas[i] == "Gato":
        print(f"El presentador abre la puerta {i + 1} y muestra un gato.")

        puerta_alternativa = [p for p in [1, 2, 3] if p != puerta_escogida and p != i + 1][0]
        cambiar = input(f"¿Quieres cambiar a la puerta {puerta_alternativa}? (s:sí | n:no): ").strip().lower()
        cambio_realizado = cambiar == "s"
        if cambio_realizado:
            puerta_escogida = puerta_alternativa
        break

print(f"\nHas elegido la puerta {puerta_escogida}.")
gano = puertas[puerta_escogida - 1] == "Auto"

if gano:
    print("¡¡¡ Has ganado un auto !!!")
else:
    print("Lo siento, había un gato.")

print(f"\nEl auto estaba en la puerta {aleatorio}. Tú elegiste la puerta {puerta_escogida}.")

if cambio_realizado and gano:
    print("¡Fue buena idea cambiar de puerta!")
elif cambio_realizado and not gano:
    print("Fue una mala idea cambiar de puerta.")
elif not cambio_realizado and gano:
    print("¡Fue buena idea quedarte con tu puerta!")
elif not cambio_realizado and not gano:
    print("Fue una mala idea quedarte con tu puerta.")
