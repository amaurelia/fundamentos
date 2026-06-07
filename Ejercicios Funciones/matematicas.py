def sumar(x, y):
    resultado = x + y
    if resultado > 100:
        print("El resultado es demasiado grande")
    return resultado


def restar(x, y):
    resultado = x - y
    if resultado < 0:
        print("El resultado es negativo")
    return resultado


def multiplicar(x, y):
    resultado = x * y
    if resultado > 100:
        print("El resultado es demasiado grande")
    return resultado


def dividir(x, y):
    if y == 0:
        print("No se puede dividir por cero")
        return None
    return round(x / y, 2)


# Pruebas solicitadas
print("sumar(3, 12) =", sumar(3, 12))
print("restar(4, 9) =", restar(4, 9))
print("multiplicar(13, 9) =", multiplicar(13, 9))
print("dividir(11, 5) =", dividir(11, 5))
