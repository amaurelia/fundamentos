print("=== Bienvenido al sistema de votación para el mejor cantante ===")

votos_michael_jackson = 0
votos_madonna = 0
votos_david_bowie = 0
opcion = 0
while opcion!=4:
    opcion = int(input("\nIngrese una opción (1:Votar | 2:Ver resultados | 3:Ver ganador | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Votar ***")
            voto = int(input("\nIngrese una opción (1:Votar por Michael Jackson | 2:Votar por Madonna | 3:Votar por David Bowie | 4:Salir): "))
            match voto:
                case 1:
                    print("Votar por Michael Jackson")
                    votos_michael_jackson += 1
                    print("Voto registrado")
                case 2:
                    print("Votar por Madonna")
                    votos_madonna += 1
                    print("Voto registrado")
                case 3:
                    print("Votar por David Bowie")
                    votos_david_bowie += 1
                    print("Voto registrado")
                case _:
                    print("Opción no válida")   
        case 2:
            print("\n *** Ver resultados ***")
            print(f"Michael Jackson: {votos_michael_jackson} votos")
            print(f"Madonna: {votos_madonna} votos")
            print(f"David Bowie: {votos_david_bowie} votos")
        case 3:
            print("\n *** Ver ganador ***")
            if votos_michael_jackson > votos_madonna and votos_michael_jackson > votos_david_bowie:
                print("El ganador es Michael Jackson")
            elif votos_madonna > votos_michael_jackson and votos_madonna > votos_david_bowie:
                print("El ganador es Madonna")
            elif votos_david_bowie > votos_michael_jackson and votos_david_bowie > votos_madonna:
                print("El ganador es David Bowie")
            else:
                print("Hay un empate")
        case 4:
            print("\n *** Salir ***")