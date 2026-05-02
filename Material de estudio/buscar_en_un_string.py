# Buscar en un string

texto = "Hola mundo"
# Podemos usar el operador in para verificar si un elemento está presente en una secuencia, como una cadena de texto
if "Hola" in texto:
    print("La palabra 'Hola' está presente en el texto")
    
# También podemos usar el método find para buscar la posición de una subcadena dentro de una cadena de texto
posicion = texto.find("mundo")
if posicion != -1:
    print("La palabra 'mundo' está presente en el texto en la posición:", posicion)
# El método find devuelve -1 si la subcadena no se encuentra en la cadena de texto
