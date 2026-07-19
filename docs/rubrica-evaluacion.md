# 📊 Rúbrica de evaluación

> [⬅️ Volver al programa](../README.md) · [📅 Syllabus](syllabus.md) · [🎓 Examen final](examen-final-por-perfil.md)

Cómo evaluar (o autoevaluarte) el trabajo del programa de forma objetiva y consistente.
Aplica tanto al alumno autodidacta como al instructor.

En un programa políglota **no basta con que el código funcione**: lo que se evalúa es si el
estudiante entendió *qué permanece y qué cambia* al pasar el concepto de un lenguaje a otro.

## 1. Reto de transferencia de cada clase

Cada clase termina con un **reto de transferencia**: implementar el concepto en un lenguaje que
no sea el de partida, respetando el `casos.json` común. Puntúalo con esta escala graduada:

| Nivel | Descripción | Puntos |
|---|---|---:|
| **A — Competente** | Pasa el verificador de equivalencia **y** el código es idiomático en el lenguaje destino; explica qué diferencia semántica tuvo que salvar. | 3 |
| **B — En desarrollo** | Pasa el verificador, pero el código es una traducción literal del original (no idiomática) o no argumenta las diferencias. | 2 |
| **C — Inicial** | No pasa todos los casos, o solo funciona en el caso feliz. | 1 |
| **0 — No entregado** | Sin evidencia. | 0 |

**Aprobado de una clase:** nivel B o superior.
**Aprobado de una parte:** ≥ 80 % de sus clases en nivel B+ y el [quiz](../autoevaluaciones/README.md) de la parte ≥ 70 %.

## 2. Criterios transversales (aplican a todo entregable)

| Criterio | Qué se evalúa |
|---|---|
| **Equivalencia demostrada** | El verificador pasa: todas las implementaciones producen la misma salida ante el mismo `casos.json`. |
| **Idiomática** | El código respeta las convenciones del lenguaje destino (no es C escrito con sintaxis de Python). |
| **Clasificación de la diferencia** | Distingue correctamente si un cambio es **sintáctico**, **semántico** o **paradigmático**. |
| **Honestidad técnica** | No se afirma una equivalencia que el lenguaje no ofrece; se nombran los límites. |
| **Reproducibilidad** | Otra persona ejecuta los comandos dados y obtiene el mismo resultado. |
| **Comunicación** | Explicación clara, en español, con el término correcto (ver [glosario](../glosario/README.md)). |

## 3. Rúbrica de laboratorio (verificador de equivalencia)

Para los [laboratorios](../labs/README.md):

| Criterio | A (3) | B (2) | C (1) |
|---|---|---|---|
| Ejecución | Corre el verificador en toda la parte y lee el informe | Lo corre en una clase | No lo ejecuta |
| Diagnóstico | Ante un fallo, identifica si es de entrada/salida, semántico o de toolchain | Detecta que falla | No interpreta el fallo |
| Toolchains | Instala y verifica al menos 5 lenguajes del núcleo | Trabaja con 2–3 | Solo con el suyo |
| Comparación | Documenta una diferencia semántica real observada entre dos salidas | Anota diferencias superficiales | No compara |

## 4. Rúbrica del proyecto integrador (Parte 11)

El [proyecto integrador](../classes/parte-11-proyecto-integrador-poliglota/README.md) es el
entregable de mayor peso: un sistema con componentes en varios lenguajes. Evalúa sobre 100:

| Bloque | Peso | Qué se evalúa |
|---|---:|---|
| **Diseño y contratos** | 20 | Las responsabilidades entre componentes están separadas y el contrato entre ellos es explícito y versionado. |
| **Elección de lenguaje justificada** | 20 | Cada componente usa su lenguaje **por una razón** (rendimiento, ecosistema, expresividad), no por costumbre. |
| **Implementación** | 25 | Los componentes funcionan y son idiomáticos en su lenguaje. |
| **Frontera e interoperabilidad** | 20 | Los datos cruzan la frontera correctamente: serialización, tipos, errores y fallos parciales contemplados. |
| **Ingeniería** | 15 | Pruebas, dependencias fijadas, build reproducible y documentación de cómo ejecutarlo. |

**Aprobado:** ≥ 70/100, con **frontera e interoperabilidad ≥ 12/20** (es el corazón de la parte).

## 5. Calificación final del programa

| Componente | Peso |
|---|---:|
| Retos de transferencia (media de las 12 partes) | 40 % |
| Autoevaluaciones por parte | 20 % |
| Proyecto integrador (Parte 11) | 40 % |

**Aprobado del programa:** ≥ 70 % global y proyecto integrador aprobado.
