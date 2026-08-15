# 🔤 BASIC — 1964

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

BASIC se diseñó con un objetivo que ningún otro lenguaje de este Atlas tuvo: **que lo pudiera usar un
estudiante de historia**. Y lo consiguió tanto que durante los años ochenta **venía grabado en la ROM
de casi todos los ordenadores domésticos del mundo** — al encenderlos, lo primero que aparecía era un
intérprete de BASIC esperando.

> **🎯 Por qué está en este programa**
>
> BASIC es un **primo de la familia históricos / shell** ([Atlas](README.md#historicos-shell)), y es
> el antepasado de dos fichas de este Atlas: [VBA](vba.md) y [VB.NET](vbnet.md).
>
> Aporta al programa una idea que el curso defiende desde varios ángulos: **la accesibilidad es una
> decisión de diseño con consecuencias**. Y aporta el contraste histórico con la clase 083 —**el
> `GOTO` y por qué la programación estructurada tuvo que imponerse**—, que es difícil de entender sin
> ver de dónde veníamos.

| | |
|---|---|
| **Año** | **1 de mayo de 1964**, a las 4 de la madrugada, en Dartmouth |
| **Autoría** | **John G. Kemeny** y **Thomas E. Kurtz**, Dartmouth College |
| **Familia** | Históricos; con influencia de [FORTRAN](fortran.md) y ALGOL |
| **Paradigma** | Imperativo; estructurado a partir de los años ochenta |
| **Tipado** | Dinámico o estático según el dialecto; con sufijos (`$`, `%`, `!`) |
| **Memoria** | Automática; sin punteros en los dialectos clásicos |
| **Ejecución** | Interpretado —lo habitual— o compilado (QuickBASIC, PowerBASIC) |
| **Estado** | 🟡 **Histórico**, con descendientes muy vivos: [VBA](vba.md) y [VB.NET](vbnet.md) |

---

## 📜 Historia

En 1963, **John Kemeny** y **Thomas Kurtz**, matemáticos de Dartmouth, tenían una convicción poco
compartida: **que todos los estudiantes —no solo los de ciencias— deberían saber usar un ordenador**.

El problema era que programar entonces significaba **[FORTRAN](fortran.md) o ensamblador**, con
tarjetas perforadas y un turno de días. Así que hicieron dos cosas a la vez:

1. **El Sistema de Tiempo Compartido de Dartmouth**, para que varias personas usaran el ordenador
   simultáneamente desde teletipos.
2. **BASIC** —*Beginner's All-purpose Symbolic Instruction Code*—, un lenguaje que se pudiera aprender
   en una tarde.

**El primer programa BASIC se ejecutó el 1 de mayo de 1964**, y en pocos años **más del 80 % de los
estudiantes de Dartmouth sabía programar** — una cifra que no se ha vuelto a alcanzar en ninguna
universidad generalista.

Y los autores tomaron una decisión que merece recordarse: **lo pusieron en el dominio público**, sin
licencia ni restricciones, porque su objetivo era que se extendiera.

**Se extendió.** En 1975, **Bill Gates y Paul Allen** escribieron **Altair BASIC** — el primer producto
de Microsoft. Y en los años ochenta, **BASIC venía en la ROM** del Commodore 64, el ZX Spectrum, el
Apple II, el Amstrad CPC y el MSX.

> **Eso significa que una generación entera aprendió a programar encendiendo el ordenador y
> escribiendo.** No había que instalar nada, ni configurar nada, ni elegir nada: el ordenador
> arrancaba en un lenguaje de programación. Es una propiedad que se perdió y que muchos consideran
> una pérdida real.

**Y también recibió la crítica más famosa que ha recibido un lenguaje**: **Edsger Dijkstra** escribió
en 1975 que *"es prácticamente imposible enseñar buena programación a estudiantes que han estado
expuestos a BASIC: como programadores potenciales, están mentalmente mutilados sin esperanza de
regeneración."*

**Era una exageración polémica y señalaba algo real**: el BASIC de la época **tenía números de línea y
`GOTO`, y no tenía funciones con parámetros locales ni bloques**. Se programaba con saltos, y eso
producía lo que se llamó **código espagueti** (clase 083).

**Y el propio Kurtz estuvo de acuerdo**: en 1984 diseñó **True BASIC**, estructurado y sin números de
línea. **QuickBASIC (1985)** hizo lo mismo en el mundo Microsoft, con procedimientos, tipos definidos
por el usuario y un compilador de verdad.

## 🏭 Dónde vive hoy

- **Como [VBA](vba.md)**: en Excel, Access y Office — probablemente **el lenguaje con más usuarios
  activos del mundo** que no se consideran programadores.
- **Como [VB.NET](vbnet.md)**: aplicaciones de empresa en mantenimiento.
- **FreeBASIC, QB64 y PureBasic**: dialectos modernos, con comunidades pequeñas y activas.
- **Retroinformática y educación**: emuladores del C64 y del Spectrum, y proyectos como el BBC micro:bit
  que recuperan la idea del ordenador que arranca programable.
- **Y en sistemas industriales heredados**, con dialectos propios de cada fabricante.

## 🧠 Lo que enseña: la programación estructurada, vista desde antes

Este es el BASIC que Dijkstra criticaba, y **merece verlo para entender la clase 083**:

```basic
10 INPUT "Precio, cantidad, descuento"; P, C, D
20 IF P <= 0 THEN GOTO 60
30 LET T = P * C * (1 - D)
40 PRINT "Total: "; T
50 GOTO 70
60 PRINT "Precio no válido"
70 END
```

**Los números de línea y el `GOTO` son el problema** (clase 083): con veinte líneas se lee; con dos
mil, **el flujo de control es un grafo que nadie puede seguir**, y **no hay ámbitos**: todas las
variables son globales (clase 087).

**Y la respuesta fue la programación estructurada**, que Böhm y Jacopini habían demostrado suficiente
en 1966 —**secuencia, selección e iteración bastan para cualquier programa**— y que Dijkstra defendió
en *Go To Statement Considered Harmful*.

Y el mismo programa en BASIC moderno **es otro lenguaje**:

```freebasic
Dim As Double p, c, d
Input "", p, c, d

If p <= 0 Then
    Print "Precio no valido"
Else
    Print Using "Total: ##.##"; p * c * (1 - d)
End If
```

**Sin números de línea, con bloques, con tipos declarados y con `End If`.** Es exactamente la
transición que [Fortran](fortran.md) hizo con el formato libre y que [RPG](rpg.md) hizo con el formato
totalmente libre (clase 146) — **el mismo lenguaje, después de aprender**.

Y la lección que queda es de la clase 175: **casi ninguna decisión antigua fue estúpida cuando se
tomó**. Los números de línea eran **el editor**: sin pantalla ni ratón, escribir `25 PRINT X`
insertaba una línea entre la 20 y la 30. **Era una solución a un problema real que dejó de existir.**

## 🔄 Lo que quedó

- **La idea de que el ordenador debe ser programable por su usuario**, que sobrevive en las hojas de
  cálculo (clase 163) y en proyectos educativos.
- **El REPL como forma de aprender**: escribir una línea y ver el resultado (clase 124).
- **[VBA](vba.md) y [VB.NET](vbnet.md)**, que son descendientes directos.
- **Y `Print Using`**, cuya idea de formato por plantilla llegó hasta [COBOL](cobol.md) y las
  imágenes de edición.

## ⚙️ Cómo se ejecuta hoy

```bash
fbc main.bas && ./main            # FreeBASIC: compila a nativo
qb64pe -x main.bas                 # QB64 Phoenix Edition
bwbasic main.bas                    # Bywater BASIC, el clásico de GNU
# Y en el navegador: emuladores de C64 y de ZX Spectrum
```

## 🧪 El programa de la clase 041 en BASIC

Esta versión se escribe aquí y **no está verificada en CI** (clase 040). Está en **FreeBASIC**,
estructurado.

```freebasic
Dim As Double precio, cantidad, descuento, total

Input "", precio, cantidad, descuento

total = precio * cantidad * (1 - descuento)

Print "Total: " & Format(total, "0.00")
```

**Lo que hay que ver.**

- **`Dim As Double`** declara el tipo — algo que el BASIC clásico no exigía, y que los dialectos
  modernos recomiendan siempre (`Option Explicit`), por la misma razón que `implicit none` en
  [Fortran](fortran.md) y `use strict` en [Perl](perl.md) (clase 137): **sin declaración, un nombre
  mal escrito crea una variable nueva**.
- **`&` concatena**, como en [VB.NET](vbnet.md) — y por el mismo motivo: **evitar la ambigüedad de
  `+`** entre suma y concatenación (clase 100).
- **Las palabras en lugar de símbolos** —`Dim`, `Print`, `Input`, `End If`— son la herencia de la
  ficha: **legibilidad para quien empieza**, y la razón por la que se eligió el nombre "Beginner's".
- **Y no hay números de línea**, que es la diferencia entera entre el BASIC que Dijkstra criticó y
  este.

## 📚 Fuentes y bibliografía

- **Kemeny y Kurtz**, *Back to BASIC: The History, Corruption, and Future of the Language* (1985) —
  los autores explicando qué querían y qué creen que se estropeó por el camino.
- **Edsger Dijkstra**, *Go To Statement Considered Harmful* (1968) y *How do we tell truths that might
  hurt?* (1975) — la crítica; corta y polémica.
- **Böhm y Jacopini** (1966) — el teorema que demuestra que secuencia, selección e iteración bastan
  (clase 083).
- [FreeBASIC](https://www.freebasic.net/) y [QB64 Phoenix](https://qb64phoenix.com/) — los dialectos
  vivos.
- **Dartmouth**, [*BASIC at 50*](https://www.dartmouth.edu/basicfifty/) — archivo histórico con el
  contexto del sistema de tiempo compartido.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [VBA](vba.md) · [VB.NET](vbnet.md) · [Pascal](pascal.md) · [Fortran](fortran.md)
