import random

def mostrar_color_random():
    # Generar valores aleatorios para R, G y B
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # ANSI escape para fondo RGB
    inicio = f"\033[48;2;{r};{g};{b}m"
    texto  = f"   RGB({r},{g},{b})   "  # texto a mostrar
    fin    = "\033[0m"
    print(inicio + texto + fin)

# Ejemplo: mostrar 5 colores aleatorios
for _ in range(5):
    mostrar_color_random()
