# Clase 014 — Cómo elegir lenguaje para un problema

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

La Parte 0 se cierra con la pregunta que todo lo anterior hace posible responder: dado un problema y su contexto, ¿qué lenguaje conviene? Esta pregunta solo tiene sentido para quien ha entendido que los lenguajes no son intercambiables ni son todos equivalentes: cada uno encarna decisiones de diseño —sobre memoria, tipos, concurrencia, ejecución— que lo hacen bueno para unas cosas y mediocre para otras. Elegir bien es un acto de ingeniería, y como todo acto de ingeniería consiste en ponderar restricciones que compiten entre sí, no en encontrar un óptimo absoluto que no existe.

El error que esta clase quiere prevenir es tratar la elección como una cuestión de gusto o de moda. Polya insiste en que la primera fase de resolver un problema es *entenderlo*, y elegir lenguaje antes de entender el problema es exactamente saltarse esa fase: es responder antes de saber la pregunta. Hunt y Thomas van en la misma dirección cuando describen la caja de herramientas del programador pragmático: la habilidad no está en tener un martillo excelente, sino en saber cuándo el problema es un clavo. Al terminar deberías poder justificar una elección con argumentos que resistan a un colega escéptico, y —tan importante como eso— reconocer cuándo la respuesta correcta no es un lenguaje sino varios.

## 🧩 Situación

Un equipo va a construir un servicio web con dos exigencias muy distintas conviviendo en el mismo producto: una interfaz interactiva en el navegador y un módulo de cálculo numérico que consume un tercio del presupuesto de CPU. Alguien propone lo que siempre se propone: "usemos un solo lenguaje para todo, será más simple". La propuesta es atractiva porque promete uniformidad, pero encierra un error de razonamiento: confunde uniformidad de herramienta con simplicidad de sistema. Si el lenguaje único es JavaScript, el módulo numérico será lento o exigirá contorsiones; si es C, la interfaz será un calvario; si es Python, tendrás lo peor de ambos.

La respuesta realista es políglota: TypeScript en el frontend, porque el navegador solo ejecuta JavaScript y el tipado estático reduce los errores de una interfaz grande; Go o Java en el backend, por su modelo de concurrencia y su ecosistema de servicios; y quizá Rust o C para el núcleo de cálculo, encapsulado tras una interfaz estrecha. Esa arquitectura tiene un coste —más toolchains, más perfiles en el equipo, una frontera entre lenguajes que hay que diseñar con cuidado, tema de la Parte 10— y ese coste es precisamente lo que hay que ponderar. La decisión no es "políglota sí o no", sino si el beneficio de cada lenguaje extra supera el coste que añade.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Enumerar los criterios que intervienen en la elección de lenguaje y explicar cómo se ponderan entre sí.
2. Asociar tipos de problema con las familias de lenguajes que mejor encajan y decir por qué.
3. Justificar una elección con argumentos técnicos y de contexto, no por moda ni por costumbre.
4. Reconocer cuándo un sistema debe ser políglota y qué coste añade cada lenguaje extra.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Criterios de elección | Rendimiento, seguridad, ecosistema, equipo, plazo |
| 2 | Problema → familia | Cada tipo de problema tiene familias que encajan |
| 3 | Sistemas políglotas | Elegir por componente, no un solo lenguaje para todo |
| 4 | El coste de la elección | Toda decisión cierra puertas además de abrirlas |

## 📖 Definiciones y características

Un **criterio de selección** es cualquier factor que inclina la balanza, y lo esencial es que se ponderan: ninguno es absoluto y casi siempre entran en conflicto. Los más habituales son cinco. El **rendimiento** importa cuando el coste computacional o la latencia son parte del requisito, y no antes: elegir C para un script que corre una vez al día es optimizar lo que nadie mide. La **plataforma** a veces decide sola, porque no negocia: si el código corre en un navegador, será JavaScript o algo que compile a JavaScript, y si corre dentro de un motor de base de datos, será SQL. El **ecosistema** —bibliotecas maduras, herramientas, documentación, respuestas ya escritas a los problemas que vas a tener— pesa a menudo más que el lenguaje en sí, y es la razón principal de que Python domine el análisis de datos pese a no ser rápido. El **equipo** es un criterio técnico legítimo, no una excusa: un lenguaje que nadie del equipo domina introduce un riesgo real de defectos y de plazos. Y el **plazo y el horizonte de mantenimiento** cambian el cálculo por completo: un prototipo de dos semanas y un sistema que vivirá diez años no premian las mismas propiedades.

