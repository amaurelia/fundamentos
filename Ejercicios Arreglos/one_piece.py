piratas = [
    "Monkey D. Luffy", "Roronoa Zoro", "Sanji", "Nami", "Usopp", "Nico Robin",
    "Franky", "Brook", "Jinbe",
    "Shanks", "Marshall D. Teach", "Charlotte Linlin", "Kaido", "Buggy",
    "Trafalgar D. Water Law", "Eustass Kid"
]

recompensas = [
    3000, 1200, 1100, 366, 200, 930,
    500, 383, 1100,
    4000, 3960, 4388, 4611, 3189,
    3000, 3000
]

# 1) Pirata mas buscado
indice_max = 0
for i in range(1, len(recompensas)):
    if recompensas[i] > recompensas[indice_max]:
        indice_max = i

print("=== Pirata mas buscado ===")
print(f"{piratas[indice_max]} -> {recompensas[indice_max]} millones de berries")

# 2) Piratas sobre umbral
print("\n=== Piratas sobre umbral ===")
umbral = int(input("Ingresa umbral de recompensa (millones): "))

hay_resultados = False
for i in range(len(piratas)):
    if recompensas[i] > umbral:
        print(f"- {piratas[i]} ({recompensas[i]})")
        hay_resultados = True

if not hay_resultados:
    print("No hay piratas sobre ese umbral.")

# 3) Resumen de recompensas
total = 0
for valor in recompensas:
    total += valor

promedio = total / len(recompensas)

print("\n=== Resumen ===")
print(f"Total recompensas: {total} millones")
print(f"Promedio: {promedio:.2f} millones")
