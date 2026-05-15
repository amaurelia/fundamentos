print("=== Postulación a la Beca ===")
print()

p = float(input("Nota de programación (1.0 – 7.0): "))
i = float(input("Nota de inglés (1.0 – 7.0): "))

print()

if p < 4.0 or i < 4.0:
    print("No puedes postular a la beca.")
elif p > 6.0 and i > 6.0:
    print("¡Puedes postular! Probabilidad de obtener la beca: 40%")
elif p > 4.0 and i > 6.0:
    print("¡Puedes postular! Probabilidad de obtener la beca: 20%")
else:
    print("Puedes postular, pero sin ventaja especial.")
