import socket
import threading
import uuid
import ast
import json
import re
import time
import math
import random
import copy

players = {}
clients = {}
lock = threading.Lock()
broadcast_lock = threading.Lock()
CHAT_DURACION_SEGUNDOS = 4.0
FRAME_TIME = 1.0 / 30.0
FRAME_TIME_BROADCAST = 1.0 / 20.0
RADIO_DIFUSION_EFECTOS = 260
EFECTO_DURACION_SEGUNDOS = 0.35
efectos_recientes = []
profesor_id = None
laboratorio_alerta = {"texto": None, "expira": 0.0}
laboratorio_alerta_disparada = False

# Geometria del mapa exterior (igual al cliente) para generar spawns validos.
RADIO_JUGADOR = 20
LAGO_X, LAGO_Y = 620, 430
LAGO_RX, LAGO_RY = 110, 65
CASA_X, CASA_Y, CASA_W, CASA_H = 290, 50, 130, 100
ARBOLES = [
    (100, 80),
    (500, 170),
    (700, 90),
    (200, 450),
    (450, 340),
    (150, 300),
    (700, 250),
    (370, 470),
]


def rata_inicial():
    return {
        "x": 400.0,
        "y": 300.0,
        "hp": 0,
        "hp_max": 8000,
        "vx": 1.5,
        "vy": 0.8,
        "estado": "patrulla",
        "ataque_timer": 0,
        "patrol_timer": 90,
        "magic_timer": random.randint(200, 380),
        "magic_casteo": 0,
        "magic_hechizo": 0,
        "magic_proyectiles": [],
        "vel_boost_timer": 0,
        "veneno_charcos": [],
        "objetivo_id": None,
        "objetivo_nombre": None,
        "activo": False,
        "controlado_por": None,
    }


raton = rata_inicial()


def normalizar_color(color, fallback="#1565c0"):
    if isinstance(color, str):
        valor = color.strip()
        if re.fullmatch(r"#[0-9a-fA-F]{6}", valor):
            return valor.lower()
    return fallback


def spawn_es_valido(px, py):
    rx = LAGO_RX + RADIO_JUGADOR
    ry = LAGO_RY + RADIO_JUGADOR
    if ((px - LAGO_X) / rx) ** 2 + ((py - LAGO_Y) / ry) ** 2 < 1:
        return False

    for ax, ay in ARBOLES:
        if ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5 < RADIO_JUGADOR + 18:
            return False

    pared_y = CASA_Y + CASA_H // 4
    px_puerta = CASA_X + CASA_W // 2 - 14
    en_cuerpo = (
        CASA_X - RADIO_JUGADOR < px < CASA_X + CASA_W + RADIO_JUGADOR
        and pared_y - RADIO_JUGADOR < py < CASA_Y + CASA_H + RADIO_JUGADOR
    )
    en_puerta = (
        px_puerta - RADIO_JUGADOR < px < px_puerta + 28 + RADIO_JUGADOR
        and py > CASA_Y + CASA_H - 40 - RADIO_JUGADOR
    )
    return not (en_cuerpo and not en_puerta)


def generar_spawns_validos(max_spawns=20):
    spawns = []
    for y in range(100, 561, 60):
        for x in range(80, 761, 60):
            if spawn_es_valido(x, y):
                spawns.append((x, y))
            if len(spawns) >= max_spawns:
                return spawns
    return spawns


SPAWN_POINTS = generar_spawns_validos(20)


def obtener_spawn_inicial():
    if not SPAWN_POINTS:
        return (400, 300)
    ocupados = {tuple(pos[:2]) for pos in players.values()}
    for spawn in SPAWN_POINTS:
        if spawn not in ocupados:
            return spawn
    return SPAWN_POINTS[len(players) % len(SPAWN_POINTS)]


