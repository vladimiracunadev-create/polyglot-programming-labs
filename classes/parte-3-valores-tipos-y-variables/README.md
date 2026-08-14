# Parte 3 — Valores, tipos y variables

> [⏮️ Parte 2](../parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 4](../parte-4-control-del-programa/README.md)

**16 clases** · rango 041–056 · clases de **código** · nivel intermedio · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **La materia prima de todo programa: cómo cada lenguaje nombra, tipa, convierte y muta un valor.**

---

## 🧭 De qué trata esta parte

Aquí empiezan las **clases de código**: cada una trae el mismo problema resuelto en los diez lenguajes del núcleo, con el código a la vista y verificado contra un `casos.json` común. La Parte 3 elige el terreno más elemental posible —valores, tipos y variables— justamente porque es donde las diferencias entre lenguajes son más profundas de lo que parecen.

El recorrido es deliberado: primero qué es un valor y qué es un nombre, luego los tipos primitivos uno por uno (con sus trampas reales: desbordamiento, punto flotante, Unicode), después los **dos ejes** con los que se clasifica cualquier sistema de tipos —estático/dinámico y fuerte/débil— y por último las tres decisiones que más consecuencias tienen: la ausencia de valor, la mutabilidad y la evaluación de expresiones.

Al terminar dispondrás del vocabulario que las ocho partes siguientes dan por sabido, y de algo más incómodo y más útil: la conciencia de que `0.1 + 0.2`, `"5" + 3` y una cadena vacía dentro de un `if` no significan lo mismo en todos los lenguajes.

## 🎒 Qué necesitas traer

Las Partes 0–2. En particular el pseudocódigo (007), el `casos.json` y el verificador (012), y tener al menos un toolchain instalado para ejecutar las implementaciones.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Distinguir literal, valor, variable y constante, y declarar cada uno en los diez lenguajes.
2. Explicar el rango, el signo y el desbordamiento de un entero, y por qué el punto flotante no es exacto.
3. Situar cualquier lenguaje en los ejes estático/dinámico y fuerte/débil, con un ejemplo que lo demuestre.
4. Elegir entre `null`, `Option` y un valor centinela sabiendo qué garantiza cada uno.
5. Predecir el resultado de una conversión implícita antes de ejecutarla.
6. Leer y escribir por entrada y salida estándar en los diez lenguajes del núcleo.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Nombres y valores · clases 041–042

Qué es un valor sin nombre y qué añade la variable: declarar, inicializar y asignar como tres actos distintos.

- **[041 · Literales, valores, variables y constantes](041-literales-valores-variables-y-constantes/README.md)** — Un valor puro —el número `27000`, la cadena `"hola"`— no tiene nombre ni domicilio: existe solo mientras alguien lo sostiene. Literal, valor, variable y constante son cuatro nociones distintas que el lenguaje cotidiano funde en una sola palabra.
- **[042 · Declaración, asignación e inicialización](042-declaracion-asignacion-e-inicializacion/README.md)** — **Declarar** es introducir un nombre en un ámbito, **inicializar** es darle su primer valor y **asignar** es cambiárselo después. Separarlos explica por qué Java se queja de una variable «posiblemente no inicializada» y Python no puede hacerlo.

### 🔹 Los tipos primitivos, uno por uno · clases 043–048

Enteros, reales, booleanos, caracteres y cadenas, cada uno con la trampa que esconde.

- **[043 · Tipos primitivos: enteros, reales, booleanos, caracteres](043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md)** — Enteros, reales, booleanos y caracteres son los átomos con los que se construye todo dato compuesto: primitivos porque el lenguaje los trae incorporados y porque suelen corresponder a algo que la CPU sabe manejar directamente.
- **[044 · Enteros: tamaño, signo, desbordamiento y bases](044-enteros-tamano-signo-desbordamiento-y-bases/README.md)** — La distinción entre **valor** y **representación**: `255`, `0xff`, `0o377` y `0b11111111` son cuatro formas de escribir un mismo número. Debajo aparecen el tamaño en bits, el signo en complemento a dos y el desbordamiento — y el hueco de C, que no tiene especificador para binario.
- **[045 · Números reales: punto flotante, precisión y decimales](045-numeros-reales-punto-flotante-precision-y-decimales/README.md)** — Un real matemático tiene infinitos vecinos infinitamente cercanos; la máquina solo tiene bits finitos. IEEE 754 explica por qué `0.1 + 0.2 != 0.3` en casi todos los lenguajes, y qué hacer con el dinero, donde ese error no es aceptable.
- **[046 · Booleanos y valores de verdad](046-booleanos-y-valores-de-verdad/README.md)** — En 1854 Boole demostró que la lógica es un álgebra de dos valores. De ahí salen las condiciones de todo programa — y la pregunta incómoda de qué considera «verdadero» cada lenguaje: `0`, la cadena vacía, la lista vacía y `null` no votan lo mismo en todas partes.
- **[047 · Caracteres, texto y Unicode](047-caracteres-texto-y-unicode/README.md)** — Toda la escritura humana que una computadora manipula es, por dentro, una sucesión de números. Unicode, punto de código, UTF-8 y la diferencia entre «carácter», «byte» y «lo que se ve en pantalla»: la fuente de los bugs más difíciles de reproducir.
- **[048 · Cadenas: representación, inmutabilidad e interpolación](048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md)** — La cadena es el tipo compuesto que más usarás y el que más decisiones de diseño esconde: mutable o inmutable, indexada por bytes o por caracteres, con o sin interpolación. Cada lenguaje eligió distinto y todos tienen su razón.

