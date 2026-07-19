# Clase 018 — Familia scripting dinámico: Python, Ruby, Perl, PHP, Lua

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia de los lenguajes **dinámicos**: interpretados, sin declaración obligatoria de tipos, diseñados para que un humano escriba una solución en minutos en vez de horas. Python y PHP están en el núcleo del curso; Ruby, Perl y Lua son sus primos cercanos. Todos comparten una misma apuesta de diseño —poner al programador por delante de la máquina— pero cada uno con un acento distinto: la claridad de Python, la felicidad del desarrollador en Ruby, el poder textual de Perl, la web en PHP y la ligereza embebible de Lua.

Esto importa porque esta familia es donde casi todo el mundo empieza y donde se hace una parte enorme del trabajo real: automatización, análisis de datos, prototipos, backends web y scripting de sistemas. Sebesta traza su linaje hasta Perl y los shells de Unix, y Tate, en *Seven Languages in Seven Weeks*, dedica capítulos a Ruby y a otros dinámicos precisamente porque su expresividad enseña a pensar en programas más cortos. Entender qué comparten te permite saltar de uno a otro reconociendo el 80% al vuelo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué comparte esta familia (tipado dinámico pero fuerte, interpretación, poca ceremonia).
2. Distinguir el acento de cada miembro (claridad, felicidad del dev, texto, web, embebido).
3. Diferenciar tipado **dinámico** de tipado **débil**, dos ejes independientes.
4. Reconocer código de un primo apoyándote en Python o PHP.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Rasgos comunes | Tipado dinámico, interpretado, poca ceremonia |
| 2 | Python y PHP | Los representantes del núcleo: claridad y web |
| 3 | Ruby, Perl, Lua | Felicidad del dev, procesamiento de texto, embebido |
| 4 | Dinámico ≠ débil | Dos ejes de tipado que se confunden |
| 5 | Cuándo brillan y cuándo no | Prototipos y scripting vs. núcleos críticos |

## 📖 Definiciones y características

El rasgo que une a esta familia es el **tipado dinámico**: el tipo de un valor se conoce y comprueba en tiempo de ejecución, no de compilación, y una variable puede apuntar sucesivamente a un número, un texto o una lista. Esto elimina la "ceremonia" —declaraciones, anotaciones, recompilaciones— y permite escribir y probar ideas casi tan rápido como se piensan. El segundo rasgo es que son **interpretados** (o compilados a un bytecode que corre en una máquina virtual ligera), lo que da un ciclo de edición-ejecución inmediato, ideal para explorar. El precio es rendimiento: al no conocer los tipos por adelantado, el intérprete hace más trabajo en cada operación. Sebesta encuadra a estos lenguajes como "scripting languages" cuya prioridad histórica fue pegar programas y automatizar tareas, no exprimir la CPU.

Cada miembro nació de una necesidad y conserva su carácter. **Perl** (Larry Wall, 1987) fue el rey del procesamiento de texto y las expresiones regulares en la era de la administración de sistemas Unix; su lema, "hay más de una forma de hacerlo" (TMTOWTDI), celebra la flexibilidad hasta el punto de la ilegibilidad. **Python** (Guido van Rossum, 1991) reaccionó con la filosofía opuesta —"debería haber una forma obvia de hacerlo", recogida en el *Zen de Python*—, apostando por la legibilidad y la indentación significativa; hoy es el lenguaje más usado para enseñar y para ciencia de datos. **Ruby** (Yukihiro "Matz" Matsumoto, 1995) puso como meta explícita la "felicidad del programador": bloques, todo-es-un-objeto y metaprogramación potente, que Rails llevó al mundo web. **PHP** (Rasmus Lerdorf, 1994) nació incrustado en HTML para hacer páginas dinámicas y, pese a su historia caótica, sus versiones modernas (8.x) son un lenguaje sólido con tipos opcionales. **Lua** (PUC-Rio, Brasil, 1993) eligió lo contrario del maximalismo: minimalismo radical, una sola estructura de datos (la tabla) y un intérprete diminuto pensado para embeberse en juegos y sistemas.

La confusión más frecuente sobre esta familia es equiparar **dinámico** con **débil**. Son ejes independientes. El tipado dinámico dice *cuándo* se comprueban los tipos (en ejecución); el tipado débil dice *cuánto* el lenguaje convierte tipos entre sí sin quejarse. Python es dinámico pero **fuerte**: `"3" + 5` es un error, no un `"35"` ni un `8`. JavaScript, en cambio, es dinámico y más débil: `"3" + 5` da `"35"`. Van Roy y Haridi recomiendan pensar el tipado como un espectro de garantías, no como un interruptor, y esta familia es el mejor sitio para ver los dos ejes actuando por separado.

