def mostrar_estado(hechicero):
    print(
        f"{hechicero['nombre']} | "
        f"Nivel: {hechicero['nivel']} | "
        f"Tecnica: {hechicero['tecnica']} | "
        f"Energia: {hechicero['energia']}"
    )


def validar_energia(hechicero):
    return hechicero["energia"] > 0


def atacar(atacante, defensor):
    if not validar_energia(atacante):
        print(f"{atacante['nombre']} no tiene energia para atacar.")
        return

    dano = atacante["nivel"]
    defensor["energia"] -= dano

    if defensor["energia"] < 0:
        defensor["energia"] = 0

    print(f"{atacante['nombre']} ataca a {defensor['nombre']} y causa {dano} de dano.")

    if not validar_energia(defensor):
        print(f"{defensor['nombre']} ya no puede seguir luchando.")


def usar_tecnica(hechicero):
    if not validar_energia(hechicero):
        print(f"{hechicero['nombre']} no tiene energia para usar tecnica.")
        return

    hechicero["energia"] -= 2

    if hechicero["energia"] < 0:
        hechicero["energia"] = 0

    print(f"{hechicero['nombre']} usa su tecnica: {hechicero['tecnica']} (-2 energia)")

    if not validar_energia(hechicero):
        print(f"{hechicero['nombre']} se quedo sin energia.")


def combate(hechicero1, hechicero2):
    turno = 1
    print("=== INICIO DEL COMBATE ===")

    while validar_energia(hechicero1) and validar_energia(hechicero2):
        print(f"\n--- Turno {turno} ---")

        atacar(hechicero1, hechicero2)
        if not validar_energia(hechicero2):
            break

        usar_tecnica(hechicero1)

        atacar(hechicero2, hechicero1)
        if not validar_energia(hechicero1):
            break

        usar_tecnica(hechicero2)

        mostrar_estado(hechicero1)
        mostrar_estado(hechicero2)

        turno += 1

    print("\n=== FIN DEL COMBATE ===")
    if validar_energia(hechicero1):
        print(f"Gana {hechicero1['nombre']}")
    elif validar_energia(hechicero2):
        print(f"Gana {hechicero2['nombre']}")
    else:
        print("Empate")


# Datos de prueba
gojo = {"nombre": "Gojo", "nivel": 10, "tecnica": "Infinito", "energia": 20}
sukuna = {"nombre": "Sukuna", "nivel": 9, "tecnica": "Dominio Maldito", "energia": 20}

mostrar_estado(gojo)
mostrar_estado(sukuna)
atacar(gojo, sukuna)
usar_tecnica(sukuna)
combate(gojo, sukuna)
