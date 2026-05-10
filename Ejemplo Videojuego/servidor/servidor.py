import socket
import threading
import uuid
import ast
import json
import re
import time

players = {}
clients = {}
lock = threading.Lock()
broadcast_lock = threading.Lock()
CHAT_DURACION_SEGUNDOS = 4.0

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

def handle_client(conn, addr):
    """Maneja a cada cliente conectado"""
    player_id = str(uuid.uuid4())[:8]
    
    # Posicion inicial: (x, y, estado, nombre, color, chat, clase)
    with lock:
        spawn_x, spawn_y = obtener_spawn_inicial()
        players[player_id] = [spawn_x, spawn_y, "exterior", f"Jugador-{player_id}", "#1565c0", None, "paladin"]
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

                    with lock:
                        players[player_id] = [x, y, estado, nombre, color, chat, clase]

                    difundir_estado()
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
                        players[player_id] = [x, y, estado, nombre, color, chat, clase]

                    difundir_estado()
    
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
    while True:
        conn, addr = server.accept()
        print(f"Nueva conexión desde {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\nServidor detenido")
    server.close()
