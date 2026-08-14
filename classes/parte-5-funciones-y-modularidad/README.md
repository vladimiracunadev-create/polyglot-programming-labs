# Parte 5 — Funciones y modularidad

> [⏮️ Parte 4](../parte-4-control-del-programa/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 6](../parte-6-datos-y-estructuras/README.md)

**16 clases** · rango 073–088 · clases de **código** · nivel intermedio · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **La función como contrato: firma, paso de parámetros, cierres y fronteras de módulo.**

---

## 🧭 De qué trata esta parte

La función es la primera herramienta de abstracción real: permite dar nombre a un proceso y, con ese nombre, dejar de pensar en cómo está hecho. Esta parte la estudia como **contrato** —qué promete la firma y qué garantiza— y no como una forma de ahorrar líneas repetidas.

La sección más importante es la que casi todos los cursos despachan en un párrafo: **qué recibe realmente una función**. Paso por valor, paso por referencia y el modelo de propiedad y préstamo de Rust son tres respuestas incompatibles a la misma pregunta, y verlas juntas resuelve de una vez la confusión sobre por qué a veces «se modifica afuera» y a veces no.

Después vienen los nombres —alcance, sombreado, cierres, pureza— y el salto de la función al **módulo**: fronteras, visibilidad e importación. Es el punto en que el curso deja de hablar de programas de un archivo y empieza a hablar de proyectos.

## 🎒 Qué necesitas traer

Las Partes 3 y 4. La mutabilidad (054) y el control de flujo son requisito directo; los genéricos (078) se apoyan en el sistema de tipos de la Parte 3.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Leer una firma como un contrato y detectar qué no promete.
2. Predecir si una función puede modificar el argumento que recibió, en cada uno de los diez lenguajes.
3. Explicar movimiento y préstamo de Rust comparándolos con copia y referencia.
4. Escribir una función genérica y explicar el coste de su implementación en cada lenguaje.
5. Identificar qué captura un cierre y por qué eso cambia el resultado del programa.
6. Organizar un proyecto en módulos con fronteras y visibilidad explícitas.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 La firma como contrato · clases 073–078

Parámetros, valores por defecto, argumentos nombrados, variádicos, retornos múltiples y genéricos.

- **[073 · Firma, parámetros, argumentos y retorno](073-firma-parametros-argumentos-y-retorno/README.md)** — La función es la primera y más importante herramienta de abstracción: dar **nombre** a un proceso para poder olvidarse de cómo está hecho. Su **firma** es un contrato — y leer contratos ajenos es la mitad del trabajo de programar.
- **[074 · Parámetros por defecto y opcionales](074-parametros-por-defecto-y-opcionales/README.md)** — Un parámetro que trae su propio valor por defecto simplifica la llamada común sin cerrar la puerta al caso especial. Cuándo se evalúa ese valor por defecto es una diferencia semántica real entre lenguajes, y una fuente clásica de bugs en Python.
- **[075 · Argumentos nombrados y de palabra clave](075-argumentos-nombrados-y-de-palabra-clave/README.md)** — Pasar los argumentos diciendo a qué parámetro corresponde cada uno, en vez de confiar en el orden. Convierte `crear(true, false, true)` en algo legible, y es una de las diferencias más visibles entre Python y la familia C.
- **[076 · Parámetros variádicos](076-parametros-variadicos/README.md)** — Una función que no fija de antemano cuántos argumentos recibe: acepta uno, tres o cuarenta. Es lo que hay detrás de `print`, `printf` y `format`, y cada lenguaje lo resuelve con un mecanismo distinto (empaquetado, arreglo, slice).
- **[077 · Múltiples retornos y desestructuración](077-multiples-retornos-y-desestructuracion/README.md)** — Que una función entregue **más de un valor de una vez**, y que quien la llama reparta esos valores en variables. Tuplas en Python y Rust, retornos múltiples en Go, `out` en C#: el mismo problema con soluciones que revelan el diseño de cada lenguaje.
- **[078 · Genéricos y polimorfismo paramétrico](078-genericos-y-polimorfismo-parametrico/README.md)** — Escribir la función **una sola vez** y que sirva para muchos tipos sin renunciar a la comprobación del compilador. Los genéricos son la respuesta tipada a la duplicación, y su coste —monomorfización o borrado— cambia por completo entre Rust, Java y Go.

### 🔹 Qué recibe realmente la función · clases 079–081

Las tres respuestas al paso de parámetros: valor, referencia y propiedad.

