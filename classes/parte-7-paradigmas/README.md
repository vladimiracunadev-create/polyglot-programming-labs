# Parte 7 — Paradigmas

> [⏮️ Parte 6](../parte-6-datos-y-estructuras/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 8](../parte-8-como-funcionan-los-lenguajes/README.md)

**16 clases** · rango 107–122 · clases de **código** · nivel intermedio · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Los ocho estilos de resolver: qué considera cada paradigma una pieza legítima de solución.**

---

## 🧭 De qué trata esta parte

Un paradigma no es una sintaxis: es un **marco mental** que decide cómo se descompone un problema y qué cuenta como pieza válida de la solución. Por eso el mismo problema resuelto en dos paradigmas no se parece ni en la forma ni en el vocabulario, aunque produzca la misma salida — que es justo lo que el verificador de equivalencia demuestra en cada clase.

La parte recorre imperativo y estructurado, procedimental, orientado a objetos (con su variante de prototipos, que JavaScript usa por debajo), funcional en tres escalones, declarativo, lógico, orientado a eventos, reactivo, concurrente y asíncrono. Ninguno se presenta como superior: cada uno se explica por el problema que vino a resolver y por el que crea.

Es la parte donde el curso rentabiliza toda su estructura comparada: ver la misma tarea como objetos, como composición de funciones puras y como consulta declarativa es lo que convierte los paradigmas en herramientas elegibles en vez de en banderas.

## 🎒 Qué necesitas traer

Las Partes 5 y 6. Funciones de primera clase (085), cierres (083), pureza (084) y registros (099) son requisito; sin ellos lo funcional y lo OO quedan en eslóganes.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Identificar el paradigma dominante de un fragmento de código ajeno y sus consecuencias.
2. Sustituir un condicional por polimorfismo, y saber cuándo no conviene hacerlo.
3. Explicar la orientación a objetos por prototipos de JavaScript sin recurrir a la analogía de clases.
4. Componer funciones y aplicar currying para fabricar funciones nuevas en vez de duplicarlas.
5. Escribir la misma transformación en versión imperativa, funcional y declarativa (SQL).
6. Distinguir concurrencia de asincronía y elegir el modelo adecuado a un problema real.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Qué es un paradigma · clase 107

La clase que da el criterio con el que se leen las quince siguientes.

- **[107 · Qué es un paradigma y por qué importa](107-que-es-un-paradigma-y-por-que-importa/README.md)** — Un **paradigma** no es un lenguaje ni una sintaxis: es un marco mental que decide qué cuenta como una pieza legítima de la solución. Por eso el mismo problema resuelto en dos paradigmas no se parece ni en la forma ni en el vocabulario.

### 🔹 Imperativo y sus herederos · clases 108–109

El estilo más antiguo y su evolución hacia el orden: estructurado, procedimental y modular.

- **[108 · Imperativo y estructurado](108-imperativo-y-estructurado/README.md)** — El paradigma **imperativo** describe la computación como una secuencia de comandos que modifican un estado; el **estructurado** le impone tres construcciones (secuencia, selección, iteración) y prohíbe el salto arbitrario. Es la base sobre la que discuten todos los demás.
- **[109 · Procedimental y modular](109-procedimental-y-modular/README.md)** — Cuando un programa deja de caber en la cabeza, la respuesta clásica es dar nombre a las partes: **procedimientos** y **módulos**. Es el imperativo que crece y descubre que necesita fronteras internas.

### 🔹 Orientación a objetos · clases 110–113

Estado encapsulado, polimorfismo, interfaces y el modelo de prototipos de JavaScript.

- **[110 · Orientado a objetos: clases, objetos y estado](110-orientado-a-objetos-clases-objetos-y-estado/README.md)** — La orientación a objetos responde a una pregunta abierta: si el estado mutable es tan poderoso como peligroso, ¿cómo se domestica? Su respuesta es encapsularlo junto a las operaciones que lo respetan.
- **[111 · Herencia, composición y polimorfismo](111-herencia-composicion-y-polimorfismo/README.md)** — El problema que la OO resuelve de verdad no es «modelar el mundo con clases»: es **eliminar los condicionales que preguntan de qué tipo es un valor**. El polimorfismo sustituye el `if` por despacho, y la composición suele batir a la herencia.
- **[112 · Interfaces, traits y clases abstractas](112-interfaces-traits-y-clases-abstractas/README.md)** — Una **interfaz** desacopla lo que un cliente necesita de cómo alguien decide dárselo. Interfaces de Java y Go, traits de Rust y clases abstractas de C++ resuelven lo mismo con reglas distintas: nominal frente a estructural, explícito frente a implícito.
- **[113 · OO basado en prototipos (JavaScript)](113-oo-basado-en-prototipos-javascript/README.md)** — Casi todo lo que aprendiste de OO asume un modelo que JavaScript **no tiene por debajo**: no hay clases, hay **prototipos**. Entender la cadena de prototipos explica la sintaxis `class` de ES6 y por qué a veces se comporta de forma inesperada.

