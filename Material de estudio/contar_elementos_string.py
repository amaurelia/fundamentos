# count permite contar el número de veces que un elemento aparece en una secuencia, como una cadena de texto
texto = "Hola mundo"

# Podemos usar el método count para contar cuántas veces aparece una subcadena en una cadena de texto
contador = texto.count("o")
print("La letra 'o' aparece", contador, "veces en el texto")

# También podemos usar el método count para contar cuántas veces aparece una palabra en una cadena de texto
contador_palabra = texto.count("mundo")
print("La palabra 'mundo' aparece", contador_palabra, "veces en el texto")
