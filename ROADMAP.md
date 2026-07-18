# 🗺️ Roadmap

> [⬅️ Volver al programa](README.md) · [📚 Índice completo](classes/README.md)

Estado del programa **Polyglot Programming Labs**: **completo — las 176 clases en 12 partes están construidas.** Las clases de código (Partes 3–11) traen sus 10 implementaciones del núcleo verificadas en CI; las de método (Partes 0–2) son conceptuales.

Leyenda: ✅ construida.

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

## Construcción (completada)

1. **Infraestructura y portal** ✅ — manifest, índice, README, verificador de equivalencia, CI (matriz por lenguaje), sitio.
2. **Partes 0–2** ✅ — método políglota, Atlas de familias y toolchains/comandos (clases de método).
3. **Partes 3–11** ✅ — clases de código: valores, control, funciones, datos, paradigmas, runtime, ingeniería, interoperabilidad y proyecto integrador, cada una con 10 implementaciones verificadas.

## Cómo seguir aprendiendo

El programa termina en la [clase 176](classes/parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md) con una idea: el conocimiento es transferible. Elige un lenguaje del [Atlas](atlas/README.md) que no domines, léelo por su familia y resuelve una clase en él.

## Cómo se genera todo

Todo deriva de [`classes/_manifest.json`](classes/_manifest.json), producido por
[`scripts/build.py`](scripts/build.py) a partir de [`scripts/curriculo.py`](scripts/curriculo.py).
Re-ejecutar `python scripts/build.py` actualiza índice y README sin pisar el contenido escrito a mano.
