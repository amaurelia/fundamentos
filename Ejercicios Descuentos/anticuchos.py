precio = 15000

rol = input("¿Eres estudiante de informática, profesor u otro? (estudiante/profesor/otro): ").strip().lower()

if rol == "estudiante":
    descuento = 5
elif rol == "profesor":
    descuento = 95
else:
    descuento = 0

total = precio * (1 - descuento / 100)

print("\n--- Resumen del combo ---")
print("Precio base: $", precio)
print("Descuento aplicado:", descuento, "%")
print("Total a pagar: $", int(total))
