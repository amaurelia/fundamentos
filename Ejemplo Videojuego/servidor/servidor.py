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
        "hp": 8000,
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
        snapshot_jugadores = {
            pid: {
                "x": datos[0],
                "y": datos[1],
                "estado": datos[2],
                "nombre": datos[3],
                "color": datos[4],
                "clase": datos[6],
                "chat": datos[5]["texto"] if isinstance(datos[5], dict) and datos[5].get("expira", 0) > time.time() else None,
            }
            for pid, datos in players.items()
        }
        snapshot_raton = copy.deepcopy(raton)
        conexiones = list(clients.items())

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
                    "tu_chat": jugador["chat"],
                    "tu_hp": players[pid][7],
                    "tu_hp_max": players[pid][8],
                    "tu_muerto": players[pid][9],
                    "tu_muerte_timer": players[pid][10],
                    "raton": snapshot_raton,
                    "jugadores": {oid: info for oid, info in snapshot_jugadores.items() if oid != pid},
                }
                conn.sendall((json.dumps(payload) + "\n").encode())
            except Exception:
                desconectados.append(pid)

    if desconectados:
        with lock:
            for pid in desconectados:
                clients.pop(pid, None)
                players.pop(pid, None)


def aplicar_habilidad(player_id, accion):
    if accion not in ("ataque_paladin", "hechizo_fuego", "sanacion"):
        return

    datos = players.get(player_id)
    if not datos:
        return

    if datos[9]:
        return

    if accion == "sanacion":
        datos[7] = min(datos[8], datos[7] + 25)
        return

    if datos[2] != "subterraneo" or raton["hp"] <= 0:
        return

    px, py = datos[0], datos[1]
    dist = math.hypot(px - raton["x"], py - raton["y"])
    if accion == "ataque_paladin" and dist < 120:
        raton["hp"] = max(0, raton["hp"] - 20)
    elif accion == "hechizo_fuego" and dist < 180:
        raton["hp"] = max(0, raton["hp"] - 30)


def _daniar_jugador(pid, danio):
    datos = players.get(pid)
    if not datos or datos[9]:
        return
    datos[7] = max(0, datos[7] - danio)
    if datos[7] <= 0:
        datos[9] = True
        datos[10] = 7 * 60


def _actualizar_respawn_jugadores():
    for datos in players.values():
        if not datos[9]:
            continue
        datos[10] -= 1
        if datos[10] <= 0:
            datos[9] = False
            datos[7] = datos[8]
            datos[0] = 400
            datos[1] = 350
            datos[2] = "exterior"


def _subterraneo_vivos():
    vivos = []
    for pid, datos in players.items():
        if datos[2] == "subterraneo" and not datos[9]:
            vivos.append((pid, datos))
    return vivos


def actualizar_raton():
    _actualizar_respawn_jugadores()
    r = raton

    vivos = _subterraneo_vivos()
    if r["hp"] <= 0 or not vivos:
        r["objetivo_id"] = None
        r["objetivo_nombre"] = None
        return

    objetivo_id, objetivo = min(
        vivos,
        key=lambda item: math.hypot(item[1][0] - r["x"], item[1][1] - r["y"]),
    )
    r["objetivo_id"] = objetivo_id
    r["objetivo_nombre"] = objetivo[3]

    dx = objetivo[0] - r["x"]
    dy = objetivo[1] - r["y"]
    dist = math.hypot(dx, dy)

    VEL_BASE = 2.2
    DETECCION = 220
    ALCANCE = 45

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
            if hechizo == 1 and dist > 0:
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
            elif hechizo == 2:
                r["vel_boost_timer"] = 4 * 60
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

    if dist < ALCANCE:
        r["estado"] = "ataca"
        if r["ataque_timer"] == 0:
            for pid, datos in vivos:
                if math.hypot(datos[0] - r["x"], datos[1] - r["y"]) < ALCANCE:
                    _daniar_jugador(pid, 25)
            r["ataque_timer"] = 60
    elif dist < DETECCION and dist > 0:
        r["estado"] = "persigue"
        r["x"] += (dx / dist) * vel_actual
        r["y"] += (dy / dist) * vel_actual
    else:
        r["estado"] = "patrulla"
        r["patrol_timer"] -= 1
        if r["patrol_timer"] <= 0:
            angulo = random.uniform(0, 2 * math.pi)
            r["vx"] = 1.5 * math.cos(angulo)
            r["vy"] = 1.5 * math.sin(angulo)
            r["patrol_timer"] = random.randint(60, 150)
        r["x"] = max(50, min(800 - 50, r["x"] + r["vx"]))
        r["y"] = max(100, min(600 - 60, r["y"] + r["vy"]))


