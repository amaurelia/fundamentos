recompensas_piratas = [
    ["Monkey D. Luffy", 3000],
    ["Roronoa Zoro", 1200],
    ["Sanji", 1100],
    ["Nami", 366],
    ["Usopp", 200],
    ["Nico Robin", 930],
    ["Franky", 500],
    ["Brook", 383],
    ["Jinbe", 1100],
    ["Shanks", 4000],
    ["Marshall D. Teach", 3960],
    ["Charlotte Linlin", 4388],
    ["Kaido", 4611],
    ["Buggy", 3189],
    ["Trafalgar D. Water Law", 3000],
    ["Eustass Kid", 3000]
]

# 1) Separar en dos arreglos paralelos
piratas = []
recompensas = []
for nombre, recompensa in recompensas_piratas:
    piratas.append(nombre)
    recompensas.append(recompensa)

print("=== Arreglos separados ===")
print("Piratas:", piratas)
print("Recompensas:", recompensas)

# 2) Pirata mas buscado
indice_max = 0
for i in range(1, len(recompensas)):
    if recompensas[i] > recompensas[indice_max]:
        indice_max = i

print("=== Pirata mas buscado ===")
print(f"{piratas[indice_max]} -> {recompensas[indice_max]} millones de berries")

# 3) Piratas sobre umbral
print("\n=== Piratas sobre umbral ===")
umbral = int(input("Ingresa umbral de recompensa (millones): "))

hay_resultados = False
for i in range(len(piratas)):
    if recompensas[i] > umbral:
        print(f"- {piratas[i]} ({recompensas[i]})")
        hay_resultados = True

if not hay_resultados:
    print("No hay piratas sobre ese umbral.")

# 4) Resumen de recompensas
total = 0
for valor in recompensas:
    total += valor

promedio = total / len(recompensas)

print("\n=== Resumen ===")
print(f"Total recompensas: {total} millones")
print(f"Promedio: {promedio:.2f} millones")
