# 🧭 Rutas por perfil

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md) · [📅 Syllabus](../docs/syllabus.md) · [🎓 Examen final por perfil](../docs/examen-final-por-perfil.md)

El programa es **secuencial** (001→176) y esa sigue siendo la forma recomendada de estudiarlo: cada
clase asume la anterior y el orden no es decorativo. Pero si llegas con experiencia previa, no
necesitas el mismo tiempo en todo. Estas cinco rutas responden a una pregunta concreta: **¿qué de lo
que ya sabes se transfiere, y qué te va a resultar genuinamente nuevo?**

## Cómo funciona una ruta

Una ruta **no recorta el programa**: reordena el esfuerzo. Todas comparten tres reglas:

1. **La [Parte 0](../classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) no se salta nunca.** Fija el método de comparación (sintáctico / semántico / paradigmático) sin el cual las demás partes se leen como una lista de curiosidades.
2. **Las partes «de foco» se estudian completas**, con las diez implementaciones y el verificador ejecutado. Son donde está tu hueco real.
3. **El resto se lee**, sin ejecutar cada implementación, y se vuelve a ellas cuando hagan falta. El [índice](../classes/README.md) permite saltar a cualquier clase por número.

Cada ruta cierra con su [examen final por perfil](../docs/examen-final-por-perfil.md), que combina
teoría, una transferencia verificada con el `casos.json` y una explicación escrita.

---

## 🐍 «Vengo de Python o de lenguajes dinámicos»

**Lo que ya traes:** modelar problemas, estructuras de datos de alto nivel, comprensiones, funciones
de primera clase y un ecosistema de paquetes. Buena parte de las Partes 4 y 6 te resultarán
familiares en el fondo aunque cambie la forma.

**Lo que te va a costar:** que el compilador te exija cosas antes de ejecutar, que la memoria tenga
dueño y que un entero tenga tamaño. El salto no es sintáctico: es que aparecen garantías que en
Python no existían y errores que ocurrían en ejecución y ahora ocurren al compilar.

**Foco (estudia completas):**

- [Parte 3 — Valores, tipos y variables](../classes/parte-3-valores-tipos-y-variables/README.md) · tipado estático vs. dinámico, inferencia, nulabilidad y desbordamiento.
- [Parte 5 — Funciones y modularidad](../classes/parte-5-funciones-y-modularidad/README.md) · paso por valor y referencia, genéricos, y el modelo de propiedad de Rust (081).
- [Parte 8 — Cómo funcionan los lenguajes](../classes/parte-8-como-funcionan-los-lenguajes/README.md) · pila y heap, GC frente a propiedad, y por qué tu lenguaje te ahorraba todo eso.

**Primera clase recomendada tras la Parte 0:** [050 · Tipado estático vs. dinámico](../classes/parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md).

---

## ⚙️ «Quiero sistemas (C / Rust)»

**Lo que ya traes:** si vienes de lenguajes con recolector, traes diseño y estructuras; si vienes de
C, traes el modelo de memoria pero probablemente no las alternativas modernas a la gestión manual.

**Lo que te va a costar:** la disciplina de propiedad y préstamos, y aceptar que el compilador
rechaza programas que «funcionarían». La clave está en ver las **tres** respuestas al problema de
liberar memoria una al lado de la otra, no solo la que usa tu lenguaje.

**Foco (estudia completas):**

- [Parte 2 — Toolchains y comandos](../classes/parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md) · compilar, enlazar, construir artefactos.
- [Parte 6 — Datos y estructuras](../classes/parte-6-datos-y-estructuras/README.md) · propiedad y ciclo de vida (103), copia frente a referencia (102).
- [Parte 8 — Cómo funcionan los lenguajes](../classes/parte-8-como-funcionan-los-lenguajes/README.md) · la parte central de esta ruta: pila, heap, `malloc`/`free`, GC, RAII y préstamos.
- [Parte 10 — Interoperabilidad](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) · FFI, ABI y bindings: donde C es el idioma franco de todos.

