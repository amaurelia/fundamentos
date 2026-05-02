# isalnum() verifica si todos los caracteres de una cadena son alfanuméricos
texto = "Hola123"
# Podemos usar el método isalnum para verificar si todos los caracteres de la cadena son alfanuméricos
if texto.isalnum():
    print("La cadena solo contiene caracteres alfanuméricos")
else:
    print("La cadena contiene otros caracteres además de alfanuméricos")