# Un ciclo for es una estructura de control que permite ejecutar un bloque de código un número determinado de veces
# En python, el ciclo for se implementa con la palabra clave for seguida de una variable y la función range
# La función range genera una secuencia de números, que se pueden usar para iterar sobre una secuencia de elementos
# La sintaxis del ciclo for es la siguiente:

# for variable in range(inicio, fin, paso):

# El ciclo for se ejecutará desde el valor de inicio hasta el valor de fin, incrementando el valor de la variable en cada iteración según el paso
# Si no se especifica el valor de inicio, se asume que es 0
# Si no se especifica el valor de paso, se asume que es 1
# Ejemplo de un ciclo for que imprime los números del 0 al 9
for i in range(10):
    print(i)
    
# Ejemplo de un ciclo for que imprime los números del 1 al 10
for i in range(1, 11):
    print(i)
    
# Ejemplo de un ciclo for que imprime los números del 0 al 10 de 2 en 2
for i in range(0, 11, 2):
    print(i)
    
# break es una palabra clave que se usa para salir de un ciclo for antes de que se complete todas las iteraciones
for i in range(10):
    if i == 5:
        break
    print(i)
