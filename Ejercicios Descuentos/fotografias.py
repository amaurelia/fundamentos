precio_por_foto = 5000

fotos = int(input("¿Cuántas fotos de Spider-Man tomaste esta semana?: "))

if fotos >= 5 and fotos <= 10:
    aumento = 1
elif fotos > 10:
    aumento = 2
else:
    aumento = 0

precio_ajustado = precio_por_foto * (1 + aumento / 100)
total = precio_ajustado * fotos

print("\n--- Pago semanal de Peter Parker ---")
print("Fotos entregadas:", fotos)
print("Aumento por foto:", aumento, "%")
print("Precio por foto: $", round(precio_ajustado, 2))
print("Total a cobrar: $", round(total, 2))
