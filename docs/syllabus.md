# 📅 Syllabus y cronograma

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md) · [🗺️ Roadmap](../ROADMAP.md)

Planificación temporal de **Polyglot Programming Labs** (176 clases · 12 partes).
Las horas son estimadas: leer la clase, estudiar las 10 implementaciones, ejecutar el
verificador de equivalencia y resolver el reto de transferencia.

> Ritmo de referencia: **~10 h/semana**. A ese ritmo el programa completo son **~10 meses**;
> a tiempo completo (~30 h/semana), **~3,5 meses**. No es obligatorio hacerlo entero: usa las
> [rutas por perfil](../rutas/README.md) para un subconjunto coherente.

## Horas por parte

Las partes 0–2 son **clases de método** (más cortas: se leen y se razonan). Las partes 3–11 son
**clases de código**: cada una trae 10 implementaciones que comparar, y por eso pesan más.

| Parte | Tema | Clases | Tipo | Horas aprox. | Semanas @10h |
|---|---|---:|---|---:|---:|
| 0 | Pensamiento computacional y el método políglota | 14 | método | ~21 | 2,1 |
| 1 | Atlas y genealogía de los lenguajes | 14 | método | ~21 | 2,1 |
| 2 | Herramientas, toolchains y anatomía de comandos | 12 | método | ~18 | 1,8 |
| 3 | Valores, tipos y variables | 16 | código | ~40 | 4,0 |
| 4 | Control del programa | 16 | código | ~40 | 4,0 |
| 5 | Funciones y modularidad | 16 | código | ~40 | 4,0 |
| 6 | Datos y estructuras | 18 | código | ~45 | 4,5 |
| 7 | Paradigmas | 16 | código | ~40 | 4,0 |
| 8 | Cómo funcionan los lenguajes | 16 | código | ~40 | 4,0 |
| 9 | Ingeniería de software políglota | 16 | código | ~40 | 4,0 |
| 10 | Interoperabilidad y fronteras entre lenguajes | 10 | código | ~25 | 2,5 |
| 11 | Proyecto integrador políglota | 12 | proyecto | ~36 | 3,6 |
| | **Total** | **176** | | **~406 h** | **~41 sem** |

*(Cada clase de código ronda las 2,5 h: ~40 min de concepto, ~1 h leyendo y comparando las 10
implementaciones, ~50 min de reto. Las de método rondan 1,5 h.)*

## Dependencias entre partes

- **Parte 0** es prerrequisito de todo: fija el método de comparación (sintáctico / semántico / paradigmático).
- **0 → 3 → 4 → 5** es la columna vertebral: sin valores y tipos no hay control, y sin control no hay funciones.
- **6** (datos) asume 3 y 5.
- **7** (paradigmas) asume 5 y 6: no se entiende lo funcional sin funciones de primera clase ni lo OO sin registros.
- **8** (runtime) es transversal y se puede adelantar si te interesa el "por qué" de la memoria; gana leído tras 6.
- **1** (Atlas) y **2** (toolchains) son de consulta: puedes leerlas por encima y volver cuando aparezca un lenguaje nuevo.
- **9** (ingeniería) asume 5 y 6; **10** (interoperabilidad) asume 8 y 9.
- **11** (proyecto integrador) asume todo lo anterior: es donde se junta.

## Cómo planificar una semana tipo (10 h)

| Día | Actividad |
|---|---|
| 2 sesiones de 2 h | Dos clases nuevas: concepto → pseudocódigo → leer las 10 implementaciones. |
| 1 sesión de 2 h | Retos de transferencia de esas clases (portar el código a un lenguaje que no domines). |
| 1 sesión de 2 h | Ejecutar el verificador y comparar salidas; anotar diferencias semánticas. |
| 1 sesión de 2 h | Repaso: [autoevaluación](../autoevaluaciones/README.md) de la parte y [glosario](../glosario/README.md). |

## Evaluación

El progreso se mide con la [rúbrica de evaluación](rubrica-evaluacion.md) y cada ruta cierra con
su [examen final por perfil](examen-final-por-perfil.md).
