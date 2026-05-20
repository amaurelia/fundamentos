verde = "\033[32m"
rojo  = "\033[31m"
texto = "Golpe normal. Daño x1"
reset = "\033[0m"

tu = f"{verde}[TÚ]{reset}"
p1 = f"{rojo}[01]{reset}"
p2 = f"{rojo}[02]{reset}"
p3 = f"{rojo}[03]{reset}"

def dibujo_puertas(p1, p2, p3):
    return f"""
 __________________________________________________
|                |                |                |
|                |                |                |
|                |                |                |
|      {p1}      |      {p2}      |      {p3}      |
|                |                |                |
|                |                |                |
|________________|________________|________________|
"""

def puertas_gato_01(p2, p3):
    return rf"""
 __________________________________________________
|                |                |                |
|   /\_____/\    |                |                |
|  /  o   o  \   |                |                |
| ( ==  ^  == )  |      {p2}      |      {p3}      |
|  )         (   |                |                |
| (           )  |                |                |
|________________|________________|________________|
"""

def puertas_gato_02(p1, p3):
    return rf"""
 __________________________________________________
|                |                |                |
|                |   /\_____/\    |                |
|                |  /  o   o  \   |                |
|      {p1}      | ( ==  ^  == )  |      {p3}      |
|                |  )         (   |                |
|                | (           )  |                |
|________________|________________|________________|
"""

def puertas_gato_03(p1, p2):
    return rf"""
 __________________________________________________
|                |                |                |
|                |                |   /\_____/\    |
|                |                |  /  o   o  \   |
|      {p1}      |      {p2}      | ( ==  ^  == )  |
|                |                |  )         (   |
|                |                | (           )  |
|________________|________________|________________|
"""

reveal_auto_01 = r"""
 __________________________________________________
|                |                |                |
|   __________   |   /\_____/\    |   /\_____/\    |
|  /  ______  \  |  /  o   o  \   |  /  o   o  \   |
|  |  A U T O |  | ( ==  ^  == )  | ( ==  ^  == )  |
|  |__________|  |  )         (   |  )         (   |
|   (o)    (o)   | (           )  | (           )  |
|________________|________________|________________|
"""

reveal_auto_02 = r"""
 __________________________________________________
|                |                |                |
|   /\_____/\    |   __________   |   /\_____/\    |
|  /  o   o  \   |  /  ______  \  |  /  o   o  \   |
| ( ==  ^  == )  |  |  A U T O |  | ( ==  ^  == )  |
|  )         (   |  |__________|  |  )         (   |
| (           )  |   (o)    (o)   | (           )  |
|________________|________________|________________|
"""

reveal_auto_03 = r"""
 __________________________________________________
|                |                |                |
|   /\_____/\    |   /\_____/\    |   __________   |
|  /  o   o  \   |  /  o   o  \   |  /  ______  \  |
| ( ==  ^  == )  | ( ==  ^  == )  |  |  A U T O |  |
|  )         (   |  )         (   |  |__________|  |
| (           )  | (           )  |   (o)    (o)   |
|________________|________________|________________|
"""

import random

aleatorio = random.randint(1, 3)
match aleatorio:
    case 1:
        puertas = ["Auto", "Gato", "Gato"]
    case 2:
        puertas = ["Gato", "Auto", "Gato"]
    case 3:
        puertas = ["Gato", "Gato", "Auto"]

print(dibujo_puertas(p1, p2, p3))
puerta_escogida = int(input("Elige una puerta (1, 2, o 3): "))
if puerta_escogida == 1:
    print("Has elegido la puerta 1.")
    p1 = tu
elif puerta_escogida == 2:
    print("Has elegido la puerta 2.")
    p2 = tu
elif puerta_escogida == 3:
    print("Has elegido la puerta 3.")
    p3 = tu

print(dibujo_puertas(p1, p2, p3))

for i in range(3):
    if i != puerta_escogida - 1 and puertas[i] == "Gato":
        print(f"El presentador abre la puerta {i + 1} y muestra un gato.")
        if i == 0:
            print(puertas_gato_01(p2, p3))
        elif i == 1:
            print(puertas_gato_02(p1, p3))
        elif i == 2:
            print(puertas_gato_03(p1, p2))

        puerta_alternativa = [p for p in [1, 2, 3] if p != puerta_escogida and p != i + 1][0]
        cambiar = input(f"¿Quieres cambiar a la puerta {puerta_alternativa}? (1:sí | 2:no): ").strip().lower()
        cambio_realizado = cambiar == "1"
        if cambio_realizado:
            puerta_escogida = puerta_alternativa
        break

print(f"\nHas elegido la puerta {puerta_escogida}.")
if puertas[puerta_escogida - 1] == "Auto":
    print("¡¡¡ Has ganado un auto !!!")
else:
    print("Lo siento, había un gato.")

print("\n--- Revelación final ---")
if aleatorio == 1:
    print(reveal_auto_01)
elif aleatorio == 2:
    print(reveal_auto_02)
elif aleatorio == 3:
    print(reveal_auto_03)
print(f"El auto estaba en la puerta {aleatorio}. Tú elegiste la puerta {puerta_escogida}.")

gano = puertas[puerta_escogida - 1] == "Auto"
if cambio_realizado and gano:
    print(f"{verde}¡Fue buena idea cambiar de puerta!{reset}")
elif cambio_realizado and not gano:
    print(f"{rojo}Fue una mala idea cambiar de puerta.{reset}")
elif not cambio_realizado and gano:
    print(f"{verde}¡Fue buena idea quedarte con tu puerta!{reset}")
elif not cambio_realizado and not gano:
    print(f"{rojo}Fue una mala idea quedarte con tu puerta.{reset}")
