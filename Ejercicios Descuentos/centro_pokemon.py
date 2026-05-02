precio = 800

nivel = int(input("Ingresa el nivel del Pokémon: "))

if nivel >= 5 and nivel <= 15:
    descuento = 5
elif nivel >= 16 and nivel <= 30:
    descuento = 7
elif nivel >= 31 and nivel <= 50:
    descuento = 10
elif nivel > 50:
    descuento = 15
else:
    descuento = 0

total = precio * (1 - descuento / 100)

print("\n--- Centro Pokémon ---")
print("Nivel del Pokémon:", nivel)
print("Descuento aplicado:", descuento, "%")
print("Costo de la atención:", int(total), "yenes")
