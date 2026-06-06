peleadores = [
    {"nombre": "Goku",    "raza": "Saiyajin",     "poder_de_pelea": 80000},
    {"nombre": "Vegeta",  "raza": "Saiyajin",     "poder_de_pelea": 60000},
    {"nombre": "Krillin", "raza": "Humano",        "poder_de_pelea": 35000},
    {"nombre": "Piccolo", "raza": "Namekusejin",   "poder_de_pelea": 70000},
    {"nombre": "Gohan",   "raza": "Mestizo",       "poder_de_pelea": 75000}
]

# 1) Peleadores con poder de pelea mayor a 40.000
print("=== Peleadores con poder > 40.000 ===")
for p in peleadores:
    if p["poder_de_pelea"] > 40000:
        print(f"- {p['nombre']} ({p['poder_de_pelea']})")

# 2) Peleadores de la raza Saiyajin
print("\n=== Peleadores Saiyajin ===")
for p in peleadores:
    if p["raza"] == "Saiyajin":
        print(f"- {p['nombre']}")

# 3) Razas registradas sin repetir
print("\n=== Razas registradas ===")
razas = []
for p in peleadores:
    if p["raza"] not in razas:
        razas.append(p["raza"])
for raza in razas:
    print(f"- {raza}")

# 4) Peleador con mayor poder de pelea
print("\n=== Peleador mas poderoso ===")
mas_poderoso = peleadores[0]
for p in peleadores:
    if p["poder_de_pelea"] > mas_poderoso["poder_de_pelea"]:
        mas_poderoso = p
print(f"{mas_poderoso['nombre']} con {mas_poderoso['poder_de_pelea']} puntos")

# 5) Agregar a Yamcha
peleadores.append({"nombre": "Yamcha", "raza": "Humano", "poder_de_pelea": 8000})
print("\n=== Yamcha agregado ===")
print(f"Total de peleadores: {len(peleadores)}")
print(f"Ultimo: {peleadores[-1]}")
