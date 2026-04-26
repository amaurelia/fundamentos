# una excepción es un error que ocurre durante la ejecución de un programa
# en python, las excepciones se manejan con la estructura try-except
# la sintaxis de try-except es la siguiente:

# try:
#   bloque de código que puede generar una excepción
# except TipoDeExcepcion:
#   bloque de código que se ejecuta si se genera una excepción del tipo especificado

try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Ocurrió un error, no se puede dividir por cero")
else:
    print("Sin errores, el resultado es:", resultado)
finally:
    print("Este bloque se ejecuta siempre, independientemente de si se generó una excepción o no")