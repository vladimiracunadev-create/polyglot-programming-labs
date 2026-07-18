# 🗺️ Roadmap

> [⬅️ Volver al programa](README.md) · [📚 Índice completo](classes/README.md)

Estado del programa **Polyglot Programming Labs**: 176 clases en 12 partes. El **esqueleto** (carpetas, manifest, índice y README con la anatomía) está completo; el **contenido a fondo** se escribe parte por parte.

Leyenda: ✅ construida · 🏗️ en progreso · 🚧 planificada.

| Parte | Título | Clases | Estado |
|---|---|---|---|
| 0 | Pensamiento computacional y el método políglota | 14 | 🏗️ en progreso (001–003) |
| 1 | Atlas y genealogía de los lenguajes | 14 | 🚧 planificada |
| 2 | Herramientas, toolchains y anatomía de comandos | 12 | 🚧 planificada |
| 3 | Valores, tipos y variables | 16 | 🏗️ en progreso (041 insignia) |
| 4 | Control del programa | 16 | 🚧 planificada |
| 5 | Funciones y modularidad | 16 | 🚧 planificada |
| 6 | Datos y estructuras | 18 | 🚧 planificada |
| 7 | Paradigmas | 16 | 🚧 planificada |
| 8 | Cómo funcionan los lenguajes | 16 | 🚧 planificada |
| 9 | Ingeniería de software políglota | 16 | 🚧 planificada |
| 10 | Interoperabilidad y fronteras entre lenguajes | 10 | 🚧 planificada |
| 11 | Proyecto integrador políglota | 12 | 🚧 planificada |

## Orden de construcción

1. **Infraestructura y portal** ✅ — manifest, índice, README, verificador de equivalencia, CI, sitio.
2. **Parte 0 completa** 🏗️ — el método políglota y el pensamiento computacional.
3. **Parte 3 (Valores)** 🏗️ — empezando por la clase insignia 041.
4. **Partes 1–2 (Atlas + Toolchains)** — la base de comprensión y herramientas.
5. **Resto de partes** en orden curricular.

## Cómo se genera todo

Todo deriva de [`classes/_manifest.json`](classes/_manifest.json), producido por
[`scripts/build.py`](scripts/build.py) a partir de [`scripts/curriculo.py`](scripts/curriculo.py).
Re-ejecutar `python scripts/build.py` actualiza índice y README sin pisar el contenido escrito a mano.
