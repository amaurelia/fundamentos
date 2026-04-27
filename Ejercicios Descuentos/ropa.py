print("=== Tienda de Ropa ===")
print()


print("Ropa disponible:")
print("Faldas — $10.000")
print("Blusas — $5.500")
print("Pantalones — $5.000")
print("Chaquetas — $14.000")
print()


faldas = input("¿Cuántas faldas desea comprar?: ")
blusas = input("¿Cuántas blusas desea comprar?: ")
pantalones = input("¿Cuántos pantalones desea comprar?: ")
chaquetas = input("¿Cuántas chaquetas desea comprar?: ")

total_faldas = 10000 * int(faldas)
total_blusas = 5500 * int(blusas)
total_pantalones = 5000 * int(pantalones)
total_chaquetas = 14000 * int(chaquetas)
total = total_faldas + total_blusas + total_pantalones + total_chaquetas

print()
print(f"Resumen de compra:")
print(f"Faldas: {faldas} x $10.000 = ${total_faldas}")
print(f"Blusas: {blusas} x $5.500 = ${total_blusas}")
print(f"Pantalones: {pantalones} x $5.000 = ${total_pantalones}")
print(f"Chaquetas: {chaquetas} x $14.000 = ${total_chaquetas}")
print(f"Total sin descuento: ${total}")
print()


codigo = input("Ingrese un código de descuento (si tiene): ")

match codigo:
    case "PRIMAVERAVERANO":
        print("¡Descuento del 15% aplicado por código PRIMAVERAVERANO!")
        descuento = 0.15
    case "FUNDAMENTOS":
        print("¡Descuento del 20% aplicado por código FUNDAMENTOS!")
        descuento = 0.20
    case "ALAMODA":
        print("¡Descuento del 25% aplicado por código ALAMODA!")
        descuento = 0.25
    case _:
        print("No se aplicó ningún descuento.")
        descuento = 0.0

total_final = total * (1 - descuento)
print(f"Total a pagar: ${round(total_final)}.")
print()
