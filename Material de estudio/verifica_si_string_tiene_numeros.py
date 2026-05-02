# isdigit() verifica si todos los caracteres de una cadena son números
texto = "12345"
# Podemos usar el método isdigit para verificar si todos los caracteres de la cadena son números
if texto.isdigit():
    print("La cadena solo contiene números")
else:
    print("La cadena contiene otros caracteres además de números")