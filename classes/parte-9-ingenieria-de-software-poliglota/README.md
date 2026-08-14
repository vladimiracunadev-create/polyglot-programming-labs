# Parte 9 — Ingeniería de software políglota

> [⏮️ Parte 8](../parte-8-como-funcionan-los-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 10](../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md)

**16 clases** · rango 139–154 · clases de **código** · nivel avanzado · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Que funcione, que se construya igual siempre, que llegue a producción y que se pueda cambiar.**

---

## 🧭 De qué trata esta parte

Escribir código que funciona hoy en tu máquina es la parte fácil. Esta parte trata todo lo demás: pruebas, depuración, observabilidad, dependencias, builds reproducibles, control de versiones, revisión, CI, despliegue, diseño, refactorización, patrones, rendimiento, seguridad y deuda técnica — cada práctica comparada entre los diez lenguajes.

El hilo conductor es la evidencia. Cada práctica responde a una pregunta comprobable: ¿cómo sé que funciona? ¿cómo sé que la build de hoy es la de ayer? ¿cómo sé qué está pasando en producción? ¿cómo sé que este refactor no rompió nada? Las herramientas cambian de nombre en cada lenguaje; las preguntas no.

El repositorio que estás leyendo es su propio caso de estudio: el verificador de equivalencia es literalmente una prueba de integración entre diez lenguajes, y su CI orquesta siete toolchains. Cuando la clase 147 habla de integración continua multi-lenguaje, habla de un problema que este repo tuvo que resolver de verdad.

## 🎒 Qué necesitas traer

Las Partes 2 y 5–8. Las herramientas de la Parte 2 (pruebas, paquetes, formateadores) se dan aquí por instaladas y comprendidas.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Escribir pruebas unitarias y de integración en los diez lenguajes del núcleo.
2. Diagnosticar con depurador y con registro estructurado, y saber cuándo toca cada uno.
3. Fijar dependencias con lockfile y explicar por qué una build sin ellos no es reproducible.
4. Montar una CI que valide varios lenguajes en paralelo sin duplicar la lógica.
5. Refactorizar apoyándote en pruebas y argumentar por qué el comportamiento no cambió.
6. Perfilar antes de optimizar y defender la decisión con datos en vez de con intuición.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Comprobar que funciona · clases 139–142

Pruebas unitarias y de integración, depuradores y observabilidad en producción.

- **[139 · Pruebas unitarias por lenguaje](139-pruebas-unitarias-por-lenguaje/README.md)** — Una **prueba unitaria** ejerce un trozo de código y afirma que el resultado observado es el esperado. Modesto de enunciar y la pieza que sostiene todo lo demás: sin ella, refactorizar es apostar.
- **[140 · Pruebas de integración y el verificador de equivalencia](140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md)** — La prueba de **integración** mira qué ocurre cuando las partes se encuentran. En este curso hay un ejemplo poco común y muy literal: el verificador de equivalencia es una prueba de integración entre diez lenguajes.
- **[141 · Depuradores: gdb, lldb, pdb y los de IDE](141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md)** — El **depurador** congela un programa vivo y te deja mirar dentro: puntos de ruptura, inspección de variables, ejecución paso a paso. `gdb`, `lldb`, `pdb` y los de IDE cambian de comandos, no de modelo mental.
- **[142 · Registro (logging) y observabilidad](142-registro-logging-y-observabilidad/README.md)** — En producción no puedes pausar nada: tu única ventana es lo que el sistema haya decidido contar de sí mismo. Registro estructurado, niveles, trazas y métricas — y la diferencia entre registrar y observar.

### 🔹 Que se construya igual siempre · clases 143–145

Dependencias con lockfile, builds reproducibles y control de versiones políglota.

- **[143 · Dependencias, versiones y lockfiles](143-dependencias-versiones-y-lockfiles/README.md)** — Ningún proyecto serio se sostiene solo con el código propio. Versionado semántico, resolución y **lockfile**: sin fijar versiones exactas, «funciona» es una afirmación sobre hoy y sobre esta máquina.
- **[144 · Compilación reproducible y empaquetado](144-compilacion-reproducible-y-empaquetado/README.md)** — Entre el fuente y el artefacto de producción media la *build*. Que sea **reproducible** —mismo fuente, mismo resultado, byte a byte— es lo que permite auditar qué se está ejecutando realmente.
- **[145 · Git y control de versiones para proyectos políglotas](145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md)** — Git aplicado a un repositorio con siete lenguajes: qué se versiona y qué no, cómo se organizan los artefactos de compilación de cada toolchain y por qué el historial es documentación de las decisiones, no solo respaldo.