def difundir_estado():
    with lock:
        ahora = time.time()
        alerta_texto = laboratorio_alerta["texto"] if laboratorio_alerta["expira"] > ahora else None
        snapshot_jugadores = {
            pid: {
                "x": datos[0],
                "y": datos[1],
                "estado": datos[2],
                "nombre": datos[3],
                "color": datos[4],
                "chat": datos[5]["texto"] if isinstance(datos[5], dict) and datos[5].get("expira", 0) > ahora else None,
                "clase": datos[6],
                "hp": datos[7],
                "hp_max": datos[8],
                "muerto": datos[9],
                "muerte_timer": datos[10],
                "es_profesor": pid == profesor_id,
            }
            for pid, datos in players.items()
        }
        snapshot_raton = copy.deepcopy(raton)
        conexiones = list(clients.items())
        while efectos_recientes and efectos_recientes[0]["expira"] <= ahora:
            efectos_recientes.pop(0)
        snapshot_efectos = list(efectos_recientes)

    desconectados = []
    with broadcast_lock:
        for pid, conn in conexiones:
            try:
                jugador = snapshot_jugadores.get(pid)
                if jugador is None:
                    continue
                payload = {
                    "tu_id": pid,
                    "tu_pos": [jugador["x"], jugador["y"], jugador["estado"]],
                    "tu_nombre": jugador["nombre"],
                    "tu_color": jugador["color"],
                    "tu_clase": jugador["clase"],
                    "tu_chat": jugador["chat"],
                    "tu_hp": jugador["hp"],
                    "tu_hp_max": jugador["hp_max"],
                    "tu_muerto": jugador["muerto"],
                    "tu_muerte_timer": jugador["muerte_timer"],
                    "raton": snapshot_raton,
                    "profesor_id": profesor_id,
                    "laboratorio_alerta": alerta_texto,
                    "jugadores": {oid: info for oid, info in snapshot_jugadores.items() if oid != pid},
                    "efectos": _efectos_cercanos_para_jugador(pid, snapshot_jugadores, snapshot_efectos),
                }
                conn.sendall((json.dumps(payload, separators=(",", ":")) + "\n").encode())
            except Exception:
                desconectados.append(pid)

    if desconectados:
        with lock:
            for pid in desconectados:
                clients.pop(pid, None)
                players.pop(pid, None)


def aplicar_habilidad(player_id, accion):
    if accion not in (
        "ataque_paladin", "ataque_paladin_izq", "ataque_paladin_der",
        "hechizo_fuego", "sanacion", "danio_pincho",
        "mutante_transformar", "mutante_esfera", "mutante_veneno", "mutante_velocidad",
    ):
        return

    datos = players.get(player_id)
    if not datos:
        return

    if datos[9]:
        return

    if accion == "sanacion":
        datos[7] = min(datos[8], datos[7] + 25)
        return

    if accion == "danio_pincho":
        datos[7] = max(0, datos[7] - 10)
        return

    if accion == "mutante_transformar":
        if player_id == profesor_id and datos[2] == "subterraneo" and not datos[9]:
            _aplicar_transformacion_profesor(player_id)
            _activar_modo_mutante(player_id)
        return

    if accion == "mutante_velocidad":
        if player_id == profesor_id and raton["activo"] and raton["controlado_por"] == player_id:
            raton["vel_boost_timer"] = 4 * 60
        return

    if accion in ("mutante_esfera", "mutante_veneno"):
        if player_id == profesor_id and raton["activo"] and raton["controlado_por"] == player_id:
            raton["magic_hechizo"] = 1 if accion == "mutante_esfera" else 3
            raton["magic_casteo"] = 1
        return

    if datos[2] != "subterraneo" or not raton["activo"] or raton["controlado_por"] != profesor_id:
        return

    px, py = datos[0], datos[1]
    dist = math.hypot(px - raton["x"], py - raton["y"])
    if accion == "ataque_paladin" and dist < 120:
        _daniar_profesor_mutante(20)
    elif accion in ("ataque_paladin_izq", "ataque_paladin_der") and dist < 120:
        _daniar_profesor_mutante(25)
    elif accion == "hechizo_fuego" and dist < 1800:
        _daniar_profesor_mutante(360)


