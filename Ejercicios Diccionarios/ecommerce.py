pedido = {
    "cliente": {"nombre": "Luis", "email": "luis@example.com"},
    "productos": [
        {"nombre": "Notebook Gamer", "precio": 800000, "cantidad": 1},
        {"nombre": "Mouse",          "precio": 20000,  "cantidad": 2},
        {"nombre": "Teclado",        "precio": 50000,  "cantidad": 1}
    ],
    "estado": "pendiente"
}

# 1) Email del cliente
print("=== Email del cliente ===")
print(pedido["cliente"]["email"])

# 2) Total del pedido
print("\n=== Total del pedido ===")
total = 0
for producto in pedido["productos"]:
    total += producto["precio"] * producto["cantidad"]
print(f"Total: ${total:,}")

# 3) Arreglo con nombres de productos
print("\n=== Productos en el carrito ===")
nombres = []
for producto in pedido["productos"]:
    nombres.append(producto["nombre"])
print(nombres)

# 4) Cambiar estado a "enviado"
pedido["estado"] = "enviado"
print(f"\n=== Estado actualizado: {pedido['estado']} ===")

# 5) Agregar NVIDIA RTX 5090
pedido["productos"].append({"nombre": "NVIDIA RTX 5090", "precio": 3600000, "cantidad": 1})
print("\n=== NVIDIA RTX 5090 agregada al carrito ===")
print("Productos actuales:")
for producto in pedido["productos"]:
    subtotal = producto["precio"] * producto["cantidad"]
    print(f"  - {producto['nombre']}: ${producto['precio']:,} x {producto['cantidad']} = ${subtotal:,}")
