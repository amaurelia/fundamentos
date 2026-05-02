# Para agregar color a la salida de la terminal, podemos usar códigos de escape ANSI.
# Estos códigos comienzan con \033[ y terminan con m, y pueden incluir números que representan diferentes colores y estilos.
# Por ejemplo, para cambiar el color del texto a rojo, podemos usar \033[31m, y para volver al color normal, usamos \033[0m.
# Aquí hay un ejemplo de cómo usar estos códigos para mostrar texto en diferentes colores:
# Colores de texto:
# \033[30m - Negro
# \033[31m - Rojo
# \033[32m - Verde
# \033[33m - Amarillo
# \033[34m - Azul
# \033[35m - Magenta
# \033[36m - Cian
# \033[37m - Blanco
# Colores de fondo:
# \033[40m - Fondo negro
# \033[41m - Fondo rojo
# \033[42m - Fondo verde
# \033[43m - Fondo amarillo
# \033[44m - Fondo azul
# \033[45m - Fondo magenta
# \033[46m - Fondo cian
# \033[47m - Fondo blanco
# Ejemplo de uso:
rojo  = "\033[31m"  # Código para texto rojo
verde = "\033[32m"  # Código para texto verde
azul  = "\033[34m"  # Código para texto azul
reset = "\033[0m"   # Código para resetear el color
print(rojo + "Este texto es rojo" + reset)
print(verde + "Este texto es verde" + reset)
print(azul + "Este texto es azul" + reset)

# También podemos combinar colores de texto y fondo:
print("\033[31m\033[47m" + "Texto rojo con fondo blanco" + reset)
print("\033[32m\033[40m" + "Texto verde con fondo negro" + reset)
print("\033[34m\033[43m" + "Texto azul con fondo amarillo" + reset)
print("\033[35m\033[46m" + "Texto magenta con fondo cian" + reset)
print("\033[36m\033[45m" + "Texto cian con fondo magenta" + reset)
