import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import socket
import threading
import ast
import json
import math
import re


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

    # --- Red ---
    SERVIDOR_PORT = 5000
    # IP del servidor del profesor. 127.0.0.1 solo funciona en la misma maquina.
    SERVIDOR_HOSTS = ["3.85.165.104", "172.31.82.40", "127.0.0.1"]

    # --- Chat ---
    CHAT_MAX_CARACTERES = 120
    CHAT_DURACION_FRAMES = 240  # ~4s a 60 FPS


class JuegoMultijugador:
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

        color_elegido = colorchooser.askcolor(
            color=cfg.COLOR_CUERPO,
            title="Escoge tu color",
            parent=self.root,
        )[1]
        self.color = self._normalizar_color(color_elegido, cfg.COLOR_CUERPO)

        # Conectar al servidor
        self.socket = None
        conectado = False
        for host in cfg.SERVIDOR_HOSTS:
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
                "No se pudo conectar al servidor en: " + ", ".join(cfg.SERVIDOR_HOSTS),
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
        self.chat_burbujas = {}

        # Otros jugadores
        self.otros_jugadores = {}
        self.id_jugador = None
        self.nombre_color_sincronizado = False

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
                "chat": self.chat_pendiente,
            }) + "\n"
            self.socket.send(msg.encode())
            self.chat_pendiente = None
        except:
            pass

    @staticmethod
    def _normalizar_color(color, fallback):
        if isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color.strip()):
            return color.strip().lower()
        return fallback

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

        # Arboles
        for ax, ay in cfg.ARBOLES:
            c.create_oval(ax-18, ay-8, ax+18, ay+14, fill=cfg.COLOR_SOMBRA_ARBOL, outline="")
            c.create_oval(ax-20, ay-25, ax+20, ay+10, fill=cfg.COLOR_COPA, outline=cfg.COLOR_BORDE_COPA, width=2)
            c.create_rectangle(ax-5, ay+8, ax+5, ay+20, fill=cfg.COLOR_TRONCO, outline="")

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
        if self.id_jugador:
            chat = self.chat_burbujas.get(self.id_jugador)
            if chat:
                self._dibujar_chat_en_posicion(x, y, chat["texto"])

    # --- Input ---

    def tecla_presionada(self, evento):
        tecla = evento.keysym.lower()

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
        if ((px - lx) / rx) ** 2 + ((py - ly) / ry) ** 2 < 1:
            return True
        for ax, ay in cfg.ARBOLES:
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

    # --- Game loop ---

    def _loop(self):
        self._actualizar_timers_chat()
        dx, dy = 0, 0
        if not self.chat_activo:
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

            toca_barril = any(
                math.hypot(self.px - bx, self.py - by) < cfg.RADIO + cfg.RADIO_BARRIL
                for bx, by in cfg.BARRILES
            )
            self._dibujar_exterior()
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

            self._dibujar_interior()
            self.canvas.tag_raise(self.hud)
            self.canvas.itemconfig(self.jugadores_online,
                                   text=f"Jugadores: {len(self.otros_jugadores)+1}/20")
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        if self.chat_input is None:
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
            self.canvas.itemconfig(
                self.chat_input,
                text="Presiona Enter o F12 para hablar",
            )
        self.canvas.tag_raise(self.chat_input)

        self.root.after(16, self._loop)


if __name__ == "__main__":
    root = tk.Tk()
    JuegoMultijugador(root)
    root.mainloop()
