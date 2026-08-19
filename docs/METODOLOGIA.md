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
| 🧟 Vivos | El mismo problema en los 12 lenguajes antiguos que siguen en producción (`vivos.md`), con lo que cada uno enseña y no enseña ningún otro. |
| 🔬 Comparación · 🧬 Familia | Las diferencias, clasificadas; y cómo lo hace el resto de la familia. |
| ✅ Prueba común | El `casos.json` que verifica la equivalencia. |
| 🧪 Reto · ⚠️ Errores · ❓ FAQ | Transferencia, trampas conocidas y dudas frecuentes. |
| 🔗 Referencias | Los libros de la parte y el libro de cada lenguaje, **y qué uso hace de ellos esta clase**. |

## El contenido se ancla en libros

Cada parte tiene una **bibliografía real** y cada clase cita las obras de su área y el libro de
referencia de cada lenguaje. Las explicaciones se apoyan en esa literatura —Sebesta y Scott para
semántica de lenguajes, Pierce para tipos, Cormen y Sedgewick para estructuras, McConnell, Martin
y Fowler para ingeniería, Kleppmann y Newman para sistemas— pero **la redacción es original**: se
explica la idea, no se reproduce el texto.

### El registro de fuentes

Citar el nombre de un libro no basta para que alguien lo compruebe. La fuente de verdad de la
bibliografía es **[`sources/bibliography.json`](../sources/bibliography.json)**: una entrada por
obra, cada una con **localizador resoluble** —ISBN-13 para los libros, DOI para los artículos, URL
https de la fuente primaria para normas y documentación oficial— y con la lista de clases que la
citan. Lo que no se pudo resolver se marca `"status": "pendiente"`; no se borra ni se rellena por
intuición.

Además, **cada cita declara el uso que esa clase hace de la obra**, no solo su nombre: para qué
sirve ahí, no que exista.

### Dos capas de verificación, separadas a propósito

| Herramienta | Red | ¿Bloquea? | Qué comprueba |
|---|---|---|---|
| [`scripts/verificar_fuentes.py`](../scripts/verificar_fuentes.py) | no | **sí, en CI** | Que el registro cumple el esquema; que todo ISBN-13 tiene dígito de control válido y todo artículo su DOI; que el `locator` es canónico; que toda obra citada está en el registro y ninguna entrada queda sin usar; que cada cita declara su uso; que ningún bloque de fuentes se repite entre clases; y que las cifras del README salen del recuento, no de la mano. |
| [`scripts/refrescar_fuentes.py`](../scripts/refrescar_fuentes.py) | sí | no | Resuelve cada ISBN contra Open Library y cada DOI contra Crossref comparando título y autores, hace GET a las ediciones libres, actualiza `verified_on` y `accessed`, y **reporta lo que dejó de resolver sin borrarlo**. |

Están separadas por una razón práctica: si la red entra en el CI, el CI se vuelve inestable y se
acaba ignorando. La capa que bloquea es determinista y offline; la que consulta al mundo se
ejecuta a mano o programada.

> Los generadores históricos de partes (`scripts/gen_parte*.py`) producen el bloque de referencias
> en su formato antiguo, sin nota de uso. Si se vuelve a ejecutar alguno, `verificar_fuentes.py`
> lo detendrá en CI: es justo para eso.

## Qué verifica la máquina y qué no

Es una distinción que el programa mantiene explícita para no prometer de más:

| Se verifica en CI | No se verifica (material de lectura) |
|---|---|
| Que las 10 implementaciones de cada clase de código producen **la misma salida** ante el mismo `casos.json` | El texto de las clases y las comparaciones |
| Que los primos **Ruby, Perl y Lua** de `primos.md` producen esa misma salida | Los otros 17 primos (Zig, Prolog, Objective-C…) |
| Que **COBOL, Fortran, Ada, Pascal, Lisp, Tcl, Perl y C++** de `vivos.md` compilan, se ejecutan y dan esa misma salida | PL/I, MUMPS, Smalltalk y ensamblador, correctos pero **sin sello de máquina**; RPG, JCL, VBA y AutoLISP, con el contrato **adaptado y declarado** |
| Que la estructura del repositorio y los enlaces son válidos | El [Atlas](../atlas/README.md) de familias y las [60 fichas de lenguaje](../atlas/lenguajes.md) |
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
