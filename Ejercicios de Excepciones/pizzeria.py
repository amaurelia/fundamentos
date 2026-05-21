print("=== Pedido de Pizzería ===")
print()

TAMANIOS = ["pequeña", "mediana", "grande"]

# --- Tamaño ---
while True:
    try:
        tamano = input("Ingresa el tamaño de la pizza (pequeña / mediana / grande): ").strip().lower()
        if tamano not in TAMANIOS:
            raise ValueError('El tamaño debe ser "pequeña", "mediana" o "grande".')
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Cantidad ---
while True:
    try:
        cantidad = int(input("Ingresa la cantidad de pizzas (entre 1 y 10): "))
        if cantidad < 1 or cantidad > 10:
            raise ValueError("La cantidad debe estar entre 1 y 10.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Teléfono ---
while True:
    try:
        telefono = input("Ingresa el número de teléfono (9 dígitos): ").strip()
        if not telefono.isdigit() or len(telefono) != 9:
            raise ValueError("El teléfono debe tener exactamente 9 dígitos numéricos.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Hora de entrega ---
while True:
    try:
        hora = int(input("Ingresa la hora de entrega (entre 10 y 22): "))
        if hora < 10 or hora > 22:
            raise ValueError("La hora de entrega debe estar entre 10 y 22.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print("=== Pedido registrado ===")
print(f"  Tamaño    : {tamano}")
print(f"  Cantidad  : {cantidad}")
print(f"  Teléfono  : {telefono}")
print(f"  Hora      : {hora}:00")
print()
print("¡Tu pizza estará lista pronto!")