El **ecosistema** merece detenerse porque es el criterio que más se subestima y el que más veces decide. Elegir un lenguaje nunca es elegir solo su sintaxis y su semántica: es adoptar su gestor de paquetes, sus formateadores, sus depuradores, sus bibliotecas y su comunidad, todo lo que la Parte 2 desmenuza. Un lenguaje técnicamente superior con ecosistema pobre suele perder frente a uno mediocre con ecosistema rico, porque en un proyecto real la mayor parte del trabajo consiste en integrar cosas que ya existen, no en escribir algoritmos desde cero. Hunt y Thomas lo formulan como cuestión de cartera de conocimiento y de herramientas: el valor de una herramienta incluye todo lo que viene con ella.

Un **sistema políglota** es aquel que usa varios lenguajes, cada uno donde rinde mejor, y conviene decirlo con claridad: es lo **normal** en producción, no la excepción ni un signo de mal diseño. Casi cualquier aplicación web seria es ya políglota sin que nadie lo haya decidido explícitamente, porque tiene SQL en la base de datos, JavaScript en el navegador y otro lenguaje en el servidor. La decisión consciente no es si serlo, sino cuántos lenguajes justificar y dónde poner las fronteras. Cada lenguaje añadido tiene un coste concreto: otro toolchain que mantener, otro conjunto de dependencias que actualizar, otra convención de estilo, y sobre todo una **frontera** entre componentes donde los tipos y los errores tienen que traducirse, que es donde aparecen los fallos más difíciles. Por eso la regla práctica es exigir a cada lenguaje extra que se gane su sitio con una ventaja clara en su componente, y concentrar en las fronteras el esfuerzo de diseño.

## 🔎 Ejemplo

```text
Problema                         Familias que encajan
-------------------------------  ----------------------------
Script rápido / automatización   Python, Bash, PHP
Servicio web de alto tráfico     Go, Java, C#
Núcleo de rendimiento crítico    C, Rust, C++
Interactividad en el navegador   JavaScript, TypeScript
Consulta y análisis de datos     SQL, Python (con librerías)
```

Esta tabla es útil pero peligrosa si se lee como un recetario, así que conviene entender el **porqué** de cada fila. Para automatización se eligen lenguajes dinámicos e interpretados porque el ciclo escribir-ejecutar es inmediato y no hay compilación de por medio: cuando el programa se escribe en veinte minutos y corre una vez al día, el tiempo de desarrollo domina y el de ejecución es irrelevante. Para un servicio de alto tráfico se eligen lenguajes compilados con concurrencia madura y recolección de basura, porque el cuello de botella es atender muchas peticiones simultáneas sin gestionar memoria a mano. Para un núcleo crítico se baja a C o Rust porque ahí sí importa el control fino de la memoria y la ausencia de pausas de recolección. Para el navegador no hay elección real: es la plataforma la que decide. Y para consultar datos, SQL gana porque cambia de paradigma —describes qué quieres, no cómo obtenerlo— y deja que el motor decida el plan de ejecución, algo que ningún bucle escrito a mano superará sobre millones de filas.

La lección transversal es que la fila correcta depende de cuál sea la restricción dominante, y esa restricción sale del análisis del problema que hiciste en la clase 003, no de una tabla. Si el mismo cálculo numérico se ejecuta una vez al mes, Python es una respuesta perfectamente buena; si se ejecuta un millón de veces por segundo, no lo es. Mismo problema en abstracto, contexto distinto, respuesta distinta.

## ✍️ Práctica

Toma este enunciado: *una app móvil con sincronización en la nube*. Propón un lenguaje por componente y justifica cada elección en una frase, siguiendo estos pasos:

