print("=== Bienvenido al sistema de registro de avistamientos ===")

nina = ""
gary = ""
iris = ""
luke = ""
opcion = 0
while opcion!=4:
    opcion = int(input("\nIngrese una opción (1:Registrar | 2:Ver | 3:Buscar | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Registrar avistamiento ***")
            testigo = input("Quién (n:nina | g:gary | i:iris | l:luke): ")
            descripcion = input("¿Qué fue lo que vio?: ")
            match testigo:
                case "n":
                    nina = descripcion
                case "g":
                    gary = descripcion
                case "i":
                    iris = descripcion
                case "l":
                    luke = descripcion
        case 2:
            print("\n *** Avistamientos registrados ***")
            if nina!="":
                print(f"Nina: {nina}")
            if gary!="":
                print(f"Gary: {gary}")
            if iris!="":
                print(f"Iris: {iris}")
            if luke!="":
                print(f"Luke: {luke}")
            if nina=="" and gary=="" and iris=="" and luke=="":
                print("No hay registros")
        case 3:
            print("\n *** Buscar avistamiento ***")
            if "luces" in nina:
                print("Nina vio luces")
            if "luces" in gary:
                print("Gary vio luces")
            if "luces" in iris:
                print("Iris vio luces")
            if "luces" in luke:
                print("Luke vio luces")
            if "luces" not in nina and "luces" not in gary and "luces" not in iris and "luces" not in luke:
                print("Nadie ha visto luces en el cielo")
        case 4:
            print("\n *** Salir ***")