**Primera clase recomendada tras la Parte 0:** [127 · La pila (stack) y el marco de llamada](../classes/parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md).

---

## 🌐 «Web (JavaScript / TypeScript)»

**Lo que ya traes:** asincronía, eventos, cierres y un modelo de objetos flexible. Las Partes 4 y 7
tocan cosas que usas a diario sin haberles puesto nombre.

**Lo que te va a costar:** los tipos como garantía y no como anotación opcional, y el hecho de que
el modelo de prototipos que usas por debajo no es el de la mayoría de lenguajes. También la memoria:
nunca la administraste y en la Parte 8 se explica quién lo hacía por ti.

**Foco (estudia completas):**

- [Parte 3 — Valores, tipos y variables](../classes/parte-3-valores-tipos-y-variables/README.md) · el tipado estructural de TypeScript frente al nominal de Java o C#, y la coerción de JS (049, 051).
- [Parte 7 — Paradigmas](../classes/parte-7-paradigmas/README.md) · prototipos (113), eventos (119), reactivo (120) y `async`/`await` (122).
- [Parte 10 — Interoperabilidad](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) · contratos de API (160) y WebAssembly (162).

**Primera clase recomendada tras la Parte 0:** [113 · OO basado en prototipos (JavaScript)](../classes/parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md).

---

## 🏢 «Backend de empresa (Java / C# / Go)»

**Lo que ya traes:** tipos estáticos, interfaces, pruebas, CI y despliegue. Gran parte de la Parte 9
la reconocerás; lo nuevo será verla comparada entre diez toolchains en vez de en el tuyo.

**Lo que te va a costar:** los paradigmas que tu stack no favorece —funcional de verdad, declarativo
más allá del ORM, lógico— y la concurrencia sin memoria compartida (canales de Go, actores del BEAM).

**Foco (estudia completas):**

- [Parte 5 — Funciones y modularidad](../classes/parte-5-funciones-y-modularidad/README.md) · visibilidad, contratos y genéricos comparados (078, 087).
- [Parte 7 — Paradigmas](../classes/parte-7-paradigmas/README.md) · interfaces y traits (112), funcional (114–116), concurrencia (121–122).
- [Parte 9 — Ingeniería de software políglota](../classes/parte-9-ingenieria-de-software-poliglota/README.md) · CI multi-lenguaje, refactorización, patrones comparados y perfilado.

**Primera clase recomendada tras la Parte 0:** [112 · Interfaces, traits y clases abstractas](../classes/parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md).

---

## 🗃️ «Datos (SQL)»

**Lo que ya traes:** pensamiento declarativo, conjuntos y una intuición fuerte sobre coste de
consulta. Eres quien mejor entenderá la Parte 7 cuando llegue a lo declarativo y lo lógico.

**Lo que te va a costar:** el control de flujo imperativo y el estado mutable, que en SQL casi no
existen. También la vida de los datos fuera de la base: serialización, formatos y persistencia.

**Foco (estudia completas):**

- [Parte 4 — Control del programa](../classes/parte-4-control-del-programa/README.md) · lo imperativo que SQL te ahorró: bucles, condicionales y errores.
- [Parte 6 — Datos y estructuras](../classes/parte-6-datos-y-estructuras/README.md) · mapas, registros, JSON y persistencia (105, 106).
- [Parte 7 — Paradigmas](../classes/parte-7-paradigmas/README.md) · declarativo (117) y lógico (118): tu terreno, explicado desde fuera.

**Primera clase recomendada tras la Parte 0:** [117 · Declarativo: consultas y transformación (SQL)](../classes/parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md).

---

## Si no te reconoces en ninguna

Entonces la ruta es el programa entero en orden, que es para lo que fue diseñado: **~406 h en ~41
semanas** a diez horas semanales, según el [cronograma](../docs/syllabus.md). Empieza por la
[clase 001](../classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/001-que-es-programar-y-por-que-comparar-lenguajes-la-tesis-poliglota/README.md)
y no te saltes nada: el orden global es el mismo argumento contado de principio a fin.
