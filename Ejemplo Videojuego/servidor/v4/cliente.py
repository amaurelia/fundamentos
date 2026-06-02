import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import socket
import threading
import ast
import json
import math
import re
import time
import random
import os
import sys


class cfg:
    # --- Ventana ---
    ANCHO = 800
    ALTO = 600

    # --- Personaje ---
    VELOCIDAD = 5
    RADIO = 20

    # --- Colores del fondo ---
    COLOR_CESPED_CLARO = "#4a7c3f"
    COLOR_CESPED_OSCURO = "#3d6b35"

    # --- Colores del personaje ---
    COLOR_CUERPO = "#1565c0"
    COLOR_BORDE_CUERPO = "#0d47a1"
    COLOR_CARA = "#ffcc80"
    COLOR_BORDE_CARA = "#e65100"

    # --- Colores de los arboles ---
    COLOR_SOMBRA_ARBOL = "#2d5a27"
    COLOR_COPA = "#2e7d32"
    COLOR_BORDE_COPA = "#1b5e20"
    COLOR_TRONCO = "#5d4037"
    RADIO_ARBOL = 18

    # --- Colores de los barriles ---
    COLOR_BARRIL = "#8B4513"
    COLOR_BARRIL_ARO = "#5C3317"
    RADIO_BARRIL = 14

    # --- Lago ---
    LAGO_X = 620
    LAGO_Y = 430
    LAGO_RX = 110
    LAGO_RY = 65
    COLOR_LAGO = "#1a6fa8"
    COLOR_LAGO_BORDE = "#0d47a1"
    COLOR_LAGO_BRILLO = "#4fc3f7"

    # --- Casa (exterior) ---
    CASA_X = 290
    CASA_Y = 50
    CASA_W = 130
    CASA_H = 100
    COLOR_CASA_PARED = "#d4a064"
    COLOR_CASA_TECHO = "#8B2500"
    COLOR_CASA_PUERTA = "#5d3a1a"

    # --- Interior ---
    COLOR_PISO = "#c8a96e"
    COLOR_PISO_ALT = "#b8995e"
    COLOR_PARED_INT = "#7a5c2e"
    SALIDA_INT_X = ANCHO // 2

    # Muebles: (x, y, ancho, alto, color, etiqueta)
    MUEBLES = [
        (120, 100, 150, 60, "#5d4037", "mesa"),
        (120, 160, 40, 40, "#4e342e", "silla"),
        (230, 160, 40, 40, "#4e342e", "silla"),
        (590, 80, 90, 130, "#455a64", "armario"),
        (250, 380, 220, 25, "#37474f", "estante"),
        (100, 300, 60, 60, "#bf8040", "canion"),
    ]

    # --- Posiciones de los arboles (x, y) ---
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

    # --- Posiciones de los barriles (x, y) ---
    BARRILES = [
        (460, 230),
        (250, 300),
        (560, 250),
        (700, 180),
        (100, 480),
    ]

    # --- Nuevos mapas ---
    # Árbol especial en (500, 170) que lleva a la casita del árbol
    ARBOL_CASITA_X = 500
    ARBOL_CASITA_Y = 170
    # Escalera al 2° piso (posición dentro del interior)
    ESCALERA_INT_X = 620
    ESCALERA_INT_Y = 390
    ESCALERA_INT_W = 60
    ESCALERA_INT_H = 70
    # Trampilla al subterráneo (posición dentro del interior)
    TRAMPILLA_INT_X = 385
    TRAMPILLA_INT_Y = 210
    TRAMPILLA_INT_W = 55
    TRAMPILLA_INT_H = 45
    # Puentes del mapa de agua
    PUENTES_AGUA = [
        (70,  175, 310, 210),
        (260, 295, 490, 330),
        (440, 175, 670, 210),
        (140, 415, 380, 450),
        (540, 330, 760, 365),
    ]

    # --- Red ---
    SERVIDOR_PORT = 5000
    # IP del servidor del profesor. 127.0.0.1 solo funciona en la misma maquina.
    SERVIDOR_HOSTS = ["127.0.0.1", "3.85.165.104", "172.31.82.40"]

    # --- Chat ---
    CHAT_MAX_CARACTERES = 120
    CHAT_DURACION_FRAMES = 240  # ~4s a 60 FPS


# --- Quest: El Experimento del Profesor Álvaro ---
# Cada NPC tiene: nombre, mapa donde vive, posición y color
NPCS_DATA = {
    "fotografo":     {"nombre": "Fotógrafo",         "estado": "exterior",     "x": 350, "y": 330, "color": "#e67e22"},
    "borracho":      {"nombre": "Borracho del bar",  "estado": "bar",          "x": 250, "y": 300, "color": "#8e44ad"},
    "borracho_clima": {"nombre": "Cliente ebrio",    "estado": "bar",          "x": 560, "y": 380, "color": "#9b59b6"},
    "rumorista":     {"nombre": "Cliente nervioso",  "estado": "bar",          "x": 630, "y": 230, "color": "#34495e"},
    "bibliotecaria": {"nombre": "Bibliotecaria",     "estado": "biblioteca",   "x": 660, "y": 220, "color": "#16a085"},
    "ayudante":      {"nombre": "Ayudante nervioso", "estado": "casita_arbol", "x": 560, "y": 300, "color": "#c0392b"},
    "guardia":       {"nombre": "Guardia jubilado",  "estado": "interior",     "x": 490, "y": 290, "color": "#2c3e50"},
    "conserje":      {"nombre": "Conserje",          "estado": "exterior",     "x": 240, "y": 430, "color": "#7f8c8d"},
    "debug_laboratorio": {"nombre": "Técnico debug", "estado": "interior",     "x": 210, "y": 260, "color": "#f1c40f"},
}


