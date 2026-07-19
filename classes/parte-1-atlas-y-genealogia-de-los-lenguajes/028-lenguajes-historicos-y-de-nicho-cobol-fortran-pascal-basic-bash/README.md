# Clase 028 — Lenguajes históricos y de nicho: COBOL, Fortran, Pascal, BASIC, Bash

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

El Atlas se cierra con un grupo que no forma una familia por parentesco sino por destino: lenguajes que marcaron una época y, en vez de desaparecer, se replegaron a un nicho donde siguen siendo insustituibles. **COBOL** (1959) todavía mueve las transacciones de bancos y aseguradoras; **Fortran** (1957) sostiene el cálculo científico de alto rendimiento; **Pascal** (1970) enseñó programación estructurada a generaciones enteras y dejó descendencia en Delphi; **BASIC** (1964) puso la programación al alcance de quien no era ingeniero y acompañó la llegada del ordenador personal; y **Bash** (1989) no es histórico en absoluto, sino la herramienta viva que orquesta la administración de sistemas y la integración continua de hoy.

Conocerlos aporta dos cosas distintas. Una es perspectiva histórica: casi todo lo que damos por evidente en un lenguaje moderno fue en su día una decisión discutida que alguno de estos tomó por primera vez. Sebesta organiza precisamente así su recorrido por la evolución de los lenguajes, mostrando que cada uno respondía a un problema concreto de su tiempo. La otra es una lección de ingeniería que se paga cara cuando se ignora: el software no se retira porque envejezca, sino cuando el coste de reemplazarlo baja del coste de mantenerlo, y en estos casos esa cuenta nunca ha salido. Entender por qué un lenguaje de 1959 sigue en producción crítica es entender cómo funciona de verdad la industria del software.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Situar cada lenguaje en su época, su motivación de diseño y su nicho actual.
2. Explicar con argumentos económicos y técnicos por qué algunos lenguajes "viejos" siguen en producción crítica.
3. Reconocer qué idea aportó cada uno que hoy damos por descontada.
4. Tratar Bash como habilidad transferible imprescindible y explicar su modelo de procesos y tuberías.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | COBOL: la banca | Miles de millones de líneas aún en producción |
| 2 | Pascal y BASIC | Enseñaron a programar a generaciones enteras |
| 3 | Fortran: la ciencia | El pionero que no se jubila |
| 4 | Bash: el pegamento vivo | Automatización y orquestación en Unix |
| 5 | Por qué sobreviven | La economía del reemplazo frente a la del mantenimiento |

## 📖 Definiciones y características

**COBOL** (COmmon Business-Oriented Language, comité CODASYL, 1959, con influencia decisiva de Grace Hopper y su lenguaje FLOW-MATIC) nació de una idea insólita para su tiempo: que el código de negocio debía poder leerlo alguien que no fuera programador. De ahí su sintaxis deliberadamente verbal, con sentencias que parecen frases en inglés y un programa dividido en secciones que declaran el entorno, los datos y el procedimiento por separado. Esa verbosidad, tan burlada después, resolvió un problema real de legibilidad y de división del trabajo. Pero la razón técnica de que COBOL siga vivo es otra y mucho menos conocida: su aritmética es **decimal de punto fijo**, no binaria de punto flotante. Cuando declaras un importe con un número exacto de dígitos enteros y decimales, las operaciones se hacen en base diez y no aparece el error de representación que hace que en tantos lenguajes `0.1 + 0.2` no dé exactamente `0.3` (el asunto de la clase 045). Para un sistema que suma millones de importes monetarios al día y debe cuadrar al céntimo, esa semántica no es un detalle: es el requisito. Los lenguajes modernos lo consiguen con tipos decimales de biblioteca; COBOL lo trae en su núcleo desde 1959.

**Fortran** (1957) y **Pascal** (1970) representan las dos grandes motivaciones opuestas del diseño de lenguajes. Fortran, que la clase 027 trata en detalle, se hizo para *ejecutar rápido* fórmulas matemáticas y demostró que un compilador podía generar código competitivo con el ensamblador escrito a mano; ese pragmatismo orientado al rendimiento explica que siga reinando en la simulación climática, la física computacional y las bibliotecas de álgebra lineal. Pascal, de Niklaus Wirth, se hizo para lo contrario: para *enseñar bien*. Wirth lo diseñó como vehículo de la programación estructurada que Dijkstra, Dahl y Hoare estaban defendiendo en esos años, con un tipado estricto, estructuras de control claras y una gramática pequeña que se puede tener entera en la cabeza. Nunca dominó la industria, pero su influencia es enorme: fijó la idea de que un lenguaje debe *impedir* ciertos errores en vez de limitarse a permitirlos, y su descendiente comercial Turbo Pascal, y después Delphi, movió una parte considerable del software de escritorio de los años noventa. Cuando hoy un compilador te rechaza una asignación entre tipos incompatibles, estás cobrando una herencia de Wirth.

