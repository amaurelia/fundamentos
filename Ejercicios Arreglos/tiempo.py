personajes = [
    ["Dr. Emmett Brown", [1955, 2015, 1885, 2030]],
    ["Marty McFly", [1955, 1985, 2015, 2034]],
    ["Biff Tannen", [1955, 1985]]
]

print("=== Viajes por personaje ===")
for nombre, viajes in personajes:
    lista_anios = ", ".join(str(anio) for anio in viajes)
    print(f"{nombre}: {lista_anios}")

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
