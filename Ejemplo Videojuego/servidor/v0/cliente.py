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
        self.ataque_timer = 0
        self.particulas = []  # Lista de partículas para efectos visuales
        # Sistema de HP y muerte
        self.hp = 100
        self.hp_max = 100
        self.muerto = False
        self.muerte_timer = 0
        # Rata monstruo del sótano
        self.rata = self._rata_inicial()
        self.peces = [         # Posiciones base de los peces en mapa de agua
            (150, 280), (310, 420), (490, 150), (650, 380),
            (100, 460), (420, 310), (580, 480),
        ]

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
                        # Primera recepción: no actualices nombre/color (son los que acabas de enviar)
                        # Posteriores: sí actualiza para recibir cambios del servidor
                        if self.nombre_color_sincronizado:
                            nombre_servidor = info.get("tu_nombre")
                            if isinstance(nombre_servidor, str) and nombre_servidor.strip():
                                self.nombre = nombre_servidor.strip()
                            color_servidor = info.get("tu_color")
                            self.color = self._normalizar_color(color_servidor, self.color)
                        else:
                            # Marca como sincronizado después de la primera recepción
                            self.nombre_color_sincronizado = True
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
                                  text="Flechas para moverse | Entra a la casa por la puerta",
                                  fill="white", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 30,
                                 text="", fill="yellow", font=("Consolas", 14, "bold"))
        self.jugadores_online = c.create_text(10, 10,
                                              text="Jugadores: 1/20", fill="lime", font=("Consolas", 10))

    # --- Dibujo interior ---

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
                
                chat = self.chat_burbujas.get(jugador_id)
                if chat:
                    self._dibujar_chat_en_posicion(ox, oy, chat["texto"])

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
        
        # Mostrar efecto de casteo si está activo (para hechicero)
        if self.clase == "hechicero" and self.casteo_timer > 0:
            progress = 1 - (self.casteo_timer / self.casteo_duracion)
            barra_ancho = 30
            c.create_rectangle(x-barra_ancho//2, y+r+15, x+barra_ancho//2, y+r+20, 
                             fill="#333333", outline="#ffffff", width=1, tags="personaje")
            c.create_rectangle(x-barra_ancho//2, y+r+15, x-barra_ancho//2 + barra_ancho*progress, y+r+20,
                             fill="#ff8c00", outline="", tags="personaje")
            c.create_text(x, y+r+28, text=f"Casteando... {int(self.casteo_timer/60):.1f}s", 
                         fill="#ff8c00", font=("Consolas", 9), tags="personaje")
        
        if self.id_jugador:
            chat = self.chat_burbujas.get(self.id_jugador)
            if chat:
                self._dibujar_chat_en_posicion(x, y, chat["texto"])

    # --- Input ---

    def tecla_presionada(self, evento):
        tecla = evento.keysym.lower()

        if tecla == "f1":
            self._usar_habilidad()
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
            self._ataque_paladin()
        elif self.clase == "hechicero":
            if self.casteo_timer == 0:  # Solo puede castear si no está casteando
                self._iniciar_casteo_hechizo()
        elif self.clase == "sanador":
            self._sanar_cercanos()

    def _ataque_paladin(self):
        """Paladin hace un ataque con espada."""
        self.ataque_timer = 30  # 0.5 segundos
        self.accion_pendiente = "ataque_paladin"
        # Agregar partículas de ataque
        for i in range(8):
            angulo = (i / 8) * 2 * math.pi
            vel_x = 5 * math.cos(angulo)
            vel_y = 5 * math.sin(angulo)
            self.particulas.append({
                "x": self.px,
                "y": self.py,
                "vx": vel_x,
                "vy": vel_y,
                "vida": 30,
                "tipo": "espada"
            })

    def _iniciar_casteo_hechizo(self):
        """Inicia el casteo del hechizo de fuego del hechicero."""
        self.casteo_timer = 240  # 4 segundos a 60 FPS
        self.casteo_duracion = 240

    def _sanar_cercanos(self):
        """Sanador sana HP propio y muestra aura de sanación."""
        self.accion_pendiente = "sanacion"
        # Agregar partículas de sanación en círculo
        for i in range(12):
            angulo = (i / 12) * 2 * math.pi
            vel_x = 3 * math.cos(angulo)
            vel_y = 3 * math.sin(angulo)
            self.particulas.append({
                "x": self.px,
                "y": self.py,
                "vx": vel_x,
                "vy": vel_y,
                "vida": 45,
                "tipo": "sanacion"
            })

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

    def _actualizar_rata(self):
        """IA del ratón monstruo: patrulla, persigue y ataca al jugador."""
        if self.rata["hp"] <= 0 or self.muerto:
            return

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
        x, y = self.px, self.py
        r = cfg.RADIO
        segundos = self.muerte_timer // 60 + 1
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
        # Texto de espera
        c.create_text(x, y + r + 18, text=f"Reapareciendo en {segundos}s...",
                      fill="#ff4444", font=("Consolas", 9, "bold"))

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
        elif self.estado == "agua":
            self.px = max(cfg.RADIO, min(cfg.ANCHO - cfg.RADIO, nx))
            self.py = max(25 + cfg.RADIO, min(cfg.ALTO - cfg.RADIO, ny))
        elif self.estado == "casita_arbol":
            self.px = max(100 + cfg.RADIO, min(700 - cfg.RADIO, nx))
            self.py = max(160 + cfg.RADIO, min(cfg.ALTO - cfg.RADIO, ny))

    # --- Game loop ---

    def _loop(self):
        self._actualizar_timers_chat()
        self._actualizar_particulas()

        # --- Manejar muerte del jugador ---
        if self.muerto:
            # Redibujar el mapa actual con overlay de muerte (autoridad del servidor)
            if self.estado == "subterraneo":
                self._dibujar_subterraneo()
            elif self.estado == "interior":
                self._dibujar_interior()
            elif self.estado == "exterior":
                self._dibujar_exterior()
            self._dibujar_muerte_overlay()
            self._dibujar_hp_bar()
            self.root.after(16, self._loop)
            return

        # Actualizar timers
        if self.casteo_timer > 0:
            self.casteo_timer -= 1
            if self.casteo_timer == 0 and self.clase == "hechicero":
                # Lanzar hechizo de fuego
                self._lanzar_hechizo_fuego()
        
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
                self.estado = "subterraneo"
                self.px = tx2 + cfg.TRAMPILLA_INT_W // 2
                self.py = 200
                self._dibujar_subterraneo()
                self.root.after(16, self._loop)
                return

            self._dibujar_interior()
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
            self._dibujar_particulas()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        # Recrear chat_input cada frame (c.delete("all") lo borra)
        self.chat_input = self.canvas.create_text(
            cfg.ANCHO // 2,
            cfg.ALTO - 42,
            text="",
            fill="#ffe082",
            font=("Consolas", 11, "bold"),
        )

        if self.chat_activo:
            self.canvas.itemconfig(self.chat_input, text=f"Chat: {self.chat_texto_actual}_")
        else:
            habilidad_info = ""
            if self.clase == "paladin":
                habilidad_info = " | F1: Ataque"
            elif self.clase == "hechicero":
                habilidad_info = " | F1: Castear Fuego (4 seg)"
            elif self.clase == "sanador":
                habilidad_info = " | F1: Sanar cercanos"
            
            self.canvas.itemconfig(
                self.chat_input,
                text=f"Presiona Enter o F12 para hablar{habilidad_info}",
            )
        self.canvas.tag_raise(self.chat_input)

        self.root.after(16, self._loop)

    def _lanzar_hechizo_fuego(self):
        """Lanza el hechizo de fuego del hechicero."""
        self.accion_pendiente = "hechizo_fuego"
        # Crear partículas de fuego en la dirección frontal
        for i in range(15):
            angulo = (i / 15) * 2 * math.pi + (math.pi / 8)
            vel_x = 7 * math.cos(angulo)
            vel_y = 7 * math.sin(angulo)
            self.particulas.append({
                "x": self.px,
                "y": self.py,
                "vx": vel_x,
                "vy": vel_y,
                "vida": 60,
                "tipo": "fuego"
            })


if __name__ == "__main__":
    root = tk.Tk()
    JuegoMultijugador(root)
    root.mainloop()