1. **Descompón en componentes**: cliente móvil, servicio de sincronización, almacenamiento, y cualquier proceso auxiliar (notificaciones, tareas periódicas).
2. **Identifica la restricción dominante de cada uno.** ¿Es la plataforma la que decide? ¿El rendimiento? ¿El ecosistema disponible? Escríbelo antes de nombrar ningún lenguaje.
3. **Elige y justifica**, una frase por componente, mencionando qué criterio pesó más.
4. **Cuenta el coste.** ¿Cuántos lenguajes distintos has usado? Para cada uno más allá del segundo, argumenta qué gana el sistema que compense el toolchain adicional. Si no encuentras el argumento, reconsidera la elección.
5. **Dibuja las fronteras.** ¿Por dónde se hablan los componentes y en qué formato viajan los datos? Ahí es donde vivirán los bugs difíciles.

## ⚠️ Errores comunes

| Síntoma / creencia | Causa y cómo corregirlo |
|--------------------|--------------------------|
| Elegir por moda, por costumbre o por lo que se sabe | Ignorar el problema y su contexto. Enumera y pondera los criterios reales antes de nombrar ningún lenguaje |
| Forzar un solo lenguaje para todo el sistema | Confundir uniformidad de herramienta con simplicidad de sistema. Elige por componente y justifica cada frontera |
| Optimizar por rendimiento sin medirlo | Se paga complejidad por una ventaja que nadie necesita. Elige por rendimiento solo cuando sea un requisito verificable |
| Ignorar el ecosistema | El lenguaje "mejor" pierde si carece de bibliotecas y herramientas. Cuenta también lo que viene con él |
| Sumar lenguajes sin contar su coste | Cada uno añade toolchain, dependencias y una frontera que traducir. Exige a cada uno una ventaja clara |
| Decidir sin escribir la justificación | Una decisión sin argumentos escritos no se puede revisar después. Documenta el porqué junto a la elección |

## ❓ Preguntas frecuentes

**❓ ¿Hay un "mejor lenguaje"?** No, y esa es la tesis del curso entero. Hay lenguajes mejores **para un problema y un contexto dados**. La pregunta bien formulada nunca es "¿cuál es el mejor?" sino "¿cuál encaja con estas restricciones?", y en cuanto cambian las restricciones puede cambiar la respuesta sin que ninguno de los dos lenguajes haya cambiado.

**❓ ¿Y si el equipo solo sabe un lenguaje?** Es un criterio legítimo y con frecuencia decisivo. Un lenguaje teóricamente mejor que nadie domina traerá más defectos, revisiones más lentas y una dependencia peligrosa de la única persona que lo entiende. Lo que no es legítimo es usarlo como excusa permanente: si el desajuste entre la herramienta y el problema es grande, formar al equipo o contratar es parte de la solución.

**❓ ¿Cuándo conviene añadir un segundo lenguaje?** Cuando un componente tiene una restricción que el lenguaje principal no satisface —rendimiento, plataforma, un ecosistema irremplazable— y ese componente se puede aislar tras una frontera estrecha y bien definida. Si la frontera es ancha y difusa, el coste de traducir datos y errores entre ambos mundos se comerá la ventaja.

**❓ ¿Esta decisión se puede revertir?** Parcialmente y con esfuerzo creciente en el tiempo. Es una de las decisiones de arquitectura más caras de deshacer, porque arrastra código, dependencias, conocimiento del equipo y contrataciones. Por eso conviene escribir la justificación cuando se toma: cuando dentro de tres años alguien pregunte por qué, la respuesta debería estar documentada y no depender de la memoria de quien decidió.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), sobre entender el problema antes de elegir el método.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre la caja de herramientas y las decisiones reversibles.
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), sobre cuándo el coste computacional es realmente el criterio dominante.

---

> [⏮️ Clase 013](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/013-el-concepto-en-la-familia-leer-un-lenguaje-que-no-conoces/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 015 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/015-el-arbol-genealogico-de-los-lenguajes-mapa-general/README.md)
