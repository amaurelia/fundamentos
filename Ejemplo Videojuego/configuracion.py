# --- Ventana ---
ANCHO     = 800
ALTO      = 600

# --- Personaje ---
VELOCIDAD = 5
RADIO     = 20

# --- Colores del fondo ---
COLOR_CESPED_CLARO  = "#4a7c3f"
COLOR_CESPED_OSCURO = "#3d6b35"

# --- Colores del personaje ---
COLOR_CUERPO       = "#1565c0"
COLOR_BORDE_CUERPO = "#0d47a1"
COLOR_CARA         = "#ffcc80"
COLOR_BORDE_CARA   = "#e65100"

# --- Colores de los árboles ---
COLOR_SOMBRA_ARBOL = "#2d5a27"
COLOR_COPA         = "#2e7d32"
COLOR_BORDE_COPA   = "#1b5e20"
COLOR_TRONCO       = "#5d4037"
RADIO_ARBOL        = 18

# --- Colores de los barriles ---
COLOR_BARRIL     = "#8B4513"
COLOR_BARRIL_ARO = "#5C3317"
RADIO_BARRIL     = 14

# --- Lago ---
LAGO_X  = 620
LAGO_Y  = 430
LAGO_RX = 110   # radio horizontal
LAGO_RY =  65   # radio vertical
COLOR_LAGO        = "#1a6fa8"
COLOR_LAGO_BORDE  = "#0d47a1"
COLOR_LAGO_BRILLO = "#4fc3f7"

# --- Casa (exterior) ---
CASA_X = 290    # esquina superior izquierda
CASA_Y =  50
CASA_W = 130
CASA_H = 100
COLOR_CASA_PARED  = "#d4a064"
COLOR_CASA_TECHO  = "#8B2500"
COLOR_CASA_PUERTA = "#5d3a1a"

# --- Interior ---
COLOR_PISO      = "#c8a96e"
COLOR_PISO_ALT  = "#b8995e"
COLOR_PARED_INT = "#7a5c2e"
SALIDA_INT_X    = ANCHO // 2   # X de la puerta de salida interior

# Muebles: (x, y, ancho, alto, color, etiqueta)
MUEBLES = [
    (120, 100, 150,  60, "#5d4037", "mesa"),
    (120, 160,  40,  40, "#4e342e", "silla"),
    (230, 160,  40,  40, "#4e342e", "silla"),
    (590,  80,  90, 130, "#455a64", "armario"),
    (250, 380, 220,  25, "#37474f", "estante"),
    (100, 300,  60,  60, "#bf8040", "cañon"),
]

# --- Posiciones de los árboles (x, y) ---
# Alejados del lago (620,430,rx=110,ry=65) y de la casa (290,50,130,100)
ARBOLES = [
    (100,  80),
    (500, 170),
    (700,  90),
    (200, 450),
    (450, 340),
    (150, 300),
    (700, 250),
    (370, 470),
]

# --- Posiciones de los barriles (x, y) ---
BARRILES = [
    (460, 230),
    (250, 300),
    (560, 250),
    (700, 180),
    (100, 480),
]


