# Parte 6 — Datos y estructuras

> [⏮️ Parte 5](../parte-5-funciones-y-modularidad/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 7](../parte-7-paradigmas/README.md)

**18 clases** · rango 089–106 · clases de **código** · nivel intermedio · **~45 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Dónde se guardan los datos, qué cuesta cada operación y qué significa realmente copiar.**

---

## 🧭 De qué trata esta parte

Es la parte más larga del programa (18 clases) porque es la que más se transfiere: las estructuras de datos son las mismas en todos los lenguajes, cambian los nombres y las garantías. Un `dict` de Python, un `HashMap` de Java y un `map` de Go son la misma idea con tres contratos distintos sobre orden, nulidad y concurrencia.

El recorrido sube de lo contiguo a lo enlazado —arreglo, arreglo dinámico, tupla, rango, cadena, conjunto, mapa, pila, cola, árbol, grafo— y luego cambia de plano: cómo modelar un dato **propio** con registros y tipos algebraicos. Cada clase declara el coste real de sus operaciones, porque elegir estructura es elegir qué será barato y qué será caro.

El tramo final es el más peligroso de la programación cotidiana: **igualdad frente a identidad**, **copia superficial frente a profunda** y **propiedad de los datos**. Ahí nacen los bugs de aliasing que no se reproducen. La parte cierra sacando los datos del proceso: archivos, JSON y persistencia.

## 🎒 Qué necesitas traer

Las Partes 3–5. La mutabilidad (054), el paso de parámetros (079–081) y los genéricos (078) son requisito directo.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Elegir la estructura adecuada a partir del coste de las operaciones que vas a hacer.
2. Explicar por qué un arreglo dinámico tiene coste amortizado y qué pasa al recrecerse.
3. Modelar un dato del dominio con registros y tipos algebraicos en lugar de con banderas sueltas.
4. Distinguir igualdad de identidad y copia superficial de profunda en los diez lenguajes.
5. Serializar y deserializar a JSON sabiendo qué información del tipo se pierde en el viaje.
6. Persistir datos eligiendo formato con criterio de interoperabilidad y longevidad.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Secuencias · clases 089–093

De la memoria contigua a la cadena: las estructuras lineales y su coste real.

- **[089 · Arreglos de tamaño fijo](089-arreglos-de-tamano-fijo/README.md)** — El **arreglo de tamaño fijo** es la estructura primitiva de la que descienden casi todas las demás: un bloque contiguo de memoria con acceso en tiempo constante por índice. Entenderlo es entender por qué todo lo demás cuesta lo que cuesta.
- **[090 · Listas, vectores y arreglos dinámicos](090-listas-vectores-y-arreglos-dinamicos/README.md)** — El **arreglo dinámico** —`list`, `Vec`, `ArrayList`, slice— no crece por arte de magia: reserva de más y se recopia cuando se llena. Ese detalle explica su coste amortizado y por qué invalida referencias en algunos lenguajes.
- **[091 · Tuplas y registros posicionales](091-tuplas-y-registros-posicionales/README.md)** — La **tupla** es la colección de tamaño fijo y heterogénea cuyos elementos se identifican por posición. Es la estructura mínima para devolver dos cosas a la vez, y el escalón previo al registro con nombres.
- **[092 · Rangos y secuencias](092-rangos-y-secuencias/README.md)** — El **rango** describe «todos los enteros de a hasta b» sin materializarlos: una representación perezosa que ahorra memoria y expresa la intención. Aquí se ve además el eterno detalle de si el extremo es inclusivo o exclusivo.
- **[093 · Cadenas como estructura de datos](093-cadenas-como-estructura-de-datos/README.md)** — Dejar de ver la cadena como un escalar «que guarda texto» y verla como una **estructura de datos**: secuencia indexable de caracteres o bytes, con coste real en cada operación de concatenación, corte o búsqueda.

### 🔹 Colecciones por clave y por disciplina · clases 094–096

Conjuntos, mapas y las estructuras que restringen el acceso a propósito.

- **[094 · Conjuntos (sets) y unicidad](094-conjuntos-sets-y-unicidad/README.md)** — El **conjunto** no es «una lista que rechaza repetidos»: es una idea matemática en código, con pertenencia en tiempo constante y operaciones de unión, intersección y diferencia que expresan lógica que en bucles quedaría ilegible.
- **[095 · Mapas / diccionarios / tablas hash](095-mapas-diccionarios-tablas-hash/README.md)** — El **mapa** —diccionario, tabla hash— asocia claves con valores y, junto con el arreglo, sostiene buena parte de la programación real. Entender el hash y la colisión explica por qué el orden de iteración no es el que insertaste.
- **[096 · Pilas y colas](096-pilas-y-colas/README.md)** — **Pila** y **cola** no son dos colecciones más: son dos **disciplinas de acceso** que restringen deliberadamente dónde se inserta y de dónde se saca. LIFO y FIFO son decisiones de diseño, no limitaciones.

