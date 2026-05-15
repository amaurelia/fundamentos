print("=== El Videojuego Divertido ===")
print()

ram = int(input("RAM disponible (GB): "))
tarjeta = input("¿Tienes tarjeta de video? (True/False): ")
tarjeta = tarjeta.strip().lower() == "true"

print()

if not tarjeta:
    print("El juego no funciona en tu computador.")
elif ram < 2:
    print("El juego funciona a 30 FPS.")
else:
    print("El juego funciona a 60 FPS.")
