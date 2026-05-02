import tkinter as tk
import math
import configuracion as cfg


class Juego:
    def __init__(self, root):
        self.root = root
        self.root.title("Aventura")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=cfg.ANCHO, height=cfg.ALTO)
        self.canvas.pack()

        self.estado    = "exterior"
        self.px        = cfg.ANCHO // 2
        self.py        = cfg.ALTO  // 2
        self.msg_timer = 0
        self.hud       = None
        self.msg       = None

        self.teclas = set()
        self.root.bind("<KeyPress>",   self.tecla_presionada)
        self.root.bind("<KeyRelease>", self.tecla_soltada)

        self._dibujar_exterior()
        self._loop()

    # ── Dibujo exterior ────────────────────────────────────────────────────────

    def _dibujar_exterior(self):
        c = self.canvas
        c.delete("all")

        # Césped
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
        c.create_rectangle(cx+10,    pared_y+10, cx+35,    pared_y+35, fill="#aee6ff", outline="#555")
        c.create_rectangle(cx+cw-35, pared_y+10, cx+cw-10, pared_y+35, fill="#aee6ff", outline="#555")
        px_p = cx + cw // 2 - 14
        c.create_rectangle(px_p, cy+ch-40, px_p+28, cy+ch,
                           fill=cfg.COLOR_CASA_PUERTA, outline="#3e2000", width=2)

        # Árboles
        for ax, ay in cfg.ARBOLES:
            c.create_oval(ax-18, ay-8,  ax+18, ay+14, fill=cfg.COLOR_SOMBRA_ARBOL, outline="")
            c.create_oval(ax-20, ay-25, ax+20, ay+10, fill=cfg.COLOR_COPA, outline=cfg.COLOR_BORDE_COPA, width=2)
            c.create_rectangle(ax-5, ay+8, ax+5, ay+20, fill=cfg.COLOR_TRONCO, outline="")

        # Barriles
        for bx, by in cfg.BARRILES:
            r = cfg.RADIO_BARRIL
            c.create_oval(bx-r, by-r, bx+r, by+r,
                          fill=cfg.COLOR_BARRIL, outline=cfg.COLOR_BARRIL_ARO, width=3)
            c.create_line(bx-r+2, by-4, bx+r-2, by-4, fill=cfg.COLOR_BARRIL_ARO, width=2)
            c.create_line(bx-r+2, by+4, bx+r-2, by+4, fill=cfg.COLOR_BARRIL_ARO, width=2)

        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                  text="Flechas para moverse  |  Entra a la casa por la puerta",
                                  fill="white", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 30,
                                  text="", fill="yellow", font=("Consolas", 14, "bold"))

    # ── Dibujo interior ────────────────────────────────────────────────────────

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
        c.create_rectangle(0,           0,           cfg.ANCHO,   g,         fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(0,           cfg.ALTO-g,  cfg.ANCHO,   cfg.ALTO,  fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(0,           0,           g,           cfg.ALTO,  fill=cfg.COLOR_PARED_INT, outline="")
        c.create_rectangle(cfg.ANCHO-g, 0,           cfg.ANCHO,   cfg.ALTO,  fill=cfg.COLOR_PARED_INT, outline="")

        # Puerta de salida (hueco en pared inferior)
        sx = cfg.SALIDA_INT_X
        c.create_rectangle(sx-28, cfg.ALTO-g-2, sx+28, cfg.ALTO,
                           fill=cfg.COLOR_CASA_PUERTA, outline="#3e2000", width=2)
        c.create_text(sx, cfg.ALTO-g-15, text="Salida", fill="white", font=("Consolas", 10, "bold"))

        # Muebles
        for mx, my, mw, mh, mcolor, mlabel in cfg.MUEBLES:
            c.create_rectangle(mx, my, mx+mw, my+mh, fill=mcolor, outline="#2e1a0e", width=2)
            c.create_text(mx+mw//2, my+mh//2, text=mlabel, fill="#f5deb3", font=("Consolas", 9))

        self._dibujar_personaje()
        self.hud = c.create_text(cfg.ANCHO//2, cfg.ALTO-18,
                                  text="Flechas para moverse  |  Toca la salida para salir",
                                  fill="white", font=("Consolas", 12))
        self.msg = c.create_text(cfg.ANCHO//2, 50,
                                  text="Bienvenido a la casa",
                                  fill="yellow", font=("Consolas", 14, "bold"))
        self.msg_timer = 120

    # ── Personaje ──────────────────────────────────────────────────────────────

    def _dibujar_personaje(self):
        self.canvas.delete("personaje")
        c = self.canvas
        x, y, r = self.px, self.py, cfg.RADIO
        c.create_oval(x-r+4, y-r+8, x+r+4, y+r+8,
                      fill=cfg.COLOR_SOMBRA_ARBOL, outline="", tags="personaje")
        c.create_oval(x-r, y-r, x+r, y+r,
                      fill=cfg.COLOR_CUERPO, outline=cfg.COLOR_BORDE_CUERPO, width=2, tags="personaje")
        c.create_oval(x-r+5, y-r+2, x+r-5, y+4,
                      fill=cfg.COLOR_CARA, outline=cfg.COLOR_BORDE_CARA, width=1, tags="personaje")
        c.create_oval(x-7, y-10, x-3, y-6, fill="black", tags="personaje")
        c.create_oval(x+3, y-10, x+7, y-6, fill="black", tags="personaje")

    # ── Input ──────────────────────────────────────────────────────────────────

    def tecla_presionada(self, evento):
        self.teclas.add(evento.keysym.lower())

    def tecla_soltada(self, evento):
        self.teclas.discard(evento.keysym.lower())

    # ── Colisiones ─────────────────────────────────────────────────────────────

    def _bloqueado_exterior(self, px, py):
        # Lago (elipse)
        lx, ly = cfg.LAGO_X, cfg.LAGO_Y
        rx = cfg.LAGO_RX + cfg.RADIO
        ry = cfg.LAGO_RY + cfg.RADIO
        if ((px - lx) / rx) ** 2 + ((py - ly) / ry) ** 2 < 1:
            return True
        # Árboles
        for ax, ay in cfg.ARBOLES:
            if math.hypot(px - ax, py - ay) < cfg.RADIO + cfg.RADIO_ARBOL:
                return True
        # Casa: bloque todo el rectángulo salvo el hueco de la puerta
        cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
        pared_y = cy + ch // 4
        px_p    = cx + cw // 2 - 14
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
        ny = max(cfg.RADIO, min(cfg.ALTO  - cfg.RADIO, self.py + dy))

        if self.estado == "exterior":
            if not self._bloqueado_exterior(nx, self.py): self.px = nx
            if not self._bloqueado_exterior(self.px, ny): self.py = ny

        elif self.estado == "interior":
            g = 30
            # Paredes laterales y superior siempre bloquean
            nx = max(cfg.RADIO + g, min(cfg.ANCHO - cfg.RADIO - g, nx))
            # Pared inferior: hay hueco en la puerta de salida
            sx = cfg.SALIDA_INT_X
            limite_inf = cfg.ALTO - cfg.RADIO - g if abs(nx - sx) > 30 else cfg.ALTO - cfg.RADIO
            ny = max(cfg.RADIO + g, min(limite_inf, ny))

            if not self._bloqueado_interior(nx, self.py): self.px = nx
            if not self._bloqueado_interior(self.px, ny): self.py = ny

    # ── Game loop ──────────────────────────────────────────────────────────────

    def _loop(self):
        dx, dy = 0, 0
        if "up"    in self.teclas: dy -= cfg.VELOCIDAD
        if "down"  in self.teclas: dy += cfg.VELOCIDAD
        if "left"  in self.teclas: dx -= cfg.VELOCIDAD
        if "right" in self.teclas: dx += cfg.VELOCIDAD

        self._mover(dx, dy)

        if self.estado == "exterior":
            # ¿Entra a la casa por la puerta?
            cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
            px_puerta = cx + cw // 2
            if math.hypot(self.px - px_puerta, self.py - (cy + ch)) < cfg.RADIO + 18:
                self.estado = "interior"
                self.px = cfg.SALIDA_INT_X
                self.py = cfg.ALTO - 85
                self._dibujar_interior()
                self.root.after(16, self._loop)
                return

            # Mensaje barriles
            toca_barril = any(
                math.hypot(self.px - bx, self.py - by) < cfg.RADIO + cfg.RADIO_BARRIL
                for bx, by in cfg.BARRILES
            )
            self._dibujar_personaje()
            self.canvas.tag_raise(self.hud)
            if toca_barril:
                self.canvas.itemconfig(self.msg, text="Este es un barrel")
                self.msg_timer = 80
            elif self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        elif self.estado == "interior":
            # ¿Sale por la puerta?
            sx = cfg.SALIDA_INT_X
            if self.py > cfg.ALTO - 75 and abs(self.px - sx) < 30:
                self.estado = "exterior"
                cx, cy, cw, ch = cfg.CASA_X, cfg.CASA_Y, cfg.CASA_W, cfg.CASA_H
                self.px = cx + cw // 2
                self.py = cy + ch + 40
                self._dibujar_exterior()
                self.root.after(16, self._loop)
                return

            self._dibujar_personaje()
            self.canvas.tag_raise(self.hud)
            if self.msg_timer > 0:
                self.msg_timer -= 1
            else:
                self.canvas.itemconfig(self.msg, text="")
            self.canvas.tag_raise(self.msg)

        self.root.after(16, self._loop)  # ~60 FPS


# --- Iniciar juego ---
if __name__ == "__main__":
    root = tk.Tk()
    Juego(root)
    root.mainloop()

