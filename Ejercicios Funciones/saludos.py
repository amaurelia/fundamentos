def saludar(nombre, edad=None, carrera=None):
    mensaje = f"Hola {nombre}"

    if edad is not None:
        if edad < 18:
            mensaje += f"\nQue joven eres con {edad} anios!"
        else:
            mensaje += f"\nToda una experiencia con {edad} anios."

    if carrera is not None:
        mensaje += f"\nEstudias {carrera}, mucho exito!"

    return mensaje


# Pruebas sugeridas
print(saludar("Pepe"))
print()
print(saludar("Juan", 21, "Informatica"))
