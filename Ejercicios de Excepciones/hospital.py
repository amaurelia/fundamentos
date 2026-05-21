print("=== Registro de Paciente — Hospital ===")
print()

# --- Nombre (texto, menos de 10 letras) ---
while True:
    try:
        nombre = input("Ingresa el nombre del paciente: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        solo_letras = nombre.replace(" ", "")
        if not solo_letras.isalpha():
            raise ValueError("El nombre solo debe contener letras.")
        if len(solo_letras) >= 10:
            raise ValueError("El nombre debe tener menos de 10 letras.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Edad (entero, menor a 120) ---
while True:
    try:
        edad = int(input("Ingresa la edad del paciente: "))
        if edad < 0:
            raise ValueError("La edad no puede ser negativa.")
        if edad >= 120:
            raise ValueError("La edad debe ser menor a 120 años.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- Peso (decimal, mayor a 0) ---
while True:
    try:
        peso = float(input("Ingresa el peso del paciente (kg): "))
        if peso <= 0:
            raise ValueError("El peso debe ser mayor a 0.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

# --- RUT (termina en dígito 0-9 o letra K) ---
while True:
    try:
        rut = input("Ingresa el RUT del paciente (ej: 12345678-9 o 12345678-K): ").strip()
        if not rut:
            raise ValueError("El RUT no puede estar vacío.")
        ultimo = rut[-1].upper()
        if not (ultimo.isdigit() or ultimo == "K"):
            raise ValueError("El RUT debe terminar en un dígito del 0 al 9 o la letra K.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print("=== Ficha del paciente registrada ===")
print(f"  Nombre : {nombre}")
print(f"  Edad   : {edad} años")
print(f"  Peso   : {peso} kg")
print(f"  RUT    : {rut}")
print()
print("¡Datos guardados correctamente!")
