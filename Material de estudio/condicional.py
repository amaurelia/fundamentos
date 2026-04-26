# Un condicional es una estructura de control que permite ejecutar un bloque de código solo si se cumple una condición determinada
# En python, el condicional se implementa con la palabra clave if, elif y else

a = 10
b= 5

if a > 5:
    print("a es mayor que 5")
    
# El bloque de código dentro del if se ejecutará solo si la condición a > 5 es verdadera
# Si queremos ejecutar otro bloque de código si la condición no se cumple, podemos usar el else
if a > 5:
    print("a es mayor que 5")
else:
    print("a es menor o igual que 5")
    
# Si queremos evaluar varias condiciones, podemos usar el elif
if a > 10:
    print("a es mayor que 10")
elif a > 5:
    print("a es mayor que 5 pero menor o igual que 10")
else:
    print("a es menor o igual que 5")

# También podemos usar el operador lógico and para evaluar varias condiciones al mismo tiempo
if a > 5 and b < 10:
    print("a es mayor que 5 y b es menor que 10")

# El operador lógico or se usa para evaluar si al menos una de las condiciones es verdadera
if a > 5 or b < 10:
    print("a es mayor que 5 o b es menor que 10")
    
# El operador lógico not se usa para negar una condición
if not a > 5:
    print("a no es mayor que 5")
    
texto = "Hola mundo"
# Podemos usar el operador in para verificar si un elemento está presente en una secuencia, como una cadena de texto
if "Hola" in texto:
    print("La palabra 'Hola' está presente en el texto")