- **[079 · Paso por valor](079-paso-por-valor/README.md)** — El paso **por valor** entrega una copia: la función no recibe *tu* variable sino un duplicado. Simple de enunciar y responsable de la mitad de las confusiones sobre por qué «la modifiqué y afuera no cambió».
- **[080 · Paso por referencia](080-paso-por-referencia/README.md)** — El paso **por referencia** entrega acceso al original: la función puede alcanzar y modificar la variable de quien la llamó. Distinguir esto de «pasar un objeto por valor» resuelve la confusión más persistente de la programación.
- **[081 · Semántica de movimiento y préstamo (Rust)](081-semantica-de-movimiento-y-prestamo-rust/README.md)** — El modelo con el que Rust gestiona memoria sin recolector y sin `malloc`/`free`: **propiedad**, **movimiento** y **préstamo**. Es la tercera respuesta a un problema que C y Java resolvieron de forma opuesta, y se entiende mejor comparada que sola.

### 🔹 Dónde viven los nombres · clases 082–085

Alcance, sombreado, cierres, pureza y la función como valor de primera clase.

- **[082 · Alcance (scope) y sombreado (shadowing)](082-alcance-scope-y-sombreado-shadowing/README.md)** — Cada vez que escribes `x`, el lenguaje decide a qué variable te refieres siguiendo una regla precisa: el **alcance**. El **sombreado** —redeclarar un nombre que ya existía— es legal en unos lenguajes, un error en otros y una fuente de bugs en todos.
- **[083 · Cierres (closures) y captura de variables](083-cierres-closures-y-captura-de-variables/README.md)** — Un **cierre** es una función que se lleva consigo un pedazo del entorno donde nació. Capturar por valor o por referencia cambia el resultado del programa, y ahí es donde JavaScript, Rust y C++ toman decisiones incompatibles.
- **[084 · Funciones puras y efectos secundarios](084-funciones-puras-y-efectos-secundarios/README.md)** — Una función es **pura** cuando su resultado depende solo de sus argumentos y no observa ni cambia nada más. La distinción no es doctrinal: las funciones puras son las únicas trivialmente comprobables, cacheables y seguras entre hilos.
- **[085 · Funciones de primera clase y como valores](085-funciones-de-primera-clase-y-como-valores/README.md)** — Dejar de ver la función como una construcción especial del lenguaje y verla como **un valor más**: que se guarda en una variable, se pasa como argumento y se devuelve. Es el requisito de todo lo funcional que viene después.

### 🔹 De la función al proyecto · clases 086–088

Módulos, visibilidad, encapsulación e importación: las fronteras del código propio.

- **[086 · Módulos, paquetes y espacios de nombres](086-modulos-paquetes-y-espacios-de-nombres/README.md)** — El **módulo** es el escalón siguiente a la función: una abstracción sobre un grupo de funciones y datos, con un nombre y una frontera. Paquete, namespace, crate y módulo nombran cosas parecidas pero no iguales en cada lenguaje.
- **[087 · Visibilidad, encapsulación y contratos (public/private)](087-visibilidad-encapsulacion-y-contratos-public-private/README.md)** — La encapsulación no es etiqueta («no toques los campos ajenos») sino el mecanismo que hace **confiable** a un tipo: si el estado interno solo cambia por operaciones que preservan sus invariantes, esos invariantes se pueden dar por ciertos.
- **[088 · Importar, exportar y organizar un proyecto](088-importar-exportar-y-organizar-un-proyecto/README.md)** — La contracara de escribir funciones: saber **traer** las que ya existen, y decidir la estructura de carpetas de un proyecto real en cada lenguaje. Importar es también una decisión de acoplamiento, no solo una línea al principio del archivo.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «En Java los objetos se pasan por referencia.» | Se pasa por valor la **referencia**. La diferencia se nota en cuanto reasignas el parámetro dentro de la función. |
| «Un cierre es solo una función anónima.» | Lo que lo define no es no tener nombre, sino llevarse consigo el entorno donde nació. |
| «`private` es una regla de cortesía.» | Es el mecanismo que permite dar por ciertos los invariantes de un tipo. Sin él, no hay nada que garantizar. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

## 🔗 Qué abre esta parte

Con funciones y módulos, la Parte 6 se ocupa de lo que esas funciones manipulan: las estructuras de datos.

---

> [⏮️ Parte 4](../parte-4-control-del-programa/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 6](../parte-6-datos-y-estructuras/README.md)
