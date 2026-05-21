print("=== Clase de Pociones — Hogwarts ===")
print()

# --- Garras de dragón (entero, más de 5) ---
while True:
    try:
        garras = int(input("Ingresa la cantidad de garras de dragón (más de 5): "))
        if garras <= 5:
            raise ValueError("La cantidad debe ser mayor a 5.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Plumas de fénix (entero, máximo 3) ---
while True:
    try:
        plumas = int(input("Ingresa el número de plumas de fénix (máximo 3): "))
        if plumas < 0:
            raise ValueError("El número de plumas no puede ser negativo.")
        if plumas > 3:
            raise ValueError("El número de plumas de fénix no puede superar 3.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Código mágico del grimorio (termina en dígito 0-9 o letra X) ---
while True:
    try:
        codigo = input("Ingresa el código mágico del grimorio (ej: Gretox, Grim48439): ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")
        ultimo = codigo[-1].upper()
        if not (ultimo.isdigit() or ultimo == "X"):
            raise ValueError("El código debe terminar en un número del 0 al 9 o la letra X.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print("=== Ingredientes registrados correctamente ===")
print(f"  Garras de dragón : {garras}")
print(f"  Plumas de fénix  : {plumas}")
print(f"  Código del grimorio: {codigo}")
print()
print("¡Que la poción salga perfecta, aprendiz!")
