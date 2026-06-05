def pedir_ganador(pelea, a, b):
    while True:
        print(f"\nCombate {pelea}: {a} vs {b}")
        ganador = input("Escribe el nombre del ganador: ").strip()

        if ganador == a or ganador == b:
            return ganador

        print("Ganador invalido. Debe ser uno de los dos peleadores.")


peleadores = ["Mr.Bison", "Ryo", "Ken", "Chunly", "Zanguief", "Guile", "Vega", "Dalshim"]
print("=== Torneo Street Fighter ===")
print("Peleadores:")
for i, nombre in enumerate(peleadores, start=1):
    print(f"P{i}: {nombre}")

# Cuartos de final
g1 = pedir_ganador(1, peleadores[0], peleadores[2])
g2 = pedir_ganador(2, peleadores[1], peleadores[3])
g3 = pedir_ganador(3, peleadores[4], peleadores[6])
g4 = pedir_ganador(4, peleadores[5], peleadores[7])

# Semifinales
g5 = pedir_ganador(5, g1, g3)
g6 = pedir_ganador(6, g2, g4)

# Final
campeon = pedir_ganador(7, g5, g6)

print("\n=== Resultado final ===")
print(f"Campeon del torneo: {campeon}")
