# ➗ J — 1990

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

J es **[APL](apl.md) escrito con el teclado que ya tienes**: el mismo Kenneth Iverson, veinticuatro
años después, sustituyó los símbolos matemáticos por combinaciones de caracteres ASCII. Resolvió el
problema del teclado y creó otro — porque `+/ % #` es tan denso como `+/ ÷ ≢` y bastante menos
evocador.

> **🎯 Por qué está en este programa**
>
> J es un **primo de la familia array / científica** ([Atlas](README.md#array-cientifica)), junto a
> [APL](apl.md), [R](r.md), [Julia](julia.md), [MATLAB](matlab.md) y [Fortran](fortran.md).
>
> Aporta al programa **la programación tácita** —componer funciones **sin nombrar los argumentos**—,
> que es una idea que solo esta familia y [Haskell](haskell.md) llevan al extremo
> ([clase 115](../classes/parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md)).
> Y aporta un caso de estudio de la clase 175: **qué se gana y qué se pierde al cambiar la notación de
> un lenguaje**.

| | |
|---|---|
| **Año** | 1990; libre (GPL) desde 2011 |
| **Autoría** | **Kenneth E. Iverson** y **Roger Hui** — el mismo autor de APL |
| **Familia** | Array / científica; sucesor directo de APL |
| **Paradigma** | **Funcional y por arreglos**, con programación **tácita** |
| **Tipado** | Dinámico; **todo es un arreglo**, con rango y forma |
| **Memoria** | Recolección de basura |
| **Ejecución** | Interpretado, con un núcleo en C muy compacto |
| **Estado** | 🟡 **Nicho pequeño y estable**; finanzas, análisis y comunidad de entusiastas |

---

## 📜 Historia

**Kenneth Iverson** tenía casi setenta años cuando, en 1989, se propuso rehacer [APL](apl.md) con lo
aprendido en treinta años. Le acompañó **Roger Hui**, y el diseño se publicó en **1990**.

Los objetivos eran tres, y merecen conocerse porque son decisiones de diseño puras:

1. **Solo caracteres ASCII**: nada de teclados especiales ni de fuentes raras.
2. **Un modelo de arreglos más regular** que el de APL, con reglas de rango uniformes.
3. **Y hacer de primera clase la programación tácita**, que en APL existía y estaba poco desarrollada.

La sustitución de símbolos siguió un patrón sistemático: **una letra o un símbolo, opcionalmente
seguido de un punto o de dos puntos**, forma un verbo. Así, `#` es la cuenta, `#.` es la conversión de
base, `#:` es la representación en base.

**Y aquí está la lección de la clase 175**: **el cambio resolvió un problema real y no trajo la
adopción**. Quien ya usaba APL prefería sus símbolos —cada uno tenía forma propia y era reconocible—,
y quien no lo usaba **seguía viendo una línea de puntuación indescifrable**.

**J es libre desde 2011**, y su comunidad es pequeña y muy dedicada.

## 🏭 Dónde vive hoy

- **Análisis financiero y actuarial**, en organizaciones de la órbita APL.
- **Análisis exploratorio de datos** por quien viene de la tradición de arreglos.
- **Enseñanza de la programación por arreglos**, por ser libre y no necesitar teclado especial.
- **Y como referencia de diseño**: **BQN** y **Uiua**, los lenguajes de arreglos recientes, parten de
  las lecciones de J tanto como de las de APL.

## 🧠 Lo que enseña: la programación tácita

Esta es la aportación, y es genuinamente distinta de todo lo demás del Atlas.

**La media aritmética, en J:**

```j
media =: +/ % #
```

**Y hay que leerlo con cuidado, porque no hay ningún argumento escrito**: `+/` es "sumar todo", `#` es
"contar", y `%` es dividir. **La expresión `+/ % #` es un *fork*: aplica `+/` y `#` al mismo argumento
y combina los resultados con `%`.**

```j
   media 1 2 3 4 5
3
```

**Nunca se nombró el vector.** Eso es la **programación tácita** —o *point-free*—: **se compone la
función, no se describe el cálculo sobre valores**.

Y la comparación con [Haskell](haskell.md) es directa:

```haskell
media = (/) <$> sum <*> (fromIntegral . length)   -- lo mismo, y más largo
```

**J tiene una gramática para esto**: los **trenes** de dos y tres verbos —*hook* y *fork*— tienen
reglas de composición definidas en el lenguaje, no son una biblioteca.

**Y el segundo concepto es el rango**, que es más regular que en APL:

```j
   suma =: +/
   suma"1 tabla       NB. aplicar a cada FILA (rango 1)
   suma"2 tabla        NB. aplicar a cada MATRIZ (rango 2)
```

**`"n` declara sobre qué nivel de la estructura actúa el verbo.** Es una forma explícita y uniforme de
lo que NumPy llama `axis=` y [R](r.md) resuelve con la familia `apply` — y en J es parte de la
gramática.

> **Y el compromiso es el de la clase 154**: **el código tácito es extraordinariamente conciso y
> difícil de leer para quien no está entrenado**. J es probablemente el lenguaje de este Atlas con la
> curva más pronunciada, y quien la sube dice —de forma bastante unánime— que le cambió la manera de
> pensar en datos.

## 🔄 Estado actual

- **Libre desde 2011** (GPL), con versiones regulares; **J9** es la actual.
- **JQt y Jupyter**: entornos gráficos y cuadernos, que hacen la exploración mucho más accesible.
- **`jd`**: una base de datos columnar sobre J, en la línea de kdb+.
- **Y el linaje continúa**: **BQN** (Marshall Lochbaum, 2020) toma de J la regularidad del rango y
  vuelve a los símbolos; **Uiua** (2023) combina arreglos con una pila.

## ⚙️ Cómo se ejecuta hoy

```bash
jconsole main.ijs < entrada.txt       # consola de J
ijconsole -js "echo +/ 1 2 3"          # una expresión suelta
# Y jqt para el entorno gráfico, o el núcleo de Jupyter
```

## 🧪 El programa de la clase 041 en J

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```j
NB. Leer la línea, convertirla a números y calcular el total
v =: ".  1!:1 [ 3           NB. 1!:1[3 lee la entrada estándar; ". la convierte
total =: (*/ 2 {. v) * 1 - {: v

NB. Y la versión tácita, sin nombrar el vector:
total2 =: 3 : '(*/ 2 {. y) * 1 - {: y'

echo 'Total: ' , (8j2 ": total)
```

**Lo que hay que ver.**

- **`*/ 2 {. v`** es exactamente lo mismo que `×/ 2↑v` en [APL](apl.md): **toma los dos primeros y
  redúcelos con el producto**. La correspondencia símbolo a símbolo entre los dos lenguajes es directa,
  y comparar las dos fichas enseña la traducción.
- **`{: v` es el último elemento**, donde APL usaba `⊃⌽v`.
- **`8j2 ": total`** formatea con 8 posiciones y 2 decimales: `":` es el verbo de formato, y `8j2`
  es su argumento izquierdo. **Es `%.2f` con otra gramática.**
- **`1!:1` es una llamada al sistema** por número — la interfaz de entrada y salida de J, que es
  deliberadamente austera.
- **Y `3 : '...'` define un verbo explícito**, con `y` como argumento derecho. **La existencia de dos
  estilos —tácito y explícito— es la seña de identidad del lenguaje**, y la elección entre ellos es la
  decisión de legibilidad de la clase 146.

## 📚 Fuentes y bibliografía

- [jsoftware.com](https://www.jsoftware.com/) — descarga, documentación y el *J Primer*.
- [Learning J](https://www.jsoftware.com/help/learning/contents.htm) — **Roger Stokes**; libre y el
  camino recomendado.
- [J Wiki](https://code.jsoftware.com/wiki/Main_Page) — ensayos, recetas y la explicación de los
  trenes.
- **Kenneth Iverson**, *J Introduction and Dictionary* — el diccionario del lenguaje, que es
  literalmente un diccionario: cada símbolo con su definición.
- [BQN](https://mlochbaum.github.io/BQN/) — para ver hacia dónde ha ido el diseño de lenguajes de
  arreglos después de J.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [APL](apl.md) · [R](r.md) · [Haskell](haskell.md) · [Julia](julia.md) ·
[MATLAB](matlab.md)
