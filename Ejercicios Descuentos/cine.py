print("=== Compra de Entradas ===")
print()

cantidad_total = 0
tipo = input("Seleccione un tipo de entrada (1:Estreno-6.000 | 2:Normal-4.500): ")
print()

if( tipo == "1" ):
    tipo = "Estreno"
    precio = 6000
else:
    tipo = "Normal"
    precio = 4500
    
cantidad = int(input(f"¿Cuántas entradas {tipo} desea comprar?: "))
print()
subtotal = precio * cantidad

if cantidad >= 4:
    print("¡Descuento del 20% aplicado por comprar 4 o más entradas!")
    descuento = 0.20
elif cantidad >= 2:
    print("¡Descuento del 10% aplicado por comprar 2 o más entradas!")
    descuento = 0.10
else:
    descuento = 0.0

total_final = subtotal * (1 - descuento)
print(f"Total a pagar por {cantidad} entradas {tipo}: ${round(total_final)}.")
print()
