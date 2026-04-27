print("=== Compra de Cursos Académicos ===")
print()

print("Cursos disponibles:")
print("  1. Liderazgo      — $200.000")
print("  2. Programación   — $230.000")
print("  3. Cyberseguridad — $270.000")
print()

curso = input("Seleccione un curso (1-3): ")

while curso != "1" and curso != "2" and curso != "3":
    print("Opción no válida.")
    curso = input("Seleccione un curso (1-3): ")

if curso == "1":
    nombre = "Liderazgo"
    precio = 200000
elif curso == "2":
    nombre = "Programación"
    precio = 230000
else:
    nombre = "Cyberseguridad"
    precio = 270000

nota = float(input("Ingrese su nota (1.0 - 7.0): "))

if nota >= 6.6:
    porcentaje = 0.20
elif nota >= 6.0:
    porcentaje = 0.15
elif nota >= 5.0:
    porcentaje = 0.10
else:
    porcentaje = 0.0

print(f"¡Descuento del {int(porcentaje * 100)}% aplicado por obtener una nota de {nota}!")
total = precio * (1 - porcentaje)
print(f"Total a pagar por el curso de {nombre}: ${round(total)}.")
