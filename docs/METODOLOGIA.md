# 🧭 Metodología

> [⬅️ Volver al programa](../README.md) · [🧱 Currículo](CURRICULO.md) · [📊 Rúbrica](rubrica-evaluacion.md) · [📅 Syllabus](syllabus.md)

Cómo se enseña en este programa y por qué. La tesis es simple: **el conocimiento de programación
es transferible**. Un concepto se aprende una vez y luego se reconoce, se compara y se aplica en
cualquier lenguaje. Lo que cambia entre lenguajes no es el concepto, sino su forma —y a veces,
sus garantías.

## Unidad mínima: la ficha de transferencia

Cada conocimiento se enseña mediante la misma secuencia:

1. **Situación** — problema comprensible y observable.
2. **Modelo** — entradas, salidas, reglas y casos límite.
3. **Algoritmo** — pseudocódigo neutral, sin lenguaje.
4. **Formas** — solución imperativa, funcional, orientada a objetos o declarativa, cuando correspondan.
5. **Lenguajes** — implementación **idiomática**, nunca traducción mecánica.
6. **Comparación** — sintaxis, tipos, memoria, errores y ecosistema.
7. **Prueba común** — mismos casos y resultados observables (`casos.json`).
8. **Transferencia** — resolver una variante en un lenguaje que no se explicó paso a paso.

## Las tres clases de diferencia

Es la herramienta central del programa y se fija en la [Parte 0](../classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md).
Ante cualquier diferencia entre dos lenguajes, la pregunta es siempre a cuál de estas tres pertenece:

| Clase | Pregunta | Ejemplo |
|---|---|---|
| **Sintáctica** | ¿Se escribe distinto, pero significa esencialmente lo mismo? | `!=` frente a `<>`; llaves frente a indentación. |
| **Semántica** | ¿Cambia el comportamiento, el tipo, la mutabilidad o la memoria? | Rust es inmutable por defecto; Python no. |
| **Paradigmática** | ¿El lenguaje invita a estructurar la solución de otra manera? | Resolver con una consulta SQL en vez de un bucle. |

Confundirlas es el error más común del programador políglota: tratar una diferencia semántica
como si fuera cosmética es lo que produce bugs al portar código.

## Anatomía de una clase

Toda clase sigue la misma estructura, para que estudiar la número 150 cueste lo mismo que la 41:

| Sección | Qué aporta |
|---|---|
| 🎯 Objetivo · 📚 Resultados | Qué sabrás hacer, en términos verificables. |
| 🗺️ Temas · 📖 Definiciones | El vocabulario preciso (alimenta el [glosario](../glosario/README.md)). |
| 🧩 Situación · 🧮 Modelo | El problema concreto y su contrato de entrada/salida. |
| 📐 Algoritmo | Pseudocódigo neutral: la solución antes del lenguaje. |
| 🌐 Implementaciones | El código **a la vista** en los 10 lenguajes, enlazado a su archivo real. |
| 🧬 Primos | Bajo cada bloque, el mismo programa en los primos de esa familia (`primos.md`). |
| 🔬 Comparación · 🧬 Familia | Las diferencias, clasificadas; y cómo lo hace el resto de la familia. |
| ✅ Prueba común | El `casos.json` que verifica la equivalencia. |
| 🧪 Reto · ⚠️ Errores · ❓ FAQ | Transferencia, trampas conocidas y dudas frecuentes. |
| 🔗 Referencias | Los libros de la parte y el libro del lenguaje. |

## El contenido se ancla en libros

Cada parte tiene una **bibliografía real** (definida en [`scripts/curriculo.py`](../scripts/curriculo.py))
y cada clase cita las obras de su área y el libro de referencia de cada lenguaje. Las
explicaciones se apoyan en esa literatura —Sebesta y Scott para semántica de lenguajes, Pierce
para tipos, Cormen y Sedgewick para estructuras, McConnell, Martin y Fowler para ingeniería,
Kleppmann y Newman para sistemas— pero **la redacción es original**: se explica la idea, no se
reproduce el texto.

## Qué verifica la máquina y qué no

Es una distinción que el programa mantiene explícita para no prometer de más:

| Se verifica en CI | No se verifica (material de lectura) |
|---|---|
| Que las 10 implementaciones de cada clase de código producen **la misma salida** ante el mismo `casos.json` | El texto de las clases y las comparaciones |
| Que los primos **Ruby, Perl y Lua** de `primos.md` producen esa misma salida | Los otros 17 primos (Zig, Prolog, Objective-C…) |
| Que la estructura del repositorio y los enlaces son válidos | El [Atlas](../atlas/README.md) de familias |
| Que el Markdown pasa el linter | Las autoevaluaciones |

Si el badge de CI está verde, garantiza la **equivalencia demostrada** de las implementaciones,
no la prosa. Ver [laboratorios](../labs/README.md).

## Principio de implementación idiomática

Una implementación no se acepta si es una traducción token a token de otra. Debe leerse como la
escribiría alguien de esa comunidad: `gofmt` en Go, PEP 8 en Python, las convenciones de
*Effective Java*. El objetivo es que el estudiante vea **cómo piensa cada lenguaje**, no cómo se
disfraza uno de otro.

Igualmente, **no se afirma una equivalencia que el lenguaje no ofrece**. Cuando un concepto no
tiene equivalente directo (por ejemplo, propiedad de Rust en Python), se dice explícitamente y se
explica qué se pierde o se gana.

## Evaluación

Una entrega no se considera completa por compilar: debe explicar **qué conocimiento se transfirió
y qué cambió** al pasar de un lenguaje a otro. Los criterios detallados, la escala graduada y los
pesos están en la [rúbrica de evaluación](rubrica-evaluacion.md), y cada ruta cierra con su
[examen final por perfil](examen-final-por-perfil.md).
