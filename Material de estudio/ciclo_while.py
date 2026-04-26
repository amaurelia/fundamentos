# Un ciclo while es una estructura de control que permite ejecutar un bloque de código mientras se cumpla una condición determinada
# La sintaxis del ciclo while es la siguiente:

# while condición:
#   El bloque de código dentro del while se ejecutará mientras la condición sea verdadera

# Ejemplo de un ciclo while que imprime los números del 0 al 9
i = 0
while i < 10:
    print(i)
    i += 1
    
# Ejemplo de un ciclo while que continúa ejecutándose mientras el usuario ingrese "s"
opcion = "s"
while opcion == "s":
    print("El ciclo se ejecuta")
    opcion = input("¿Desea continuar? (s/n): ")
      
# break es una palabra clave que se usa para salir de un ciclo while antes de que la condición se vuelva falsa
contador = 0
while True:
    print(contador)
    contador += 1
    if contador >= 10:
        break

# Es importante tener cuidado con los ciclos while, ya que si la condición nunca se vuelve falsa, el ciclo se ejecutará indefinidamente, lo que se conoce como un ciclo infinito
# Por ejemplo, el siguiente código es un ciclo infinito porque la condición siempre es verdadera
while True:
    print("Este ciclo se ejecuta para siempre")