**BASIC** (Kemeny y Kurtz, Dartmouth, 1964) tuvo la ambición más política del grupo: que cualquier estudiante, no solo los de ciencias e ingeniería, pudiera programar la computadora de la universidad a través de un sistema de tiempo compartido. Simplificó todo lo simplificable —líneas numeradas, pocas palabras clave, un intérprete que respondía de inmediato— y esa accesibilidad lo convirtió, una década más tarde, en el lenguaje que venía de fábrica en los microordenadores domésticos. Millones de personas escribieron su primer programa en BASIC. También arrastró la peor herencia de la época, el salto incondicional `GOTO` y el estado global, que la crítica de Dijkstra a la programación con saltos dejó definitivamente en evidencia; sus versiones posteriores lo abandonaron. **Bash** (Brian Fox, proyecto GNU, 1989, sucesor libre del Bourne shell de 1977) es el único del grupo que no es una reliquia: es el lenguaje en el que se escriben los scripts de despliegue, los ganchos de integración continua y la automatización diaria de cualquier sistema Unix. Su modelo es genuinamente distinto al de todos los demás lenguajes del curso, porque su unidad de composición no es la función sino el **proceso**: cada comando es un programa independiente con una entrada y una salida de texto, y la tubería `|` conecta la salida de uno con la entrada del siguiente. Kernighan y Pike construyen sobre esa idea todo *The Unix Programming Environment*: herramientas pequeñas que hacen una cosa bien y se combinan mediante flujos de texto. Es composición de funciones, pero a escala de sistema operativo, y por eso es tan transferible.

- **COBOL** — 1959 (comité CODASYL, Grace Hopper influyente), para negocios. Clave: aún sostiene núcleos bancarios y de seguros.
- **Pascal** — 1970 (Niklaus Wirth), diseñado para enseñar programación estructurada. Clave: claridad; padre de Delphi.
- **BASIC** — 1964 (Kemeny y Kurtz), pensado para principiantes. Clave: llevó la programación a los ordenadores personales.
- **Bash** — 1989 (Brian Fox, GNU), shell de Unix. Clave: automatización viva; su modelo de tuberías y procesos es muy transferible.

## 🧩 Situación

Un banco descubre que su sistema central de cuentas corre sobre varios millones de líneas de COBOL escritas a lo largo de cuatro décadas, y que el puñado de personas capaces de mantenerlo se está jubilando. La reacción intuitiva —"reescribámoslo en algo moderno"— tropieza con la realidad en cuanto se hacen los números. Ese código no es solo código: es la acumulación de miles de reglas de negocio, excepciones regulatorias y casos límite que nadie documentó nunca porque se descubrieron corrigiendo incidencias reales a lo largo de cuarenta años. Reescribirlo significa redescubrir todas esas reglas, y hacerlo sobre un sistema que no puede detenerse ni equivocarse en un solo céntimo. Los proyectos que lo han intentado suelen medirse en años y en centenares de millones, y varios han fracasado en público.

La lección no es que COBOL sea bueno ni que reescribir sea imposible, sino que el valor de un sistema en producción está en gran parte fuera del lenguaje: está en la corrección ya demostrada por décadas de uso. Por eso el criterio de la clase 014 se aplica también hacia atrás: el coste de cambiar de lenguaje incluye recuperar todo el conocimiento que el código viejo encapsula sin decirlo. Entender esto cambia cómo se mira el software "legado": no es un fracaso de mantenimiento, es un activo caro de sustituir.

## 🔎 Ejemplo

Bash es el más vigente de este grupo: su modelo de tuberías es puro y transferible.

```text
# Contar cuántos archivos .md hay, en una línea:
ls *.md | wc -l

# Tubería: la salida de un comando es la entrada del siguiente
cat notas.txt | grep "TODO" | sort | uniq
```

Mira la segunda línea con atención, porque contiene un modelo de programación completo. Se leen cuatro programas independientes, escritos por gente distinta en momentos distintos, que no se conocen entre sí y que sin embargo colaboran: uno emite el contenido del archivo, otro filtra las líneas que contienen `TODO`, otro las ordena y el último elimina duplicados. Nada de eso requirió una interfaz común, un formato compartido ni una biblioteca: basta con que todos acepten texto por su entrada y produzcan texto por su salida. Es exactamente la composición de funciones —`uniq(sort(grep(cat(x))))`— con el proceso como unidad y el texto como tipo universal.

