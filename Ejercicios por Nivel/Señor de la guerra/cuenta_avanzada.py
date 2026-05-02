# Cuenta desde el 6 hasta el 30 pero solo los pares excepto 20 y 24

for i in range(6, 31, 2):
    if i == 20 or i == 24:
        continue
    print(i)