### 🔹 Que llegue a producción · clases 146–148

Revisión de código, integración continua multi-lenguaje, entrega y despliegue.

- **[146 · Revisión de código y estándares](146-revision-de-codigo-y-estandares/README.md)** — Los datos de McConnell sobre inspecciones de código son contundentes: revisar a conciencia detecta una fracción enorme de los defectos, más barata que cualquier otra fase. Aquí se ve qué mirar y cómo dar la crítica.
- **[147 · Integración continua (CI) multi-lenguaje](147-integracion-continua-ci-multi-lenguaje/README.md)** — La **integración continua** nace de una observación incómoda: cuanto más tarda un cambio en fundirse con el trabajo de los demás, más caro es integrarlo. En un repo políglota hay que orquestar además siete toolchains.
- **[148 · Entrega y despliegue](148-entrega-y-despliegue/README.md)** — Separar **entrega** de **despliegue**: que un artefacto esté listo no obliga a ponerlo delante de los usuarios hoy. Estrategias, reversión y por qué desplegar debería ser aburrido.

### 🔹 Que se pueda cambiar · clases 149–151

Diseño y arquitectura, refactorización segura y patrones comparados entre lenguajes.

- **[149 · Diseño y arquitectura comparada](149-diseno-y-arquitectura-comparada/README.md)** — El **diseño** reparte el sistema en piezas y define cómo se hablan; la **arquitectura** es ese diseño a la escala más alta. Comparar cómo distintos lenguajes empujan hacia estilos distintos evita copiar arquitecturas fuera de contexto.
- **[150 · Refactorización segura](150-refactorizacion-segura/README.md)** — Refactorizar es **cambiar la estructura interna sin alterar el comportamiento observable**. Las dos mitades de la definición importan: sin pruebas que sostengan la segunda, no estás refactorizando, estás reescribiendo con los ojos cerrados.
- **[151 · Patrones de diseño comparados entre lenguajes](151-patrones-de-diseno-comparados-entre-lenguajes/README.md)** — Los patrones del *GoF* no son leyes: son soluciones recurrentes en un contexto. Compararlos entre lenguajes revela que varios patrones clásicos son andamios para suplir algo que otro lenguaje ya trae de serie.

### 🔹 Que aguante · clases 152–154

Rendimiento medido, seguridad desde la primera línea y deuda técnica gestionada.

- **[152 · Rendimiento y perfilado (profiling)](152-rendimiento-y-perfilado-profiling/README.md)** — «Measure, don't guess». La intuición sobre rendimiento es sistemáticamente mala; el perfilado la sustituye por datos y casi siempre señala un lugar distinto al que habrías optimizado.
- **[153 · Seguridad: entradas, memoria y dependencias](153-seguridad-entradas-memoria-y-dependencias/README.md)** — La seguridad no es una capa final sino una postura desde la primera línea: validar toda entrada externa, tratar la memoria con cuidado en los lenguajes que lo exigen y vigilar la cadena de dependencias.
- **[154 · Mantenibilidad, documentación y deuda técnica](154-mantenibilidad-documentacion-y-deuda-tecnica/README.md)** — El software se lee, se modifica y se reescribe durante años. Documentación que envejece bien, y **deuda técnica** entendida como lo que es: una decisión de financiación, no un pecado.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Las pruebas son para proyectos grandes.» | Son lo que permite cambiar el código sin miedo. En un proyecto pequeño el miedo simplemente se nota antes. |
| «Refactorizar es mejorar el código.» | Es cambiar la estructura **sin alterar el comportamiento observable**. Si el comportamiento cambia, es otra cosa y necesita otras precauciones. |
| «Optimizo esto que se ve lento.» | «Measure, don't guess»: el perfilador casi siempre señala un sitio distinto al que habrías tocado. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

## 🔗 Qué abre esta parte

Con el oficio cubierto, la Parte 10 aborda lo que ningún curso de un solo lenguaje puede enseñar: qué ocurre en la frontera entre dos.

---

> [⏮️ Parte 8](../parte-8-como-funcionan-los-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 10](../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md)
