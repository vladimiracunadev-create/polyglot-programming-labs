# 🗺️ Roadmap

> [⬅️ Volver al programa](README.md) · [📚 Índice completo](classes/README.md)

Estado del programa **Polyglot Programming Labs**: 176 clases en 12 partes. El **esqueleto** (carpetas, manifest, índice y README con la anatomía) está completo; el **contenido a fondo** se escribe parte por parte.

Leyenda: ✅ construida · 🏗️ en progreso · 🚧 planificada.

| Parte | Título | Clases | Estado |
|---|---|---|---|
| 0 | Pensamiento computacional y el método políglota | 14 | ✅ construida (001–014) |
| 1 | Atlas y genealogía de los lenguajes | 14 | ✅ construida (015–028) |
| 2 | Herramientas, toolchains y anatomía de comandos | 12 | ✅ construida (029–040) |
| 3 | Valores, tipos y variables | 16 | ✅ construida (041–056) |
| 4 | Control del programa | 16 | ✅ construida (057–072) |
| 5 | Funciones y modularidad | 16 | ✅ construida (073–088) |
| 6 | Datos y estructuras | 18 | ✅ construida (089–106) |
| 7 | Paradigmas | 16 | ✅ construida (107–122) |
| 8 | Cómo funcionan los lenguajes | 16 | ✅ construida (123–138) |
| 9 | Ingeniería de software políglota | 16 | ✅ construida (139–154) |
| 10 | Interoperabilidad y fronteras entre lenguajes | 10 | ✅ construida (155–164) |
| 11 | Proyecto integrador políglota | 12 | ✅ construida (165–176) |

## Orden de construcción

1. **Infraestructura y portal** ✅ — manifest, índice, README, verificador de equivalencia, CI, sitio.
2. **Parte 0 completa** ✅ — el método políglota y el pensamiento computacional.
3. **Partes 1–2 completas** ✅ — Atlas de familias y toolchains/comandos.
4. **Parte 3 (Valores)** 🏗️ — clases de código, empezando por la insignia 041.
5. **Resto de partes** en orden curricular.

## Cómo se genera todo

Todo deriva de [`classes/_manifest.json`](classes/_manifest.json), producido por
[`scripts/build.py`](scripts/build.py) a partir de [`scripts/curriculo.py`](scripts/curriculo.py).
Re-ejecutar `python scripts/build.py` actualiza índice y README sin pisar el contenido escrito a mano.