def _daniar_jugador(pid, danio):
    datos = players.get(pid)
    if not datos or datos[9]:
        return
    datos[7] = max(0, datos[7] - danio)
    if datos[7] <= 0:
        datos[9] = True
        datos[10] = 10 * 60 if datos[2] == "practica" else 7 * 60
        if datos[2] == "subterraneo" and not datos[3].endswith(", el ebrio"):
            datos[3] = f"{datos[3]}, el ebrio"
            if len(datos) > 11:
                datos[11] = True
        if pid == profesor_id:
            _desactivar_modo_mutante()


def _actualizar_respawn_jugadores():
    for datos in players.values():
        if not datos[9]:
            continue
        datos[10] -= 1
        if datos[10] <= 0:
            datos[9] = False
            datos[7] = datos[8]
            if len(datos) > 11:
                datos[11] = datos[11] or datos[2] == "subterraneo"
            if datos[3] == "Profesor Alvaro":
                datos[2] = "exterior"
                datos[0] = 400
                datos[1] = 350
                _desactivar_modo_mutante()
                continue
            if datos[2] == "practica":
                datos[0] = 400
                datos[1] = 540
            elif datos[2] == "subterraneo":
                datos[0] = 400
                datos[1] = 350
                datos[2] = "exterior"
            else:
                datos[0] = 400
                datos[1] = 350
                datos[2] = "exterior"


def _efectos_cercanos_para_jugador(player_id, snapshot_jugadores, snapshot_efectos):
    receptor = snapshot_jugadores.get(player_id)
    if not receptor:
        return []

    rx = receptor["x"]
    ry = receptor["y"]
    restado = receptor["estado"]
    visibles = []
    for efecto in snapshot_efectos:
        if efecto["player_id"] == player_id:
            continue
        if efecto["estado"] != restado:
            continue
        if math.hypot(efecto["x"] - rx, efecto["y"] - ry) > RADIO_DIFUSION_EFECTOS:
            continue
        visibles.append({
            "id": efecto["id"],
            "player_id": efecto["player_id"],
            "accion": efecto["accion"],
            "x": efecto["x"],
            "y": efecto["y"],
            "estado": efecto["estado"],
        })
    return visibles


def registrar_evento_efecto(player_id, accion):
    # danio_pincho no necesita difusión visual; evitar spam de eventos mejora rendimiento.
    if accion not in ("ataque_paladin", "ataque_paladin_izq", "ataque_paladin_der", "hechizo_fuego", "sanacion"):
        return
    datos = players.get(player_id)
    if not datos:
        return
    if datos[9]:
        return
    efectos_recientes.append({
        "id": f"{player_id}-{time.time_ns()}",
        "player_id": player_id,
        "accion": accion,
        "x": datos[0],
        "y": datos[1],
        "estado": datos[2],
        "expira": time.time() + EFECTO_DURACION_SEGUNDOS,
    })


def _subterraneo_vivos():
    vivos = []
    for pid, datos in players.items():
        if datos[2] == "subterraneo" and not datos[9]:
            vivos.append((pid, datos))
    return vivos


def _marcar_alerta_laboratorio():
    global laboratorio_alerta_disparada
    if laboratorio_alerta_disparada:
        return
    laboratorio_alerta_disparada = True
    laboratorio_alerta["texto"] = "Alguien ha entrado en el laboratorio del profesor Alvaro"
    laboratorio_alerta["expira"] = time.time() + 8.0


def _asegurar_profesor(player_id):
    global profesor_id
    if profesor_id is None:
        profesor_id = player_id


def _es_profesor(player_id):
    return player_id == profesor_id


def _aplicar_transformacion_profesor(player_id):
    datos = players.get(player_id)
    if not datos:
        return
    datos[3] = "Profesor Alvaro"
    datos[4] = "#7b1fa2"
    datos[6] = "profesor"
    datos[7] = 100
    datos[8] = 100