### 🔹 Los dos ejes del sistema de tipos · clases 049–052

Conversión, cuándo se comprueba, cuánto se tolera y cuánto deduce el compilador.

- **[049 · Conversión de tipos: casting explícito vs. coerción implícita](049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md)** — Los datos del mundo exterior llegan casi siempre como **texto**. Convertirlos tiene dos formas muy distintas: el **casting explícito**, que tú pides, y la **coerción implícita**, que el lenguaje hace por su cuenta — y que es donde nacen los resultados sorprendentes.
- **[050 · Tipado estático vs. dinámico](050-tipado-estatico-vs-dinamico/README.md)** — El primero de los dos grandes ejes de todo sistema de tipos: **cuándo** se comprueban. Estático es antes de ejecutar (el compilador rechaza); dinámico es durante (el programa falla en el momento). No es una jerarquía de calidad: es una elección con costes en ambos lados.
- **[051 · Tipado fuerte vs. débil](051-tipado-fuerte-vs-debil/README.md)** — El segundo eje: **cuántas** conversiones inseguras tolera el lenguaje cuando una operación recibe tipos que no encajan. Fuerte y débil no es lo mismo que estático y dinámico, y confundir los dos ejes es el error de vocabulario más repetido del campo.
- **[052 · Inferencia de tipos](052-inferencia-de-tipos/README.md)** — La **inferencia** permite no escribir el tipo sin renunciar a tenerlo: `var` en C#, `let` en Rust, `:=` en Go, `auto` en C++. El compilador lo deduce, y entender hasta dónde llega esa deducción evita tanto ruido como sorpresas.

### 🔹 Ausencia, mutación y expresión · clases 053–056

Las tres decisiones con más consecuencias, y el cierre con entrada/salida estándar.

- **[053 · Nulabilidad: null, nil, None, Option y valores ausentes](053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md)** — La ausencia de valor parece trivial hasta que tumba un servicio en producción. `null`, `nil`, `None`, `Option` y `Maybe` son respuestas distintas al mismo problema, y la diferencia entre «puede fallar» declarado en el tipo o descubierto en ejecución.
- **[054 · Mutabilidad e inmutabilidad](054-mutabilidad-e-inmutabilidad/README.md)** — Detrás de una pregunta doméstica —¿cómo construyo la cadena `1-2-3-…-n`?— se esconde una decisión profunda de diseño: si un valor puede cambiar después de creado. La inmutabilidad no es purismo funcional: es lo que hace seguro compartir un dato entre hilos.
- **[055 · Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit](055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md)** — `a + b * c` esconde más decisiones de las que parece: precedencia, asociatividad, orden de evaluación y qué ocurre si un operando tiene efectos colaterales. Aquí entran también los operadores bit a bit, que son los mismos en casi todos los lenguajes por herencia de C.
- **[056 · Entrada y salida básica: leer y escribir](056-entrada-y-salida-basica-leer-y-escribir/README.md)** — La parte cierra con lo que ha sostenido en silencio a todas las clases anteriores: leer de la entrada estándar y escribir en la salida estándar. Es el contrato exacto que hace verificable la equivalencia entre diez lenguajes.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Tipado fuerte y tipado estático son sinónimos.» | Son ejes independientes: Python es dinámico y fuerte; C es estático y relativamente débil. |
| «Los decimales fallan por un bug del lenguaje.» | Es IEEE 754, y ocurre igual en los diez. Lo que cambia es qué ofrece cada lenguaje para el dinero. |
| «Una cadena es un tipo simple.» | Es una estructura de datos con codificación, coste por operación y una decisión de mutabilidad detrás. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

## 🔗 Qué abre esta parte

Con valores que nombrar y tipar, la Parte 4 les añade lo único que falta para tener un programa: decidir y repetir.

---

> [⏮️ Parte 2](../parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 4](../parte-4-control-del-programa/README.md)
