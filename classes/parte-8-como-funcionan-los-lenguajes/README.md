# Parte 8 — Cómo funcionan los lenguajes

> [⏮️ Parte 7](../parte-7-paradigmas/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 9](../parte-9-ingenieria-de-software-poliglota/README.md)

**16 clases** · rango 123–138 · clases de **código** · nivel intermedio · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Lo que ocurre bajo el código: compilación, memoria, concurrencia y por qué falla lo que falla.**

---

## 🧭 De qué trata esta parte

Esta es la parte que convierte la explicación en comprensión. Todo lo estudiado hasta aquí —tipos, funciones, estructuras, paradigmas— descansa sobre un conjunto de mecanismos concretos: un pipeline de compilación, una pila, un heap, una estrategia para liberar memoria y un modelo de ejecución concurrente.

El recorrido baja por capas. Primero el viaje del texto a la acción y las tres respuestas —compilador, intérprete, JIT— con su comparación AOT/JIT. Después, dónde viven los datos: pila, heap y las referencias que los alcanzan. Luego, las **tres respuestas a «quién libera la memoria»**: manual en C, recolector en Java o Go, y propiedad con préstamos en Rust y C++, comparadas por fin en el mismo sitio.

El tramo final es la concurrencia vista desde abajo: por qué `cuenta += 1` no es atómico, qué son las corrutinas y los canales, cómo el modelo de actores elimina lo compartido y por qué el código que escribes no es el que se ejecuta. Cierra con el diagnóstico: clasificar un error por la fase en que nace y depurar en cada runtime.

## 🎒 Qué necesitas traer

Las Partes 5 y 6, en particular propiedad y ciclo de vida (103), paso de parámetros (079–081) y la Parte 7 para la concurrencia (121–122).

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Situar cualquier mensaje de error en la fase del pipeline donde nace.
2. Explicar la diferencia práctica entre AOT y JIT en arranque, rendimiento y tamaño.
3. Decir qué vive en la pila y qué en el heap para un programa dado, en cada lenguaje.
4. Comparar gestión manual, recolector y propiedad nombrando qué garantiza y qué cuesta cada uno.
5. Reproducir una condición de carrera y explicar por qué la reordenación la hace posible.
6. Depurar con el instrumental nativo de cada runtime en lugar de a base de imprimir.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Del texto a la acción · clases 123–126

El pipeline de compilación y las tres formas de ejecutar lo que produce.

- **[123 · Del código a la ejecución: fases de compilación](123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md)** — Toda ejecución arranca con el mismo viaje: texto plano → tokens → árbol sintáctico → análisis semántico → código. Conocer las fases convierte cada mensaje de error en una coordenada del pipeline, no en un misterio.
- **[124 · Compilador, intérprete y JIT](124-compilador-interprete-y-jit/README.md)** — Qué se hace con el árbol después: compilar a máquina, interpretar directamente o compilar en caliente con un **JIT**. Estas tres respuestas explican la mayoría de las diferencias de rendimiento y de arranque entre lenguajes.
- **[125 · Bytecode y máquinas virtuales (JVM, CLR, V8)](125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md)** — `javac` no produce código de máquina sino **bytecode** para una máquina virtual imaginaria. JVM, CLR y V8 comparten esa idea, y con ella la portabilidad, el JIT y las herramientas de introspección que la acompañan.
- **[126 · AOT vs. JIT: costos y beneficios](126-aot-vs-jit-costos-y-beneficios/README.md)** — **AOT** frente a **JIT**, cara a cara: el compromiso entre tiempo de arranque, rendimiento sostenido, tamaño del artefacto y capacidad de optimizar con información de ejecución. Es una decisión de ingeniería que se paga en cada despliegue.

### 🔹 Dónde viven los datos · clases 127–129

Pila, marco de llamada, heap y las referencias que lo enlazan todo.

- **[127 · La pila (stack) y el marco de llamada](127-la-pila-stack-y-el-marco-de-llamada/README.md)** — Toda función llamada necesita recordar sus datos locales y a dónde volver. La **pila de llamadas** y su marco lo hacen posible — y explican el desbordamiento de pila, el coste de la recursión profunda y el contenido de un stack trace.
- **[128 · El heap y la asignación dinámica](128-el-heap-y-la-asignacion-dinamica/README.md)** — El **heap** es donde viven los datos cuyo tamaño o vida no se conocen al compilar. Más flexible que la pila y bastante más caro: cada asignación implica buscar espacio y cada olvido implica una fuga.
- **[129 · Referencias, apuntadores y direcciones](129-referencias-apuntadores-y-direcciones/README.md)** — A los datos del heap se accede *a través* de algo que dice dónde están: dirección, puntero o referencia. Distinguir esos tres términos —y el aritmético puntero de C de la referencia segura de Java— desactiva media docena de confusiones.

