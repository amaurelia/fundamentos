print("=== La Batalla Contra el Rey del Mal ===")
print()

armadura = input("¿Tienes la armadura del destino? (True/False): ")
armadura = armadura.strip().lower() == "true"

espada = input("¿Tienes la espada infinita? (True/False): ")
espada = espada.strip().lower() == "true"

nivel = int(input("Nivel del héroe: "))

print()

if nivel < 40:
    print("No tienes ninguna oportunidad contra el rey del mal.")
elif nivel < 80 and espada:
    print("Probabilidad de vencer: 20%")
elif nivel >= 80 and espada and armadura:
    print("Probabilidad de vencer: 60%")
elif nivel >= 80 and espada:
    print("Probabilidad de vencer: 40%")
else:
    print("Probabilidad de vencer: 1%")
