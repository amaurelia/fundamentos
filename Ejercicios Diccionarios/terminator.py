terminators = {
    "T-800": {
        "actor": "Arnold Schwarzenegger",
        "misiones": ["proteger a John Connor", "eliminar a Sarah Connor"]
    },
    "T-1000": {
        "actor": "Robert Patrick",
        "misiones": ["eliminar a John Connor"]
    }
}

# 1) Agregar T-X
terminators["T-X"] = {
    "actor": "Kristanna Loken",
    "misiones": ["eliminar a John Connor"]
}
print("=== T-X agregado ===")
print(f"Modelos registrados: {list(terminators.keys())}")

# 2) Misiones del T-800
print("\n=== Misiones del T-800 ===")
for mision in terminators["T-800"]["misiones"]:
    print(f"- {mision}")

# 3) Modelo y actor de cada terminator
print("\n=== Modelos y actores ===")
for modelo, datos in terminators.items():
    print(f"El modelo {modelo} fue interpretado por {datos['actor']}")

# 4) Cantidad de modelos registrados
print(f"\n=== Total de modelos: {len(terminators)} ===")
