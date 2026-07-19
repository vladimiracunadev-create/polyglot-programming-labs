# 🧱 Currículo

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md) · [📅 Syllabus](syllabus.md) · [🧭 Metodología](METODOLOGIA.md)

El currículo completo: **176 clases en 12 partes**, con numeración global y secuencial.
La fuente de verdad es [`scripts/curriculo.py`](../scripts/curriculo.py), de donde
[`scripts/build.py`](../scripts/build.py) deriva el manifiesto, el índice y los README de parte.

El criterio de ordenación es **de dependencia, no de dificultad**: cada parte usa lo anterior.
No se avanza por lenguaje sino por **concepto**: un concepto se presenta una vez y se compara
inmediatamente en los 10 lenguajes del núcleo.

## Las 12 partes

### Parte 0 — Pensamiento computacional y el método políglota · `001–014` (14 clases)

Cómo pensar un problema antes de elegir lenguaje, y el método de fichas de transferencia que
sostiene todo el programa. Aquí se fija la herramienta central: distinguir una diferencia
**sintáctica** de una **semántica** y de una **paradigmática**.

### Parte 1 — Atlas y genealogía de los lenguajes · `015–028` (14 clases)

El árbol genealógico: cada lenguaje del núcleo es el representante de una familia y abre la
puerta a decenas de primos. Se estudia junto al [Atlas](../atlas/README.md).

### Parte 2 — Herramientas, toolchains y anatomía de comandos · `029–040` (12 clases)

Del código fuente al programa que corre: instalar, ejecutar, compilar, empaquetar y probar en
cada lenguaje, con el esquema completo de cada comando.

### Parte 3 — Valores, tipos y variables · `041–056` (16 clases)

La materia prima de todo programa: cómo cada lenguaje nombra, tipa, convierte y muta los valores.
**Primera parte con código verificado en CI.**

### Parte 4 — Control del programa · `057–072` (16 clases)

Decidir, repetir y manejar errores: el flujo de ejecución expresado en cada familia de lenguajes.

### Parte 5 — Funciones y modularidad · `073–088` (16 clases)

Nombrar procesos, pasar datos y organizar el código en módulos con contratos claros.

### Parte 6 — Datos y estructuras · `089–106` (18 clases)

Modelar la información: colecciones, registros, tipos algebraicos, identidad, propiedad y persistencia.

### Parte 7 — Paradigmas · `107–122` (16 clases)

Las grandes formas de estructurar una solución: imperativo, objetos, funcional, declarativo,
lógico, eventos y concurrencia.

### Parte 8 — Cómo funcionan los lenguajes · `123–138` (16 clases)

Qué ocurre por debajo: compilación, máquinas virtuales, memoria, concurrencia y diagnóstico de errores.

### Parte 9 — Ingeniería de software políglota · `139–154` (16 clases)

Llevar el código a producción: pruebas, dependencias, Git, CI, rendimiento, seguridad y
mantenibilidad en varios lenguajes.

### Parte 10 — Interoperabilidad y fronteras entre lenguajes · `155–164` (10 clases)

Por qué los sistemas reales son políglotas y cómo comunican sus piezas: FFI, ABI, serialización,
APIs y WebAssembly.

### Parte 11 — Proyecto integrador políglota · `165–176` (12 clases)

Construir un sistema real con componentes en varios lenguajes y defender cada decisión de
lenguaje y contrato.

## Dos tipos de clase

| Tipo | Partes | Qué trae | Qué se verifica |
|---|---|---|---|
| **Método** | 0, 1, 2 | Concepto, comparación y criterio; sin implementaciones | Estructura y enlaces |
| **Código** | 3–11 | 10 implementaciones del núcleo + `casos.json` | **Equivalencia ejecutada en CI** |

## El núcleo de 10 lenguajes

Definido en [`languages.json`](../languages.json), con su comando de ejecución y su modelo:

| Lenguaje | Modelo | Familia |
|---|---|---|
| Python | interpretado, dinámico | scripting dinámico |
| JavaScript | JIT, dinámico | JavaScript / web |
| TypeScript | transpilado, estático | JavaScript / web |
| Java | JVM, estático | JVM |
| C# | CLR, estático | .NET |
| Go | compilado, estático | sistemas |
| Rust | compilado, estático (propiedad) | sistemas |
| C | compilado, estático (memoria manual) | C / llaves |
| SQL | declarativo | lógica y declarativa |
| PHP | interpretado, dinámico | scripting dinámico |

Los ~40 lenguajes restantes se comprenden **por características** en el
[Atlas](../atlas/README.md), sin implementarse: así el programa cubre amplitud sin multiplicar
el mantenimiento.

## Cómo se amplía

Ver [Ampliar el programa](EXTENDER.md) para añadir una clase, un lenguaje al núcleo o una
familia al Atlas.