class JuegoMultijugador:
    def _cargar_hosts_servidor(self):
        """Carga hosts desde archivo externo, con fallback a los definidos en cfg."""
        hosts = list(cfg.SERVIDOR_HOSTS)
        try:
            # En EXE usa carpeta del ejecutable; en .py usa carpeta del script.
            base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
            cfg_path = os.path.join(base_dir, "servidor_hosts.txt")
            if os.path.exists(cfg_path):
                nuevos = []
                with open(cfg_path, "r", encoding="utf-8") as f:
                    for linea in f:
                        host = linea.strip()
                        if host and not host.startswith("#"):
                            nuevos.append(host)
                if nuevos:
                    hosts = nuevos
        except Exception:
            pass

        # Eliminar duplicados conservando orden.
        vistos = set()
        unicos = []
        for h in hosts:
            if h not in vistos:
                vistos.add(h)
                unicos.append(h)
        return unicos

    def __init__(self, root):
        self.root = root
        self.root.title("Aventura Multijugador")
        self.root.resizable(False, False)

        self.root.withdraw()
        nombre = simpledialog.askstring("Nombre", "Escribe tu nombre:", parent=self.root)
        self.nombre = (nombre or "").strip()
        if not self.nombre:
            self.root.destroy()
            return

        # Seleccionar clase
        self.clase = self._seleccionar_clase()
        if not self.clase:
            self.root.destroy()
            return

        color_elegido = colorchooser.askcolor(
            color=cfg.COLOR_CUERPO,
            title="Escoge tu color",
            parent=self.root,
        )[1]
        self.color = self._normalizar_color(color_elegido, cfg.COLOR_CUERPO)

        # Conectar al servidor
        self.socket = None
        conectado = False
        self.hosts_servidor = self._cargar_hosts_servidor()
        for host in self.hosts_servidor:
            try:
                # Crear un socket por intento evita errores de reconexion en Windows.
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((host, cfg.SERVIDOR_PORT))
                s.settimeout(None)
                self.socket = s
                conectado = True
                break
            except:
                try:
                    s.close()
                except:
                    pass

        if not conectado:
            messagebox.showerror(
                "Error",
                "No se pudo conectar al servidor en: " + ", ".join(self.hosts_servidor),
            )
            root.destroy()
            return

        self.root.deiconify()

        self.canvas = tk.Canvas(root, width=cfg.ANCHO, height=cfg.ALTO)
        self.canvas.pack()

        self.estado = "exterior"
        self.px = cfg.ANCHO // 2
        self.py = cfg.ALTO // 2
        self.spawn_inicial_recibido = False
        self.msg_timer = 0
        self.hud = None
        self.msg = None
        self.chat_input = None
        self.chat_activo = False
        self.chat_texto_actual = ""
        self.chat_pendiente = None
        self.accion_pendiente = None
        self.chat_burbujas = {}

        # Otros jugadores
        self.otros_jugadores = {}
        self.id_jugador = None
        self.nombre_color_sincronizado = False

        # Sistema de habilidades
        self.habilidad_activa = False
        self.casteo_timer = 0
        self.casteo_duracion = 0
        self.casteo_accion = None
        self.ataque_timer = 0
        self.particulas = []  # Lista de partículas para efectos visuales
        self.efectos_recibidos = {}  # id_evento -> frames restantes (evita duplicados)
        self.animaciones_espada = []
        self.animaciones_efecto = []
        # Sistema de HP y muerte
        self.hp = 100
        self.hp_max = 100
        self.muerto = False
        self.muerte_timer = 0
        # Rata monstruo del sótano
        self.rata = self._rata_inicial()
        self.profesor_id = None
        self.alerta_laboratorio_texto = None
        self.alerta_laboratorio_timer = 0
        # Sala de práctica
        self.cristales = self._cristales_iniciales()
        self.pinchos = self._pinchos_iniciales()
        self.pincho_danio_timer = 0
        self.peces = [         # Posiciones base de los peces en mapa de agua
            (150, 280), (310, 420), (490, 150), (650, 380),
            (100, 460), (420, 310), (580, 480),
        ]

        # Quest: El Experimento del Profesor Álvaro
        # paso 0=inicio, 1-6=progreso, 7=completada (llave obtenida)
        self.quest_paso = 0
        self.quest_item = None   # item actual en el inventario
        self.debug_quest_unlock_usado = False

        self.teclas = set()
        self.root.bind("<KeyPress>", self.tecla_presionada)
        self.root.bind("<KeyRelease>", self.tecla_soltada)

        # Iniciar thread de recepcion
        self.thread_recepcion = threading.Thread(target=self._recibir_datos, daemon=True)
        self.thread_recepcion.start()

        # Enviar nombre y color iniciales inmediatamente
        self._enviar_posicion()

        self._dibujar_exterior()
        self._loop()

    # --- Network ---

    def _recibir_datos(self):
        """Thread que recibe datos del servidor con framing por lineas."""
        buffer = ""
        while True:
            try:
                chunk = self.socket.recv(4096).decode()
                if not chunk:
                    break
                buffer += chunk
                # Procesar todas las lineas completas del buffer
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        try:
                            info = json.loads(line)
                        except Exception:
                            info = ast.literal_eval(line)
                        self.id_jugador = info.get("tu_id")
                        if not self.spawn_inicial_recibido and "tu_pos" in info:
                            self.px, self.py, self.estado = info["tu_pos"]
                            self.spawn_inicial_recibido = True
                        nombre_srv = info.get("tu_nombre")
                        if isinstance(nombre_srv, str) and nombre_srv.strip():
                            self.nombre = nombre_srv.strip()
                        clase_srv = info.get("tu_clase")
                        if isinstance(clase_srv, str) and clase_srv.strip():
                            self.clase = clase_srv.strip().lower()
                        profesor_id_srv = info.get("profesor_id")
                        if isinstance(profesor_id_srv, str) and profesor_id_srv:
                            self.profesor_id = profesor_id_srv
                        alerta_srv = info.get("laboratorio_alerta")
                        if isinstance(alerta_srv, str) and alerta_srv.strip():
                            self.alerta_laboratorio_texto = alerta_srv.strip()
                            self.alerta_laboratorio_timer = 8 * 60
                        # El nombre y color los elige el cliente; no los sobreescribimos con datos del servidor.
                        self.otros_jugadores = info.get("jugadores", {})
                        raton_srv = info.get("raton")
                        if isinstance(raton_srv, dict):
                            self.rata = raton_srv
                        hp_srv = info.get("tu_hp")
                        if isinstance(hp_srv, int):
                            self.hp = max(0, hp_srv)
                        hp_max_srv = info.get("tu_hp_max")
                        if isinstance(hp_max_srv, int) and hp_max_srv > 0:
                            self.hp_max = hp_max_srv
                        muerto_srv = info.get("tu_muerto")
                        if isinstance(muerto_srv, bool):
                            self.muerto = muerto_srv
                        timer_srv = info.get("tu_muerte_timer")
                        if isinstance(timer_srv, int):
                            self.muerte_timer = max(0, timer_srv)
                        self._procesar_efectos_remotos(info.get("efectos"))
                        self._registrar_chat(self.id_jugador, info.get("tu_chat"))
                        for oid, datos in self.otros_jugadores.items():
                            self._registrar_chat(oid, datos.get("chat"))
                    except Exception:
                        pass  # Linea malformada, ignorar y continuar
            except Exception:
                break

    def _enviar_posicion(self):
        """Envia la posicion al servidor"""
        try:
            msg = json.dumps({
                "x": self.px,
                "y": self.py,
                "estado": self.estado,
                "nombre": self.nombre,
                "color": self.color,
                "clase": self.clase,
                "chat": self.chat_pendiente,
                "accion": self.accion_pendiente,
            }) + "\n"
            self.socket.send(msg.encode())
            self.chat_pendiente = None
            self.accion_pendiente = None
        except:
            pass

    @staticmethod
    def _normalizar_color(color, fallback):
        if isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color.strip()):
            return color.strip().lower()
        return fallback

    def _seleccionar_clase(self):
        """Abre un diálogo para seleccionar la clase del personaje."""
        resultado = simpledialog.askstring(
            "Selecciona tu Clase",
            "Escribe tu clase:\n\n1. Paladin (Ataque con espada)\n2. Hechicero (Lanza fuego)\n3. Sanador (Sana cercanos)\n\nEscribe: paladin, hechicero o sanador",
            parent=self.root
        )
        
        if resultado:
            clase = resultado.strip().lower()
            if clase in ("paladin", "1"):
                return "paladin"
            elif clase in ("hechicero", "mago", "2"):
                return "hechicero"
            elif clase in ("sanador", "3"):
                return "sanador"
        
        return None  # Canceló o selección inválida

    # --- Dibujo exterior ---

    def _dibujar_exterior(self):
        c = self.canvas
        c.delete("all")

        # Cesped
        for x in range(0, cfg.ANCHO, 80):
            for y in range(0, cfg.ALTO, 80):
                col = cfg.COLOR_CESPED_CLARO if (x // 80 + y // 80) % 2 == 0 else cfg.COLOR_CESPED_OSCURO
                c.create_rectangle(x, y, x + 80, y + 80, fill=col, outline="")

        # Lago
        lx, ly, rx, ry = cfg.LAGO_X, cfg.LAGO_Y, cfg.LAGO_RX, cfg.LAGO_RY
        c.create_oval(lx-rx, ly-ry, lx+rx, ly+ry,
                      fill=cfg.COLOR_LAGO, outline=cfg.COLOR_LAGO_BORDE, width=3)
        c.create_oval(lx-rx//2, ly-ry//3, lx+10, ly+10,
                      fill=cfg.COLOR_LAGO_BRILLO, outline="")

        # Casa
        cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
        pared_y = cy + ch // 4
        c.create_polygon(cx-10, pared_y, cx+cw+10, pared_y, cx+cw//2, cy-25,
                         fill=cfg.COLOR_CASA_TECHO, outline="#5C1A00", width=2)
        c.create_rectangle(cx, pared_y, cx+cw, cy+ch,
                           fill=cfg.COLOR_CASA_PARED, outline="#a0522d", width=2)
        c.create_rectangle(cx+10, pared_y+10, cx+35, pared_y+35, fill="#aee6ff", outline="#555")
        c.create_rectangle(cx+cw-35, pared_y+10, cx+cw-10, pared_y+35, fill="#aee6ff", outline="#555")
        px_p = cx + cw // 2 - 14
        c.create_rectangle(px_p, cy+ch-40, px_p+28, cy+ch,
                           fill=cfg.COLOR_CASA_PUERTA, outline="#3e2000", width=2)

        # Arboles (el de 500,170 es la casita del arbol - sin colision)
        for ax, ay in cfg.ARBOLES:
            c.create_oval(ax-18, ay-8, ax+18, ay+14, fill=cfg.COLOR_SOMBRA_ARBOL, outline="")
            if ax == cfg.ARBOL_CASITA_X and ay == cfg.ARBOL_CASITA_Y:
                c.create_oval(ax-22, ay-28, ax+22, ay+12,
                              fill="#1b5e20", outline="#ffd700", width=3)
                c.create_rectangle(ax-5, ay+10, ax+5, ay+22, fill=cfg.COLOR_TRONCO, outline="")
                c.create_text(ax, ay-40, text="Casita del arbol",
                              fill="#ffd700", font=("Consolas", 7, "bold"))
            else:
                c.create_oval(ax-20, ay-25, ax+20, ay+10,
                              fill=cfg.COLOR_COPA, outline=cfg.COLOR_BORDE_COPA, width=2)
                c.create_rectangle(ax-5, ay+8, ax+5, ay+20, fill=cfg.COLOR_TRONCO, outline="")

        # Indicador de mapa de agua en el borde inferior
        c.create_rectangle(0, cfg.ALTO-12, cfg.ANCHO, cfg.ALTO, fill="#1a6fa8", outline="")
        c.create_text(cfg.ANCHO//2, cfg.ALTO-6, text="v  Mapa de Agua  v",
                      fill="white", font=("Consolas", 8, "bold"))
        c.create_rectangle(0, cfg.ALTO // 2 - 70, 12, cfg.ALTO // 2 + 70, fill="#8b5a2b", outline="")
        c.create_text(18, cfg.ALTO // 2, text="<\nB\nA\nR", fill="#ffe082", font=("Consolas", 8, "bold"))
        c.create_rectangle(cfg.ANCHO - 12, cfg.ALTO // 2 - 70, cfg.ANCHO, cfg.ALTO // 2 + 70, fill="#5d4037", outline="")
        c.create_text(cfg.ANCHO - 18, cfg.ALTO // 2, text="B\nI\nB\nL\nI\nO\n>", fill="#e0f2f1", font=("Consolas", 8, "bold"))

        # Barriles
        for bx, by in cfg.BARRILES:
            r = cfg.RADIO_BARRIL
            c.create_oval(bx-r, by-r, bx+r, by+r,
                          fill=cfg.COLOR_BARRIL, outline=cfg.COLOR_BARRIL_ARO, width=3)
            c.create_line(bx-r+2, by-4, bx+r-2, by-4, fill=cfg.COLOR_BARRIL_ARO, width=2)
            c.create_line(bx-r+2, by+4, bx+r-2, by+4, fill=cfg.COLOR_BARRIL_ARO, width=2)

        # Dibujar otros jugadores
        self._dibujar_otros_jugadores()

        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                  text="Flechas para moverse | Izquierda: Bar | Derecha: Biblioteca | Casa por la puerta",
                                  fill="white", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 30,
                                 text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10,
                                              text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Dibujo interior ---

    def _dibujar_bar(self):
        c = self.canvas
        c.delete("all")

        # Piso de madera oscura
        for x in range(0, cfg.ANCHO, 50):
            for y in range(0, cfg.ALTO, 50):
                col = "#5c3b2e" if ((x // 50) + (y // 50)) % 2 == 0 else "#6b4738"
                c.create_rectangle(x, y, x + 50, y + 50, fill=col, outline="#4a2f25")

        # Paredes
        g = 30
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill="#3d2a1f", outline="")
        c.create_rectangle(0, cfg.ALTO - g, cfg.ANCHO, cfg.ALTO, fill="#3d2a1f", outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill="#3d2a1f", outline="")
        c.create_rectangle(cfg.ANCHO - g, 0, cfg.ANCHO, cfg.ALTO, fill="#3d2a1f", outline="")

        # Barra principal
        c.create_rectangle(70, 90, 330, 180, fill="#4e342e", outline="#2e1a0e", width=3)
        c.create_text(200, 78, text="Bar La Rata Tuerta", fill="#ffd166", font=("Consolas", 11, "bold"))
        for bx in range(90, 320, 55):
            c.create_oval(bx, 115, bx + 20, 135, fill="#ffe082", outline="#c9a13f")

        # Mesas y sillas
        mesas = [(460, 150), (620, 310), (420, 430)]
        for mx, my in mesas:
            c.create_oval(mx - 50, my - 35, mx + 50, my + 35, fill="#7b4f37", outline="#4a2f25", width=2)
            c.create_rectangle(mx - 8, my + 30, mx + 8, my + 58, fill="#4a2f25", outline="")
            c.create_rectangle(mx - 75, my - 15, mx - 55, my + 15, fill="#5d4037", outline="#2e1a0e")
            c.create_rectangle(mx + 55, my - 15, mx + 75, my + 15, fill="#5d4037", outline="#2e1a0e")

        # Indicador de salida (borde derecho)
        c.create_rectangle(cfg.ANCHO - 24, cfg.ALTO // 2 - 80, cfg.ANCHO, cfg.ALTO // 2 + 80,
                           fill="#228B22", outline="#00FF00", width=2)
        c.create_text(cfg.ANCHO - 12, cfg.ALTO // 2, text=">\n>\n>", fill="#00FF00", font=("Consolas", 11, "bold"))

        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(
            cfg.ANCHO // 2,
            cfg.ALTO - 18,
            text="Bar | Flechas para moverse | Salida por el borde derecho",
            fill="white",
            font=("Consolas", 12),
        )
        self.msg = c.create_text(cfg.ANCHO // 2, 42, text="", fill="#ffd166", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    def _dibujar_biblioteca(self):
        c = self.canvas
        c.delete("all")

        # Piso claro de biblioteca
        for x in range(0, cfg.ANCHO, 50):
            for y in range(0, cfg.ALTO, 50):
                col = "#d8c3a5" if ((x // 50) + (y // 50)) % 2 == 0 else "#cbb08f"
                c.create_rectangle(x, y, x + 50, y + 50, fill=col, outline="#b08f6a")

        # Paredes
        g = 30
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill="#6d4c41", outline="")
        c.create_rectangle(0, cfg.ALTO - g, cfg.ANCHO, cfg.ALTO, fill="#6d4c41", outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill="#6d4c41", outline="")
        c.create_rectangle(cfg.ANCHO - g, 0, cfg.ANCHO, cfg.ALTO, fill="#6d4c41", outline="")

        # Estanterías con libros
        estantes = [(80, 90, 320, 180), (80, 230, 320, 320), (80, 370, 320, 460), (460, 110, 720, 470)]
        colores = ["#c0392b", "#2980b9", "#27ae60", "#8e44ad", "#f39c12", "#7f8c8d"]
        for ex1, ey1, ex2, ey2 in estantes:
            c.create_rectangle(ex1, ey1, ex2, ey2, fill="#6d4c41", outline="#4e342e", width=3)
            for y in range(ey1 + 25, ey2, 35):
                c.create_line(ex1 + 8, y, ex2 - 8, y, fill="#4e342e", width=2)
                for x in range(ex1 + 12, ex2 - 20, 18):
                    c.create_rectangle(x, y - 20, x + 12, y - 2, fill=colores[(x + y) % len(colores)], outline="")

        # Mesas de lectura
        for mx, my in [(500, 180), (610, 320), (500, 450)]:
            c.create_rectangle(mx - 70, my - 28, mx + 70, my + 28, fill="#8d6e63", outline="#5d4037", width=2)
            c.create_rectangle(mx - 95, my - 16, mx - 76, my + 16, fill="#6d4c41", outline="#4e342e")
            c.create_rectangle(mx + 76, my - 16, mx + 95, my + 16, fill="#6d4c41", outline="#4e342e")

        # Indicador de salida (borde izquierdo)
        c.create_rectangle(0, cfg.ALTO // 2 - 80, 24, cfg.ALTO // 2 + 80,
                           fill="#228B22", outline="#00FF00", width=2)
        c.create_text(12, cfg.ALTO // 2, text="<\n<\n<", fill="#00FF00", font=("Consolas", 11, "bold"))

        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(
            cfg.ANCHO // 2,
            cfg.ALTO - 18,
            text="Biblioteca | Flechas para moverse | Salida por el borde izquierdo",
            fill="white",
            font=("Consolas", 12),
        )
        self.msg = c.create_text(cfg.ANCHO // 2, 42, text="", fill="#333333", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    def _dibujar_interior(self):
        c = self.canvas
        c.delete("all")

        # Piso
        for x in range(0, cfg.ANCHO, 60):
            for y in range(0, cfg.ALTO, 60):
                col = cfg.COLOR_PISO if (x // 60 + y // 60) % 2 == 0 else cfg.COLOR_PISO_ALT
                c.create_rectangle(x, y, x+60, y+60, fill=col, outline="#b0905a")

        # Paredes
        g = 30
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(0, cfg.ALTO-g, cfg.ANCHO, cfg.ALTO, fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(cfg.ANCHO-g, 0, cfg.ANCHO, cfg.ALTO, fill=cfg.COLOR_PARED_INT, outline="")

        # Puerta de salida
        sx = cfg.SALIDA_INT_X
        c.create_rectangle(sx-28, cfg.ALTO-g-2, sx+28, cfg.ALTO,
                           fill=cfg.COLOR_CASA_PUERTA, outline="#3e2000", width=2)
        c.create_text(sx, cfg.ALTO-g-15, text="Salida", fill="white", font=("Consolas", 10, "bold"))

        # Muebles
        for mx, my, mw, mh, mcolor, mlabel in cfg.MUEBLES:
            c.create_rectangle(mx, my, mx+mw, my+mh, fill=mcolor, outline="#2e1a0e", width=2)
            c.create_text(mx+mw//2, my+mh//2, text=mlabel, fill="#f5deb3", font=("Consolas", 9))

        # Escalera al 2° piso (inferior derecha)
        ex, ey = cfg.ESCALERA_INT_X, cfg.ESCALERA_INT_Y
        for i in range(5):
            c.create_rectangle(ex, ey + i*14, ex + cfg.ESCALERA_INT_W, ey + i*14 + 11,
                               fill="#c8a96e", outline="#8b6045", width=1)
        c.create_text(ex + cfg.ESCALERA_INT_W//2, ey - 14,
                      text="^ 2o Piso", fill="#ffd700", font=("Consolas", 9, "bold"))

        # Trampilla al subterráneo
        tx2, ty2 = cfg.TRAMPILLA_INT_X, cfg.TRAMPILLA_INT_Y
        c.create_rectangle(tx2, ty2, tx2 + cfg.TRAMPILLA_INT_W, ty2 + cfg.TRAMPILLA_INT_H,
                           fill="#4a3020", outline="#8b6045", width=3)
        c.create_oval(tx2+4, ty2+4, tx2+12, ty2+12, fill="#c0a060", outline="#8b6045")
        c.create_oval(tx2+4, ty2+cfg.TRAMPILLA_INT_H-12,
                      tx2+12, ty2+cfg.TRAMPILLA_INT_H-4, fill="#c0a060", outline="#8b6045")
        c.create_arc(tx2+cfg.TRAMPILLA_INT_W//2-10, ty2+cfg.TRAMPILLA_INT_H//2-5,
                     tx2+cfg.TRAMPILLA_INT_W//2+10, ty2+cfg.TRAMPILLA_INT_H//2+5,
                     start=0, extent=180, fill="#c0a060", outline="#8b6045")
        c.create_text(tx2 + cfg.TRAMPILLA_INT_W//2, ty2 - 14,
                      text="v Subterraneo", fill="#ffd700", font=("Consolas", 9, "bold"))

        # Dibujar otros jugadores
        self._dibujar_otros_jugadores()

        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="Flechas para moverse | Toca la salida para salir",
                                 fill="white", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 50,
                                 text="Bienvenido a la casa",
                                 fill="yellow", font=("Consolas", 14, "bold"))
        self.msg_timer = 120
        self.jugadores_online = c.create_text(10, 10,
                                              text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Segundo Piso ---

    def _dibujar_segundo_piso(self):
        c = self.canvas
        c.delete("all")
        g = 30
        col_pared = "#6a4c2e"

        # Piso de madera
        for x in range(0, cfg.ANCHO, 50):
            for y in range(0, cfg.ALTO, 50):
                col = "#c8a06e" if ((x // 50) + (y // 50)) % 2 == 0 else "#b09060"
                c.create_rectangle(x, y, x+50, y+50, fill=col, outline="#9a7a50")

        # Paredes
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill=col_pared, outline="")
        c.create_rectangle(0, cfg.ALTO-g, cfg.ANCHO, cfg.ALTO, fill=col_pared, outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill=col_pared, outline="")
        c.create_rectangle(cfg.ANCHO-g, 0, cfg.ANCHO, cfg.ALTO, fill=col_pared, outline="")

        # Pared divisoria x=400 con puerta en y=260-340
        mid = cfg.ANCHO // 2
        c.create_rectangle(mid-5, g, mid+5, 260, fill=col_pared, outline="")
        c.create_rectangle(mid-5, 340, mid+5, cfg.ALTO-g, fill=col_pared, outline="")
        c.create_rectangle(mid-8, 260, mid+8, 340, fill="#5d3a1a", outline="#3e2000", width=2)
        c.create_text(mid, 248, text="puerta", fill="#c8a96e", font=("Consolas", 8))

        # Ventanas
        for wx in [90, 700]:
            c.create_rectangle(wx, g+12, wx+70, g+62, fill="#aee6ff", outline="#777", width=2)
            c.create_line(wx+35, g+12, wx+35, g+62, fill="#777", width=1)
            c.create_line(wx, g+37, wx+70, g+37, fill="#777", width=1)

        # Habitacion izquierda: dormitorio
        # Cama
        c.create_rectangle(50, 90, 200, 200, fill="#7b1a1a", outline="#5a0e0e", width=2)
        c.create_rectangle(50, 90, 200, 130, fill="#e8d5c4", outline="#c4a090", width=1)
        c.create_oval(70, 96, 115, 124, fill="#f0e0d0", outline="")
        c.create_oval(125, 96, 170, 124, fill="#f0e0d0", outline="")
        c.create_text(125, 168, text="cama", fill="#f5deb3", font=("Consolas", 9))
        # Ropero
        c.create_rectangle(50, 350, 150, 490, fill="#5d4037", outline="#3e2000", width=2)
        c.create_line(100, 350, 100, 490, fill="#3e2000", width=1)
        c.create_oval(88, 416, 96, 424, fill="#c0a060", outline="")
        c.create_oval(104, 416, 112, 424, fill="#c0a060", outline="")
        c.create_text(100, 508, text="ropero", fill="#f5deb3", font=("Consolas", 9))
        # Alfombra
        c.create_oval(175, 300, 375, 445, fill="#8b1a1a", outline="#5a0e0e", width=3)
        c.create_oval(210, 325, 340, 420, fill="#a03030", outline="")

        # Habitacion derecha: estudio
        # Escritorio con pantalla
        c.create_rectangle(450, 90, 660, 170, fill="#5d4037", outline="#3e2000", width=2)
        c.create_rectangle(455, 100, 530, 160, fill="#aee6ff", outline="#888", width=1)
        c.create_text(490, 130, text="PC", fill="#0066ff", font=("Consolas", 8, "bold"))
        c.create_text(590, 130, text="escritorio", fill="#f5deb3", font=("Consolas", 9))
        # Silla giratoria
        c.create_oval(510, 178, 570, 235, fill="#37474f", outline="#263238", width=2)
        c.create_text(540, 206, text="silla", fill="#aaa", font=("Consolas", 8))
        # Estanteria con libros coloridos
        c.create_rectangle(450, 320, 750, 490, fill="#4a3728", outline="#3e2000", width=2)
        for shelf_y in [340, 380, 420, 460]:
            c.create_line(455, shelf_y, 745, shelf_y, fill="#3e2000", width=1)
        book_colors = ["#e53935", "#43a047", "#1e88e5", "#fb8c00", "#8e24aa", "#00acc1"]
        for i in range(24):
            bx = 460 + i * 22
            if bx > 740:
                break
            by = 342 + (i // 13) * 40
            if by < 465:
                c.create_rectangle(bx, by, bx+18, by+34, fill=book_colors[i % 6], outline="#000", width=1)

        # Escalera hacia abajo (esquina inferior derecha)
        ex, ey = cfg.ESCALERA_INT_X, cfg.ALTO - g - 90
        for i in range(5):
            c.create_rectangle(ex, ey + i*14, ex + cfg.ESCALERA_INT_W, ey + i*14 + 11,
                               fill="#c8a96e", outline="#8b6045", width=1)
        c.create_text(ex + cfg.ESCALERA_INT_W//2, ey - 14,
                      text="v Bajar", fill="white", font=("Consolas", 10, "bold"))

        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="2o Piso | Puerta al centro | v Bajar en escalera (der-inf)",
                                 fill="white", font=("Consolas", 11))
        self.msg = c.create_text(cfg.ANCHO//2, 50, text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Subterraneo ---

    def _dibujar_subterraneo(self):
        c = self.canvas
        c.delete("all")
        g = 30
        t = time.time()

        # Suelo de piedra oscura
        for x in range(0, cfg.ANCHO, 50):
            for y in range(0, cfg.ALTO, 50):
                col = "#2a2a2a" if ((x // 50) + (y // 50)) % 2 == 0 else "#333333"
                c.create_rectangle(x, y, x+50, y+50, fill=col, outline="#1a1a1a")

        # Paredes de ladrillo
        col_pared = "#3d2b1f"
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill=col_pared, outline="")
        c.create_rectangle(0, cfg.ALTO-g, cfg.ANCHO, cfg.ALTO, fill=col_pared, outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill=col_pared, outline="")
        c.create_rectangle(cfg.ANCHO-g, 0, cfg.ANCHO, cfg.ALTO, fill=col_pared, outline="")
        # Detalle de ladrillos en la pared superior
        for bx in range(0, cfg.ANCHO, 32):
            c.create_rectangle(bx+1, 2, bx+30, g-2, fill="#4a3025", outline="#2a1a10")

        # Tuberia horizontal superior
        c.create_rectangle(g, 68, cfg.ANCHO-g, 90, fill="#708090", outline="#4a5a6a", width=2)
        for bx in range(g+35, cfg.ANCHO-g, 70):
            c.create_oval(bx-5, 74, bx+5, 84, fill="#9090a0", outline="#606070", width=1)

        # Tuberia horizontal media
        c.create_rectangle(g, 278, cfg.ANCHO-g, 300, fill="#607080", outline="#4a5a6a", width=2)
        for bx in range(g+35, cfg.ANCHO-g, 70):
            c.create_oval(bx-5, 284, bx+5, 294, fill="#8090a0", outline="#606070", width=1)

        # Tuberia vertical izquierda
        c.create_rectangle(158, g, 180, cfg.ALTO-g, fill="#607090", outline="#4a5a6a", width=2)
        for py in range(g+35, cfg.ALTO-g, 60):
            c.create_oval(164, py-4, 174, py+4, fill="#8090a0", outline="#606070", width=1)

        # Tuberia vertical derecha
        c.create_rectangle(598, g, 620, cfg.ALTO-g, fill="#607090", outline="#4a5a6a", width=2)
        for py in range(g+35, cfg.ALTO-g, 60):
            c.create_oval(604, py-4, 614, py+4, fill="#8090a0", outline="#606070", width=1)

        # Cajas/Cajones
        for cx2, cy2 in [(230, 135), (360, 140), (510, 340), (680, 405), (82, 360), (430, 400)]:
            c.create_rectangle(cx2-22, cy2-22, cx2+22, cy2+22, fill="#5d4037", outline="#3e2000", width=2)
            c.create_line(cx2-22, cy2, cx2+22, cy2, fill="#3e2000", width=1)
            c.create_line(cx2, cy2-22, cx2, cy2+22, fill="#3e2000", width=1)

        # Antorchas animadas
        for tx, ty in [(82, 158), (718, 158), (82, 398), (718, 398), (400, 228)]:
            flicker = int(4 * math.sin(t * 9 + tx * 0.1))
            c.create_rectangle(tx-4, ty, tx+4, ty+16, fill="#8b4513", outline="")
            c.create_oval(tx-7+flicker, ty-14, tx+7-flicker, ty+2, fill="#ff8c00", outline="#ff4500", width=1)
            c.create_oval(tx-3, ty-10, tx+3, ty-2, fill="#ffff00", outline="")

        # Escalera de subida (al centro superior)
        lx = cfg.TRAMPILLA_INT_X + cfg.TRAMPILLA_INT_W // 2
        ly = g + 5
        for i in range(6):
            c.create_line(lx-15, ly + i*14, lx+15, ly + i*14, fill="#c8a96e", width=3)
        c.create_line(lx-15, ly, lx-15, ly + 5*14, fill="#8b6045", width=2)
        c.create_line(lx+15, ly, lx+15, ly + 5*14, fill="#8b6045", width=2)
        c.create_text(lx, ly - 13, text="^ Subir", fill="white", font=("Consolas", 10, "bold"))

        self._dibujar_otros_jugadores()
        self._dibujar_rata()
        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="Subterraneo | Toca la escalera central para subir",
                                 fill="#aaaaaa", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 50, text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Mapa de Agua ---

    def _dibujar_agua(self):
        c = self.canvas
        c.delete("all")
        t = time.time()

        # Agua de fondo
        c.create_rectangle(0, 0, cfg.ANCHO, cfg.ALTO, fill="#0d4f8b", outline="")

        # Ondas animadas
        for row in range(0, cfg.ALTO, 28):
            for col in range(0, cfg.ANCHO, 60):
                phase = math.sin(t * 1.5 + col * 0.04 + row * 0.02) * 5
                c.create_arc(col, row + phase, col+54, row + phase + 14,
                             start=0, extent=180, fill="#1a6fa8", outline="")

        # Reflejos de luz
        for bx, by in [(110, 140), (360, 78), (600, 195), (210, 395), (700, 345)]:
            c.create_oval(bx, by, bx+28, by+7, fill="#4fc3f7", outline="")

        # Puentes de madera
        for px1, py1, px2, py2 in cfg.PUENTES_AGUA:
            for tx in range(px1, px2, 22):
                c.create_rectangle(tx, py1, min(tx+20, px2), py2,
                                   fill="#c8a06e", outline="#8b6045", width=1)
            c.create_line(px1, py1-18, px2, py1-18, fill="#8b6045", width=2)
            c.create_line(px1, py1-18, px1, py2, fill="#8b6045", width=2)
            c.create_line(px2, py1-18, px2, py2, fill="#8b6045", width=2)
            for post_x in range(px1, px2+1, 40):
                c.create_line(post_x, py1-18, post_x, py1, fill="#8b6045", width=2)

        # Peces animados
        fish_cols = ["#ff6b35", "#ffd32a", "#e056da", "#54a0ff", "#ff9ff3", "#00d2d3", "#ff9f43"]
        for i, (fx, fy) in enumerate(self.peces):
            swim_x = fx + 35 * math.sin(t * 0.4 + i * 1.1)
            swim_y = fy + 8 * math.sin(t * 1.2 + i * 0.7)
            col = fish_cols[i % len(fish_cols)]
            going_right = math.cos(t * 0.4 + i * 1.1) > 0
            if going_right:
                c.create_oval(swim_x-14, swim_y-5, swim_x+14, swim_y+5, fill=col, outline="")
                c.create_polygon(swim_x-14, swim_y-6, swim_x-14, swim_y+6,
                                 swim_x-24, swim_y, fill=col, outline="")
                c.create_oval(swim_x+6, swim_y-3, swim_x+11, swim_y+2, fill="black", outline="")
            else:
                c.create_oval(swim_x-14, swim_y-5, swim_x+14, swim_y+5, fill=col, outline="")
                c.create_polygon(swim_x+14, swim_y-6, swim_x+14, swim_y+6,
                                 swim_x+24, swim_y, fill=col, outline="")
                c.create_oval(swim_x-11, swim_y-3, swim_x-6, swim_y+2, fill="black", outline="")

        # Indicador de salida (borde superior)
        c.create_rectangle(0, 0, cfg.ANCHO, 25, fill="#2d6a27", outline="")
        c.create_text(cfg.ANCHO//2, 13, text="^ Salida al exterior ^",
                      fill="white", font=("Consolas", 10, "bold"))

        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="Mapa de Agua | Flechas para moverse | ^ Arriba para salir",
                                 fill="white", font=("Consolas", 11))
        self.msg = c.create_text(cfg.ANCHO//2, 45, text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Casita del Arbol ---

    def _dibujar_casita_arbol(self):
        c = self.canvas
        c.delete("all")
        t = time.time()

        # Cielo
        c.create_rectangle(0, 0, cfg.ANCHO, cfg.ALTO, fill="#87ceeb", outline="")

        # Nubes animadas
        for i, (clx, cly, clw) in enumerate([(80, 55, 100), (350, 38, 130), (620, 65, 90), (200, 105, 80)]):
            drift = int(20 * math.sin(t * 0.15 + i))
            c.create_oval(clx+drift, cly, clx+clw+drift, cly+45, fill="white", outline="")
            c.create_oval(clx+20+drift, cly-18, clx+clw-20+drift, cly+32, fill="white", outline="")

        # Copas de arboles en el fondo
        for ax, ay in [(80, 510), (220, 490), (370, 515), (530, 500), (680, 508)]:
            c.create_oval(ax-45, ay-32, ax+45, ay+32, fill="#1b5e20", outline="#0a3d0a", width=2)
            c.create_oval(ax-25, ay-18, ax+25, ay+14, fill="#2e7d32", outline="")

        # Tronco del arbol principal
        c.create_rectangle(cfg.ANCHO//2-28, 420, cfg.ANCHO//2+28, cfg.ALTO, fill="#5d4037", outline="#3e2700", width=2)

        # Plataforma base de la casita
        c.create_rectangle(80, 395, 720, 428, fill="#c8a06e", outline="#8b6045", width=3)
        for px in range(80, 720, 28):
            c.create_line(px, 395, px, 428, fill="#8b6045", width=1)

        # Paredes de la casita
        c.create_rectangle(100, 160, 700, 398, fill="#d4a064", outline="#a0522d", width=3)

        # Techo a dos aguas
        c.create_polygon(70, 165, 730, 165, cfg.ANCHO//2, 62,
                         fill="#8B2500", outline="#5C1A00", width=3)

        # Piso interior
        for fx in range(100, 700, 44):
            for fy in range(160, 398, 44):
                col = "#c8a96e" if ((fx-100)//44 + (fy-160)//44) % 2 == 0 else "#b8995e"
                c.create_rectangle(fx, fy, fx+42, fy+42, fill=col, outline="#a0785a")

        # Ventanas
        for wx in [132, 570]:
            c.create_rectangle(wx, 200, wx+85, 285, fill="#aee6ff", outline="#777", width=2)
            c.create_line(wx+42, 200, wx+42, 285, fill="#777", width=1)
            c.create_line(wx, 242, wx+85, 242, fill="#777", width=1)

        # Muebles de la casita
        c.create_rectangle(255, 200, 400, 250, fill="#5d4037", outline="#3e2000", width=2)
        c.create_text(327, 225, text="mesa", fill="#f5deb3", font=("Consolas", 9))
        c.create_rectangle(425, 200, 545, 250, fill="#8b4513", outline="#5c2e00", width=2)
        c.create_text(485, 225, text="cofre", fill="#f5deb3", font=("Consolas", 9))
        c.create_rectangle(148, 315, 310, 380, fill="#455a64", outline="#263238", width=2)
        c.create_text(228, 348, text="armario", fill="#f5deb3", font=("Consolas", 9))

        # Cuerda/escalera de bajada (dentro del mapa, accesible)
        rx = cfg.ANCHO // 2
        c.create_rectangle(rx-22, 362, rx+22, 428, fill="#8b6045", outline="#5c3d1e", width=2)
        for i in range(5):
            c.create_line(rx-18, 370 + i*12, rx+18, 370 + i*12, fill="#c8a06e", width=3)
        c.create_line(rx-18, 370, rx-18, 370 + 4*12, fill="#8b6045", width=2)
        c.create_line(rx+18, 370, rx+18, 370 + 4*12, fill="#8b6045", width=2)
        c.create_text(rx, 352, text="v Bajar", fill="#fff", font=("Consolas", 10, "bold"))

        # Pajaros animados
        for i, (bx0, by0) in enumerate([(120, 88), (420, 52), (680, 98)]):
            bx = int(bx0 + 40 * math.sin(t * 0.4 + i * 1.5))
            wing = int(5 * math.sin(t * 4 + i))
            c.create_line(bx-10, by0+wing, bx, by0-5, fill="black", width=2)
            c.create_line(bx, by0-5, bx+10, by0+wing, fill="black", width=2)

        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="Casita del Arbol | Baja por la cuerda central",
                                 fill="#333333", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 50, text="", fill="#333", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="#333", font=("Consolas", 10))

    # --- Otros jugadores ---

    def _dibujar_otros_jugadores(self):
        """Dibuja todos los otros jugadores conectados con su color elegido."""
        c = self.canvas
        for jugador_id, datos in self.otros_jugadores.items():
            ox = datos.get("x", 0)
            oy = datos.get("y", 0)
            oestado = datos.get("estado", "exterior")
            nombre = str(datos.get("nombre", "")).strip() or jugador_id
            color = self._normalizar_color(datos.get("color"), "#4c6ef5")
            clase = str(datos.get("clase", "paladin")).strip().lower()
            
            if oestado == self.estado:
                r = cfg.RADIO
                c.create_text(ox + 1, oy-r-16 + 1, text=nombre, fill="black", font=("Consolas", 10, "bold"))
                c.create_text(ox, oy-r-16, text=nombre, fill="white", font=("Consolas", 10, "bold"))
                c.create_oval(ox-r+4, oy-r+8, ox+r+4, oy+r+8,
                              fill=cfg.COLOR_SOMBRA_ARBOL, outline="")
                c.create_oval(ox-r, oy-r, ox+r, oy+r,
                              fill=color, outline="#000000", width=2)
                c.create_oval(ox-r+5, oy-r+2, ox+r-5, oy+4,
                              fill="#ffcc80", outline="#e65100", width=1)
                c.create_oval(ox-7, oy-10, ox-3, oy-6, fill="black")
                c.create_oval(ox+3, oy-10, ox+7, oy-6, fill="black")

                self._dibujar_animaciones_jugador(c, jugador_id)
                
                # Dibujar atributo visual según la clase
                if clase == "paladin":
                    # Espada
                    c.create_line(ox+r+8, oy-r-5, ox+r+15, oy-r-15, fill="#c0c0c0", width=4)
                    c.create_rectangle(ox+r+12, oy-r-18, ox+r+18, oy-r-15, fill="#d4a574", outline="")
                elif clase == "hechicero":
                    # Sombrero de mago
                    c.create_polygon(ox-r-5, oy-r-3, ox-r+5, oy-r-3, ox-r+2, oy-r-15, fill="#4b0082", outline="#000080", width=2)
                    c.create_oval(ox-r-8, oy-r+2, ox-r+8, oy-r+8, fill="#4b0082", outline="#000080", width=1)
                    # Estrella en el sombrero
                    c.create_text(ox-r+1, oy-r-9, text="★", fill="#ffd700", font=("Consolas", 14))
                elif clase == "sanador":
                    # Libro
                    c.create_rectangle(ox+r+5, oy-r-8, ox+r+18, oy-r+8, fill="#8b4513", outline="#654321", width=2)
                    c.create_line(ox+r+11, oy-r-8, ox+r+11, oy-r+8, fill="#654321", width=1)
                    c.create_text(ox+r+8, oy-r-2, text="+", fill="#ff0000", font=("Consolas", 12, "bold"))
                elif clase == "profesor":
                    # Bata de laboratorio + lentes
                    c.create_rectangle(ox-r-6, oy-r+8, ox+r+6, oy+r+14, fill="#f4f7fb", outline="#cfd8dc", width=2)
                    c.create_line(ox, oy-r+8, ox, oy+r+14, fill="#b0bec5", width=1)
                    c.create_rectangle(ox-r+2, oy-r-2, ox+r-2, oy+r-4, fill="#f3d7b6", outline="#4e342e", width=2)
                    c.create_oval(ox-10, oy-10, ox-2, oy-2, fill="", outline="#263238", width=2)
                    c.create_oval(ox+2, oy-10, ox+10, oy-2, fill="", outline="#263238", width=2)
                    c.create_line(ox-2, oy-6, ox+2, oy-6, fill="#263238", width=2)
                    c.create_line(ox-r+3, oy-r+10, ox-r+12, oy-r+2, fill="#90caf9", width=2)
                    c.create_oval(ox-r+10, oy-r, ox-r+16, oy-r+6, fill="#42a5f5", outline="#1565c0", width=1)
                
                if self.clase == "sanador":
                    hp_oth = datos.get("hp", 100)
                    hp_max_oth = datos.get("hp_max", 100)
                    self._dibujar_barra_hp_personaje(c, ox, oy, hp_oth, hp_max_oth, nombre, color)

                chat = self.chat_burbujas.get(jugador_id)
                if chat:
                    self._dibujar_chat_en_posicion(ox, oy, chat["texto"])

                if datos.get("muerto"):
                    self._dibujar_muerte_overlay_en_posicion(ox, oy, datos.get("muerte_timer", 0))

    # --- Personaje ---

    def _dibujar_personaje(self):
        self.canvas.delete("personaje")
        c = self.canvas
        x, y, r = self.px, self.py, cfg.RADIO
        nombre_mostrar = str(self.nombre).strip() or "Tu jugador"
        c.create_text(x + 1, y-r-16 + 1, text=nombre_mostrar,
                      fill="black", font=("Consolas", 10, "bold"), tags="personaje")
        c.create_text(x, y-r-16, text=nombre_mostrar,
                      fill="white", font=("Consolas", 10, "bold"), tags="personaje")
        c.create_oval(x-r+4, y-r+8, x+r+4, y+r+8,
                      fill=cfg.COLOR_SOMBRA_ARBOL, outline="", tags="personaje")
        c.create_oval(x-r, y-r, x+r, y+r,
                      fill=self.color, outline=cfg.COLOR_BORDE_CUERPO, width=2, tags="personaje")
        c.create_oval(x-r+5, y-r+2, x+r-5, y+4,
                      fill=cfg.COLOR_CARA, outline=cfg.COLOR_BORDE_CARA, width=1, tags="personaje")
        c.create_oval(x-7, y-10, x-3, y-6, fill="black", tags="personaje")
        c.create_oval(x+3, y-10, x+7, y-6, fill="black", tags="personaje")

        self._dibujar_animaciones_jugador(c, self.id_jugador)
        if self.clase == "sanador":
            self._dibujar_barra_hp_personaje(c, x, y, self.hp, self.hp_max, nombre_mostrar, self.color)
        
        # Dibujar atributo visual según la clase
        if self.clase == "paladin":
            # Espada
            c.create_line(x+r+8, y-r-5, x+r+15, y-r-15, fill="#c0c0c0", width=4, tags="personaje")
            c.create_rectangle(x+r+12, y-r-18, x+r+18, y-r-15, fill="#d4a574", outline="", tags="personaje")
        elif self.clase == "hechicero":
            # Sombrero de mago
            c.create_polygon(x-r-5, y-r-3, x-r+5, y-r-3, x-r+2, y-r-15, fill="#4b0082", outline="#000080", width=2, tags="personaje")
            c.create_oval(x-r-8, y-r+2, x-r+8, y-r+8, fill="#4b0082", outline="#000080", width=1, tags="personaje")
            # Estrella en el sombrero
            c.create_text(x-r+1, y-r-9, text="★", fill="#ffd700", font=("Consolas", 14), tags="personaje")
        elif self.clase == "sanador":
            # Libro
            c.create_rectangle(x+r+5, y-r-8, x+r+18, y-r+8, fill="#8b4513", outline="#654321", width=2, tags="personaje")
            c.create_line(x+r+11, y-r-8, x+r+11, y-r+8, fill="#654321", width=1, tags="personaje")
            c.create_text(x+r+8, y-r-2, text="+", fill="#ff0000", font=("Consolas", 12, "bold"), tags="personaje")
        elif self.clase == "profesor":
            # Profesor de laboratorio: bata, lentes y matraz
            c.create_rectangle(x-r-6, y-r+8, x+r+6, y+r+14, fill="#f4f7fb", outline="#cfd8dc", width=2, tags="personaje")
            c.create_line(x, y-r+8, x, y+r+14, fill="#b0bec5", width=1, tags="personaje")
            c.create_rectangle(x-r+2, y-r-2, x+r-2, y+r-4, fill="#f3d7b6", outline="#4e342e", width=2, tags="personaje")
            c.create_oval(x-10, y-10, x-2, y-2, fill="", outline="#263238", width=2, tags="personaje")
            c.create_oval(x+2, y-10, x+10, y-2, fill="", outline="#263238", width=2, tags="personaje")
            c.create_line(x-2, y-6, x+2, y-6, fill="#263238", width=2, tags="personaje")
            c.create_line(x-r+3, y-r+10, x-r+12, y-r+2, fill="#90caf9", width=2, tags="personaje")
            c.create_oval(x-r+10, y-r, x-r+16, y-r+6, fill="#42a5f5", outline="#1565c0", width=1, tags="personaje")
        elif self.clase == "mutante":
            c.create_oval(x-r-2, y-r+2, x+r+2, y+r+6, fill="#8a4f2a", outline="#4e342e", width=2, tags="personaje")
            c.create_oval(x-r+4, y-r+8, x+r+4, y+r+12, fill="#5d4037", outline="#2e1a0e", width=2, tags="personaje")
            c.create_oval(x-r+12, y-r+2, x-r+20, y-r+10, fill="#8a4f2a", outline="#4e342e", width=1, tags="personaje")
            c.create_oval(x+r-20, y-r+2, x+r-12, y-r+10, fill="#8a4f2a", outline="#4e342e", width=1, tags="personaje")
            c.create_line(x-r+10, y+r, x-r+26, y+r+8, fill="#c0c0c0", width=3, tags="personaje")
            c.create_text(x, y-r-6, text="RAT", fill="#ff9e9e", font=("Consolas", 9, "bold"), tags="personaje")
        
        # Mostrar efecto de casteo si está activo
        if self.casteo_timer > 0:
            progress = 1 - (self.casteo_timer / self.casteo_duracion)
            barra_ancho = 40
            if self.casteo_accion == "sanacion":
                color_barra = "#ff4d6d"
                texto_casteo = "Cargando corazones"
            else:
                color_barra = "#ff8c00"
                texto_casteo = "Cargando fuego"
            c.create_rectangle(x-barra_ancho//2, y+r+15, x+barra_ancho//2, y+r+20, 
                             fill="#333333", outline="#ffffff", width=1, tags="personaje")
            c.create_rectangle(x-barra_ancho//2, y+r+15, x-barra_ancho//2 + barra_ancho*progress, y+r+20,
                             fill=color_barra, outline="", tags="personaje")
            c.create_text(x, y+r+28, text=f"{texto_casteo}... {self.casteo_timer/60:.1f}s", 
                         fill=color_barra, font=("Consolas", 9), tags="personaje")

        chat = self.chat_burbujas.get(self.id_jugador)
        if chat:
            self._dibujar_chat_en_posicion(x, y, chat["texto"])

    def _dibujar_alerta_laboratorio(self):
        self.canvas.delete("alerta_laboratorio")
        if self.alerta_laboratorio_timer <= 0 or not self.alerta_laboratorio_texto:
            return
        texto = self.alerta_laboratorio_texto
        ancho = max(520, min(760, 16 * len(texto)))
        x0 = cfg.ANCHO // 2 - ancho // 2
        x1 = cfg.ANCHO // 2 + ancho // 2
        y0 = 88
        y1 = 170
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#1a0000", outline="#ff3333", width=4, tags="alerta_laboratorio")
        self.canvas.create_text(cfg.ANCHO // 2, 118, text="ALERTA DEL LABORATORIO", fill="#ff5555", font=("Consolas", 20, "bold"), tags="alerta_laboratorio")
        self.canvas.create_text(cfg.ANCHO // 2, 150, text=texto, fill="#ffd6d6", font=("Consolas", 18, "bold"), tags="alerta_laboratorio")

    # --- Input ---

    def tecla_presionada(self, evento):
        tecla = evento.keysym.lower()

        if tecla == "f9" and self.clase in ("profesor", "mutante"):
            self.accion_pendiente = "mutante_transformar"
            return

        if self.clase == "mutante":
            if tecla == "f1":
                self.accion_pendiente = "mutante_esfera"
                return
            if tecla == "f2":
                self.accion_pendiente = "mutante_veneno"
                return
            if tecla == "f3":
                self.accion_pendiente = "mutante_velocidad"
                return

        if tecla == "f1":
            if self.clase == "paladin":
                self._ataque_paladin_izq()
            else:
                self._usar_habilidad()
            return

        if tecla == "f2":
            if self.clase == "paladin":
                self._ataque_paladin_der()
            return

        if tecla == "e" and not self.chat_activo:
            self._intentar_interactuar_npc()
            return

        if self.chat_activo:
            self._manejar_input_chat(evento)
            return

        if tecla in ("return", "kp_enter", "f12"):
            self.chat_activo = True
            self.chat_texto_actual = ""
            return

        self.teclas.add(tecla)

    def tecla_soltada(self, evento):
        self.teclas.discard(evento.keysym.lower())

    def _manejar_input_chat(self, evento):
        tecla = evento.keysym.lower()

        if tecla in ("return", "kp_enter"):
            texto = self.chat_texto_actual.strip()
            if texto:
                self.chat_pendiente = texto[:cfg.CHAT_MAX_CARACTERES]
                if self.id_jugador:
                    self.chat_burbujas[self.id_jugador] = {
                        "texto": self.chat_pendiente,
                        "timer": cfg.CHAT_DURACION_FRAMES,
                    }
            self.chat_texto_actual = ""
            self.chat_activo = False
            return

        if tecla == "escape":
            self.chat_texto_actual = ""
            self.chat_activo = False
            return

        if tecla == "backspace":
            self.chat_texto_actual = self.chat_texto_actual[:-1]
            return

        if evento.char and evento.char.isprintable() and len(self.chat_texto_actual) < cfg.CHAT_MAX_CARACTERES:
            self.chat_texto_actual += evento.char

    def _usar_habilidad(self):
        """Ejecuta la habilidad especial según la clase."""
        if self.clase == "paladin":
            self._ataque_paladin_izq()
        elif self.clase == "hechicero":
            if self.casteo_timer == 0:
                self._iniciar_casteo_hechizo()
        elif self.clase == "sanador":
            if self.casteo_timer == 0:
                self._iniciar_casteo_sanacion()

    def _ataque_paladin(self):
        """Paladin hace un ataque con espada hacia la izquierda."""
        self._ataque_paladin_izq()

    def _ataque_paladin_izq(self):
        """Paladin hace un ataque con espada hacia la izquierda."""
        self.ataque_timer = 30
        self.accion_pendiente = "ataque_paladin_izq"
        self._agregar_animacion_espada(self.px, self.py, "izq", self.id_jugador)
        self._daniar_cristales_cercanos(40, 80)

    def _ataque_paladin_der(self):
        """Paladin hace un ataque con espada hacia la derecha."""
        self.ataque_timer = 30
        self.accion_pendiente = "ataque_paladin_der"
        self._agregar_animacion_espada(self.px, self.py, "der", self.id_jugador)
        self._daniar_cristales_cercanos(40, 80)

    def _iniciar_casteo_hechizo(self):
        """Inicia el casteo del hechizo de fuego del hechicero."""
        self.casteo_timer = 90  # 1.5 segundos
        self.casteo_duracion = 90
        self.casteo_accion = "hechizo_fuego"

    def _iniciar_casteo_sanacion(self):
        """Inicia el casteo de sanación del sanador."""
        self.casteo_timer = 60  # 1 segundo
        self.casteo_duracion = 60
        self.casteo_accion = "sanacion"

    def _sanar_cercanos(self):
        """Sanador sana HP propio y muestra corazones."""
        self.accion_pendiente = "sanacion"
        self._agregar_animacion_corazon(self.px, self.py, self.id_jugador)
        self._daniar_cristales_cercanos(30, 100)

    def _rata_inicial(self):
        """Devuelve el estado inicial de la rata monstruo."""
        return {
            "x": 400.0, "y": 300.0,
            "hp": 4500, "hp_max": 4500,
            "vx": 1.5, "vy": 0.8,
            "estado": "patrulla",
            "ataque_timer": 0,
            "patrol_timer": 90,
            "magic_timer": random.randint(200, 380),
            "magic_casteo": 0,
            "magic_hechizo": 0,        # 1=proyectil  2=velocidad  3=veneno
            "magic_proyectiles": [],
            "vel_boost_timer": 0,      # frames restantes de velocidad doble
            "veneno_charcos": [],       # lista de {x,y,vida}
        }

    def _rata_inicial(self):
        """Devuelve el estado inicial de la rata monstruo."""
        return {
            "x": 400.0, "y": 300.0,
            "hp": 4500, "hp_max": 4500,
            "vx": 1.5, "vy": 0.8,
            "estado": "patrulla",
            "ataque_timer": 0,
            "patrol_timer": 90,
            "magic_timer": random.randint(200, 380),
            "magic_casteo": 0,
            "magic_hechizo": 0,        # 1=proyectil  2=velocidad  3=veneno
            "magic_proyectiles": [],
            "vel_boost_timer": 0,      # frames restantes de velocidad doble
            "veneno_charcos": [],       # lista de {x,y,vida}
        }

    # --- Sala de práctica ---

    def _cristales_iniciales(self):
        return [
            {"x": 150, "y": 150, "hp": 1000, "hp_max": 1000, "muerto": False, "muerte_timer": 0, "muerte_total": 5*60, "fase": random.uniform(0, 2*math.pi)},
            {"x": 650, "y": 150, "hp": 1000, "hp_max": 1000, "muerto": False, "muerte_timer": 0, "muerte_total": 5*60, "fase": random.uniform(0, 2*math.pi)},
            {"x": 400, "y": 300, "hp": 1000, "hp_max": 1000, "muerto": False, "muerte_timer": 0, "muerte_total": 5*60, "fase": random.uniform(0, 2*math.pi)},
            {"x": 150, "y": 450, "hp": 1000, "hp_max": 1000, "muerto": False, "muerte_timer": 0, "muerte_total": 5*60, "fase": random.uniform(0, 2*math.pi)},
            {"x": 650, "y": 450, "hp": 1000, "hp_max": 1000, "muerto": False, "muerte_timer": 0, "muerte_total": 5*60, "fase": random.uniform(0, 2*math.pi)},
        ]

    def _pinchos_iniciales(self):
        pinchos = []
        for px in range(100, cfg.ANCHO - 100, 120):
            for py in range(100, cfg.ALTO - 100, 100):
                pinchos.append({"x": px, "y": py})
        return pinchos

    def _dibujar_practica(self):
        c = self.canvas
        c.delete("all")
        t = time.time()
        # Piso de piedra
        for x in range(0, cfg.ANCHO, 50):
            for y in range(0, cfg.ALTO, 50):
                col = "#3a3a3a" if ((x // 50) + (y // 50)) % 2 == 0 else "#4a4a4a"
                c.create_rectangle(x, y, x+50, y+50, fill=col, outline="#2a2a2a")
        # Paredes
        g = 30
        c.create_rectangle(0, 0, cfg.ANCHO, g, fill="#6a5a4a", outline="")
        c.create_rectangle(0, cfg.ALTO-g, cfg.ANCHO, cfg.ALTO, fill="#6a5a4a", outline="")
        c.create_rectangle(0, 0, g, cfg.ALTO, fill="#6a5a4a", outline="")
        c.create_rectangle(cfg.ANCHO-g, 0, cfg.ANCHO, cfg.ALTO, fill="#6a5a4a", outline="")
        # Indicadores de salida
        c.create_rectangle(cfg.ANCHO//2-80, 0, cfg.ANCHO//2+80, 25, fill="#228B22", outline="#00FF00", width=2)
        c.create_text(cfg.ANCHO//2, 13, text="^ Salida al Exterior ^", fill="#00FF00", font=("Consolas", 10, "bold"))
        c.create_rectangle(cfg.ANCHO//2-80, cfg.ALTO-25, cfg.ANCHO//2+80, cfg.ALTO, fill="#228B22", outline="#00FF00", width=2)
        c.create_text(cfg.ANCHO//2, cfg.ALTO-13, text="v Salida al Exterior v", fill="#00FF00", font=("Consolas", 10, "bold"))
        # Pinchos
        for pincho in self.pinchos:
            self._dibujar_pincho(c, pincho["x"], pincho["y"], t)
        # Cristales
        self._dibujar_cristales(c, t)
        # Jugadores
        self._dibujar_otros_jugadores()
        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                 text="Sala de Práctica | Evita los pinchos | Ataca los cristales",
                                 fill="#aaaaaa", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 50, text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10, text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    def _dibujar_pincho(self, c, x, y, t):
        pulso = int(2 * math.sin(t * 3 + x * 0.03))
        base_top = y + 4
        base_bottom = y + 16
        c.create_rectangle(x-14, base_top, x+14, base_bottom, fill="#5a5a5a", outline="#303030", width=2)
        for offset in (-10, -3, 4, 11):
            alto = 16 + pulso if offset in (-3, 4) else 13 + pulso
            c.create_polygon(x+offset, base_top, x+offset+5, base_top, x+offset+2.5, base_top-alto,
                             fill="#ff7a7a", outline="#bb2222", width=1)

    def _dibujar_cristales(self, c, t):
        for cristal in self.cristales:
            x = int(cristal["x"])
            y = int(cristal["y"] + 6 * math.sin(t * 2.4 + cristal.get("fase", 0)))
            if cristal["muerto"]:
                total = max(1, cristal.get("muerte_total", 5 * 60))
                restante = max(0, cristal.get("muerte_timer", 0))
                progreso = 1 - (restante / total)
                esc = 1.0 - 0.25 * progreso
                trozos = [
                    (-15, -5, 6), (-7, 8, 5), (10, -4, 7),
                    (16, 9, 5), (-2, -12, 4), (4, 14, 6),
                ]
                for dx, dy, tam in trozos:
                    tx = x + int(dx * esc)
                    ty = y + int(dy * esc)
                    r = max(2, int(tam * esc))
                    c.create_polygon(
                        tx, ty - r,
                        tx + r, ty,
                        tx, ty + r,
                        tx - r, ty,
                        fill="#36d8ff",
                        outline="#0ba6d1",
                        width=1,
                    )
                radio_nucleo = 5 + int(4 * progreso)
                c.create_oval(
                    x - radio_nucleo,
                    y - radio_nucleo,
                    x + radio_nucleo,
                    y + radio_nucleo,
                    fill="#72f4ff",
                    outline="",
                )
                continue
            c.create_polygon(x, y-26, x+20, y-8, x+20, y+18, x, y+30, x-20, y+18, x-20, y-8,
                             fill="#00CCFF", outline="#0099FF", width=2)
            brillo = int(3 * math.sin(t * 2))
            c.create_oval(x-6+brillo, y-19, x+6+brillo, y-7, fill="#88FFFF", outline="")
            bar_w = 36
            hp_pct = cristal["hp"] / cristal["hp_max"]
            c.create_rectangle(x-bar_w//2, y-35, x+bar_w//2, y-30, fill="#330000", outline="#888888")
            c.create_rectangle(x-bar_w//2, y-35, x-bar_w//2+int(bar_w*hp_pct), y-30, fill="#00FF00", outline="")

    def _actualizar_practica(self):
        if self.pincho_danio_timer > 0:
            self.pincho_danio_timer -= 1
        for pincho in self.pinchos:
            if math.hypot(self.px - pincho["x"], self.py - pincho["y"]) < cfg.RADIO + 20:
                if self.pincho_danio_timer <= 0:
                    self.accion_pendiente = "danio_pincho"
                    self.pincho_danio_timer = 30
        for cristal in self.cristales:
            if cristal["muerto"]:
                cristal["muerte_timer"] -= 1
                if cristal["muerte_timer"] <= 0:
                    cristal["muerto"] = False
                    cristal["hp"] = cristal["hp_max"]

    def _daniar_cristales_cercanos(self, danio, alcance=80):
        if self.estado != "practica":
            return
        for cristal in self.cristales:
            if not cristal["muerto"]:
                dist = math.hypot(self.px - cristal["x"], self.py - cristal["y"])
                if dist < alcance:
                    cristal["hp"] = max(0, cristal["hp"] - danio)
                    if cristal["hp"] <= 0:
                        cristal["muerto"] = True
                        cristal["muerte_total"] = 5 * 60
                        cristal["muerte_timer"] = cristal["muerte_total"]



        r = self.rata
        dx = self.px - r["x"]
        dy = self.py - r["y"]
        dist = math.hypot(dx, dy)

        VEL_BASE  = 2.2
        DETECCION = 220
        ALCANCE   = 45

        # Velocidad actual (normal o boost x3)
        if r["vel_boost_timer"] > 0:
            r["vel_boost_timer"] -= 1
            vel_actual = VEL_BASE * 3
        else:
            vel_actual = VEL_BASE

        # Charcos de veneno: duran 10s y dañan al pisarlos
        nuevos_charcos = []
        for ch in r["veneno_charcos"]:
            ch["vida"] -= 1
            if ch["vida"] <= 0:
                continue
            if math.hypot(self.px - ch["x"], self.py - ch["y"]) < cfg.RADIO + 22:
                if ch["dmg_timer"] <= 0:
                    self.hp = max(0, self.hp - 8)
                    ch["dmg_timer"] = 45
                    if self.hp <= 0:
                        self.muerto = True
                        self.muerte_timer = 7 * 60
                else:
                    ch["dmg_timer"] -= 1
            elif ch["dmg_timer"] > 0:
                ch["dmg_timer"] -= 1
            nuevos_charcos.append(ch)
        r["veneno_charcos"] = nuevos_charcos

        # Proyectiles mágicos: mover y comprobar impacto
        nuevos_proyectiles = []
        for bolt in r["magic_proyectiles"]:
            bolt["x"] += bolt["vx"]
            bolt["y"] += bolt["vy"]
            bolt["vida"] -= 1
            if bolt["vida"] <= 0:
                continue
            if math.hypot(self.px - bolt["x"], self.py - bolt["y"]) < cfg.RADIO + 12:
                self.hp = max(0, self.hp - 35)
                if self.hp <= 0:
                    self.muerto = True
                    self.muerte_timer = 7 * 60
            else:
                nuevos_proyectiles.append(bolt)
        r["magic_proyectiles"] = nuevos_proyectiles

        # Rotación de hechizos (1 segundo de casteo)
        if r["magic_casteo"] > 0:
            r["magic_casteo"] += 1
            if r["magic_casteo"] >= 60:
                hechizo = r["magic_hechizo"]
                if hechizo == 1:
                    if dist > 0:
                        speed = 7.0
                        r["magic_proyectiles"].append({
                            "x": r["x"], "y": r["y"],
                            "vx": (dx / dist) * speed,
                            "vy": (dy / dist) * speed,
                            "vida": 180,
                        })
                elif hechizo == 2:
                    r["vel_boost_timer"] = 4 * 60
                elif hechizo == 3:
                    for _ in range(random.randint(4, 7)):
                        r["veneno_charcos"].append({
                            "x": float(random.randint(80, cfg.ANCHO - 80)),
                            "y": float(random.randint(120, cfg.ALTO - 80)),
                            "vida": 10 * 60,
                            "dmg_timer": 0,
                        })
                r["magic_casteo"] = 0
                r["magic_hechizo"] = 0
                r["magic_timer"] = random.randint(200, 380)
        else:
            r["magic_timer"] -= 1
            if r["magic_timer"] <= 0:
                r["magic_hechizo"] = random.randint(1, 3)
                r["magic_casteo"] = 1

        # Cooldown de ataque físico
        if r["ataque_timer"] > 0:
            r["ataque_timer"] -= 1

        # Durante casteo solo canaliza, no persigue ni pega
        if r["magic_casteo"] > 0:
            return

        if dist < ALCANCE:
            r["estado"] = "ataca"
            if r["ataque_timer"] == 0:
                self.hp = max(0, self.hp - 25)
                r["ataque_timer"] = 60
                if self.hp <= 0:
                    self.muerto = True
                    self.muerte_timer = 7 * 60
        elif dist < DETECCION:
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
            r["x"] = max(50, min(cfg.ANCHO - 50, r["x"] + r["vx"]))
            r["y"] = max(100, min(cfg.ALTO - 60, r["y"] + r["vy"]))

    def _registrar_chat(self, jugador_id, texto):
        if not jugador_id:
            return
        if isinstance(texto, str) and texto.strip():
            self.chat_burbujas[jugador_id] = {
                "texto": texto.strip()[:cfg.CHAT_MAX_CARACTERES],
                "timer": cfg.CHAT_DURACION_FRAMES,
            }

    def _actualizar_timers_chat(self):
        for jugador_id in list(self.chat_burbujas.keys()):
            self.chat_burbujas[jugador_id]["timer"] -= 1
            if self.chat_burbujas[jugador_id]["timer"] <= 0:
                del self.chat_burbujas[jugador_id]

    def _actualizar_particulas(self):
        """Actualiza todas las partículas activas."""
        nuevas_particulas = []
        for p in self.particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vida"] -= 1
            if p["vida"] > 0:
                nuevas_particulas.append(p)
        self.particulas = nuevas_particulas

        nuevas_espadas = []
        for espada in self.animaciones_espada:
            espada["timer"] -= 1
            if espada["timer"] > 0:
                nuevas_espadas.append(espada)
        self.animaciones_espada = nuevas_espadas

        nuevas_efectos = []
        for efecto in self.animaciones_efecto:
            efecto["timer"] -= 1
            if efecto["timer"] > 0:
                nuevas_efectos.append(efecto)
        self.animaciones_efecto = nuevas_efectos

        for efecto_id in list(self.efectos_recibidos.keys()):
            self.efectos_recibidos[efecto_id] -= 1
            if self.efectos_recibidos[efecto_id] <= 0:
                del self.efectos_recibidos[efecto_id]

    def _procesar_efectos_remotos(self, efectos):
        if not isinstance(efectos, list):
            return
        for efecto in efectos:
            if not isinstance(efecto, dict):
                continue
            efecto_id = efecto.get("id")
            if efecto_id in self.efectos_recibidos:
                continue
            accion = str(efecto.get("accion", "")).strip().lower()
            if accion not in ("ataque_paladin", "ataque_paladin_izq", "ataque_paladin_der", "hechizo_fuego", "sanacion"):
                continue
            ex = efecto.get("x")
            ey = efecto.get("y")
            player_id = efecto.get("player_id")
            if not isinstance(ex, (int, float)) or not isinstance(ey, (int, float)):
                continue
            self.efectos_recibidos[efecto_id] = 45
            if accion in ("ataque_paladin_izq", "ataque_paladin_der"):
                tipo = "izq" if accion == "ataque_paladin_izq" else "der"
                self._agregar_animacion_espada(float(ex), float(ey), tipo, player_id)
            elif accion == "sanacion":
                self._agregar_animacion_corazon(float(ex), float(ey), player_id)
            elif accion == "hechizo_fuego":
                self._agregar_animacion_fuego(float(ex), float(ey), player_id)

    def _agregar_animacion_espada(self, x, y, tipo, owner_id):
        # Reemplazar animación existente del mismo dueño (1 por usuario)
        self.animaciones_espada = [e for e in self.animaciones_espada if e.get("owner_id") != owner_id]
        self.animaciones_espada.append({
            "owner_id": owner_id,
            "tipo": tipo,
            "timer": 18,
            "duracion": 18,
        })

    def _agregar_animacion_corazon(self, x, y, owner_id):
        self.animaciones_efecto.append({
            "x": x,
            "y": y,
            "tipo": "corazon",
            "owner_id": owner_id,
            "timer": 24,
            "duracion": 24,
        })

    def _agregar_animacion_fuego(self, x, y, owner_id):
        self.animaciones_efecto.append({
            "x": x,
            "y": y,
            "tipo": "fuego",
            "owner_id": owner_id,
            "timer": 24,
            "duracion": 24,
        })

    def _dibujar_animaciones_jugador(self, c, jugador_id):
        if not jugador_id:
            return
        for espada in self.animaciones_espada:
            if espada.get("owner_id") == jugador_id:
                self._dibujar_espada_animada(c, espada)
        for efecto in self.animaciones_efecto:
            if efecto.get("owner_id") == jugador_id:
                if efecto.get("tipo") == "corazon":
                    self._dibujar_corazon_animado(c, efecto)
                elif efecto.get("tipo") == "fuego":
                    self._dibujar_fuego_animado(c, efecto)

    def _dibujar_espada_animada(self, c, espada):
        # Obtener posición actual del dueño
        owner_id = espada.get("owner_id")
        if owner_id == self.id_jugador:
            x, y = self.px, self.py
        else:
            datos_owner = self.otros_jugadores.get(owner_id, {})
            x = datos_owner.get("x", espada.get("x", 0))
            y = datos_owner.get("y", espada.get("y", 0))
        progress = 1 - (espada["timer"] / espada["duracion"])
        tipo = espada["tipo"]

        if tipo == "izq":
            angle = math.radians(220 - progress * 55)
            end_x = x + 56 * math.cos(angle)
            end_y = y + 56 * math.sin(angle)
        else:
            angle = math.radians(-40 + progress * 55)
            end_x = x + 56 * math.cos(angle)
            end_y = y + 56 * math.sin(angle)

        dx = end_x - x
        dy = end_y - y
        length = math.hypot(dx, dy) or 1.0
        dx /= length
        dy /= length
        nx = -dy
        ny = dx

        base_x = x + dx * 10
        base_y = y + dy * 10
        tip_x = x + dx * 60
        tip_y = y + dy * 60

        c.create_polygon(
            base_x + nx * 5, base_y + ny * 5,
            tip_x + nx * 2, tip_y + ny * 2,
            tip_x + dx * 10, tip_y + dy * 10,
            tip_x - nx * 2, tip_y - ny * 2,
            base_x - nx * 5, base_y - ny * 5,
            fill="#d6dde5",
            outline="#9aa7b3",
            width=2,
            smooth=True,
        )
        c.create_line(base_x, base_y, tip_x, tip_y, fill="#ffffff", width=2, capstyle=tk.ROUND)
        c.create_line(base_x - nx * 8, base_y - ny * 8, base_x + nx * 8, base_y + ny * 8, fill="#c79a56", width=4, capstyle=tk.ROUND)
        c.create_line(base_x - dx * 4, base_y - dy * 4, base_x - dx * 16, base_y - dy * 16, fill="#6b4a2e", width=5, capstyle=tk.ROUND)
        c.create_oval(base_x - dx * 18 - 3, base_y - dy * 18 - 3, base_x - dx * 18 + 3, base_y - dy * 18 + 3, fill="#8b5a2b", outline="#3d2a18")

    def _dibujar_corazon_animado(self, c, efecto):
        x = efecto["x"]
        y = efecto["y"]
        progress = 1 - (efecto["timer"] / efecto["duracion"])
        pulso = 1 + 0.35 * math.sin(progress * math.pi * 4)
        for i, offset in enumerate([(-10, 0), (0, -6), (10, 0)]):
            hx = x + offset[0] * (1 + progress)
            hy = y - 10 - progress * 18 + offset[1]
            c.create_text(hx, hy, text="♥", fill="#ff4d6d", font=("Consolas", int(16 * pulso), "bold"))

    def _dibujar_fuego_animado(self, c, efecto):
        x = efecto["x"]
        y = efecto["y"]
        progress = 1 - (efecto["timer"] / efecto["duracion"])
        num_llamas = 12
        radio_base = 18 + progress * 55
        colores = ["#ff6f00", "#ff9800", "#ffcc00", "#ff4500"]
        for i in range(num_llamas):
            angulo = math.radians(i * 360 / num_llamas)
            cx = x + radio_base * math.cos(angulo)
            cy = y + radio_base * math.sin(angulo)
            # punta de la llama apunta hacia afuera
            punta_x = x + (radio_base + 32) * math.cos(angulo)
            punta_y = y + (radio_base + 32) * math.sin(angulo)
            perp_x = -math.sin(angulo) * 12
            perp_y = math.cos(angulo) * 12
            color_llama = colores[i % len(colores)]
            c.create_polygon(
                cx + perp_x, cy + perp_y,
                punta_x, punta_y,
                cx - perp_x, cy - perp_y,
                fill=color_llama,
                outline="#b23a00",
                width=1,
            )
        # núcleo central brillante
        nr = max(5, int(16 * (1 - progress)))
        c.create_oval(x - nr, y - nr, x + nr, y + nr, fill="#fff176", outline="#ffcc00", width=2)

    def _dibujar_barra_hp_personaje(self, c, x, y, hp, hp_max, nombre, color):
        r = cfg.RADIO
        hp_max = max(1, int(hp_max))
        hp = max(0, min(int(hp), hp_max))
        bar_w = 42
        pct = hp / hp_max
        by = y + r + 8
        c.create_rectangle(x - bar_w // 2, by, x + bar_w // 2, by + 8, fill="#2d0000", outline="#000000")
        c.create_rectangle(x - bar_w // 2, by, x - bar_w // 2 + int(bar_w * pct), by + 8, fill="#00c853", outline="")
        c.create_text(x, by + 14, text=f"{hp}/{hp_max}", fill="#00ff88", font=("Consolas", 8, "bold"))

    def _crear_particulas_accion(self, x, y, accion):
        return

    def _dibujar_particulas(self):
        """Dibuja todas las partículas activas."""
        for p in self.particulas:
            x, y = p["x"], p["y"]
            alpha = int(255 * (p["vida"] / 60))  # Fade out effect
            
            if p["tipo"] == "espada":
                # Partículas de ataque (amarillo/dorado)
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="#FFD700", outline="#FFA500")
            elif p["tipo"] == "sanacion":
                # Partículas de sanación (verde)
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#00FF00", outline="#00AA00")
            elif p["tipo"] == "fuego":
                # Partículas de fuego (rojo/naranja)
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="#FF4500", outline="#FF0000")

    def _dibujar_rata(self):
        """Dibuja el ratón monstruo en el sótano."""
        if self.rata["hp"] <= 0:
            return
        c = self.canvas
        r = self.rata
        rx, ry = int(r["x"]), int(r["y"])
        atacando  = r["estado"] == "ataca"
        casteando = r["magic_casteo"] > 0
        boosteado = r["vel_boost_timer"] > 0
        hechizo   = r["magic_hechizo"]

        # Colores según estado
        if casteando and hechizo == 2:
            color_cuerpo = "#ffaa00"   # naranja: velocidad
        elif casteando and hechizo == 3:
            color_cuerpo = "#226622"   # verde oscuro: veneno
        elif casteando:
            color_cuerpo = "#883388"   # morado: proyectil
        elif atacando:
            color_cuerpo = "#cc3333"   # rojo: golpe físico
        else:
            color_cuerpo = "#888888"

        # --- Charcos de veneno ---
        t = time.time()
        for ch in r["veneno_charcos"]:
            cx2, cy2 = int(ch["x"]), int(ch["y"])
            alpha_v = ch["vida"] / 600
            pulso = int(4 * math.sin(t * 4 + cx2 * 0.05))
            c.create_oval(cx2 - 28 + pulso, cy2 - 14,
                          cx2 + 28 - pulso, cy2 + 14,
                          fill="#1a4d00", outline="#44ff44", width=2)
            c.create_oval(cx2 - 14, cy2 - 7, cx2 + 14, cy2 + 7,
                          fill="#2dcc00", outline="")
            c.create_text(cx2, cy2 - 20, text="☣",
                          font=("Arial", 10), fill="#88ff44")

        # --- Aura de casteo ---
        if casteando:
            pulso2 = int(8 * math.sin(t * 10))
            progreso = r["magic_casteo"] / 60
            radio_aura = int(35 + 15 * progreso) + pulso2
            col_aura = {1: "#cc44ff", 2: "#ffaa00", 3: "#44ff44"}.get(hechizo, "#cc44ff")
            col_in   = {1: "#8822aa", 2: "#aa6600", 3: "#226600"}.get(hechizo, "#8822aa")
            c.create_oval(rx - radio_aura, ry - radio_aura,
                          rx + radio_aura, ry + radio_aura,
                          fill="", outline=col_aura, width=3)
            c.create_oval(rx - radio_aura + 8, ry - radio_aura + 8,
                          rx + radio_aura - 8, ry + radio_aura - 8,
                          fill="", outline=col_in, width=1)

        # --- Estela de velocidad ---
        if boosteado:
            for i in range(1, 4):
                c.create_oval(rx - 18 + i*4, ry - 10 + i*3,
                              rx + 18 + i*4, ry + 14 + i*3,
                              fill="", outline="#ffaa00", width=1)

        # --- Proyectiles mágicos ---
        for bolt in r["magic_proyectiles"]:
            bx, by = int(bolt["x"]), int(bolt["y"])
            glow = int(4 * math.sin(t * 15))
            c.create_oval(bx-10-glow, by-10-glow, bx+10+glow, by+10+glow,
                          fill="#440066", outline="#cc44ff", width=2)
            c.create_oval(bx-5, by-5, bx+5, by+5, fill="#ff88ff", outline="")

        # Indicador del objetivo actual (sincronizado por servidor)
        objetivo_id = r.get("objetivo_id")
        objetivo_nombre = r.get("objetivo_nombre")
        tx, ty = None, None
        if objetivo_id and objetivo_id == self.id_jugador and self.estado == "subterraneo":
            tx, ty = self.px, self.py
        elif objetivo_id and objetivo_id in self.otros_jugadores:
            datos_obj = self.otros_jugadores.get(objetivo_id, {})
            if datos_obj.get("estado") == "subterraneo":
                tx = datos_obj.get("x")
                ty = datos_obj.get("y")

        if tx is not None and ty is not None:
            c.create_line(rx, ry, int(tx), int(ty), fill="#ff6666", width=2, dash=(6, 4))
            if objetivo_nombre:
                c.create_text(
                    rx,
                    ry - 74,
                    text=f"Objetivo: {objetivo_nombre}",
                    fill="#ff9e9e",
                    font=("Consolas", 8, "bold"),
                )

        # --- Cuerpo de la rata ---
        c.create_oval(rx-20, ry+10, rx+20, ry+18, fill="#111111", outline="")
        c.create_oval(rx-18, ry-10, rx+18, ry+14, fill=color_cuerpo, outline="#444444", width=2)
        c.create_oval(rx+10, ry-18, rx+30, ry+2, fill=color_cuerpo, outline="#444444", width=1)
        c.create_oval(rx+11, ry-28, rx+18, ry-16, fill="#ffaaaa", outline="#555")
        c.create_oval(rx+21, ry-28, rx+29, ry-16, fill="#ffaaaa", outline="#555")
        c.create_oval(rx+13, ry-14, rx+17, ry-10, fill="#ff0000", outline="")
        c.create_oval(rx+21, ry-14, rx+25, ry-10, fill="#ff0000", outline="")
        c.create_oval(rx+27, ry-5, rx+31, ry-1, fill="#ff88aa", outline="")
        c.create_line(rx-18, ry+6, rx-32, ry+18, rx-38, ry+8,
                      fill="#aaaaaa", width=3, smooth=True)
        if atacando:
            c.create_polygon(rx+22, ry+2, rx+26, ry+2, rx+24, ry+8,
                             fill="white", outline="#888")

        # Indicador de casteo
        if casteando:
            pct = int(r["magic_casteo"] / 60 * 100)
            iconos = {1: "✦", 2: "⚡", 3: "☣"}
            col_txt = {1: "#ff88ff", 2: "#ffcc00", 3: "#88ff44"}
            c.create_text(rx, ry - 50,
                          text=f"{iconos.get(hechizo,'?')} {pct}%",
                          fill=col_txt.get(hechizo, "#ff88ff"),
                          font=("Consolas", 9, "bold"))
        # Indicador de boost activo
        if boosteado:
            secs = r["vel_boost_timer"] // 60 + 1
            c.create_text(rx, ry - 62, text=f"⚡ x2 ({secs}s)",
                          fill="#ffcc00", font=("Consolas", 8, "bold"))

        # Barra de HP
        bar_w = 44
        hp_pct = r["hp"] / r["hp_max"]
        c.create_rectangle(rx - bar_w//2, ry-34, rx + bar_w//2, ry-26,
                            fill="#550000", outline="#888888")
        c.create_rectangle(rx - bar_w//2, ry-34,
                            rx - bar_w//2 + int(bar_w * hp_pct), ry-26,
                            fill="#ff3333", outline="")
        c.create_text(rx, ry-42, text="Ratón Monstruo ☠",
                      fill="#ff6666", font=("Consolas", 8, "bold"))

    def _dibujar_muerte_overlay(self):
        """Muestra la animación de muerte sobre el jugador."""
        self._dibujar_muerte_overlay_en_posicion(self.px, self.py, self.muerte_timer)
        segundos = self.muerte_timer // 60 + 1
        c = self.canvas
        x, y = self.px, self.py
        r = cfg.RADIO
        # Texto de espera solo para el jugador local.
        c.create_text(x, y + r + 18, text=f"Reapareciendo en {segundos}s...",
                      fill="#ff4444", font=("Consolas", 9, "bold"))

    def _dibujar_muerte_overlay_en_posicion(self, x, y, muerte_timer=0):
        """Dibuja la aureola y calavera de muerte para cualquier jugador."""
        r = cfg.RADIO
        c = self.canvas
        # Aureola dorada pulsante
        t = time.time()
        pulso = int(3 * math.sin(t * 6))
        for i in range(3):
            c.create_oval(x - r - 6 - i*3 + pulso, y - r - 44 - i*4,
                          x + r + 6 + i*3 - pulso, y - r - 20 + i*4,
                          fill="", outline="#ffd700", width=2)
        # Calavera
        c.create_text(x, y - r - 52, text="💀", font=("Arial", 18))

    def _dibujar_hp_bar(self):
        """Dibuja la barra de HP del jugador en pantalla."""
        bar_w, bar_h = 160, 14
        x0, y0 = 10, cfg.ALTO - 60
        hp_pct = self.hp / self.hp_max
        col = "#44dd44" if hp_pct > 0.5 else ("#ffaa00" if hp_pct > 0.25 else "#ff3333")
        self.canvas.create_rectangle(x0, y0, x0 + bar_w, y0 + bar_h,
                                     fill="#330000", outline="#888888")
        self.canvas.create_rectangle(x0, y0, x0 + int(bar_w * hp_pct), y0 + bar_h,
                                     fill=col, outline="")
        self.canvas.create_text(x0 + bar_w//2, y0 + bar_h//2,
                                text=f"HP {self.hp}/{self.hp_max}",
                                fill="white", font=("Consolas", 9, "bold"))

    def _dibujar_chat_en_posicion(self, x, y, texto):
        if not texto:
            return
        self.canvas.create_text(
            x,
            y - cfg.RADIO - 34,
            text=texto,
            fill="#fff8c9",
            font=("Consolas", 10, "bold"),
            tags="chat",
        )

    # --- Colisiones ---

    def _bloqueado_exterior(self, px, py):
        lx, ly = cfg.LAGO_X, cfg.LAGO_Y
        rx = cfg.LAGO_RX + cfg.RADIO
        ry = cfg.LAGO_RY + cfg.RADIO
        # El lago ya no bloquea: al tocarlo se va al mapa de agua
        for ax, ay in cfg.ARBOLES:
            # El arbol de la casita no bloquea (se usa para entrar)
            if ax == cfg.ARBOL_CASITA_X and ay == cfg.ARBOL_CASITA_Y:
                continue
            if math.hypot(px - ax, py - ay) < cfg.RADIO + cfg.RADIO_ARBOL:
                return True
        cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
        pared_y = cy + ch // 4
        px_p = cx + cw // 2 - 14
        en_cuerpo = (cx - cfg.RADIO < px < cx + cw + cfg.RADIO and
                     pared_y - cfg.RADIO < py < cy + ch + cfg.RADIO)
        en_puerta = (px_p - cfg.RADIO < px < px_p + 28 + cfg.RADIO and
                     py > cy + ch - 40 - cfg.RADIO)
        if en_cuerpo and not en_puerta:
            return True
        return False

    def _bloqueado_interior(self, px, py):
        for mx, my, mw, mh, *_ in cfg.MUEBLES:
            if (mx - cfg.RADIO < px < mx + mw + cfg.RADIO and
                    my - cfg.RADIO < py < my + mh + cfg.RADIO):
                return True
        return False

    def _mover(self, dx, dy):
        nx = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO, self.px + dx))
        ny = max(cfg.RADIO, min(cfg.ALTO - cfg.RADIO, self.py + dy))

        if self.estado == "exterior":
            if not self._bloqueado_exterior(nx, self.py):
                self.px = nx
            if not self._bloqueado_exterior(self.px, ny):
                self.py = ny
        elif self.estado == "interior":
            g = 30
            nx = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO - g, nx))
            sx = cfg.SALIDA_INT_X
            limite_inf = cfg.ALTO - cfg.RADIO - g if abs(nx - sx) > 30 else cfg.ALTO - cfg.RADIO
            ny = max(cfg.RADIO + g, min(limite_inf, ny))

            if not self._bloqueado_interior(nx, self.py):
                self.px = nx
            if not self._bloqueado_interior(self.px, ny):
                self.py = ny
        elif self.estado == "segundo_piso":
            g = 30
            nx = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO - g, nx))
            ny = max(cfg.RADIO + g, min(cfg.ALTO - cfg.RADIO - g, ny))
            mid = cfg.ANCHO // 2
            puerta_ini, puerta_fin = 260, 340
            # Colision pared divisoria (eje X)
            if (mid - 5 - cfg.RADIO < nx < mid + 5 + cfg.RADIO and
                    not (puerta_ini - cfg.RADIO < self.py < puerta_fin + cfg.RADIO)):
                nx = self.px
            self.px = nx
            # Colision pared divisoria (eje Y)
            if (mid - 5 - cfg.RADIO < self.px < mid + 5 + cfg.RADIO and
                    not (puerta_ini - cfg.RADIO < ny < puerta_fin + cfg.RADIO)):
                ny = self.py
            self.py = ny
        elif self.estado == "subterraneo":
            g = 30
            self.px = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO - g, nx))
            self.py = max(cfg.RADIO + g, min(cfg.ALTO - cfg.RADIO - g, ny))
        elif self.estado == "practica":
            g = 30
            self.px = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO - g, nx))
            if ny <= cfg.RADIO + 30 or ny >= cfg.ALTO - cfg.RADIO - 30:
                self.py = ny
            else:
                self.py = max(cfg.RADIO + g, min(cfg.ALTO - cfg.RADIO - g, ny))
        elif self.estado == "agua":
            self.px = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO, nx))
            self.py = max(25 + cfg.RADIO, min(cfg.ALTO - cfg.RADIO, ny))
        elif self.estado == "casita_arbol":
            self.px = max(100 + cfg.RADIO, min(700 - cfg.RADIO, nx))
            self.py = max(160 + cfg.RADIO, min(cfg.ALTO - cfg.RADIO, ny))
        elif self.estado == "bar":
            g = 30
            self.px = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO, nx))
            self.py = max(cfg.RADIO + g, min(cfg.ALTO - cfg.RADIO - g, ny))
        elif self.estado == "biblioteca":
            g = 30
            self.px = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO - g, nx))
            self.py = max(cfg.RADIO + g, min(cfg.ALTO - cfg.RADIO - g, ny))

    # --- Game loop ---

    def _loop(self):
        self._actualizar_timers_chat()
        self._actualizar_particulas()
        if self.alerta_laboratorio_timer > 0:
            self.alerta_laboratorio_timer -= 1

        # --- Manejar muerte del jugador ---
        if self.muerto:
            # Redibujar el mapa actual con overlay de muerte (autoridad del servidor)
            if self.estado == "subterraneo":
                self._dibujar_subterraneo()
            elif self.estado == "interior":
                self._dibujar_interior()
            elif self.estado == "practica":
                self._dibujar_practica()
            elif self.estado == "exterior":
                self._dibujar_exterior()
            self._dibujar_muerte_overlay()
            self._dibujar_hp_bar()
            self.root.after(16, self._loop)
            return

        # Actualizar timers
        if self.casteo_timer > 0:
            self.casteo_timer -= 1
            if self.casteo_timer == 0:
                if self.casteo_accion == "hechizo_fuego":
                    self._lanzar_hechizo_fuego()
                elif self.casteo_accion == "sanacion":
                    self._sanar_cercanos()
                self.casteo_accion = None
        
        if self.ataque_timer > 0:
            self.ataque_timer -= 1
        
        dx, dy = 0, 0
        # Solo permitir movimiento si no está casteando ni muerto
        if not self.chat_activo and self.casteo_timer == 0 and not self.muerto:
            if "up" in self.teclas:
                dy -= cfg.VELOCIDAD
            if "down" in self.teclas:
                dy += cfg.VELOCIDAD
            if "left" in self.teclas:
                dx -= cfg.VELOCIDAD
            if "right" in self.teclas:
                dx += cfg.VELOCIDAD

        self._mover(dx, dy)
        self._enviar_posicion()

        if self.estado == "exterior":
            # Transición al bar (borde izquierdo)
            if self.px <= cfg.RADIO + 2:
                self.estado = "bar"
                self.px = cfg.ANCHO - cfg.RADIO - 35
                self.py = max(cfg.RADIO + 40, min(cfg.ALTO - cfg.RADIO - 40, self.py))
                self._dibujar_bar()
                self.root.after(16, self._loop)
                return

            # Transición a biblioteca (borde derecho)
            if self.px >= cfg.ANCHO - cfg.RADIO - 2:
                self.estado = "biblioteca"
                self.px = cfg.RADIO + 35
                self.py = max(cfg.RADIO + 40, min(cfg.ALTO - cfg.RADIO - 40, self.py))
                self._dibujar_biblioteca()
                self.root.after(16, self._loop)
                return

            cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
            px_puerta = cx + cw // 2
            if math.hypot(self.px - px_puerta, self.py - (cy + ch)) < cfg.RADIO + 18:
                self.estado = "interior"
                self.px = cfg.SALIDA_INT_X
                self.py = cfg.ALTO - 85
                self._dibujar_interior()
                self.root.after(16, self._loop)
                return

            # Transicion a casita del arbol
            if math.hypot(self.px - cfg.ARBOL_CASITA_X, self.py - cfg.ARBOL_CASITA_Y) < cfg.RADIO_ARBOL + 5:
                self.estado = "casita_arbol"
                self.px = cfg.ANCHO // 2
                self.py = 280
                self._dibujar_casita_arbol()
                self.root.after(16, self._loop)
                return

            # Transición a sala de práctica (borde superior)
            if self.py <= cfg.RADIO + 5:
                self.estado = "practica"
                self.px = cfg.ANCHO // 2
                self.py = cfg.ALTO - 60
                self._dibujar_practica()
                self.root.after(16, self._loop)
                return

            # Transicion al mapa de agua (lago)
            lx, ly = cfg.LAGO_X, cfg.LAGO_Y
            rx_lago = cfg.LAGO_RX + cfg.RADIO
            ry_lago = cfg.LAGO_RY + cfg.RADIO
            if ((self.px - lx) / rx_lago) ** 2 + ((self.py - ly) / ry_lago) ** 2 < 1:
                self.estado = "agua"
                self.px = cfg.ANCHO // 2
                self.py = 80
                self._dibujar_agua()
                self.root.after(16, self._loop)
                return

            # Transicion al mapa de agua (borde inferior)
            if self.py >= cfg.ALTO - cfg.RADIO - 2:
                self.estado = "agua"
                self.px = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO, self.px))
                self.py = 60
                self._dibujar_agua()
                self.root.after(16, self._loop)
                return

            toca_barril = any(
                math.hypot(self.px - bx, self.py - by) < cfg.RADIO + cfg.RADIO_BARRIL
                for bx, by in cfg.BARRILES
            )
            self._dibujar_exterior()
            self._dibujar_npcs()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if toca_barril:
                self.canvas.itemconfig(self.msg, text="Este es un barril")
                self.msg_timer = 80
            elif self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "bar":
            # Salir por borde derecho al exterior
            if self.px >= cfg.ANCHO - cfg.RADIO - 5:
                self.estado = "exterior"
                self.px = cfg.RADIO + 35
                self.py = max(cfg.RADIO + 40, min(cfg.ALTO - cfg.RADIO - 40, self.py))
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            self._dibujar_bar()
            self._dibujar_npcs()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "biblioteca":
            # Salir por borde izquierdo al exterior
            if self.px <= cfg.RADIO + 5:
                self.estado = "exterior"
                self.px = cfg.ANCHO - cfg.RADIO - 35
                self.py = max(cfg.RADIO + 40, min(cfg.ALTO - cfg.RADIO - 40, self.py))
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            self._dibujar_biblioteca()
            self._dibujar_npcs()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "interior":
            sx = cfg.SALIDA_INT_X
            if self.py > cfg.ALTO - 75 and abs(self.px - sx) < 30:
                self.estado = "exterior"
                cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
                self.px = cx + cw // 2
                self.py = cy + ch + 40
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            # Transicion al 2o piso (escalera)
            ex, ey = cfg.ESCALERA_INT_X, cfg.ESCALERA_INT_Y
            if (ex - cfg.RADIO < self.px < ex + cfg.ESCALERA_INT_W + cfg.RADIO and
                    ey - cfg.RADIO < self.py < ey + cfg.ESCALERA_INT_H + cfg.RADIO):
                self.estado = "segundo_piso"
                # Spawnear lejos de la escalera del 2o piso (trigger > 460)
                self.px = 300
                self.py = 300
                self._dibujar_segundo_piso()
                self.root.after(16, self._loop)
                return

            # Transicion al subterraneo (trampilla)
            tx2, ty2 = cfg.TRAMPILLA_INT_X, cfg.TRAMPILLA_INT_Y
            if (tx2 - cfg.RADIO < self.px < tx2 + cfg.TRAMPILLA_INT_W + cfg.RADIO and
                    ty2 - cfg.RADIO < self.py < ty2 + cfg.TRAMPILLA_INT_H + cfg.RADIO):
                es_profesor_local = bool(self.id_jugador and self.profesor_id and self.id_jugador == self.profesor_id)
                if self.quest_paso < 7 and not es_profesor_local:
                    # Quest no completada: mostrar mensaje de bloqueo
                    self.canvas.itemconfig(self.msg, text="🔒 Necesitas la llave del sótano para entrar")
                    self.msg_timer = 120
                else:
                    self.estado = "subterraneo"
                    self.px = tx2 + cfg.TRAMPILLA_INT_W // 2
                    self.py = 200
                    self._dibujar_subterraneo()
                    self.root.after(16, self._loop)
                    return

            self._dibujar_interior()
            self._dibujar_npcs()
            self._dibujar_inventario()
            # Indicador visual de cerrojo en la trampilla si la quest no está completa
            es_profesor_local = bool(self.id_jugador and self.profesor_id and self.id_jugador == self.profesor_id)
            if self.quest_paso < 7 and not es_profesor_local:
                tx2, ty2 = cfg.TRAMPILLA_INT_X, cfg.TRAMPILLA_INT_Y
                self.canvas.create_text(
                    tx2 + cfg.TRAMPILLA_INT_W // 2, ty2 - 28,
                    text="🔒", font=("Arial", 14),
                )
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "segundo_piso":
            # Bajar por escalera (inferior derecha, dibujo en y=480)
            ex2 = cfg.ESCALERA_INT_X
            if self.py > 460 and ex2 - cfg.RADIO < self.px < ex2 + cfg.ESCALERA_INT_W + cfg.RADIO:
                self.estado = "interior"
                # Spawnear DEBAJO del rango de la escalera en interior (ey+H+RADIO=480)
                self.px = 300
                self.py = 510
                self._dibujar_interior()
                self.root.after(16, self._loop)
                return

            self._dibujar_segundo_piso()
            self._dibujar_npcs()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "subterraneo":
            # Subir por escalera (centro superior) — zona de salida más arriba
            lx2 = cfg.TRAMPILLA_INT_X + cfg.TRAMPILLA_INT_W // 2
            if self.py <= 55 and abs(self.px - lx2) < 35:
                self.estado = "interior"
                # Aparecer claramente lejos de la trampilla para evitar reingreso accidental.
                self.px = 300
                self.py = 520
                self._dibujar_interior()
                self.root.after(16, self._loop)
                return

            self._dibujar_subterraneo()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self._dibujar_hp_bar()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "practica":
            self._actualizar_practica()
            # Salir por borde superior o inferior
            if self.py <= cfg.RADIO + 5 or self.py >= cfg.ALTO - cfg.RADIO - 5:
                self.estado = "exterior"
                self.px = cfg.ANCHO // 2
                self.py = cfg.RADIO + 30
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return
            self._dibujar_practica()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self._dibujar_hp_bar()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "agua":
            # Salir por el borde superior
            if self.py <= 25 + cfg.RADIO + 5:
                self.estado = "exterior"
                self.px = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO, self.px))
                self.py = cfg.ALTO - cfg.RADIO - 30
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            self._dibujar_agua()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "casita_arbol":
            # Bajar por la cuerda (centro, zona accesible)
            rx2 = cfg.ANCHO // 2
            if 355 < self.py < 435 and abs(self.px - rx2) < 35:
                self.estado = "exterior"
                self.px = cfg.ARBOL_CASITA_X + 15
                self.py = cfg.ARBOL_CASITA_Y + 30
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            self._dibujar_casita_arbol()
            self._dibujar_npcs()
            self._dibujar_inventario()
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        self._dibujar_alerta_laboratorio()

        # Recrear chat_input cada frame (c.delete("all") lo borra)
        self.chat_input = self.canvas.create_text(
            cfg.ANCHO // 2,
            cfg.ALTO - 42,
            text="",
            fill="#ffe082",
            font=("Consolas", 11, "bold"),
        )

        if self.chat_activo:
            habilidad_info = ""
            if self.clase == "paladin":
                habilidad_info = " | F1: Espada izquierda | F2: Espada derecha"
            elif self.clase == "hechicero":
                habilidad_info = " | F1: Fuego (2s)"
            elif self.clase == "sanador":
                habilidad_info = " | F1: Corazones (1s)"

            self.canvas.itemconfig(
                self.chat_input,
                text=f"Chat: {self.chat_texto_actual}_ | Enter enviar | Esc cancelar{habilidad_info}",
            )
        else:
            self.canvas.itemconfig(
                self.chat_input,
                text="Enter o F12: abrir chat | E: interactuar NPC",
            )
        self.canvas.tag_raise(self.chat_input)

        self.root.after(16, self._loop)

    def _lanzar_hechizo_fuego(self):
        """Lanza el hechizo de fuego del hechicero."""
        self.accion_pendiente = "hechizo_fuego"
        self._agregar_animacion_fuego(self.px, self.py, self.id_jugador)
        self._daniar_cristales_cercanos(360, 700)

    # ---- Quest: El Experimento del Profesor Álvaro ----

    def _npcs_del_mapa(self):
        """Devuelve los NPCs que están en el mapa actual."""
        return {k: v for k, v in NPCS_DATA.items() if v["estado"] == self.estado}

    def _dibujar_npcs(self):
        """Dibuja los NPCs del mapa actual y el indicador de interacción."""
        c = self.canvas
        for npc_id, npc in self._npcs_del_mapa().items():
            x, y = npc["x"], npc["y"]
            r = cfg.RADIO
            color = npc["color"]
            # Sombra
            c.create_oval(x - r + 4, y - r + 8, x + r + 4, y + r + 8,
                          fill=cfg.COLOR_SOMBRA_ARBOL, outline="")
            # Cuerpo
            c.create_oval(x - r, y - r, x + r, y + r,
                          fill=color, outline="#000000", width=2)
            # Cara
            c.create_oval(x - r + 5, y - r + 2, x + r - 5, y + 4,
                          fill="#ffcc80", outline="#e65100", width=1)
            # Ojos
            c.create_oval(x - 7, y - 10, x - 3, y - 6, fill="black")
            c.create_oval(x + 3, y - 10, x + 7, y - 6, fill="black")
            # Nombre con sombra
            c.create_text(x + 1, y - r - 16 + 1, text=npc["nombre"],
                          fill="black", font=("Consolas", 9, "bold"))
            c.create_text(x, y - r - 16, text=npc["nombre"],
                          fill="white", font=("Consolas", 9, "bold"))
            # Indicador "Hablar [E]" si el jugador está cerca
            dist = math.hypot(self.px - x, self.py - y)
            if dist < 70:
                c.create_text(x, y - r - 32, text="[E] Hablar",
                              fill="#ffd700", font=("Consolas", 9, "bold"))

    def _npc_cercano(self):
        """Devuelve el ID del NPC más cercano (dentro de rango), o None."""
        for npc_id, npc in self._npcs_del_mapa().items():
            if math.hypot(self.px - npc["x"], self.py - npc["y"]) < 70:
                return npc_id
        return None

    def _intentar_interactuar_npc(self):
        """Intenta hablar con un NPC cercano al presionar E."""
        npc_id = self._npc_cercano()
        if npc_id:
            # Evita que quede una dirección "pegada" mientras se abre el diálogo modal.
            self.teclas.clear()
            self._interactuar_npc(npc_id)

    def _interactuar_npc(self, npc_id):
        """Gestiona el diálogo e intercambio de items con cada NPC según el paso de la quest."""
        paso = self.quest_paso

        if npc_id == "fotografo":
            if paso == 0:
                messagebox.showinfo(
                    "📷 Fotógrafo",
                    "¡Oye, tú! Estaba aquí sentado tranquilamente cuando vi algo enorme cruzar\n"
                    "por el callejón. ¡Enorme! ¡Saqué la cámara y lo fotografié antes de que\n"
                    "desapareciera! Nadie me cree de todas formas...\n\n"
                    "Toma una copia. ¡Es real, te lo juro!\n\n"
                    "✦ Obtuviste: Foto borrosa del ratón"
                )
                self.quest_paso = 1
                self.quest_item = "Foto borrosa"
            elif paso >= 1:
                messagebox.showinfo("📷 Fotógrafo", "Ya tienes la foto. ¡Espero que te sea útil, nadie me creyó!")

        elif npc_id == "borracho":
            if paso == 1:
                messagebox.showinfo(
                    "🍺 Borracho del bar",
                    "¿Una foto? ¡Impooosible!... Espera, espera...\n\n"
                    "Esto me recuerda al viejo Álvaro. Él venía aquí todos los días a tomar\n"
                    "café antes de encerrarse en su laboratorio. Un día dejó su taza olvidada\n"
                    "y nunca volvió a buscarla. Lleva semanas aquí...\n\n"
                    "Tómala, quizás te sirva de algo.\n\n"
                    "✦ Entregaste: Foto borrosa\n"
                    "✦ Obtuviste: Taza de café fría"
                )
                self.quest_paso = 2
                self.quest_item = "Taza de café fría"
            elif paso == 0:
                messagebox.showinfo("🍺 Borracho del bar", "¿Qué quieres? Déjame en paz... a menos que tengas algo interesante que mostrarme.")
            else:
                messagebox.showinfo("🍺 Borracho del bar", "*hipo* El viejo Álvaro... raro tipo. Espero que estés bien ahí abajo.")

        elif npc_id == "bibliotecaria":
            if paso == 2:
                messagebox.showinfo(
                    "📚 Bibliotecaria",
                    "¿La taza del profesor Álvaro?! Reconocería esa taza en cualquier lugar...\n\n"
                    "Él me prestó su manual de bioquímica avanzada y nunca lo devolvió.\n"
                    "Pero si tienes su taza, algo me dice que puedo confiar en ti.\n\n"
                    "Mira, él dejó estas notas de laboratorio olvidadas entre los libros.\n"
                    "¡Tómalas, a ver si sirven de algo!\n\n"
                    "✦ Entregaste: Taza de café fría\n"
                    "✦ Obtuviste: Notas del laboratorio"
                )
                self.quest_paso = 3
                self.quest_item = "Notas del laboratorio"
            elif paso < 2:
                messagebox.showinfo("📚 Bibliotecaria", "Shhh... Silencio en la biblioteca. ¿Buscas algo en particular?")
            else:
                messagebox.showinfo("📚 Bibliotecaria", "Espero que esas notas te ayuden. El profesor era un genio... o estaba completamente loco.")

        elif npc_id == "ayudante":
            if paso == 3:
                messagebox.showinfo(
                    "😰 Ayudante nervioso",
                    "¿Las notas de Álvaro?! ¿Cómo demonios las conseguiste...?\n\n"
                    "Escucha, yo era su asistente de laboratorio. El experimento con el ratón\n"
                    "salió terriblemente mal. La criatura mutó y Álvaro se encerró con ella.\n"
                    "Antes de desaparecer me entregó esto: su llavero. Pero le falta la llave\n"
                    "más importante... El guardia del edificio la tiene.\n\n"
                    "¡Búscalo en el interior de la casa!\n\n"
                    "✦ Entregaste: Notas del laboratorio\n"
                    "✦ Obtuviste: Llavero incompleto"
                )
                self.quest_paso = 4
                self.quest_item = "Llavero incompleto"
            elif paso < 3:
                messagebox.showinfo("😰 Ayudante nervioso", "*mira nervioso a su alrededor* No... no quiero hablar de Álvaro. Todavía no.")
            else:
                messagebox.showinfo("😰 Ayudante nervioso", "¡Ten cuidado ahí abajo! Esa cosa es... peligrosa. Mucho.")

        elif npc_id == "guardia":
            if paso == 4:
                messagebox.showinfo(
                    "👮 Guardia jubilado",
                    "El llavero del profesor... Así que tú también lo estás buscando.\n\n"
                    "Álvaro me entregó la llave del sótano 'para guardarla en caso de\n"
                    "emergencia'. Lleva semanas sin aparecer... supongo que ya es una emergencia.\n\n"
                    "Pero antes de dártela necesito ver su carnet universitario como prueba\n"
                    "de que realmente lo conoces. El conserje encontró algo hace unos días.\n"
                    "Búscalo afuera del edificio.\n\n"
                    "✦ Entregaste: Llavero incompleto\n"
                    "✦ Pista: busca al Conserje en el exterior"
                )
                self.quest_paso = 5
                self.quest_item = None
            elif paso == 6:
                messagebox.showinfo(
                    "👮 Guardia jubilado",
                    "...Dios mío. Es él, es el carnet del profesor Álvaro.\n\n"
                    "Algo debe haber pasado ahí abajo. No sé si fue un accidente o algo peor.\n"
                    "Toma, esta es la llave que él me dejó. Úsala bien.\n\n"
                    "¡Y ten mucho, MUCHO cuidado ahí abajo!\n\n"
                    "✦ Entregaste: Carnet universitario\n"
                    "✦ Obtuviste: Llave del sótano 🗝️\n"
                    "✦ ¡Quest completada! Ya puedes bajar al sótano"
                )
                self.quest_paso = 7
                self.quest_item = "Llave del sótano"
            elif paso < 4:
                messagebox.showinfo("👮 Guardia jubilado", "La trampilla del sótano está cerrada con llave. No puedo dejar entrar a cualquiera.")
            elif paso == 5:
                messagebox.showinfo("👮 Guardia jubilado", "Necesito el carnet universitario del profesor. El conserje lo tiene, búscalo afuera.")
            else:
                messagebox.showinfo("👮 Guardia jubilado", "Ya tienes la llave. ¡Ten cuidado ahí abajo, la criatura es muy peligrosa!")

        elif npc_id == "conserje":
            if paso == 5:
                messagebox.showinfo(
                    "🧹 Conserje",
                    "*suspira* ¿El carnet del profesor? Sí... lo encontré tirado en el suelo\n"
                    "hace unos días. Muy raro, muy raro.\n\n"
                    "¿Tú también escuchaste los ruidos que vienen del sótano por las noches?\n"
                    "Toma el carnet, yo no sé qué hacer con eso.\n\n"
                    "✦ Obtuviste: Carnet universitario de Álvaro"
                )
                self.quest_paso = 6
                self.quest_item = "Carnet universitario"
            elif paso < 5:
                messagebox.showinfo("🧹 Conserje", "Hola. ¿Estás bien? Estos últimos días hay ruidos muy extraños que vienen del sótano...")
            else:
                messagebox.showinfo("🧹 Conserje", "¿Ya bajaste al sótano? Espero que hayas salido bien. ¡Esos ruidos dan miedo!")

        elif npc_id == "borracho_clima":
            messagebox.showinfo(
                "🍻 Cliente ebrio",
                "*hip* ¿Sentiste ese viento? Te lo digo yo... mañana llueve seguro.\n"
                "Cuando me duele la rodilla izquierda nunca falla el clima...\n"
                "Aunque bueno... también me duele cuando no llueve. *hip*"
            )

        elif npc_id == "rumorista":
            messagebox.showinfo(
                "😨 Cliente nervioso",
                "Dicen que en el laboratorio del profesor Álvaro se oyen chillidos\n"
                "a medianoche... y que algo raspa las paredes desde adentro.\n"
                "Yo no me acercaría ni loco. Hay rumores terribles ahí abajo."
            )

        elif npc_id == "debug_laboratorio":
            tx2, ty2 = cfg.TRAMPILLA_INT_X, cfg.TRAMPILLA_INT_Y
            if self.quest_paso < 7:
                self.debug_quest_unlock_usado = True
                self.quest_paso = 7
                self.quest_item = "Llave del sótano"
                messagebox.showinfo(
                    "🧪 Técnico debug",
                    "DEBUG ACTIVADO:\n"
                    "Quest desbloqueada y acceso al laboratorio habilitado.\n"
                    "Entrando al subterráneo..."
                )
            else:
                messagebox.showinfo("🧪 Técnico debug", "Debug activo: entrando directo al laboratorio.")

            self.estado = "subterraneo"
            self.px = tx2 + cfg.TRAMPILLA_INT_W // 2
            self.py = 200
            self._dibujar_subterraneo()

    def _dibujar_inventario(self):
        """Dibuja el item actual y progreso de la quest en la esquina superior derecha."""
        if self.quest_paso == 0:
            return
        c = self.canvas
        if self.quest_paso == 7:
            txt_item = "🗝️ Llave del sótano (quest completada)"
            color_item = "#ffd700"
        elif self.quest_item:
            txt_item = f"Inventario: {self.quest_item}"
            color_item = "#90ee90"
        else:
            txt_item = "Inventario: vacío"
            color_item = "#aaaaaa"
        c.create_text(cfg.ANCHO - 10, 28, text=txt_item,
                      fill=color_item, font=("Consolas", 9, "bold"), anchor="e")
        paso_txt = f"Quest Álvaro: paso {self.quest_paso}/7"
        c.create_text(cfg.ANCHO - 10, 44, text=paso_txt,
                      fill="#888888", font=("Consolas", 8), anchor="e")


if __name__ == "__main__":
    root = tk.Tk()
    JuegoMultijugador(root)
    root.mainloop()
