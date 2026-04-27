
saldo = 0
opcion = 0
while opcion!=4:
    opcion = int(input("Ingrese una opcion (1:Depositar | 2:Retirar | 3:Consultar saldo | 4:Salir): "))
    match opcion:
        case 1:
            print("Depositar")
            monto = int(input("Ingrese el monto a depositar: "))
            saldo += monto
            print(f"Su nuevo saldo es: {saldo}")
        case 2:
            print("Retirar")
            monto = int(input("Ingrese el monto a retirar: "))
            if monto > saldo:
                print("No tiene suficiente saldo para retirar esa cantidad")
            else:
                saldo -= monto
                print(f"Su nuevo saldo es: {saldo}")
        case 3:
            print("Consultar saldo")
            print(f"Su saldo actual es: {saldo}")
        case 4:
            print("Salir")
