# Un arreglo es una estructura de datos que almacena una colección de elementos del mismo tipo.
# En Python, los arreglos se implementan como listas, que pueden contener elementos de cualquier
# tipo, pero en este contexto nos referiremos a ellas como arreglos para mantener la terminología.
# Un arreglo se define utilizando corchetes [] y los elementos se separan por comas.
# Ejemplo de un arreglo de enteros
numeros = [10, 20, 30, 40, 50]
# Ejemplo de un arreglo de cadenas
nombres = ["Alice", "Bob", "Charlie", "Diana"]
# Acceso a elementos
print(numeros[0])  # Imprime 10
print(nombres[2])  # Imprime "Charlie"
# Modificación de elementos
numeros[1] = 25
print(numeros)  # Imprime [10, 25, 30, 40, 50]
# Agregar elementos al final del arreglo
numeros.append(60)
print(numeros)  # Imprime [10, 25, 30, 40, 50, 60]
# Eliminar elementos por valor
numeros.remove(30)
print(numeros)  # Imprime [10, 25, 40, 50, 60]
# Eliminar elementos por índice
del numeros[0]
print(numeros)  # Imprime [25, 40, 50, 60]
# Longitud del arreglo
print(len(numeros))  # Imprime 4
# Iterar sobre los elementos del arreglo
for numero in numeros:
    print(numero)

# funciones utiles para arreglos
# len(arreglo) -> devuelve la cantidad de elementos en el arreglo
# append(elemento) -> agrega un elemento al final del arreglo
# remove(elemento) -> elimina la primera ocurrencia del elemento en el arreglo
# del arreglo[indice] -> elimina el elemento en la posición dada por indice
# index(elemento) -> devuelve el índice de la primera ocurrencia del elemento
# in -> operador para verificar si un elemento existe en el arreglo
# sort() -> ordena los elementos del arreglo (solo para tipos comparables)
# reverse() -> invierte el orden de los elementos en el arreglo
# pop(indice) -> elimina y devuelve el elemento en la posición dada por indice (o el último si no se especifica)
# clear() -> elimina todos los elementos del arreglo
# min(arreglo) -> devuelve el elemento mínimo del arreglo (solo para tipos comparables)
# max(arreglo) -> devuelve el elemento máximo del arreglo (solo para tipos comparables)
# sum(arreglo) -> devuelve la suma de los elementos del arreglo (solo para números)