### 🔹 Las tres respuestas a «quién libera» · clases 130–132

Manual, recolector y propiedad: el mismo problema con tres contratos incompatibles.

- **[130 · Gestión manual de memoria (C): malloc/free](130-gestion-manual-de-memoria-c-malloc-free/README.md)** — En C el contrato es explícito: cada `malloc` exitoso exige un `free`. De ahí salen las fugas, el *use-after-free* y el *double free*, tres fallos que aquí se ven provocados a propósito para reconocerlos después.
- **[131 · Recolección de basura (GC)](131-recoleccion-de-basura-gc/README.md)** — El **recolector de basura** invierte la pregunta: en vez de «¿cuándo puedo liberar esto?», el runtime averigua qué ya no es alcanzable. Cómodo y no gratuito: pausas, memoria extra y comportamiento difícil de predecir bajo carga.
- **[132 · RAII, propiedad y préstamos (Rust/C++)](132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md)** — La tercera vía: **RAII** en C++ y **propiedad con préstamos** en Rust liberan de forma determinista sin recolector, moviendo la comprobación al compilador. Es el punto donde las tres respuestas de la parte quedan comparables lado a lado.

### 🔹 Hacer varias cosas a la vez · clases 133–136

Memoria compartida, corrutinas y canales, actores y el modelo de memoria.

- **[133 · Concurrencia: procesos, hilos y memoria compartida](133-concurrencia-procesos-hilos-y-memoria-compartida/README.md)** — `cuenta += 1` no es atómico: son tres pasos, y en cuanto dos hilos los intercalan aparece la **condición de carrera**. Aquí se ve el problema real de la memoria compartida antes de estudiar cualquier solución.
- **[134 · Tareas, corrutinas y canales](134-tareas-corrutinas-y-canales/README.md)** — Los hilos del sistema operativo son caros y limitados. **Corrutinas**, tareas y canales permiten decenas de miles de unidades concurrentes ligeras — goroutines de Go, `async` de Rust — con un modelo mental distinto del hilo clásico.
- **[135 · Actores y paso de mensajes (modelo BEAM)](135-actores-y-paso-de-mensajes-modelo-beam/README.md)** — El modelo de **actores** elimina lo compartido: procesos aislados que solo se comunican por mensajes, con supervisión y reinicio. El BEAM de Erlang/Elixir muestra que la tolerancia a fallos puede ser una propiedad del lenguaje.
- **[136 · El modelo de memoria y las condiciones de carrera](136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md)** — Una idea incómoda: **el código que escribes no es el código que se ejecuta**. Compilador y CPU reordenan, y en un programa multihilo eso es observable. Aquí entran el modelo de memoria, la visibilidad y por qué `volatile` no es lo que parece.

### 🔹 Cuando algo falla · clases 137–138

Clasificar el error por su fase y diagnosticarlo con las herramientas del runtime.

- **[137 · Errores: de sintaxis, de tipos, de enlace y de ejecución](137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md)** — Un error no es solo un mensaje: es una **coordenada** en el pipeline de la clase 123. De sintaxis, de tipos, de enlace o de ejecución — saber en qué fase nace cada uno reduce el diagnóstico a la mitad.
- **[138 · Depuración: cómo se diagnostica en cada runtime](138-depuracion-como-se-diagnostica-en-cada-runtime/README.md)** — Cierra la parte devolviendo todo a la práctica: depurar es cerrar la distancia entre tu modelo mental del programa y lo que el programa realmente hace, con las herramientas que cada runtime ofrece para mirar dentro.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «El recolector de basura evita las fugas de memoria.» | Evita las clásicas, no las lógicas: una referencia viva que ya no necesitas es una fuga que el GC nunca recogerá. |
| «Rust es seguro porque no deja hacer cosas.» | Es seguro porque mueve una comprobación que en C hace el programador —y a veces olvida— al compilador. |
| «Si el código es correcto, no hay condiciones de carrera.» | Compilador y CPU reordenan. Sin sincronización explícita, «correcto» leído de arriba abajo no significa correcto al ejecutarse. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

## 🔗 Qué abre esta parte

Entendida la máquina, la Parte 9 se ocupa de la otra mitad del oficio: construir software que otras personas puedan mantener.

---

> [⏮️ Parte 7](../parte-7-paradigmas/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 9](../parte-9-ingenieria-de-software-poliglota/README.md)
