print("=== Registro de Jugador de Fútbol ===")
print()

POSICIONES = ["portero", "defensa", "centrocampista", "delantero"]

# --- Nombre ---
while True:
    try:
        nombre = input("Ingresa el nombre del jugador: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras.")
        if len(nombre) > 20:
            raise ValueError("El nombre debe tener máximo 20 caracteres.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Número de camiseta ---
while True:
    try:
        camiseta = int(input("Ingresa el número de camiseta (entre 1 y 99): "))
        if camiseta < 1 or camiseta > 99:
            raise ValueError("El número de camiseta debe estar entre 1 y 99.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Posición ---
while True:
    try:
        posicion = input("Ingresa la posición (portero / defensa / centrocampista / delantero): ").strip().lower()
        if posicion not in POSICIONES:
            raise ValueError('La posición debe ser "portero", "defensa", "centrocampista" o "delantero".')
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Goles ---
while True:
    try:
        goles = int(input("Ingresa los goles anotados (0 o más): "))
        if goles < 0:
            raise ValueError("Los goles no pueden ser negativos.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print("=== Ficha del jugador registrada ===")
print(f"  Nombre    : {nombre}")
print(f"  Camiseta  : #{camiseta}")
print(f"  Posición  : {posicion.capitalize()}")
print(f"  Goles     : {goles}")
print()
print("¡Jugador inscrito en el equipo!")
