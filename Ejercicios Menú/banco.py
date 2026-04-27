print("=== Bienvenido al sistema de gestión bancaria ===")

saldo = 0
opcion = 0
while opcion!=4:
    
    opcion = int(input("\nIngrese una opcion (1:Depositar | 2:Retirar | 3:Consultar saldo | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Depositar ***")
            monto = int(input("\nIngrese el monto a depositar: "))
            saldo += monto
            print(f"Su nuevo saldo es: {saldo}")
        case 2:
            print("\n *** Retirar ***")
            monto = int(input("\nIngrese el monto a retirar: "))
            if monto > saldo:
                print("No tiene suficiente saldo para retirar esa cantidad")
            else:
                saldo -= monto
                print(f"Su nuevo saldo es: {saldo}")
        case 3:
            print("\n *** Consultar saldo ***")
            print(f"Su saldo actual es: {saldo}")
        case 4:
            print("\n *** Salir ***")