def _activar_modo_mutante(player_id):
    datos = players.get(player_id)
    if not datos:
        return
    datos[6] = "mutante"
    datos[7] = 8000
    datos[8] = 8000
    raton["activo"] = True
    raton["controlado_por"] = player_id
    raton["hp"] = 8000
    raton["hp_max"] = 8000
    raton["x"] = float(datos[0])
    raton["y"] = float(datos[1])
    raton["objetivo_id"] = None
    raton["objetivo_nombre"] = None
    raton["magic_casteo"] = 0
    raton["magic_hechizo"] = 0
    raton["magic_proyectiles"] = []
    raton["veneno_charcos"] = []
    raton["vel_boost_timer"] = 0


def _desactivar_modo_mutante():
    raton["activo"] = False
    raton["controlado_por"] = None
    raton["hp"] = 0
    raton["objetivo_id"] = None
    raton["objetivo_nombre"] = None
    raton["magic_casteo"] = 0
    raton["magic_hechizo"] = 0
    raton["magic_proyectiles"] = []
    raton["veneno_charcos"] = []
    raton["vel_boost_timer"] = 0


def _respawn_profesor_fuera():
    if not profesor_id:
        return
    datos = players.get(profesor_id)
    if not datos:
        return
    datos[0] = 400
    datos[1] = 350
    datos[2] = "exterior"
    datos[7] = 100
    datos[8] = 100
    datos[9] = False
    datos[10] = 0
    _desactivar_modo_mutante()


def _daniar_profesor_mutante(danio):
    if not raton["activo"] or raton["controlado_por"] != profesor_id:
        return
    raton["hp"] = max(0, raton["hp"] - danio)
    datos = players.get(profesor_id)
    if datos:
        datos[7] = raton["hp"]
        datos[8] = raton["hp_max"]
        if raton["hp"] <= 0:
            datos[9] = True
            datos[10] = 10 * 60
            _desactivar_modo_mutante()


def actualizar_raton():
    _actualizar_respawn_jugadores()
    r = raton

    if not r["activo"] or r["controlado_por"] != profesor_id:
        r["objetivo_id"] = None
        r["objetivo_nombre"] = None
        return

    profe = players.get(profesor_id)
    if not profe:
        _desactivar_modo_mutante()
        return

    r["x"] = float(profe[0])
    r["y"] = float(profe[1])
    r["hp"] = profe[7]
    r["hp_max"] = profe[8]
    if profe[2] != "subterraneo" or profe[9]:
        r["objetivo_id"] = None
        r["objetivo_nombre"] = None
        return

    vivos = []
    for pid, datos in players.items():
        if pid == profesor_id:
            continue
        if datos[2] == "subterraneo" and not datos[9]:
            vivos.append((pid, datos))

    if vivos:
        objetivo_id, objetivo = min(vivos, key=lambda item: math.hypot(item[1][0] - r["x"], item[1][1] - r["y"]))
        r["objetivo_id"] = objetivo_id
        r["objetivo_nombre"] = objetivo[3]
    else:
        r["objetivo_id"] = None
        r["objetivo_nombre"] = None

    dx = 0.0
    dy = 0.0
    dist = 0.0
    if vivos:
        dx = objetivo[0] - r["x"]
        dy = objetivo[1] - r["y"]
        dist = math.hypot(dx, dy)

    VEL_BASE = 2.2

    if r["vel_boost_timer"] > 0:
        r["vel_boost_timer"] -= 1
        vel_actual = VEL_BASE * 3
    else:
        vel_actual = VEL_BASE

    nuevos_charcos = []
    for ch in r["veneno_charcos"]:
        ch["vida"] -= 1
        if ch["vida"] <= 0:
            continue
        if ch["dmg_timer"] > 0:
            ch["dmg_timer"] -= 1
        for pid, datos in vivos:
            if math.hypot(datos[0] - ch["x"], datos[1] - ch["y"]) < RADIO_JUGADOR + 22 and ch["dmg_timer"] <= 0:
                _daniar_jugador(pid, 8)
                ch["dmg_timer"] = 45
                break
        nuevos_charcos.append(ch)
    r["veneno_charcos"] = nuevos_charcos

    nuevos_proyectiles = []
    for bolt in r["magic_proyectiles"]:
        bolt["x"] += bolt["vx"]
        bolt["y"] += bolt["vy"]
        bolt["vida"] -= 1
        if bolt["vida"] <= 0:
            continue
        impacto = False
        for pid, datos in vivos:
            if math.hypot(datos[0] - bolt["x"], datos[1] - bolt["y"]) < RADIO_JUGADOR + 12:
                _daniar_jugador(pid, 35)
                impacto = True
                break
        if not impacto:
            nuevos_proyectiles.append(bolt)
    r["magic_proyectiles"] = nuevos_proyectiles

    if r["magic_casteo"] > 0:
        r["magic_casteo"] += 1
        if r["magic_casteo"] >= 60:
            hechizo = r["magic_hechizo"]
            if hechizo == 1 and vivos and dist > 0:
                speed = 7.0
                r["magic_proyectiles"].append(
                    {
                        "x": r["x"],
                        "y": r["y"],
                        "vx": (dx / dist) * speed,
                        "vy": (dy / dist) * speed,
                        "vida": 180,
                    }
                )
            elif hechizo == 3:
                for _ in range(random.randint(4, 7)):
                    r["veneno_charcos"].append(
                        {
                            "x": float(random.randint(80, 800 - 80)),
                            "y": float(random.randint(120, 600 - 80)),
                            "vida": 10 * 60,
                            "dmg_timer": 0,
                        }
                    )
            r["magic_casteo"] = 0
            r["magic_hechizo"] = 0
            r["magic_timer"] = random.randint(200, 380)
    else:
        r["magic_timer"] -= 1
        if r["magic_timer"] <= 0:
            r["magic_hechizo"] = random.randint(1, 3)
            r["magic_casteo"] = 1

    if r["ataque_timer"] > 0:
        r["ataque_timer"] -= 1

    if r["magic_casteo"] > 0:
        return

    if vivos and dist > 0:
        if dist < 45:
            r["estado"] = "ataca"
            if r["ataque_timer"] == 0:
                for pid, datos in vivos:
                    if math.hypot(datos[0] - r["x"], datos[1] - r["y"]) < 45:
                        _daniar_jugador(pid, 25)
                r["ataque_timer"] = 60
        else:
            r["estado"] = "persigue"
            r["x"] += (dx / dist) * vel_actual
            r["y"] += (dy / dist) * vel_actual
    else:
        r["estado"] = "patrulla"
        r["x"] = profe[0]
        r["y"] = profe[1]


