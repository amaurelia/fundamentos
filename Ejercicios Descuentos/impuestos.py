valor = float(input("Ingresa el valor de tu propiedad en UF: "))
metros = float(input("Ingresa los metros cuadrados de tu propiedad: "))
piscina = input("¿Tiene piscina? (s/n): ").strip().lower()
frutales = input("¿Tiene árboles frutales? (s/n): ").strip().lower()

if valor < 4000:
    porcentaje = 2.0
else:
    porcentaje = 3.0

if metros > 100:
    porcentaje += 1.0

if piscina == "s":
    porcentaje += 0.5

if frutales == "s":
    porcentaje += 0.5

costo_anual = valor * (porcentaje / 100)

print("\n--- Resumen de impuestos ---")
print("Porcentaje total a pagar:", porcentaje, "%")
print("Costo anual:", round(costo_anual, 2), "UF")
