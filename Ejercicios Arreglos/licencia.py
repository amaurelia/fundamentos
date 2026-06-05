licencias = [5, 11, 3, 15, 2, 5, 6]

suma = 0
for dias in licencias:
    suma += dias

promedio = suma / len(licencias)
mayor = max(licencias)
menor = min(licencias)

mas_de_10 = 0
for dias in licencias:
    if dias > 10:
        mas_de_10 += 1

print("=== Reporte de Licencias ===")
print(f"Promedio: {promedio:.2f} dias")
print(f"Mayor numero de dias: {mayor}")
print(f"Menor numero de dias: {menor}")
print(f"Empleados con mas de 10 dias: {mas_de_10}")
