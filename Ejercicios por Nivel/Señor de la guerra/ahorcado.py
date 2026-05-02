# Crea el siguiente juego del ahorcado
# El programa debe elegir una palabra al azar de una lista de palabras
# El jugador debe adivinar la palabra letra por letra
# El jugador tiene un número limitado de intentos para adivinar la palabra
import random
palabras = ["python", "programacion", "ahorcado", "juego", "desarrollo"]
palabra_secreta = random.choice(palabras)
letras_adivinadas = []
intentos = 6
while intentos > 0:
    letra = input("Ingresa una letra: ")
    if letra in palabra_secreta:
        letras_adivinadas.append(letra)
        print("¡Correcto!")
    else:
        intentos -= 1
        print("¡Incorrecto! Te quedan", intentos, "intentos.")
    
    palabra_mostrada = ""
    for letra_palabra in palabra_secreta:
        if letra_palabra in letras_adivinadas:
            palabra_mostrada += letra_palabra
        else:
            palabra_mostrada += "_"
    
    print("Palabra:", palabra_mostrada)
    
    if "_" not in palabra_mostrada:
        print("¡Felicidades! Has adivinado la palabra secreta:", palabra_secreta)
        break
else:
    print("¡Has perdido! La palabra secreta era:", palabra_secreta)