### 🔹 Estructuras enlazadas · clases 097–098

El salto a lo jerárquico y a lo relacional: árboles y grafos.

- **[097 · Árboles](097-arboles/README.md)** — El **árbol** es el salto de lo lineal a lo jerárquico: raíz, hijos, hojas y recorridos. Aparece en todas partes —sistemas de archivos, DOM, AST, índices de base de datos— y es la primera estructura donde la recursión resulta natural.
- **[098 · Grafos](098-grafos/README.md)** — El **grafo** es la estructura más general: vértices y aristas modelando cualquier relación. Con él llegan los recorridos en anchura y profundidad, y la conciencia de que muchos problemas «difíciles» son grafos mal reconocidos.

### 🔹 Modelar un dato propio · clases 099–100

Registros y tipos algebraicos: el vocabulario del dominio dentro del sistema de tipos.

- **[099 · Registros, structs y clases](099-registros-structs-y-clases/README.md)** — El **registro** —struct, clase, record— agrupa campos heterogéneos accedidos por **nombre**. Es el complemento exacto de la tupla y el punto donde el programa empieza a hablar el vocabulario del dominio y no el de la máquina.
- **[100 · Enumeraciones y tipos algebraicos (ADT / sum types)](100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md)** — Dos ideas confundidas bajo la palabra «enum»: el conjunto cerrado de valores con nombre, y el **tipo algebraico** que además lleva datos en cada variante. La segunda es la que hace posible `Option`/`Result` y el `match` exhaustivo.

### 🔹 Qué significa copiar · clases 101–103

Igualdad, identidad, copia superficial y profunda, y quién es dueño del dato.

- **[101 · Igualdad vs. identidad](101-igualdad-vs-identidad/README.md)** — **Igualdad** (mismo valor) e **identidad** (mismo objeto en memoria) son dos preguntas distintas que la sintaxis suele disfrazar con símbolos parecidos. `==` frente a `equals`, `is` frente a `==`: la respuesta correcta depende del lenguaje.
- **[102 · Copia superficial vs. profunda; referencia vs. valor](102-copia-superficial-vs-profunda-referencia-vs-valor/README.md)** — ¿`b = a` duplica el dato o le da un segundo nombre? Y si duplica, ¿copia también lo que hay dentro? Copia superficial, copia profunda y referencia compartida son la causa de los bugs de aliasing más caros de diagnosticar.
- **[103 · Propiedad y ciclo de vida de los datos](103-propiedad-y-ciclo-de-vida-de-los-datos/README.md)** — La pregunta más callada y consecuente de la programación de sistemas: **quién es responsable de liberar un recurso y cuándo**. Aquí se prepara el terreno para las tres respuestas —manual, GC y propiedad— que la Parte 8 desarrolla.

### 🔹 Sacar los datos del proceso · clases 104–106

Archivos, JSON y persistencia: la vida del dato más allá de la ejecución.

- **[104 · Archivos: leer y escribir texto y binario](104-archivos-leer-y-escribir-texto-y-binario/README.md)** — La entrada/salida de archivos es un **flujo** de bytes entre tu proceso y el mundo. Texto frente a binario, buffering, codificación y cierre del descriptor: cuatro decisiones que casi todos los tutoriales omiten.
- **[105 · JSON: serialización y deserialización](105-json-serializacion-y-deserializacion/README.md)** — **JSON** es el formato universal de intercambio: convertir estructuras vivas del proceso en texto que otro programa —en otro lenguaje— pueda reconstruir. Serializar es donde los tipos de cada lenguaje se encuentran con un vocabulario común y pierden algo por el camino.
- **[106 · Otros formatos y persistencia: CSV, YAML, binarios, bases de datos](106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md)** — Cierra la parte con persistencia: CSV, YAML, formatos binarios y bases de datos. Elegir representación externa es decidir quién más podrá leer tus datos, con qué coste y durante cuánto tiempo.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Una lista y un arreglo son lo mismo.» | Uno tiene tamaño fijo y coste predecible; el otro recrece, recopia y a veces invalida referencias. |
| «El diccionario conserva el orden de inserción.» | Solo en algunos lenguajes y por decisión explícita de la implementación. Depender de ello sin comprobarlo es una bomba de relojería. |
| «Copiar un objeto copia lo que hay dentro.» | Casi nunca: la copia por defecto es superficial y comparte lo interno. De ahí el bug que aparece «solo a veces». |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

## 🔗 Qué abre esta parte

Con datos y funciones dominados, la Parte 7 sube al nivel de las decisiones de estilo: los paradigmas.

---

> [⏮️ Parte 5](../parte-5-funciones-y-modularidad/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 7](../parte-7-paradigmas/README.md)