El **delta** frente al resto del curso es doble y vale la pena nombrarlo. Por un lado, la composición ocurre entre programas del sistema operativo, no dentro de un programa, lo que permite reutilizar cualquier ejecutable de cualquier lenguaje: la tubería es una de las formas de interoperabilidad más antiguas y robustas que existen, y la Parte 10 la retoma. Por otro, el precio de esa universalidad es que el único tipo es el texto, así que no hay comprobación alguna de que un comando entienda lo que el anterior le manda; la seguridad de tipos se cambia por flexibilidad total. Ese intercambio es la clase de decisión de diseño que el Atlas entero enseña a reconocer.

## ✍️ Práctica

Escribe una tubería de Bash que, dado un archivo de texto, cuente cuántas líneas contienen la palabra 'error'. (Pista: `grep` y `wc`.) Cuando la tengas funcionando, haz dos extensiones que obligan a pensar en el modelo y no solo en los comandos: primero, haz que la búsqueda ignore mayúsculas y minúsculas, y averigua si eso se consigue añadiendo otro programa a la tubería o pasando una opción al que ya tienes —la respuesta te dice algo sobre cuándo componer y cuándo configurar—. Segundo, escribe en una frase la misma operación en forma de composición de funciones, como la escribirías en un lenguaje funcional, y compárala con la tubería: verás que la estructura es idéntica y que lo único que cambia es qué es una "función" en cada mundo.

## ⚠️ Errores comunes

- **Despreciar los lenguajes "viejos"** → causa: confundir antigüedad con inutilidad → solución: reconocer que COBOL y Fortran sostienen infraestructura crítica hoy, y que siguen ahí por razones técnicas y económicas concretas, no por inercia.
- **Subestimar Bash** → causa: verlo como una colección de comandos sueltos que se copian de internet → solución: aprender su modelo de procesos y tuberías, que es un paradigma de composición y una habilidad de uso diario.
- **Proponer reescribir un sistema legado sin contar el conocimiento que encierra** → causa: ver solo las líneas de código y no las reglas de negocio no documentadas que contienen → solución: valorar la corrección demostrada por décadas de producción como parte del coste de reemplazo.
- **Creer que la verbosidad de COBOL es un error de diseño** → causa: juzgar con criterios de hoy una decisión de 1959 → solución: entender que buscaba legibilidad para personas de negocio y que su aritmética decimal exacta resolvía un requisito que muchos lenguajes modernos aún necesitan emular con bibliotecas.

## ❓ Preguntas frecuentes

- **¿Vale la pena aprender COBOL?** Como nicho puede tener sentido: la escasez de expertos frente a una demanda estable lo hace bien pagado. Como base formativa, no: enseña poco que no aprendas mejor en otro sitio y su modelo mental no se transfiere a casi nada moderno.
- **¿Bash cuenta como lenguaje de programación?** Sí: tiene variables, condicionales, bucles, funciones y sustitución de comandos. Lo que lo hace peculiar es que su unidad de composición es el proceso y su único tipo de datos es el texto, algo que ningún otro lenguaje del curso comparte.
- **¿Qué queda hoy de Pascal?** Su descendencia directa (Delphi y Free Pascal) mantiene una comunidad activa, pero su verdadera herencia es conceptual: la idea de que un lenguaje debe impedir errores mediante tipos estrictos y estructuras de control claras pasó a Ada, Modula y, por esa vía, al diseño de casi todo lo que vino después.
- **¿Por qué no se reescriben de una vez estos sistemas?** Porque el coste no es proporcional a las líneas de código, sino al conocimiento no documentado que contienen y al riesgo de que el reemplazo falle en un sistema que no puede fallar. La estrategia habitual no es reescribir de golpe, sino envolver el núcleo tras una interfaz moderna y sustituirlo por partes.
- **¿Fortran y COBOL son lo mismo, "lenguajes viejos"?** Se parecen solo en la edad. Fortran optimiza cálculo numérico en coma flotante para ir lo más rápido posible; COBOL optimiza aritmética decimal exacta y procesamiento de registros para no perder un céntimo. Son respuestas opuestas a problemas opuestos, y por eso ninguno sustituyó al otro.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2: evolución de los lenguajes principales.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), sobre la composición como modelo de programación.

---

> [⏮️ Clase 027](../../parte-1-atlas-y-genealogia-de-los-lenguajes/027-familia-array-y-cientifica-apl-r-julia-fortran-matlab/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 029 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/029-que-es-un-toolchain-del-codigo-fuente-al-programa-que-corre/README.md)
