import random

print("=== Cartón de Lotería ===")
print()

usados = ""
fila1 = ""
fila2 = ""
fila3 = ""
contador = 0

while contador < 15:
    num = random.randint(1, 30)
    # f"|{num:02d}|" Es un f-string que convierte el |5| en |05|.
    # El formato :02d indica que el número debe tener al menos 2 dígitos, rellenando con ceros a la izquierda si es necesario.
    marca = f"|{num:02d}|"
    if marca not in usados:
        usados += marca
        if contador < 5:
            fila1 += f"{num:02d} "
        elif contador < 10:
            fila2 += f"{num:02d} "
        else:
            fila3 += f"{num:02d} "
        contador += 1

print(fila1)
print(fila2)
print(fila3)