def game_loop():
    while True:
        try:
            with lock:
                actualizar_raton()
            difundir_estado()
        except Exception:
            pass
        time.sleep(FRAME_TIME)

def handle_client(conn, addr):
    """Maneja a cada cliente conectado"""
    player_id = str(uuid.uuid4())[:8]
    
    # Posicion inicial: (x, y, estado, nombre, color, chat, clase, hp, hp_max, muerto, muerte_timer)
    with lock:
        spawn_x, spawn_y = obtener_spawn_inicial()
        players[player_id] = [spawn_x, spawn_y, "exterior", f"Jugador-{player_id}", "#1565c0", None, "paladin", 100, 100, False, 0]
        clients[player_id] = conn
    
    try:
        print(f"Jugador conectado: {addr} (ID: {player_id})")
        difundir_estado()
        buffer = ""
        while True:
            chunk = conn.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk
            # Procesar todas las lineas completas del buffer
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
                    except ValueError:
                        continue
                    except TypeError:
                        continue
                    estado = payload.get("estado", "exterior")
                    nombre = str(payload.get("nombre", "")).strip() or f"Jugador-{player_id}"
                    clase = str(payload.get("clase", "paladin")).strip().lower() or "paladin"
                    if clase not in ("paladin", "hechicero", "sanador"):
                        clase = "paladin"
                    with lock:
                        color_actual = players[player_id][4]
                        chat_actual = players[player_id][5]
                    color = normalizar_color(payload.get("color"), color_actual)
                    chat_nuevo = payload.get("chat")
                    if isinstance(chat_nuevo, str):
                        chat_nuevo = chat_nuevo.strip()
                    if isinstance(chat_nuevo, str) and chat_nuevo:
                        chat = {"texto": chat_nuevo[:120], "expira": time.time() + CHAT_DURACION_SEGUNDOS}
                    else:
                        chat = chat_actual

                    accion = payload.get("accion")
                    if isinstance(accion, str):
                        accion = accion.strip().lower()
                    else:
                        accion = None

                    with lock:
                        hp = players[player_id][7]
                        hp_max = players[player_id][8]
                        muerto = players[player_id][9]
                        muerte_timer = players[player_id][10]
                        if muerto:
                            x = players[player_id][0]
                            y = players[player_id][1]
                            estado = players[player_id][2]
                        players[player_id] = [x, y, estado, nombre, color, chat, clase, hp, hp_max, muerto, muerte_timer]
                        if accion:
                            aplicar_habilidad(player_id, accion)
                else:
                    # Compatibilidad basica con clientes antiguos: "x,y,estado"
                    parts = data.split(",")
                    if len(parts) < 2:
                        continue
                    try:
                        x, y = int(parts[0]), int(parts[1])
                    except ValueError:
                        continue
                    estado = parts[2] if len(parts) > 2 else "exterior"

                    with lock:
                        nombre = players[player_id][3]
                        color = players[player_id][4]
                        chat = players[player_id][5]
                        clase = players[player_id][6]
                        hp = players[player_id][7]
                        hp_max = players[player_id][8]
                        muerto = players[player_id][9]
                        muerte_timer = players[player_id][10]
                        if muerto:
                            x = players[player_id][0]
                            y = players[player_id][1]
                            estado = players[player_id][2]
                        players[player_id] = [x, y, estado, nombre, color, chat, clase, hp, hp_max, muerto, muerte_timer]
    
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
