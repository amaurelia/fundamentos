completo = False
papas_fritas = False
bebida = False
helado = False
empanadas = False
nuggets = False
opcion = 0
while opcion!=4:
    opcion = int(input("Ingrese una opcion (1:Registrar | 2:Ver | 3:Total | 4:Salir): "))
    match opcion:
        case 1:
            print("Registrar")
            comida = input("¿Qué comida desea registrar? (c:completo | p:papas fritas | b:bebida | h:helado | e:empanadas | n:nuggets): ")
            match comida:
                case "c":
                    completo = True
                case "p":
                    papas_fritas = True
                case "b":
                    bebida = True
                case "h":
                    helado = True
                case "e":
                    empanadas = True
                case "n":
                    nuggets = True
            print("Comida registrada")
        case 2:
            print("Ver")
            if completo:
                print("Completo")
            if papas_fritas:
                print("Papas fritas")
            if bebida:
                print("Bebida")
            if helado:
                print("Helado")
            if empanadas:
                print("Empanadas")
            if nuggets:
                print("Nuggets")
            if not completo and not papas_fritas and not bebida and not helado and not empanadas and not nuggets:
                print("No hay comidas registradas")
        case 3:
            print("Total")
            total = 0
            if completo:
                total += 5000
            if papas_fritas:
                total += 2000
            if bebida:
                total += 1500
            if helado:
                total += 1000
            if empanadas:
                total += 3000
            if nuggets:
                total += 2500
            print(f"El total a pagar es: {total}")
        case 4:
            print("Salir")