# Ingresa las notas de 5 alumnos y calcula el porcentaje de aprobados

contador_aprobados = 0
for i in range(5):
    nota = float(input("Ingresa la nota del alumno " + str(i + 1) + ": "))
    if nota >= 4:
        contador_aprobados += 1

porcentaje_aprobados = (contador_aprobados / 5) * 100
print("El porcentaje de alumnos aprobados es:", porcentaje_aprobados, "%")