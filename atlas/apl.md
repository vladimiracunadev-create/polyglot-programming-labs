# 🔣 APL — 1966

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

APL es el lenguaje más raro de este Atlas y uno de los más influyentes: **usa un alfabeto propio de
símbolos matemáticos**, necesitaba un teclado especial, y **cada símbolo es una operación sobre
arreglos completos**. Un programa APL de una línea puede hacer lo que en otro lenguaje son treinta —y
esa densidad es a la vez su virtud y la razón de su marginalidad.

> **🎯 Por qué está en este programa**
>
> APL es un **primo de la familia array / científica** ([Atlas](README.md#array-cientifica)), que no
> tiene representante en el núcleo — su influencia llega al curso por [R](r.md), NumPy,
> [Julia](julia.md), [MATLAB](matlab.md) y el [Fortran](fortran.md) moderno.
>
> Aporta al programa **la programación por arreglos en su forma original y más pura**
> ([clase 089](../classes/parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md)): el
> pensamiento sin bucles, con operadores que se combinan. Es el antepasado directo de todo lo
> vectorizado que se hace hoy.

| | |
|---|---|
| **Año** | 1966 (implementado); la notación es de **1957-1962** |
| **Autoría** | **Kenneth E. Iverson**, Harvard e IBM — **Premio Turing 1979** |
| **Familia** | Array / científica |
| **Paradigma** | **Funcional y por arreglos**, con operadores de orden superior |
| **Tipado** | Dinámico; **todo es un arreglo** —un escalar es un arreglo de rango 0— |
| **Memoria** | Recolección de basura |
| **Ejecución** | Interpretado, con primitivas muy optimizadas |
| **Estado** | 🟡 **Vivo en nichos**: finanzas, actuarial y seguros; comunidad pequeña y activa |

---

## 📜 Historia

**Kenneth Iverson** no diseñó APL como lenguaje de programación: lo diseñó **como notación matemática
para describir algoritmos**, y lo publicó en 1962 en un libro cuyo título es literalmente
*A Programming Language* — de donde sale el acrónimo.

Durante años fue **una notación en papel** para enseñar y para describir arquitecturas. **IBM la usó
para especificar formalmente el System/360**, antes de que existiera un intérprete.

En **1966**, IBM implementó **APL\360**, y ocurrió algo inesperado: el sistema de tiempo compartido
con APL se convirtió en una herramienta de análisis de negocio. **Actuarios, financieros y analistas
—no programadores— empezaron a usarlo directamente**, porque una operación sobre una tabla entera se
escribía en una línea.

**Iverson recibió el Premio Turing en 1979**, y su conferencia —*Notation as a Tool of Thought*— es
uno de los mejores textos que se han escrito sobre por qué la notación importa: **una buena notación
no solo expresa las ideas, ayuda a tenerlas**.

Después Iverson diseñó **[J](j.md)** (1990), que conserva la semántica y **sustituye los símbolos por
ASCII** — resolviendo el problema del teclado a costa de la legibilidad.

## 🏭 Dónde vive hoy

- **Servicios financieros y seguros**: modelos actuariales, valoración de carteras y sistemas de
  riesgo, sobre todo con **Dyalog APL**.
- **Análisis de datos** en organizaciones que lo adoptaron y nunca se fueron.
- **[Kdb+/q](https://kx.com/)**, un descendiente de APL que es **el estándar de facto en datos de
  series temporales financieras de alta frecuencia** — probablemente el uso comercial más valioso de
  la familia.
- **Y como comunidad viva**: Dyalog, GNU APL y APL de código abierto tienen usuarios activos y
  competiciones anuales.

## 🧠 Lo que enseña: notación como herramienta de pensamiento

El ejemplo clásico. **Esto calcula la media de un vector:**

```apl
(+/x) ÷ ≢x
```

Y se lee: **la suma acumulada (`+/`) de `x`, dividida entre la cuenta (`≢`) de `x`**.

Y este es el ejemplo más famoso — **la criba de Eratóstenes en una línea**:

```apl
(~R∊R∘.×R)/R←1↓⍳N
```

**Dos ideas hacen posible esa densidad**, y las dos están en todos los lenguajes vectorizados de hoy:

**Una, los operadores actúan sobre estructuras completas.** No hay bucles porque no hacen falta:
`+/` es la reducción, `∘.×` es el producto exterior, `⍳` genera un rango.

**Y dos, los operadores se combinan.** `/` no es una función: es un **operador de orden superior** que
recibe una función y devuelve otra. `+/` es "reducir con suma", `×/` es "reducir con producto",
`⌈/` es "el máximo". **Es `fold` de la clase 115**, veinte años antes de que la programación funcional
lo popularizara.

> **Y el precio hay que decirlo, porque define su historia**: **APL es de escritura rápida y de
> lectura lentísima**. Un programa denso es difícil de revisar (clase 146), y su fama de "lenguaje de
> solo escritura" —merecida a medias— junto con **la necesidad de un teclado especial** lo dejaron
> fuera de la corriente principal.
>
> **Y aun así ganó**: la idea sobrevivió sin los símbolos. **Cuando alguien escribe
> `np.sum(a * b, axis=0)` o `datos |> filtrar |> resumir`, está pensando como Iverson** (clase 089).

## 🔄 Lo que se ha modernizado

- **Dyalog APL**: la implementación comercial de referencia, con objetos, interfaz con .NET y Python,
  y hoy con licencia gratuita para uso personal y educativo.
- **Símbolos sin teclado especial**: los editores modernos insertan los caracteres con prefijos, y el
  teclado dejó de ser una barrera.
- **[J](j.md)** y **[q/kdb+](https://kx.com/)** como descendientes en ASCII.
- **BQN y Uiua**: lenguajes de arreglos de diseño reciente, que revisan la notación con lo aprendido
  en sesenta años.
- **Y la vuelta de las ideas**: `einsum`, la difusión de formas (*broadcasting*) de NumPy y las
  operaciones de arreglo de [Fortran](fortran.md) y [Julia](julia.md) son APL con otra ropa.

## ⚙️ Cómo se ejecuta hoy

```bash
apl --script main.apl          # GNU APL
dyalog -script main.apls        # Dyalog
# Y en el navegador: tryapl.org, sin instalar nada
```

## 🧪 El programa de la clase 041 en APL

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```apl
⍝ Leer la línea, convertirla en tres números y calcular el total
v ← ⍎⍞                          ⍝ ⍞ lee una línea; ⍎ la evalúa como expresión APL
total ← (v[1] × v[2]) × 1 - v[3]
⍝ Y con la reducción, sin índices:
total ← (×/ 2↑v) × 1 - ⊃⌽v
⎕ ← 'Total: ', ⍕2 ⍕ total
```

**Lo que hay que ver, y es lo más didáctico de la ficha.**

- **`×/ 2↑v`** dice: **toma los dos primeros (`2↑`) y redúcelos con el producto (`×/`)**. Es
  `precio × cantidad` **sin nombrar ninguno de los dos** — la operación se define sobre la estructura,
  no sobre los elementos.
- **`⊃⌽v`** es "el primero (`⊃`) de la inversa (`⌽`)", es decir, **el último elemento**. En APL se
  combinan operaciones simples en lugar de tener una función `last`.
- **Los índices empiezan en 1** por defecto —y es configurable con `⎕IO`—, como
  [R](r.md), [Fortran](fortran.md), [Julia](julia.md) y [MATLAB](matlab.md).
- **`⍝` es el comentario**, y `⎕ ←` es la salida.
- **Y la comparación con las otras diecinueve versiones de la clase 041 es el contenido**: todas
  declaran tres variables; **APL declara un vector y opera sobre él**. Es exactamente el mismo reflejo
  que delata a [R](r.md) en su ficha, y viene del mismo sitio.

## 📚 Fuentes y bibliografía

- **Kenneth Iverson**, *Notation as a Tool of Thought* (Turing Award Lecture, 1979) — libre en línea;
  **léelo aunque no vayas a tocar APL nunca**: es de los mejores textos sobre notación y pensamiento.
- [TryAPL](https://tryapl.org/) — probarlo en el navegador, con teclado en pantalla.
- [Dyalog Documentation Centre](https://docs.dyalog.com/) — manuales y el libro *Mastering Dyalog APL*
  (libre en PDF).
- [APL Wiki](https://aplwiki.com/) — historia, dialectos y comparativas.
- **Kenneth Iverson**, *A Programming Language* (1962) — el libro original, que era una notación antes
  que un lenguaje.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [J](j.md) · [R](r.md) · [Julia](julia.md) · [MATLAB](matlab.md) ·
[Fortran](fortran.md)
