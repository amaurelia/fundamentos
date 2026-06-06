lenguajes = [
    {
        "nombre": "Python",
        "tipo": "interpretado",
        "creado_en": 1991,
        "creador": "Guido van Rossum",
        "descripcion": "Lenguaje facil de aprender, con sintaxis clara y versatil",
        "popularidad": 9,
        "paradigmas": ["OOP", "funcional", "procedural"]
    },
    {
        "nombre": "Java",
        "tipo": "compilado",
        "creado_en": 1995,
        "creador": "James Gosling",
        "descripcion": "Lenguaje orientado a objetos, robusto y multiplataforma",
        "popularidad": 8,
        "paradigmas": ["OOP", "funcional"]
    },
    {
        "nombre": "C",
        "tipo": "compilado",
        "creado_en": 1972,
        "creador": "Dennis Ritchie",
        "descripcion": "Lenguaje de bajo nivel, base de muchos sistemas operativos",
        "popularidad": 7,
        "paradigmas": ["procedural"]
    }
]

# 1) Agregar JavaScript
lenguajes.append({
    "nombre": "JavaScript",
    "tipo": "interpretado",
    "creado_en": 1995,
    "creador": "Brendan Eich",
    "descripcion": "Lenguaje facil de aprender para el desarrollo web",
    "popularidad": 9,
    "paradigmas": ["OOP", "funcional"]
})
print("=== JavaScript agregado ===")
print(f"Total lenguajes: {len(lenguajes)}")

# 2) Lenguajes interpretados
print("\n=== Lenguajes interpretados ===")
for lang in lenguajes:
    if lang["tipo"] == "interpretado":
        print(f"- {lang['nombre']}")

# 3) Promedio de popularidad
total_pop = 0
for lang in lenguajes:
    total_pop += lang["popularidad"]
promedio = total_pop / len(lenguajes)
print(f"\n=== Promedio de popularidad: {promedio:.2f} ===")

# 4) Lenguajes creados despues de 1990
print("\n=== Creados despues de 1990 ===")
for lang in lenguajes:
    if lang["creado_en"] > 1990:
        print(f"- {lang['nombre']} ({lang['creado_en']})")

# 5) Lenguajes con "facil" en la descripcion
print("\n=== Lenguajes con 'facil' en descripcion ===")
for lang in lenguajes:
    if "facil" in lang["descripcion"].lower():
        print(f"- {lang['nombre']}: {lang['descripcion']}")
