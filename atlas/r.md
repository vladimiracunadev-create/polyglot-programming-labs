# 📊 R — 1993

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

R no es un lenguaje de programación de propósito general al que se le añadió estadística: **es
estadística a la que se le añadió un lenguaje**. Esa inversión explica todo lo que resulta raro al
llegar de otro sitio — y también por qué sigue siendo insustituible en su terreno.

> **🎯 Por qué está en este programa**
>
> R es un **primo de la familia de scripting dinámico** ([Atlas](README.md#scripting-dinamico)),
> cuyos representantes en el núcleo son [Python](python.md) y [PHP](php.md).
>
> Aporta al programa la **programación vectorizada**: en R, la unidad de trabajo **no es el valor,
> es el vector**, y casi ningún programa lleva bucles
> ([clase 089](../classes/parte-6-datos-y-estructuras/089-arreglos-y-vectores/README.md)). Es la misma
> idea que [APL](apl.md), [J](j.md), [Fortran](fortran.md) moderno y NumPy, y quien la entiende aquí
> la reconoce en los cuatro.

| | |
|---|---|
| **Año** | 1993; **1.0** en 2000; el *tidyverse* a partir de 2014 |
| **Autoría** | **Ross Ihaka** y **Robert Gentleman**, Universidad de Auckland — de ahí las dos erres |
| **Familia** | Scripting dinámico / array; implementación libre de **S** (Bell Labs, 1976) |
| **Paradigma** | Funcional y vectorizado; con varios sistemas de objetos (S3, S4, R5, R7) |
| **Tipado** | **Dinámico**, con vectores tipados y coerción automática |
| **Memoria** | Recolección de basura; **copia al modificar** |
| **Ejecución** | Interpretado, con partes críticas en C y [Fortran](fortran.md) |
| **Estado** | 🟢 **Estándar** en estadística, bioinformática e investigación académica |

---

## 📜 Historia

En **1976**, **John Chambers** creó **S** en los Laboratorios Bell —los mismos de
[C](c.md) y Unix— para que los estadísticos pudieran analizar datos de forma interactiva sin escribir
[Fortran](fortran.md). S se comercializó como S-PLUS y era caro.

En **1993**, **Ross Ihaka** y **Robert Gentleman**, en Auckland, escribieron una implementación libre
compatible con S. La llamaron **R** por sus dos nombres y por el juego con la letra anterior.

La decisión que lo hizo despegar fue **CRAN (1997)**: un archivo central de paquetes **con pruebas
automáticas y revisión antes de publicar**. Es la misma idea de [CPAN](perl.md) (clase 143), con una
diferencia importante: **CRAN comprueba que cada paquete construya y pase sus pruebas en varias
plataformas antes de aceptarlo**, y avisa al autor cuando un cambio en otro paquete lo rompe. Es
integración continua a escala de ecosistema (clase 147).

Y en **2014** llegó el segundo cambio: **el *tidyverse*** de Hadley Wickham —`dplyr`, `ggplot2`,
`tidyr`— que **redefinió el estilo del lenguaje** hacia canalizaciones legibles y una gramática de
gráficos. Hoy hay, de hecho, **dos dialectos de R**: el base y el tidy, y conviene saberlo al leer
código ajeno.

## 🏭 Dónde vive hoy

- **Estadística académica**: es el idioma común de la investigación cuantitativa.
- **Bioinformática y genómica**: **Bioconductor** es un ecosistema entero de miles de paquetes.
- **Farmacéutica y ensayos clínicos**: R está aceptado por las agencias reguladoras para análisis de
  ensayos, con validación documentada.
- **Análisis y visualización**: **ggplot2** sigue siendo la mejor biblioteca de gráficos estadísticos
  que existe, y **Shiny** permite publicar análisis como aplicaciones web.
- **Informes reproducibles**: **R Markdown** y **Quarto** mezclan texto, código y resultados —
  la respuesta directa a la deuda de reproducibilidad de la clase 154.

## 🧠 Lo que enseña: pensar en vectores

Este es el cambio mental que R produce y que se transfiere a NumPy, a
[Julia](julia.md), a [MATLAB](matlab.md) y al [Fortran](fortran.md) moderno:

```r
x <- c(1, 2, 3, 4, 5)
y <- x * 2 + 1           # ← se opera sobre TODO el vector. Sin bucle.
mean(x[x > 2])            # filtrar con un vector lógico, y agregar
```

**No hay bucle porque no hace falta.** La operación se define sobre el vector entero, y por debajo se
ejecuta en C o Fortran (clase 155). Un bucle explícito en R **es lento y es señal de que hay una forma
mejor** — lo contrario de lo que enseña casi cualquier otro lenguaje de esta lista.

Y hay tres rarezas de R que merecen explicación porque desconciertan a quien llega:

**Una, los índices empiezan en 1**, como [Fortran](fortran.md), [MATLAB](matlab.md), [Lua](lua.md) y
[Julia](julia.md) — y a diferencia de casi todos los demás. Es una convención de las matemáticas, no
un error.

**Dos, la evaluación perezosa de los argumentos.** R **no evalúa un argumento hasta que se usa**, y
—más raro todavía— **una función puede ver la expresión que le pasaron, no solo su valor**:

```r
graficar <- function(x) plot(x, main = deparse(substitute(x)))
graficar(altura_pacientes)   # el título sale "altura_pacientes"
```

**Eso es evaluación no estándar**, y es la magia que hace posible que `dplyr` escriba
`filter(datos, edad > 30)` sin comillas. Es potentísimo y es la razón de que el código R sea difícil
de analizar (clase 150).

**Y tres, la copia al modificar**: los argumentos se comportan como si se copiaran, así que **una
función no puede modificar el objeto de quien la llama** (clase 081). Eso da seguridad y cuesta
memoria, y el intérprete optimiza el caso común evitando copias reales.

## 🔄 Lo que se ha modernizado

- **El *tidyverse*** y el operador de canalización, hoy también nativo: `datos |> filter(...) |>
  summarise(...)`.
- **Quarto**: la evolución de R Markdown, que además publica desde Python y Julia — informes con
  código ejecutable y salida versionable (clase 154).
- **`data.table` y `arrow`**: rendimiento de nivel industrial sobre conjuntos grandes.
- **`renv` y `pak`**: entornos y dependencias reproducibles por proyecto, con fichero de bloqueo
  (clase 143) — un problema que R tuvo mal resuelto durante años.
- **`Rcpp` y `extendr`**: escribir las partes críticas en [C++](cpp.md) o en [Rust](rust.md) e
  integrarlas sin fricción (clase 156).

## ⚙️ Cómo se ejecuta hoy

```bash
Rscript main.R < entrada.txt        # el comando de la clase 041
R -q -e 'sessionInfo()'

R -e 'renv::restore()'               # entorno reproducible (clase 143)
R -e 'devtools::test()'               # pruebas con testthat (clase 139)
quarto render informe.qmd             # informe reproducible
```

## 🧪 El programa de la clase 041 en R

```r
v <- as.numeric(strsplit(readLines("stdin", n = 1), " ")[[1]])
total <- v[1] * v[2] * (1 - v[3])
cat(sprintf("Total: %.2f\n", total))
```

**Lo que hay que ver, y es lo que delata al lenguaje.**

- **No hay tres variables: hay un vector `v` de tres elementos.** Todas las demás fichas de la clase
  041 declaran `precio`, `cantidad` y `descuento`; R trata la línea como **un objeto vectorial** y
  accede por posición. **Ese reflejo es el lenguaje entero.**
- **`v[1]` es el primero**, no el segundo (clase 089).
- **`<-` es la asignación idiomática**, aunque `=` funcione. Es herencia de S y de los teclados APL
  que tenían una tecla con la flecha.
- **`[[1]]` frente a `[1]`**: `strsplit` devuelve **una lista de vectores** —porque podría partir
  varias cadenas a la vez—, y `[[1]]` saca el primer elemento **desenvuelto**. La distinción entre
  `[` y `[[` es una de las primeras cosas que hay que entender en R (clase 099).
- **`as.numeric` convierte el vector entero de golpe**, no elemento a elemento. Otra vez: la unidad es
  el vector.

## 📚 Fuentes y bibliografía

- [R for Data Science](https://r4ds.hadley.nz/) — **Hadley Wickham** y Garrett Grolemund; libre en
  línea, y el punto de entrada estándar al R moderno.
- [Advanced R](https://adv-r.hadley.nz/) — el mismo autor; **el libro que explica el lenguaje por
  dentro**: entornos, evaluación no estándar y los sistemas de objetos. Imprescindible para las
  clases 087, 088 y 122.
- [CRAN Task Views](https://cran.r-project.org/web/views/) — el mapa de paquetes por dominio.
- **W. N. Venables, B. D. Ripley**, *Modern Applied Statistics with S* — el clásico, todavía útil.
- [Bioconductor](https://www.bioconductor.org/) — el ecosistema de bioinformática, con su propio ciclo
  de publicación.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Python](python.md) · [Julia](julia.md) · [MATLAB](matlab.md) · [APL](apl.md) ·
[Fortran](fortran.md)
