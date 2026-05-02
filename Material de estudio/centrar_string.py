# center permite centrar un string dentro de un ancho especificado, rellenando con espacios a ambos lados
texto = "Hola mundo"

# Podemos usar el método center para centrar el texto dentro de un ancho de 20 caracteres   
texto_centrado = texto.center(20)
print(texto_centrado)  # "    Hola mundo     "

# También podemos especificar un carácter de relleno diferente a los espacios, como el guion (-)
texto_centrado_con_guion = texto.center(20, "-")
print(texto_centrado_con_guion)  # "----Hola mundo-----"