- **Python** — 1991 (Guido van Rossum), prioriza la legibilidad. Clave: núcleo del curso; el más usado en enseñanza y datos.
- **Ruby** — 1995 (Matz), diseñado para la felicidad del programador. Clave: bloques y metaprogramación; base de Rails.
- **Perl** — 1987 (Larry Wall), rey del texto y las regex. Clave: "hay más de una forma de hacerlo".
- **PHP** — 1994 (Lerdorf), nacido para la web incrustado en HTML. Clave: núcleo del curso; moderno y con tipos opcionales desde la 8.x.
- **Lua** — 1993 (PUC-Rio), minimalista y embebible. Clave: tablas como única estructura; scripting de juegos y sistemas.

## 🧩 Situación

Un equipo necesita renombrar diez mil archivos siguiendo un patrón antes de una migración. Nadie propone escribirlo en C: se resuelve en diez líneas de Python durante el café. Esa inmediatez —de la idea al resultado sin declarar tipos, compilar ni gestionar memoria— es la razón de ser de toda la familia dinámica. Pero el mismo equipo, cuando meses después el servicio que procesa millones de peticiones por segundo se queda corto de rendimiento, reescribe el núcleo caliente en Go o Rust y deja Python para el pegamento. Saber cuándo brilla cada familia es parte del oficio.

## 🔎 Ejemplo

Un saludo con interpolación de una variable revela el aire de familia: todos dinámicos, sin declarar tipos, con sintaxis distinta para lo mismo.

```text
Python:  nombre = "Ada"; print(f"Hola, {nombre}")
Ruby:    nombre = "Ada"; puts "Hola, #{nombre}"
PHP:     $nombre = "Ada"; echo "Hola, $nombre";
Perl:    my $nombre = "Ada"; print "Hola, $nombre\n";
Lua:     nombre = "Ada"; print("Hola, " .. nombre)
```

El **delta** entre primos es puramente cosmético: `f"{x}"` en Python, `#{x}` en Ruby, el `$` que marca variable en PHP y Perl, el `..` de concatenación en Lua. Ninguna declara el tipo de `nombre`; todas lo infieren en ejecución. Si conoces uno, lees los otros casi sin esfuerzo: eso es exactamente lo que significa "pertenecer a una familia".

## ✍️ Práctica

Compara la interpolación de cadenas en Python (`f"{x}"`), Ruby (`#{x}`) y PHP (`"$x"`). ¿De qué **clase** de diferencia se trata: sintáctica, semántica o paradigmática? Luego intenta lo contrario: escribe `"3" + 5` mentalmente en Python y en JavaScript y predice el resultado de cada uno. ¿Qué eje de tipado explica la diferencia?

## ⚠️ Errores comunes

- **Creer que "dinámico" significa "sin reglas"** → causa: confundir tipado dinámico con débil → solución: recordar que Python es dinámico pero fuerte: no suma texto y número sin protestar.
- **Usar la familia dinámica para todo** → causa: ignorar su coste en rendimiento → solución: reservarla para scripting, prototipos y pegamento; llevar los núcleos críticos a lenguajes compilados.
- **Portar un dinámico a otro cambiando solo la sintaxis** → causa: asumir semántica idéntica → solución: verificar diferencias reales (verdad de valores, copia vs. referencia, orden de evaluación).

## ❓ Preguntas frecuentes

- **¿Python es lento?** Comparado con C o Rust, sí; pero para la inmensa mayoría de tareas su velocidad de **desarrollo** compensa de sobra, y las partes calientes se delegan a librerías en C.
- **¿Por qué PHP arrastra mala fama?** Por su historia temprana caótica e inconsistente; las versiones modernas (8.x) son un lenguaje coherente, rápido y con tipos opcionales.
- **¿Dónde se usa Lua si casi nadie lo nombra?** Embebido: motores de juegos, Redis, Neovim, routers. Su tamaño diminuto lo hace ideal como lenguaje de extensión dentro de otros programas.

## 🔗 Referencias

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 (scripting languages) y cap. 5-6 (nombres y tipos).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), cap. de Ruby.
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 017](../../parte-1-atlas-y-genealogia-de-los-lenguajes/017-familia-c-y-de-las-llaves-c-c-plus-plus-objective-c/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 019 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/019-familia-jvm-java-kotlin-scala-groovy-clojure/README.md)
