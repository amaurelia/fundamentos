print("=== El Dilema del Prisionero ===")
print()
print("Cada persona debe declarar si es inocente o si delata al otro.")
print("Opciones: inocente / culpable")
print()

p1 = input("Declaración de la Persona 1 (inocente/culpable): ").strip().lower()
p2 = input("Declaración de la Persona 2 (inocente/culpable): ").strip().lower()

print()
print("=== Sentencia ===")

if p1 == "inocente" and p2 == "inocente":
    print("Persona 1: 1 año de prisión por receptación.")
    print("Persona 2: 1 año de prisión por receptación.")
elif p1 == "culpable" and p2 == "inocente":
    print("Persona 1: Queda en libertad.")
    print("Persona 2: 10 años de prisión.")
elif p1 == "inocente" and p2 == "culpable":
    print("Persona 1: 10 años de prisión.")
    print("Persona 2: Queda en libertad.")
elif p1 == "culpable" and p2 == "culpable":
    print("Persona 1: 10 años de prisión.")
    print("Persona 2: 10 años de prisión.")
else:
    print("Declaración no reconocida. Ingresa 'inocente' o 'culpable'.")
