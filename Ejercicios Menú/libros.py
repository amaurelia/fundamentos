print("=== Bienvenido al sistema de registro de libros ===")

titulo1 = ""
autor1 = ""
anio1 = 0
titulo2 = ""
autor2 = ""
anio2 = 0
titulo3 = ""
autor3 = ""
anio3 = 0
opcion = 0
while opcion!=4:
    opcion = int(input("\nIngrese una opción (1:Registrar libro | 2:Ver libros | 3:Buscar libro | 4:Salir): "))
    match opcion:
        case 1:
            print("\n *** Registrar libro ***")
            titulo = input("\nIngrese el título del libro: ")
            autor = input("\nIngrese el autor del libro: ")
            anio = int(input("\nIngrese el año de publicación del libro: "))
            if titulo1 == "":
                titulo1 = titulo
                autor1 = autor
                anio1 = anio
            elif titulo2 == "":
                titulo2 = titulo
                autor2 = autor
                anio2 = anio
            elif titulo3 == "":
                titulo3 = titulo
                autor3 = autor
                anio3 = anio
            else:
                print("No se pueden registrar más libros")
        case 2:
            print("\n *** Ver libros ***")
            if titulo1 != "":
                print(f"Libro 1: {titulo1} - {autor1} - {anio1}")
            if titulo2 != "":
                print(f"Libro 2: {titulo2} - {autor2} - {anio2}")
            if titulo3 != "":
                print(f"Libro 3: {titulo3} - {autor3} - {anio3}")
            if titulo1 == "" and titulo2 == "" and titulo3 == "":
                print("No hay libros registrados")  
        case 3:
            print("\n *** Buscar libro ***")
            busqueda = input("\nIngrese el título del libro a buscar: ")
            if busqueda == titulo1:
                print(f"Libro encontrado: {titulo1} - {autor1} - {anio1}")
            elif busqueda == titulo2:
                print(f"Libro encontrado: {titulo2} - {autor2} - {anio2}")
            elif busqueda == titulo3:
                print(f"Libro encontrado: {titulo3} - {autor3} - {anio3}")
            else:
                print("Libro no encontrado")
        case 4:
            print("\n *** Salir ***")
    