### 🔹 Funcional · clases 114–116

Inmutabilidad y pureza, composición y currying, y los patrones para encadenar efectos.

- **[114 · Funcional I: inmutabilidad y funciones puras](114-funcional-i-inmutabilidad-y-funciones-puras/README.md)** — La programación funcional no empieza por `map` ni por las lambdas: empieza por una decisión sobre el **estado**. Sustituir la celda que se modifica por el valor que se transforma cambia lo que se puede razonar y lo que se puede paralelizar.
- **[115 · Funcional II: composición, currying y aplicación parcial](115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md)** — Una función pura es un ladrillo; la **composición** es el cemento. Con currying y aplicación parcial se fabrican funciones nuevas a partir de las que ya tienes, en vez de escribir otra función casi igual.
- **[116 · Funcional III: functores, mónadas y efectos (visión práctica)](116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md)** — *Functor* y *mónada* arrastran fama de dificultad que aquí se desmonta con una visión práctica: son patrones para encadenar operaciones sobre valores envueltos —opcionales, resultados, listas, asincronía— sin desenvolverlos a mano en cada paso.

### 🔹 Declarativo y lógico · clases 117–118

Describir el qué en vez del cómo: SQL y el motor de inferencia de Prolog.

- **[117 · Declarativo: consultas y transformación (SQL)](117-declarativo-consultas-y-transformacion-sql/README.md)** — El paradigma **declarativo** invierte la pregunta: no «qué pasos doy» sino «qué propiedades tiene el resultado». SQL es la implementación más usada del mundo, y compararla con el bucle equivalente hace visible el trabajo que hace el optimizador.
- **[118 · Lógico: reglas, hechos y unificación (Prolog)](118-logico-reglas-hechos-y-unificacion-prolog/README.md)** — La forma más radical de lo declarativo: describir **hechos** y **reglas** y dejar que un motor de inferencia busque las soluciones por unificación y backtracking. Prolog cambia hasta lo que significa «llamar» a algo.

### 🔹 Eventos, flujos y concurrencia · clases 119–122

Cuando el control se invierte: callbacks, streams, hilos y `async`/`await`.

- **[119 · Orientado a eventos y callbacks](119-orientado-a-eventos-y-callbacks/README.md)** — En el paradigma **orientado a eventos** tu código deja de mandar: registra callbacks y espera a ser llamado. Esa inversión del control es la base de toda interfaz de usuario y de todo servidor, y explica por qué el orden de ejecución deja de leerse de arriba abajo.
- **[120 · Reactivo y flujos de datos (streams)](120-reactivo-y-flujos-de-datos-streams/README.md)** — Tratar el dato como una **corriente** que pasa por una tubería de transformaciones, en lugar de una colección que se recorre. Cambia la pregunta que le haces a los datos y permite trabajar con lo que aún no ha llegado.
- **[121 · Concurrente: hilos, tareas y canales](121-concurrente-hilos-tareas-y-canales/README.md)** — El paradigma **concurrente** rompe el supuesto de una sola línea de ejecución: hilos, tareas y canales. Aquí aparece por primera vez la necesidad de sincronizar, y con ella la clase de bugs que no se reproducen al depurar.
- **[122 · Asíncrono: async/await y promesas](122-asincrono-async-await-y-promesas/README.md)** — El asíncrono persigue lo mismo que la concurrencia —no quedarse esperando— con otra filosofía: un solo hilo que suspende y reanuda. `async`/`await` y promesas, y el famoso «color» de las funciones que contagia a todo lo que las llama.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «La programación funcional es usar `map` y lambdas.» | Empieza por una decisión sobre el estado, no por una sintaxis. Se puede escribir código imperativo lleno de lambdas. |
| «JavaScript tiene clases desde ES6.» | Tiene azúcar sintáctico sobre prototipos. La diferencia se nota en cuanto inspeccionas la cadena de prototipos. |
| «Concurrente y asíncrono son sinónimos.» | La concurrencia reparte trabajo entre líneas de ejecución; la asincronía evita esperar bloqueado, a menudo en un solo hilo. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

## 🔗 Qué abre esta parte

Vistos los estilos, la Parte 8 baja al nivel que los explica: qué hace realmente la máquina con tu código.

---

> [⏮️ Parte 6](../parte-6-datos-y-estructuras/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 8](../parte-8-como-funcionan-los-lenguajes/README.md)
