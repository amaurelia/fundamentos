print("=== Sistema de Estacionamiento ===")
print()

TOTAL_PLAZAS = 5
PRECIO_POR_HORA = 500

# Cada plaza es un diccionario con patente y hora de ingreso, o None si está libre
plazas = [None] * TOTAL_PLAZAS


def plazas_disponibles():
    return plazas.count(None)


def buscar_auto(patente):
    for i, plaza in enumerate(plazas):
        if plaza is not None and plaza["patente"].upper() == patente.upper():
            return i
    return -1


while True:
    print()
    print("--- MENÚ ---")
    print("1. Ingresar auto")
    print("2. Ver autos estacionados")
    print("3. Registrar salida de auto")
    print("4. Cantidad de autos estacionados")
    print("5. Salir")
    print()

    opcion = input("Selecciona una opción (1-5): ").strip()

    if opcion == "1":
        # Ingresar un nuevo auto
        if plazas_disponibles() == 0:
            print("Lo sentimos, el estacionamiento está lleno. No hay plazas disponibles.")
        else:
            # Patente
            while True:
                patente = input("Ingresa la patente del auto: ").strip().upper()
                if not patente:
                    print("Error: la patente no puede estar vacía.")
                elif buscar_auto(patente) != -1:
                    print(f"Error: la patente {patente} ya está registrada en el estacionamiento.")
                else:
                    break

            # Hora de ingreso
            while True:
                try:
                    hora_ingreso = int(input("Hora de ingreso (0-24): "))
                    if hora_ingreso < 0 or hora_ingreso > 24:
                        raise ValueError("La hora debe estar entre 0 y 24.")
                except ValueError as e:
                    print(f"Error: {e}")
                else:
                    break

            # Asignar primera plaza libre
            for i in range(TOTAL_PLAZAS):
                if plazas[i] is None:
                    plazas[i] = {"patente": patente, "hora_ingreso": hora_ingreso}
                    print(f"Auto {patente} ingresado en la plaza {i + 1} a las {hora_ingreso}:00.")
                    break

    elif opcion == "2":
        # Mostrar autos registrados
        autos = [(i + 1, p) for i, p in enumerate(plazas) if p is not None]
        if not autos:
            print("No hay autos estacionados actualmente.")
        else:
            print("Autos estacionados:")
            for num_plaza, p in autos:
                print(f"  Plaza {num_plaza}: {p['patente']} (ingresó a las {p['hora_ingreso']}:00)")

    elif opcion == "3":
        # Registrar salida de un auto
        autos = [(i, p) for i, p in enumerate(plazas) if p is not None]
        if not autos:
            print("No hay autos estacionados actualmente.")
        else:
            patente = input("Ingresa la patente del auto que sale: ").strip().upper()
            idx = buscar_auto(patente)
            if idx == -1:
                print(f"Error: no se encontró ningún auto con la patente {patente}.")
            else:
                hora_ingreso = plazas[idx]["hora_ingreso"]

                # Hora de salida
                while True:
                    try:
                        hora_salida = int(input("Hora de salida (0-24): "))
                        if hora_salida < 0 or hora_salida > 24:
                            raise ValueError("La hora debe estar entre 0 y 24.")
                        if hora_salida < hora_ingreso:
                            raise ValueError(f"La hora de salida ({hora_salida}) no puede ser menor a la de ingreso ({hora_ingreso}).")
                    except ValueError as e:
                        print(f"Error: {e}")
                    else:
                        break

                horas = hora_salida - hora_ingreso
                total = horas * PRECIO_POR_HORA
                plazas[idx] = None

                print(f"Auto {patente} retirado de la plaza {idx + 1}.")
                print(f"Tiempo estacionado: {horas} hora(s).")
                print(f"Total a pagar: ${total:,}")

    elif opcion == "4":
        # Cantidad de autos estacionados
        cantidad = TOTAL_PLAZAS - plazas_disponibles()
        print(f"Autos estacionados: {cantidad}/{TOTAL_PLAZAS}")
        print(f"Plazas disponibles: {plazas_disponibles()}/{TOTAL_PLAZAS}")

    elif opcion == "5":
        print("¡Hasta pronto!")
        break

    else:
        print("Opción no válida. Por favor, selecciona entre 1 y 5.")
