fruteria = [
    ["Manzana", 1200],
    ["Platano", 800],
    ["Naranja", 1000],
    ["Sandia", 2500],
    ["Uva", 1800],
    ["Kiwi", 1500],
    ["Pera", 1100],
    ["Mango", 2200]
]

# 1) Fruta mas cara
fruta_mas_cara = fruteria[0]
for fruta in fruteria:
    if fruta[1] > fruta_mas_cara[1]:
        fruta_mas_cara = fruta

print("=== Fruta mas cara ===")
print(f"{fruta_mas_cara[0]} -> ${fruta_mas_cara[1]} por kilo")

# 2) Frutas sobre umbral
umbral = int(input("\nIngresa umbral de precio: "))
print("Frutas sobre el umbral:")

hay_frutas = False
for nombre, precio in fruteria:
    if precio > umbral:
        print(f"- {nombre} (${precio})")
        hay_frutas = True

if not hay_frutas:
    print("No hay frutas sobre ese umbral.")

# 3) Promedio de precios
suma = 0
for _, precio in fruteria:
    suma += precio

promedio = suma / len(fruteria)
print(f"\nPromedio de precios: ${promedio:.2f}")

# 4) Agregar palta
fruteria.append(["Palta", 8500])
print("\nSe agrego Palta con precio 8500.")
print("Lista actualizada:")
for nombre, precio in fruteria:
    print(f"- {nombre}: ${precio}")
