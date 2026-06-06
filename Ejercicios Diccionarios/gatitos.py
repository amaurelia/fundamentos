gatitos = {
    "Michi":  {"edad": 2, "color": "gris",    "juguetes": ["pelota", "raton de peluche"]},
    "Pelusa": {"edad": 4, "color": "blanco",  "juguetes": ["cuerda"]},
    "Canela": {"edad": 1, "color": "naranja", "juguetes": ["pluma", "pelota"]},
    "Luna":   {"edad": 3, "color": "negro",   "juguetes": ["raton de peluche"]}
}

# 1) Agregar Bigotes
gatitos["Bigotes"] = {"edad": 3, "color": "negro", "juguetes": ["pluma"]}
print("=== Bigotes agregado ===")
print(f"Total de gatitos: {len(gatitos)}")

# 2) Juguetes de Michi
print("\n=== Juguetes de Michi ===")
for juguete in gatitos["Michi"]["juguetes"]:
    print(f"- {juguete}")

# 3) Edad promedio
total_edad = 0
for datos in gatitos.values():
    total_edad += datos["edad"]
promedio = total_edad / len(gatitos)
print(f"\n=== Edad promedio: {promedio:.2f} anios ===")

# 4) Gato con mayor edad
print("\n=== Gato mas viejo ===")
nombre_mayor = ""
edad_mayor = -1
for nombre, datos in gatitos.items():
    if datos["edad"] > edad_mayor:
        edad_mayor = datos["edad"]
        nombre_mayor = nombre
print(f"{nombre_mayor} con {edad_mayor} anios")

# 5) Imprimir nombre, edad y color de cada gato
print("\n=== Todos los gatitos ===")
for nombre, datos in gatitos.items():
    print(f"El gatito {nombre} tiene {datos['edad']} anios y es de color {datos['color']}")

# 6) Gatos que no son negros y tienen pelota o raton de peluche
print("\n=== No son negros y tienen pelota o raton de peluche ===")
for nombre, datos in gatitos.items():
    tiene_juguete = "pelota" in datos["juguetes"] or "raton de peluche" in datos["juguetes"]
    if datos["color"] != "negro" and tiene_juguete:
        print(f"- {nombre}")
