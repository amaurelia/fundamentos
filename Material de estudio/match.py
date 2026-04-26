# match es una estructura de control que permite ejecutar un bloque de código dependiendo del valor de una variable
# En python, el match se implementa con la palabra clave match seguida de la variable que se quiere evaluar
# La sintaxis del match es la siguiente:
# match variable:
# case valor1:
# bloque de código para el caso valor1
# case valor2:
# bloque de código para el caso valor2
# case _:
# bloque de código para el caso por defecto (cuando no se cumple ningún caso anterior)
# Ejemplo de un match que evalúa el día de la semana
dia = input("Ingrese el día de la semana: ")
match dia:
    case "lunes":
        print("Hoy es lunes")
    case "martes":
        print("Hoy es martes")
    case "miércoles":
        print("Hoy es miércoles")
    case "jueves":
        print("Hoy es jueves")
    case "viernes":
        print("Hoy es viernes")
    case "sábado":
        print("Hoy es sábado")
    case "domingo":
        print("Hoy es domingo")
    case _:
        print("El día ingresado no es válido")