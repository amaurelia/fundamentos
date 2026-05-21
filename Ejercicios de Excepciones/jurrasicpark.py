print("=== Control de Dinosaurios — Jurassic Park ===")
print()

# --- Velociraptors (entero, entre 5 y 20) ---
while True:
    try:
        velociraptors = int(input("Ingresa el número de Velociraptors (entre 5 y 20): "))
        if velociraptors < 5 or velociraptors > 20:
            raise ValueError("El número de Velociraptors debe estar entre 5 y 20.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- T-Rex (entero, máximo 2) ---
while True:
    try:
        trex = int(input("Ingresa el número de T-Rex (máximo 2): "))
        if trex < 0:
            raise ValueError("El número de T-Rex no puede ser negativo.")
        if trex > 2:
            raise ValueError("El número de T-Rex no puede superar 2.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Triceratops (entero, mínimo 3) ---
while True:
    try:
        triceratops = int(input("Ingresa el número de Triceratops (mínimo 3): "))
        if triceratops < 3:
            raise ValueError("El número de Triceratops debe ser al menos 3.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Nombre del recinto (debe incluir "Sector") ---
while True:
    try:
        recinto = input('Ingresa el nombre del recinto (debe incluir la palabra "Sector"): ').strip()
        if not recinto:
            raise ValueError("El nombre del recinto no puede estar vacío.")
        if "sector" not in recinto.lower():
            raise ValueError('El nombre del recinto debe incluir la palabra "Sector".')
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Tipo de alimento (debe incluir "carne" o "plantas") ---
while True:
    try:
        alimento = input('Ingresa el tipo de alimento (debe incluir "carne" o "plantas"): ').strip()
        if not alimento:
            raise ValueError("El tipo de alimento no puede estar vacío.")
        alimento_lower = alimento.lower()
        if "carne" not in alimento_lower and "plantas" not in alimento_lower:
            raise ValueError('El tipo de alimento debe incluir "carne" o "plantas".')
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print("=== Registro del recinto completado ===")
print(f"  Velociraptors : {velociraptors}")
print(f"  T-Rex         : {trex}")
print(f"  Triceratops   : {triceratops}")
print(f"  Recinto       : {recinto}")
print(f"  Alimento      : {alimento}")
print()
print("¡Mantén las cercas electrificadas, guardia!")
