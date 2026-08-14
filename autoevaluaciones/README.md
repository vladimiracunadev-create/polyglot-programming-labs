# 📝 Autoevaluaciones

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md) · [📊 Rúbrica](../docs/rubrica-evaluacion.md) · [🎓 Examen final](../docs/examen-final-por-perfil.md)

**90 preguntas** repartidas en **una batería por cada una de las 12 partes**, con opciones, respuesta
correcta y **explicación razonada** de por qué lo es (y, cuando ayuda, de por qué las otras no).

## 🎯 Qué evalúan (y qué no)

Estas preguntas miden **comprensión transferible**, no memoria de sintaxis. Ninguna pregunta pide
recordar el nombre exacto de un método ni el orden de los argumentos de una función: eso se consulta
en la documentación y se olvida sin consecuencias. Lo que se evalúa es el criterio que el programa
enseña:

| Se pregunta por… | Ejemplo del tipo de pregunta |
|---|---|
| **Clasificar una diferencia** | Al portar de Python a Rust, una variable ya no se puede reasignar. ¿Es sintáctico, semántico o paradigmático — y cuál es el arreglo idiomático? |
| **Predecir un comportamiento** | Qué imprime una conversión implícita, qué considera «verdadero» un lenguaje, qué pasa al desbordar un entero. |
| **Elegir con criterio** | Cuándo conviene un `match` sobre un `switch`, cuándo un `Result` sobre una excepción, qué estructura de datos pide el coste que necesitas. |
| **Diagnosticar** | Ante un fallo de FFI, un aliasing inesperado o una condición de carrera: en qué capa nace el problema. |

Si una pregunta se puede responder consultando la sintaxis en Google, no está en el banco.

## 🚀 Cómo usarlas

1. **Estudia la parte completa primero.** Cada batería asume que leíste sus clases y ejecutaste el verificador; contestar antes solo mide lo que ya sabías al llegar.
2. **Responde sin volver al material.** El objetivo es detectar huecos, no puntuar alto.
3. **Lee la explicación aunque hayas acertado.** Varias explicaciones añaden el matiz entre lenguajes que la pregunta no cabía en enunciar.
4. **Cada fallo apunta a una clase concreta.** Vuelve a esa clase, no a la parte entera — el README de la parte te dice qué se aprende en cada una.
5. **Repite la batería una semana después.** Lo que sigue en pie a los siete días es lo que de verdad se transfiere.

## 🗂️ Las 12 baterías

| Parte | Tema | Preguntas | Clases que cubre |
|---:|---|---:|---|
| 0 | [Pensamiento computacional y el método políglota](../classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) | 8 | 001–014 |
| 1 | [Atlas y genealogía de los lenguajes](../classes/parte-1-atlas-y-genealogia-de-los-lenguajes/README.md) | 8 | 015–028 |
| 2 | [Herramientas, toolchains y anatomía de comandos](../classes/parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md) | 8 | 029–040 |
| 3 | [Valores, tipos y variables](../classes/parte-3-valores-tipos-y-variables/README.md) | 8 | 041–056 |
| 4 | [Control del programa](../classes/parte-4-control-del-programa/README.md) | 8 | 057–072 |
| 5 | [Funciones y modularidad](../classes/parte-5-funciones-y-modularidad/README.md) | 8 | 073–088 |
| 6 | [Datos y estructuras](../classes/parte-6-datos-y-estructuras/README.md) | 7 | 089–106 |
| 7 | [Paradigmas](../classes/parte-7-paradigmas/README.md) | 7 | 107–122 |
| 8 | [Cómo funcionan los lenguajes](../classes/parte-8-como-funcionan-los-lenguajes/README.md) | 7 | 123–138 |
| 9 | [Ingeniería de software políglota](../classes/parte-9-ingenieria-de-software-poliglota/README.md) | 7 | 139–154 |
| 10 | [Interoperabilidad y fronteras entre lenguajes](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) | 7 | 155–164 |
| 11 | [Proyecto integrador políglota](../classes/parte-11-proyecto-integrador-poliglota/README.md) | 7 | 165–176 |
| | **Total** | **90** | **001–176** |

## 💻 Dónde responderlas

- 🌐 **[Quiz interactivo](https://vladimiracunadev-create.github.io/polyglot-programming-labs/autoevaluaciones/quiz.html)** — corrige al instante, muestra la explicación y no envía nada a ningún servidor.
- 📈 **[Progreso](https://vladimiracunadev-create.github.io/polyglot-programming-labs/autoevaluaciones/progreso.html)** — el avance se guarda **solo en tu navegador** (`localStorage`). Si borras los datos del sitio, se pierde: no hay cuenta ni copia remota.
- 📄 **[`preguntas.json`](preguntas.json)** — el banco completo en crudo, por si prefieres imprimirlo, importarlo o generar tus propias variantes.

## 📏 Cómo interpretar el resultado

| Aciertos | Lectura honesta |
|---|---|
| **7–8 de 8** | La parte está cerrada. Sigue a la siguiente. |
| **5–6** | Comprensión con huecos concretos: vuelve a las clases de los fallos, no a toda la parte. |
| **3–4** | Falta el concepto, no el detalle. Relee el README de la parte y las clases del bloque afectado. |
| **0–2** | Conviene rehacer la parte. Si además fallaste la anterior, el hueco viene de más atrás. |

> Estas baterías **no son una certificación** y ningún resultado se registra en ningún sitio. Miden
> comprensión para que tú decidas si sigues adelante. La evaluación con criterio de instructor está
> en la [rúbrica](../docs/rubrica-evaluacion.md) y en el [examen final por perfil](../docs/examen-final-por-perfil.md).
