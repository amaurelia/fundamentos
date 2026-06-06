misterios = [
    {"id": 1,  "titulo": "El Triangulo de las Bermudas",   "categoria": "paranormal",    "estado": "sin resolver"},
    {"id": 2,  "titulo": "El caso del Zodiaco",            "categoria": "criminal",       "estado": "en investigacion"},
    {"id": 3,  "titulo": "La ciudad perdida de Atlantida", "categoria": "historico",      "estado": "sin resolver"},
    {"id": 4,  "titulo": "El monstruo del Lago Ness",      "categoria": "paranormal",    "estado": "sin resolver"},
    {"id": 5,  "titulo": "El asesinato de JFK",            "categoria": "criminal",       "estado": "sin resolver"},
    {"id": 6,  "titulo": "Luces de Phoenix",               "categoria": "extraterrestre", "estado": "en investigacion"},
    {"id": 7,  "titulo": "El misterio de Roanoke",         "categoria": "historico",      "estado": "sin resolver"},
    {"id": 8,  "titulo": "El hombre de Somerton",          "categoria": "criminal",       "estado": "sin resolver"},
    {"id": 9,  "titulo": "Area 51",                        "categoria": "extraterrestre", "estado": "en investigacion"},
    {"id": 10, "titulo": "El Yeti",                        "categoria": "paranormal",    "estado": "sin resolver"}
]

# 1) Misterios paranormales
print("=== Misterios paranormales ===")
for m in misterios:
    if m["categoria"] == "paranormal":
        print(f"- {m['titulo']}")

# 2) Cantidad sin resolver
sin_resolver = 0
for m in misterios:
    if m["estado"] == "sin resolver":
        sin_resolver += 1
print(f"\n=== Sin resolver: {sin_resolver} ===")

# 3) Titulo mas largo
print("\n=== Titulo mas largo ===")
mas_largo = misterios[0]
for m in misterios:
    if len(m["titulo"]) > len(mas_largo["titulo"]):
        mas_largo = m
print(f"{mas_largo['titulo']} ({len(mas_largo['titulo'])} caracteres)")

# 4) Categorias distintas
print("\n=== Categorias distintas ===")
categorias = []
for m in misterios:
    if m["categoria"] not in categorias:
        categorias.append(m["categoria"])
print(f"Total: {len(categorias)}")
for cat in categorias:
    print(f"- {cat}")

# 5) Imprimir frase por cada misterio
print("\n=== Descripcion de cada misterio ===")
for m in misterios:
    print(f"{m['titulo']} es un misterio de la categoria {m['categoria']} y esta con estado {m['estado']}")

# 6) Cambiar estado del misterio con id 5 a "resuelto"
for m in misterios:
    if m["id"] == 5:
        m["estado"] = "resuelto"
        print(f"\n=== Misterio {m['id']} actualizado: {m['titulo']} -> {m['estado']} ===")
        break

# 7) Mostrar toda la informacion del misterio con id 9
print("\n=== Informacion del misterio id 9 ===")
for m in misterios:
    if m["id"] == 9:
        print(f"ID       : {m['id']}")
        print(f"Titulo   : {m['titulo']}")
        print(f"Categoria: {m['categoria']}")
        print(f"Estado   : {m['estado']}")
        break
