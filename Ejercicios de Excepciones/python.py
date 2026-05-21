import re

print("=== Nombre de archivo Python ===")
print()

CARACTERES_INVALIDOS = set("áéíóúàèìòùâêîôûãõäëïöüñÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÄËÏÖÜÑ ")

while True:
    try:
        nombre = input("Ingresa el nombre de tu archivo Python (ej: mi_programa.py): ").strip()

        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")

        if not nombre.endswith(".py"):
            raise ValueError('El nombre debe terminar con ".py".')

        if len(nombre) >= 20:
            raise ValueError("El nombre debe tener menos de 20 caracteres en total.")

        if not re.match(r'^[a-zA-Z0-9]+\.py$', nombre):
            raise ValueError(
                "El nombre solo puede contener letras (sin ñ ni tildes) y números, sin espacios."
            )

    except ValueError as e:
        print(f"Error: {e}")
    else:
        break

print()
print(f'¡Perfecto! Tu archivo se llamará: "{nombre}"')
print("¡Listo para guardar!")
