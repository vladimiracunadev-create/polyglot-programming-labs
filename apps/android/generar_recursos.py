#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el icono y las pantallas de arranque de la app Android.

`@capacitor/assets` espera encontrar en `resources/`:

    icon.png          1024×1024   se recorta a todas las densidades
    splash.png        2732×2732   pantalla de arranque (claro)
    splash-dark.png   2732×2732   pantalla de arranque (oscuro)

Se generan aquí, con Pillow, en vez de versionar imágenes hechas a mano: así el
icono deriva de la misma identidad del portal (el degradado morado del sitio y
el globo del programa) y se puede regenerar sin abrir un editor.

Uso:  python apps/android/generar_recursos.py
Requiere: pip install pillow
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(AQUI, "resources")

# Los mismos colores que el portal (scripts/generar_sitio.py).
MORADO = (124, 92, 255)
MORADO_OSCURO = (91, 33, 182)
FONDO_OSCURO = (11, 16, 32)
FONDO_CLARO = (247, 247, 251)
TEXTO_CLARO = (232, 236, 255)


def degradado(lado: int, arriba: tuple[int, int, int], abajo: tuple[int, int, int]) -> Image.Image:
    """Degradado vertical: el mismo recurso visual que usa el sitio en las cabeceras."""
    img = Image.new("RGB", (1, lado))
    px = img.load()
    for y in range(lado):
        t = y / max(lado - 1, 1)
        px[0, y] = tuple(round(a + (b - a) * t) for a, b in zip(arriba, abajo))
    return img.resize((lado, lado))


def icono(lado: int = 1024) -> Image.Image:
    """Icono: cuadrado con degradado, un globo terráqueo simplificado y «10»."""
    img = degradado(lado, MORADO, MORADO_OSCURO).convert("RGBA")
    d = ImageDraw.Draw(img)
    c, r = lado / 2, lado * 0.30
    ancho = max(2, round(lado * 0.018))
    blanco = (255, 255, 255, 235)

    # Circunferencia del globo.
    d.ellipse([c - r, c - r, c + r, c + r], outline=blanco, width=ancho)
    # Ecuador y dos trópicos: las horizontales del meridiano.
    for dy in (-r * 0.55, 0.0, r * 0.55):
        semi = (r * r - dy * dy) ** 0.5
        d.line([c - semi, c + dy, c + semi, c + dy], fill=blanco, width=ancho)
    # Meridianos: elipses cada vez más estrechas, que es como se dibuja un globo.
    for k in (1.0, 0.55, 0.18):
        d.ellipse([c - r * k, c - r, c + r * k, c + r], outline=blanco, width=ancho)
    return img


def splash(lado: int, fondo: tuple[int, int, int], tinta: tuple[int, int, int]) -> Image.Image:
    """Pantalla de arranque: fondo liso y el globo centrado, sin texto (escala mal)."""
    img = Image.new("RGB", (lado, lado), fondo).convert("RGBA")
    marca = icono(round(lado * 0.28))
    # Borde redondeado por máscara, para que no aparezca un cuadrado duro sobre el fondo.
    mascara = Image.new("L", marca.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, marca.size[0] - 1, marca.size[1] - 1],
                                              radius=round(marca.size[0] * 0.22), fill=255)
    pos = ((lado - marca.size[0]) // 2, (lado - marca.size[1]) // 2)
    img.paste(marca, pos, mascara)
    d = ImageDraw.Draw(img)
    barra = round(lado * 0.006)
    y = pos[1] + marca.size[1] + round(lado * 0.06)
    d.rounded_rectangle([lado * 0.38, y, lado * 0.62, y + barra], radius=barra, fill=tinta)
    return img.convert("RGB")


def main() -> int:
    os.makedirs(RES, exist_ok=True)
    icono().convert("RGB").save(os.path.join(RES, "icon.png"))
    splash(2732, FONDO_CLARO, MORADO).save(os.path.join(RES, "splash.png"))
    splash(2732, FONDO_OSCURO, TEXTO_CLARO).save(os.path.join(RES, "splash-dark.png"))
    for n in ("icon.png", "splash.png", "splash-dark.png"):
        ruta = os.path.join(RES, n)
        print(f"  resources/{n} ({os.path.getsize(ruta) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
