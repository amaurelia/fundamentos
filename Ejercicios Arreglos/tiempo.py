personajes = [
    ["Dr. Emmett Brown", [1955, 2015, 1885, 2030]],
    ["Marty McFly", [1955, 1985, 2015, 2034]],
    ["Biff Tannen", [1955, 1985]]
]

ANIO_ACTUAL = 2026

# 1) Personaje que viajo al anio mas lejano
personaje_mas_lejano = ""
anio_mas_lejano = -1
for nombre, viajes in personajes:
    max_personaje = max(viajes)
    if max_personaje > anio_mas_lejano:
        anio_mas_lejano = max_personaje
        personaje_mas_lejano = nombre

distancia = abs(anio_mas_lejano - ANIO_ACTUAL)
print("=== Viaje mas lejano ===")
print(f"{personaje_mas_lejano} llego hasta el anio {anio_mas_lejano}")
print(f"Distancia respecto a {ANIO_ACTUAL}: {distancia} anios")

umbral = int(input("\nIngresa anio umbral: "))
print(f"Personajes que viajaron despues de {umbral}:")

alguien = False
for nombre, viajes in personajes:
    for anio in viajes:
        if anio > umbral:
            print(f"- {nombre}")
            alguien = True
            break

if not alguien:
    print("Ningun personaje viajo despues de ese anio.")

# 3) Nuevo viaje de Marty al 2022
for personaje in personajes:
    if personaje[0] == "Marty McFly":
        personaje[1].append(2022)
        break

print("\n=== Viajes actualizados ===")
for nombre, viajes in personajes:
    lista_anios = ", ".join(str(anio) for anio in viajes)
    print(f"{nombre}: {lista_anios}")
