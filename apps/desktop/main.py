#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Polyglot Programming Labs — aplicación de escritorio (Windows, macOS y Linux).

Sirve el sitio del curso **embebido en el propio ejecutable** desde un servidor
local en 127.0.0.1 y lo abre en el navegador del sistema. Así el curso se ve tal
cual está diseñado —el HTML real, con el código de los diez lenguajes resaltado,
el buscador y la autoevaluación— sin depender de conexión ni de GitHub Pages.

Por qué un servidor local y no `file://`: el buscador del portal carga
`busqueda.json` con `fetch`, y el navegador bloquea esa petición bajo `file://`
por política de origen. Con `http://127.0.0.1:<puerto>` el portal funciona
entero, y el servidor solo escucha en la interfaz de loopback: no queda expuesto
a la red.

Uso:
    python apps/desktop/main.py            # abre la ventana de control
    python apps/desktop/main.py --no-gui   # solo servidor, imprime la URL
    python apps/desktop/main.py --puerto 8099

Empaquetado (lo hace .github/workflows/desktop.yml):
    pyinstaller --onefile --windowed --name PolyglotProgrammingLabs \\
                --add-data "site;site" apps/desktop/main.py
"""
from __future__ import annotations

import argparse
import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser

APP = "Polyglot Programming Labs"


def raiz_del_sitio() -> str:
    """Localiza `site/` tanto ejecutando el .py como dentro del binario de PyInstaller.

    PyInstaller descomprime los datos de `--add-data` en `sys._MEIPASS`; fuera del
    binario, el sitio está dos niveles por encima de este archivo.
    """
    empaquetado = getattr(sys, "_MEIPASS", None)
    candidatos = []
    if empaquetado:
        candidatos.append(os.path.join(empaquetado, "site"))
    aqui = os.path.dirname(os.path.abspath(__file__))
    candidatos.append(os.path.join(os.path.dirname(os.path.dirname(aqui)), "site"))
    for c in candidatos:
        if os.path.isfile(os.path.join(c, "index.html")):
            return c
    raise SystemExit(
        "No encuentro el sitio del curso.\n"
        "Genera el portal con:  python scripts/generar_sitio.py"
    )


def contar(raiz: str) -> dict[str, int]:
    """Recuento real de lo que hay dentro. Se muestra en la ventana y en la consola.

    No es decorativo: es la comprobación anti-vacío del lado del usuario. Si el
    ejecutable se empaquetó sin contenido, aquí se ve un cero en vez de un curso.
    """
    clases = partes = primos = paginas = 0
    for base, _dirs, ficheros in os.walk(raiz):
        carpeta = os.path.basename(base)
        for f in ficheros:
            if not f.endswith(".html"):
                continue
            paginas += 1
            if f == "README.html":
                if carpeta[:3].isdigit():
                    clases += 1
                elif carpeta.startswith("parte-"):
                    partes += 1
            elif f == "primos.html":
                primos += 1
    return {"clases": clases, "partes": partes, "primos": primos, "paginas": paginas}


def puerto_libre(preferido: int = 8765) -> int:
    """Devuelve el puerto preferido si está libre; si no, uno que dé el sistema."""
    for puerto in (preferido, 0):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", puerto))
                return s.getsockname()[1]
            except OSError:
                continue
    raise SystemExit("No hay ningún puerto local disponible.")


class Silencioso(http.server.SimpleHTTPRequestHandler):
    """Sirve el sitio sin escupir una línea de log por cada recurso pedido."""

    def log_message(self, formato, *args):  # noqa: A002 - firma de la stdlib
        pass


def arrancar_servidor(raiz: str, puerto: int) -> socketserver.TCPServer:
    def handler(*args, **kwargs):
        return Silencioso(*args, directory=raiz, **kwargs)

    servidor = socketserver.ThreadingTCPServer(("127.0.0.1", puerto), handler)
    servidor.daemon_threads = True
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def ventana(url: str, datos: dict[str, int], servidor) -> None:
    """Ventana de control mínima en Tkinter: estado, recuento y botones.

    El curso se lee en el navegador (es HTML pensado para un navegador); esta
    ventana solo mantiene vivo el servidor y da la puerta de entrada.
    """
    import tkinter as tk
    from tkinter import ttk

    FONDO, TARJETA, TINTA, SUAVE, ACENTO = "#0b1020", "#111831", "#e8ecff", "#91a7ff", "#7c5cff"

    raiz = tk.Tk()
    raiz.title(APP)
    raiz.geometry("620x430")
    raiz.minsize(560, 400)
    raiz.configure(bg=FONDO)

    tk.Label(raiz, text="🌐  " + APP, font=("Segoe UI", 19, "bold"),
             bg=FONDO, fg=TINTA).pack(anchor="w", padx=24, pady=(22, 2))
    tk.Label(raiz, text="Un concepto, diez lenguajes. El curso completo, sin conexión.",
             font=("Segoe UI", 10), bg=FONDO, fg=SUAVE).pack(anchor="w", padx=24)

    tarjeta = tk.Frame(raiz, bg=TARJETA)
    tarjeta.pack(fill="x", padx=24, pady=18)
    filas = [("Clases", datos["clases"]), ("Partes", datos["partes"]),
             ("Anexos de primos", datos["primos"]), ("Páginas HTML", datos["paginas"])]
    for i, (etiqueta, valor) in enumerate(filas):
        tk.Label(tarjeta, text=etiqueta, font=("Segoe UI", 10), bg=TARJETA,
                 fg=SUAVE).grid(row=i, column=0, sticky="w", padx=16, pady=5)
        tk.Label(tarjeta, text=str(valor), font=("Segoe UI", 12, "bold"), bg=TARJETA,
                 fg=TINTA).grid(row=i, column=1, sticky="e", padx=16)
    tarjeta.columnconfigure(1, weight=1)

    tk.Label(raiz, text=f"Servidor local: {url}", font=("Consolas", 10),
             bg=FONDO, fg=ACENTO).pack(anchor="w", padx=24)
    tk.Label(raiz, text="Solo escucha en 127.0.0.1 (tu equipo). Nada sale a Internet.",
             font=("Segoe UI", 9), bg=FONDO, fg=SUAVE).pack(anchor="w", padx=24, pady=(2, 14))

    botones = tk.Frame(raiz, bg=FONDO)
    botones.pack(anchor="w", padx=24)
    ttk.Button(botones, text="📚 Abrir el curso",
               command=lambda: webbrowser.open(url)).pack(side="left")
    ttk.Button(botones, text="🧭 Rutas por perfil",
               command=lambda: webbrowser.open(url + "rutas/README.html")).pack(side="left", padx=8)
    ttk.Button(botones, text="🔎 Buscador",
               command=lambda: webbrowser.open(url + "buscar.html")).pack(side="left")

    def cerrar() -> None:
        servidor.shutdown()
        raiz.destroy()

    ttk.Button(raiz, text="Salir", command=cerrar).pack(anchor="w", padx=24, pady=16)
    raiz.protocol("WM_DELETE_WINDOW", cerrar)
    raiz.mainloop()


def main() -> int:
    ap = argparse.ArgumentParser(description=f"{APP} — curso offline en tu equipo")
    ap.add_argument("--puerto", type=int, default=8765, help="puerto local (por defecto 8765)")
    ap.add_argument("--no-gui", action="store_true", help="sin ventana: solo servidor")
    ap.add_argument("--no-abrir", action="store_true", help="no abrir el navegador al arrancar")
    args = ap.parse_args()

    raiz = raiz_del_sitio()
    datos = contar(raiz)
    if datos["clases"] == 0:
        print("ERROR: el sitio empaquetado no contiene ninguna clase.", file=sys.stderr)
        return 1

    puerto = puerto_libre(args.puerto)
    servidor = arrancar_servidor(raiz, puerto)
    url = f"http://127.0.0.1:{puerto}/"

    print(f"{APP}")
    print(f"  {datos['clases']} clases · {datos['partes']} partes · "
          f"{datos['primos']} anexos de primos · {datos['paginas']} páginas")
    print(f"  Sirviendo en {url}  (Ctrl+C para salir)")

    if not args.no_abrir:
        webbrowser.open(url)

    if args.no_gui:
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            servidor.shutdown()
        return 0

    try:
        ventana(url, datos, servidor)
    except Exception as exc:  # sin entorno gráfico: se degrada a modo consola
        print(f"  (sin ventana: {exc}; sigue sirviendo, Ctrl+C para salir)")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            servidor.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
