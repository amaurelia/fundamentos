print("=== El Helado de Tu Amigo ===")
print()

print("Sabores disponibles: vainilla, chocolate, mixto")
sabor = input("Sabor de helado: ").strip().lower()

print("Salsas disponibles: manjar, chocolate, frutilla")
salsa = input("Salsa: ").strip().lower()

print()

if sabor == "vainilla" and salsa == "frutilla":
    print("Resultado: ¡Desabrido!")
elif sabor == "chocolate":
    print("Resultado: ¡Sabroso!")
elif sabor == "mixto" and salsa in ("manjar", "frutilla"):
    print("Resultado: ¡Sabroso!")
else:
    print("Resultado: Normal.")