def game_loop():
    proximo_broadcast = time.perf_counter()
    while True:
        inicio = time.perf_counter()
        try:
            with lock:
                actualizar_raton()
            ahora = time.perf_counter()
            if ahora >= proximo_broadcast:
                difundir_estado()
                proximo_broadcast = ahora + FRAME_TIME_BROADCAST
        except Exception:
            pass
        transcurrido = time.perf_counter() - inicio
        time.sleep(max(0.0, FRAME_TIME - transcurrido))

def handle_client(conn, addr):
    """Maneja a cada cliente conectado"""
    player_id = str(uuid.uuid4())[:8]
    last_estado = "exterior"

    with lock:
        spawn_x, spawn_y = obtener_spawn_inicial()
        players[player_id] = [spawn_x, spawn_y, "exterior", f"Jugador-{player_id}", "#1565c0", None, "paladin", 100, 100, False, 0, False]
        clients[player_id] = conn
        _asegurar_profesor(player_id)
        if player_id == profesor_id:
            players[player_id][3] = "Profesor Alvaro"
            players[player_id][4] = "#7b1fa2"
            players[player_id][6] = "profesor"
            _aplicar_transformacion_profesor(player_id)

    try:
        print(f"Jugador conectado: {addr} (ID: {player_id})")
        difundir_estado()
        buffer = ""
        while True:
            chunk = conn.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                data = line.strip()
                if not data:
                    continue

                try:
                    payload = json.loads(data)
                except Exception:
                    try:
                        payload = ast.literal_eval(data)
                    except Exception:
                        payload = None

                if isinstance(payload, dict):
                    try:
                        x = int(payload.get("x"))
                        y = int(payload.get("y"))
                    except (TypeError, ValueError):
                        continue

                    estado = payload.get("estado", "exterior")
                    nombre = str(payload.get("nombre", "")).strip() or f"Jugador-{player_id}"
                    clase = str(payload.get("clase", "paladin")).strip().lower() or "paladin"
                    if clase not in ("paladin", "hechicero", "sanador", "profesor", "mutante"):
                        clase = "paladin"
                    accion = payload.get("accion")
                    accion = accion.strip().lower() if isinstance(accion, str) else None

                    with lock:
                        datos_previos = players.get(player_id)
                        if not datos_previos:
                            continue
                        last_estado = datos_previos[2]
                        color_actual = datos_previos[4]
                        chat_actual = datos_previos[5]
                        color = normalizar_color(payload.get("color"), color_actual)
                        chat_nuevo = payload.get("chat")
                        if isinstance(chat_nuevo, str):
                            chat_nuevo = chat_nuevo.strip()
                        if chat_nuevo:
                            chat = {"texto": chat_nuevo[:120], "expira": time.time() + CHAT_DURACION_SEGUNDOS}
                        else:
                            chat = chat_actual

                        hp = datos_previos[7]
                        hp_max = datos_previos[8]
                        muerto = datos_previos[9]
                        muerte_timer = datos_previos[10]
                        ebrio = datos_previos[11] if len(datos_previos) > 11 else False
                        if muerto:
                            x = datos_previos[0]
                            y = datos_previos[1]
                            estado = datos_previos[2]
                        if player_id == profesor_id:
                            nombre = "Profesor Alvaro"
                            color = "#7b1fa2"
                            clase = "profesor" if clase != "mutante" else "mutante"
                        players[player_id] = [x, y, estado, nombre, color, chat, clase, hp, hp_max, muerto, muerte_timer, ebrio]
                        if player_id != profesor_id and estado == "subterraneo" and last_estado != "subterraneo" and not muerto:
                            _marcar_alerta_laboratorio()
                        if accion:
                            aplicar_habilidad(player_id, accion)
                            registrar_evento_efecto(player_id, accion)
                else:
                    parts = data.split(",")
                    if len(parts) < 2:
                        continue
                    try:
                        x, y = int(parts[0]), int(parts[1])
                    except ValueError:
                        continue
                    estado = parts[2] if len(parts) > 2 else "exterior"

                    with lock:
                        datos_previos = players.get(player_id)
                        if not datos_previos:
                            continue
                        last_estado = datos_previos[2]
                        nombre = datos_previos[3]
                        color = datos_previos[4]
                        chat = datos_previos[5]
                        clase = datos_previos[6]
                        hp = datos_previos[7]
                        hp_max = datos_previos[8]
                        muerto = datos_previos[9]
                        muerte_timer = datos_previos[10]
                        ebrio = datos_previos[11] if len(datos_previos) > 11 else False
                        if muerto:
                            x = datos_previos[0]
                            y = datos_previos[1]
                            estado = datos_previos[2]
                        if player_id == profesor_id:
                            nombre = "Profesor Alvaro"
                            color = "#7b1fa2"
                            clase = "profesor" if clase != "mutante" else "mutante"
                        if player_id != profesor_id and estado == "subterraneo" and last_estado != "subterraneo" and not muerto:
                            _marcar_alerta_laboratorio()
                        players[player_id] = [x, y, estado, nombre, color, chat, clase, hp, hp_max, muerto, muerte_timer, ebrio]

    except Exception as e:
        print(f"Error con {addr}: {e}")

    finally:
        with lock:
            clients.pop(player_id, None)
            players.pop(player_id, None)
        conn.close()
        difundir_estado()
        print(f"Jugador desconectado: {addr} (ID: {player_id})")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 5000))
server.listen(20)

print("Servidor de Aventura Multijugador iniciado en puerto 5000")
print("Máximo de jugadores: 20")
print("Esperando conexiones...")

try:
    threading.Thread(target=game_loop, daemon=True).start()
    while True:
        conn, addr = server.accept()
        print(f"Nueva conexión desde {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\nServidor detenido")
    server.close()
