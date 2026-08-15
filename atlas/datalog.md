# 🧾 Datalog — 1977

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Datalog es [Prolog](prolog.md) **al que se le han quitado cosas a propósito** — sin funciones, sin
negación sin restricciones, sin orden de cláusulas significativo — y **de esa renuncia salen tres
garantías** que Prolog no puede dar: **termina siempre, el resultado no depende del orden, y se puede
optimizar como una consulta**.

> **🎯 Por qué está en este programa**
>
> Datalog es un **primo de la familia lógica y declarativa** ([Atlas](README.md#logica-declarativa)),
> cuyo representante en el núcleo es [SQL](sql.md).
>
> Aporta al programa la demostración más limpia de la tesis que atraviesa el curso (clases 118, 146 y
> 164): **lo que un lenguaje prohíbe es lo que sus herramientas pueden prometer**. Y aporta el
> concepto de **recursión declarativa** — consultar una jerarquía o un grafo sin escribir el recorrido
> (clase 099).

| | |
|---|---|
| **Año** | Formalizado hacia 1977; base teórica en bases de datos deductivas de los ochenta |
| **Autoría** | Comunidad académica de bases de datos; el nombre, de Hervé Gallaire y Jack Minker |
| **Familia** | Lógica y declarativa; **subconjunto decidible de Prolog** |
| **Paradigma** | **Lógico declarativo**, sobre relaciones |
| **Tipado** | Según la implementación; los datos son tuplas de constantes |
| **Memoria** | Gestionada por el motor |
| **Ejecución** | Evaluación **ascendente** con punto fijo (semi-naïve), o mágica |
| **Estado** | 🟢 **En auge**: análisis de programas, seguridad, bases de datos y grafos |

---

## 📜 Historia

Datalog surgió a finales de los setenta en la intersección de dos comunidades: **la lógica** —de donde
venía [Prolog](prolog.md)— y **las bases de datos** —donde el modelo relacional de Codd (ficha de
[SQL](sql.md)) acababa de ganar—.

La pregunta era: **¿qué subconjunto de la lógica se puede evaluar como una consulta a una base de
datos, con garantías?** Y la respuesta fue quitar tres cosas de Prolog:

1. **Los términos compuestos y las funciones**: solo hay constantes y variables, así que **el
   universo de valores es finito**.
2. **El corte y el control explícito**: no hay forma de guiar la búsqueda.
3. **El orden de las cláusulas como semántica**: da igual cómo se escriban.

**Y de ahí salen las garantías**: **todo programa Datalog termina**, y **el resultado es único** —el
menor punto fijo—, independientemente de la estrategia de evaluación. Eso es lo que Prolog no puede
prometer.

Durante los ochenta y noventa fue sobre todo académico. **Y desde 2010 ha vuelto con fuerza**, por
una razón muy concreta: **es el lenguaje ideal para el análisis de programas** — donde las preguntas
son relaciones recursivas sobre grafos enormes.

## 🏭 Dónde vive hoy

- **Análisis estático de programas**: **Soufflé** (Oracle Labs) y **Doop** analizan millones de líneas
  de Java o C++ expresando el análisis de punteros y de flujo **como reglas Datalog** (clase 150).
- **Seguridad**: **CodeQL** de GitHub —el motor de análisis de vulnerabilidades— usa un lenguaje de
  consulta con raíces en Datalog, y **Semmle**, su antecesor, era Datalog puro.
- **Bases de datos**: **Datomic** —del autor de [Clojure](clojure.md)— usa Datalog como lenguaje de
  consulta; también **XTDB** y **LogicBlox**.
- **Redes y configuración en la nube**: verificación de reglas de acceso y de topologías.
- **Y en investigación**, como base de sistemas de razonamiento incremental.

## 🧠 Lo que enseña: recursión sin recorrido

Este es el ejemplo canónico, y explica el paradigma entero:

```prolog
% HECHOS: lo que se sabe
padre(ana, luis).
padre(luis, marta).
padre(marta, jorge).

% REGLAS: lo que se deriva
ancestro(X, Y) :- padre(X, Y).
ancestro(X, Y) :- padre(X, Z), ancestro(Z, Y).    % ← recursiva
```

**Y con eso, `ancestro(ana, jorge)` es cierto** — sin escribir un bucle, sin una pila y sin decidir si
se recorre en anchura o en profundidad.

**El motor calcula el punto fijo**: aplica las reglas una y otra vez hasta que no se derivan hechos
nuevos. Y como no hay funciones, **el conjunto de hechos posibles es finito**, así que **termina
siempre**.

Y la comparación con los otros dos lenguajes declarativos del Atlas es lo más instructivo de esta
ficha:

| | [Prolog](prolog.md) | **Datalog** | [SQL](sql.md) |
|---|---|---|---|
| Recursión | sí | **sí, y termina** | sí, con `WITH RECURSIVE` |
| ¿Termina siempre? | **no** | **sí** | sí |
| ¿Importa el orden? | **sí** | **no** | no |
| Evaluación | descendente, con vuelta atrás | **ascendente, punto fijo** | plan del optimizador |
| Funciones y términos | sí | **no** | limitado |
| Optimizable como consulta | difícil | **sí** | sí |

**Y la fila de la terminación es la que justifica el lenguaje**: **en análisis de programas se
ejecutan reglas sobre grafos de millones de nodos**, y no poder garantizar que el análisis termina lo
haría inservible.

Y hay una segunda propiedad, muy práctica, que explica su vuelta: **el mantenimiento incremental**.

```text
Si cambia un hecho, NO hay que recalcularlo todo:
el motor propaga solo lo que se ve afectado.
```

**Eso es lo que permite que un análisis de código se actualice al guardar un fichero** en lugar de
tardar minutos, y es lo que hace viable a CodeQL y a los motores de reglas modernos.

## 🔄 Lo que se ha modernizado

- **Soufflé**: compila Datalog **a C++ paralelo**, con estructuras de datos especializadas — Datalog
  con rendimiento industrial.
- **Motores incrementales**: **Differential Dataflow** y **DDlog** recalculan solo lo afectado.
- **Extensiones prácticas**: agregados, negación estratificada y tipos, que amplían el lenguaje sin
  perder las garantías.
- **Datalog embebido**: en [Racket](racket.md) (`#lang datalog`), en Clojure (Datomic, Datascript) y
  como biblioteca en varios lenguajes (clase 163).
- **Y su influencia en SQL**: `WITH RECURSIVE` (SQL:1999) es, esencialmente, **Datalog dentro de SQL**.

## ⚙️ Cómo se ejecuta hoy

```bash
souffle -F hechos/ -D salida/ analisis.dl      # Soufflé: compila y ejecuta
racket -e '(require datalog)'                   # dentro de Racket
# Y en Datomic o XTDB, como lenguaje de consulta de la base de datos
```

## 🧪 El programa de la clase 041 en Datalog

Es la versión que aparece en el `primos.md` de la clase 041, y es un **contrato adaptado**
(clase 040): **Datalog puro no tiene entrada, salida ni aritmética general**.

```prolog
% Datalog puro no tiene E/S: se declaran los hechos y la regla que deriva el total.
venta(15000, 2, 0.10).

total(T) :- venta(P, C, D), T = P * C * (1 - D).
```

**Lo que hay que ver, y es lo más interesante de la ficha.**

- **No hay programa, hay una base de conocimiento.** El hecho `venta(...)` es un dato; la regla
  `total(T)` **declara qué significa el total**, y el motor lo deriva. **Nadie llama a nada.**
- **`T = P * C * (1 - D)` es una extensión**, no Datalog puro: **el Datalog original no tiene
  aritmética**, precisamente porque las funciones romperían la garantía de finitud. Las
  implementaciones prácticas la añaden con cuidado, y **declararlo es más honesto que fingir**
  (clase 040).
- **La coma es conjunción**, como en [Prolog](prolog.md).
- **Y no hay orden**: da igual escribir la regla antes o después del hecho, y da igual el orden de los
  literales dentro de la regla. **Esa independencia es exactamente la garantía que Prolog no tiene** —
  y es la razón de que Datalog se pueda optimizar como una consulta [SQL](sql.md).

## 📚 Fuentes y bibliografía

- [Soufflé](https://souffle-lang.github.io/) — el motor moderno; su documentación es la mejor
  introducción práctica.
- **Serge Abiteboul, Richard Hull, Victor Vianu**, *Foundations of Databases* — libre en línea; los
  capítulos de Datalog son la referencia teórica.
- [What You Always Wanted to Know About Datalog (And Never Dared to Ask)](https://ieeexplore.ieee.org/document/43410)
  — Ceri, Gottlob y Tanca (1989); el artículo divulgativo clásico.
- **Yannis Smaragdakis, Martin Bravenboer**, *Using Datalog for Fast and Easy Program Analysis* — por
  qué el análisis de programas encontró aquí su lenguaje.
- [Documentación de Datomic](https://docs.datomic.com/query/query-data-reference.html) — Datalog como
  lenguaje de consulta de una base de datos real.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Prolog](prolog.md) · [SQL](sql.md) · [Clojure](clojure.md) · [Racket](racket.md)
