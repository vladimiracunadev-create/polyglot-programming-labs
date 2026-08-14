# Parte 10 — Interoperabilidad y fronteras entre lenguajes

> [⏮️ Parte 9](../parte-9-ingenieria-de-software-poliglota/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 11](../parte-11-proyecto-integrador-poliglota/README.md)

**10 clases** · rango 155–164 · clases de **código** · nivel avanzado · **~25 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Las fronteras entre lenguajes: FFI, ABI, serialización, contratos, Wasm e incrustación.**

---

## 🧭 De qué trata esta parte

Hasta aquí el curso estudiaba un problema resuelto en diez lenguajes que no se hablaban entre sí. Esta parte cambia la pregunta: cómo esos lenguajes **conviven dentro de un mismo sistema**. Es el territorio que justifica el enfoque políglota, porque todo sistema real de cierto tamaño lo es.

Las fronteras se ordenan de la más íntima a la más laxa. La **FFI** llama una función de otro lenguaje dentro del mismo proceso, con la ABI como contrato silencioso que, cuando no coincide, no da error sino corrupción. Los **bindings** envuelven esa frontera para hacerla habitable. Después, las fronteras por datos: serialización, contratos de API y el canal por el que viajan los bytes.

Cierra con dos terrenos comunes —WebAssembly como objetivo independiente de arquitectura, y la incrustación de un intérprete dentro de un anfitrión— y con la decisión que todo lo anterior vuelve informada: qué lenguaje merece cada componente y qué coste de frontera se acepta a cambio.

## 🎒 Qué necesitas traer

Las Partes 6, 8 y 9. Propiedad y ciclo de vida (103), memoria y punteros (128–130) y contratos de módulo (087) son requisito directo.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Llamar a una función de C desde otro lenguaje y explicar qué garantías se pierden al cruzar.
2. Diagnosticar un fallo de ABI distinguiéndolo de un error de tipos en el código fuente.
3. Elegir entre JSON, Protobuf y MessagePack con un criterio de tamaño, velocidad y legibilidad.
4. Definir un contrato de API versionado que sobreviva a un cambio en uno de los dos lados.
5. Decidir el canal de comunicación según el acoplamiento temporal que quieras aceptar.
6. Justificar por escrito la elección de lenguaje de cada componente de un sistema.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 La frontera íntima: mismo proceso · clases 155–158

Por qué los sistemas son políglotas, la FFI, la ABI que la sostiene y los bindings que la hacen usable.

- **[155 · Por qué los sistemas reales son políglotas](155-por-que-los-sistemas-reales-son-poliglotas/README.md)** — Cambia la pregunta del curso: hasta aquí un problema resuelto en diez lenguajes que no se hablaban; a partir de ahora, cómo esos lenguajes **conviven dentro de un mismo sistema** y qué se paga en cada frontera.
- **[156 · La FFI (Foreign Function Interface): llamar a C desde todos](156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md)** — La frontera más íntima: llamar, dentro del mismo proceso, una función compilada por otro lenguaje. La **FFI** convierte a C en el idioma franco — y en el punto donde se pierden las garantías de seguridad del lenguaje que llama.
- **[157 · ABI, enlace y convenciones de llamada](157-abi-enlace-y-convenciones-de-llamada/README.md)** — Bajo la firma de la FFI hay un contrato silencioso: la **ABI**. Convención de llamada, alineación, tamaño de tipos y decoración de nombres — cuando no coinciden, el programa no falla con un error claro sino con corrupción.
- **[158 · Enlaces (bindings) y wrappers](158-enlaces-bindings-y-wrappers/README.md)** — La FFI cruda es peligrosa, y nadie quiere programar así a diario. Los **bindings** y *wrappers* envuelven esa frontera para devolver al lenguaje anfitrión sus tipos, sus errores y su gestión de recursos.

### 🔹 La frontera por datos · clases 159–161

Serialización, contratos de API y los canales por los que viajan los bytes.

- **[159 · Serialización entre lenguajes: JSON, Protobuf, MessagePack](159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md)** — La mayoría de las fronteras reales no comparten proceso ni memoria. Serializar —JSON, Protobuf, MessagePack— es acordar cómo se escriben los datos en el cable, con un compromiso claro entre legibilidad, tamaño y velocidad.
- **[160 · Contratos de API: REST, gRPC y esquemas](160-contratos-de-api-rest-grpc-y-esquemas/README.md)** — El formato resuelve *cómo* viajan los datos; el **contrato de API** resuelve *qué* datos y *qué* operaciones. REST, gRPC y esquemas versionados: sin contrato explícito, la integración funciona hasta el primer cambio.
- **[161 · Procesos y comunicación: stdin/stdout, sockets, colas](161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md)** — Falta el canal: por dónde salen los bytes de un proceso y entran en otro. `stdin`/`stdout`, sockets y colas de mensajes determinan el acoplamiento temporal —si ambos extremos deben estar vivos a la vez— más que cualquier otra decisión.

### 🔹 Terrenos comunes · clases 162–163

WebAssembly como objetivo compartido e incrustar un lenguaje dentro de otro.

- **[162 · WebAssembly como objetivo común](162-webassembly-como-objetivo-comun/README.md)** — **WebAssembly** ofrece un punto de encuentro que la ABI de C no puede dar: independiente de arquitectura y de sistema operativo, con aislamiento por defecto. Un objetivo común al que compilan hoy Rust, C, Go y varios más.
- **[163 · Incrustar un lenguaje en otro (Lua, Python embebido)](163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)** — Incrustar invierte la relación y la vuelve jerárquica: un programa anfitrión hospeda un intérprete y le expone funciones. Es como Lua entró en los motores de juego y como Python se usa para extender aplicaciones grandes.

### 🔹 La decisión · clase 164

Elegir el lenguaje de cada componente con criterios explícitos.

- **[164 · Elegir el lenguaje correcto para cada componente](164-elegir-el-lenguaje-correcto-para-cada-componente/README.md)** — Cierra la parte con la decisión que todo lo anterior hace informada: qué lenguaje merece cada componente, con qué criterios explícitos y qué coste de frontera se acepta a cambio.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Si la firma está bien declarada, la FFI funciona.» | Bajo la firma está la ABI: convención de llamada, alineación y tamaños. Cuando no coinciden, el fallo es corrupción silenciosa. |
| «Un formato común basta para integrar dos servicios.» | El formato dice cómo se escriben los datos; el contrato dice cuáles y qué operaciones. Sin contrato, la integración dura hasta el primer cambio. |
| «Políglota significa usar muchos lenguajes.» | Significa pagar conscientemente el coste de cada frontera a cambio de una ventaja concreta y defendible. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

## 🔗 Qué abre esta parte

Con las fronteras comprendidas, la Parte 11 construye un sistema real que las usa todas.

---

> [⏮️ Parte 9](../parte-9-ingenieria-de-software-poliglota/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 11](../parte-11-proyecto-integrador-poliglota/README.md)
