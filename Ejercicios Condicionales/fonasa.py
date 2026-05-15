print("=== Descuento FONASA ===")
print()

tramo = input("Tramo FONASA (A, B, C o D): ").strip().upper()
edad = int(input("Edad: "))

print()

if tramo == "D":
    print("Tu descuento es: 20%")
elif tramo == "C" and edad >= 18:
    print("Tu descuento es: 15%")
elif tramo == "C" and edad < 18:
    print("Tu descuento es: 18%")
elif tramo in ("A", "B") and edad < 65:
    print("Tu descuento es: 25%")
elif tramo in ("A", "B") and edad >= 65:
    print("Tu descuento es: 40%")
else:
    print("Tramo no reconocido.")
