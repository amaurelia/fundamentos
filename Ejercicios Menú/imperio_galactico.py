ESPECIES_VALIDAS = [
    "humano", "twi'lek", "rodiano", "zabrak", "mirialan",
    "nautolan", "togruta", "keldor", "weequay", "gran",
    "duros", "sulustano", "bothan", "chiss", "devaronian"
]

postulantes = []

def ingresar_postulante():
    print()
    print("--- Registro de nuevo postulante ---")

    # Nombre
    while True:
        try:
            nombre = input("Nombre: ").strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío.")
            if not nombre.replace(" ", "").isalpha():
                raise ValueError("El nombre solo puede contener letras.")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break

    # Edad
    while True:
        try:
            edad = int(input("Edad: "))
            if edad <= 0 or edad > 150:
                raise ValueError("La edad debe ser un número entre 1 y 150.")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break

    # Especie
    print(f"Especies válidas: {', '.join(ESPECIES_VALIDAS)}")
    while True:
        try:
            especie = input("Especie: ").strip().lower()
            if not especie:
                raise ValueError("La especie no puede estar vacía.")
            if especie not in ESPECIES_VALIDAS:
                raise ValueError(f"Especie no reconocida. Elige una de la lista.")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break

    # Sensible a la fuerza
    while True:
        try:
            fuerza_input = input("¿Es sensible a la Fuerza? (si / no): ").strip().lower()
            if fuerza_input not in ("si", "sí", "no"):
                raise ValueError('Debes responder "si" o "no".')
            sensible = fuerza_input in ("si", "sí")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break

    postulante = {
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "sensible": sensible
    }
    postulantes.append(postulante)
    print(f"\n✓ Postulante {nombre} registrado con éxito.")


def es_calificado(p):
    return p["edad"] < 25 and p["especie"] == "humano" and p["sensible"]


def mostrar_todos():
    print()
    if not postulantes:
        print("No hay postulantes registrados aún.")
        return
    print("--- Todos los postulantes ---")
    for i, p in enumerate(postulantes, 1):
        fuerza = "Sí" if p["sensible"] else "No"
        calificado = "✓ CALIFICADO" if es_calificado(p) else "✗ No calificado"
        print(f"  {i}. {p['nombre']} | Edad: {p['edad']} | Especie: {p['especie'].capitalize()} | Fuerza: {fuerza} | {calificado}")


def mostrar_calificados():
    print()
    calificados = [p for p in postulantes if es_calificado(p)]
    if not calificados:
        print("No hay postulantes calificados.")
        return
    print("--- Postulantes calificados ---")
    for i, p in enumerate(calificados, 1):
        print(f"  {i}. {p['nombre']} | Edad: {p['edad']}")


def mostrar_porcentaje():
    print()
    if not postulantes:
        print("No hay postulantes registrados aún.")
        return
    total = len(postulantes)
    calificados = sum(1 for p in postulantes if es_calificado(p))
    porcentaje = (calificados / total) * 100
    print(f"Total de postulantes : {total}")
    print(f"Calificados          : {calificados}")
    print(f"Porcentaje           : {porcentaje:.1f}%")


# --- Programa principal ---
print("=" * 50)
print("  IMPERIO GALÁCTICO — Reclutamiento de Pilotos")
print("        Cazas TIE Fighter — Clase Elite")
print("=" * 50)

while True:
    print()
    print("--- MENÚ ---")
    print("1. Ingresar nuevo postulante")
    print("2. Mostrar todos los postulantes")
    print("3. Mostrar postulantes calificados")
    print("4. Porcentaje de postulantes calificados")
    print("5. Salir")
    print()

    try:
        opcion = input("Selecciona una opción (1-5): ").strip()
        if opcion not in ("1", "2", "3", "4", "5"):
            raise ValueError("Debes ingresar un número entre 1 y 5.")
    except ValueError as e:
        print(f"Error: {e}")
        continue

    if opcion == "1":
        ingresar_postulante()
    elif opcion == "2":
        mostrar_todos()
    elif opcion == "3":
        mostrar_calificados()
    elif opcion == "4":
        mostrar_porcentaje()
    elif opcion == "5":
        print()
        print("El Imperio te observa. Que la oscuridad te guíe.")
        break
