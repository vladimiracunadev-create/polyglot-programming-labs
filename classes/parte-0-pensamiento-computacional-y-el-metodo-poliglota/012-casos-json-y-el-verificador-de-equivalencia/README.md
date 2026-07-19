# Clase 012 — casos.json y el verificador de equivalencia

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Este curso hace una afirmación fuerte en cada clase: "estas diez implementaciones, escritas en diez lenguajes distintos, resuelven el mismo problema". Es una afirmación fácil de escribir y muy fácil de equivocar. Basta que la versión de Rust imprima `27000` donde las demás imprimen `27000.00`, o que la de C# use coma decimal porque tomó el idioma del sistema, para que la equivalencia prometida sea falsa aunque el texto siga diciendo lo contrario. El objetivo de esta clase es entender el mecanismo que convierte esa promesa en una comprobación: un archivo `casos.json` que fija el contrato de la clase y un verificador que ejecuta todas las implementaciones contra él.

La idea de fondo no es una ocurrencia del curso, sino una práctica de ingeniería con raíces profundas. Polya cierra su método de resolución de problemas con una cuarta fase que casi todo el mundo se salta: *volver atrás y revisar* la solución. Hunt y Thomas la convierten en hábito operativo en *The Pragmatic Programmer* cuando insisten en que todo lo que pueda comprobarse automáticamente debe comprobarse automáticamente, porque la disciplina humana se agota y la de una máquina no. Y Cormen y sus coautores, en *Introduction to Algorithms*, separan con cuidado la **especificación** de un problema —qué entra y qué debe salir— de cualquier algoritmo que lo resuelva; `casos.json` es exactamente esa especificación, escrita en un formato que una máquina puede leer.

## 🧩 Situación

Imagina que has escrito nueve implementaciones de una clase y estás satisfecho: las leíste todas, hacen lo mismo, se parecen. Añades la décima, en Rust, y la das por buena. Meses después, alguien estudia la clase, copia la versión de Rust y obtiene `27000` mientras el texto de la clase promete `27000.00`. No es un error del estudiante: es que nadie ejecutó nunca las diez juntas y comparó carácter a carácter. Leer código y creer que dos programas coinciden es un juicio humano, y los juicios humanos sobre igualdad de salidas son notoriamente malos: el ojo corrige, completa y perdona diferencias que una comparación de cadenas no perdona.

El verificador cambia la naturaleza del problema. Ya no se trata de confiar en que las implementaciones son equivalentes, sino de que el proyecto no puede publicar una clase donde no lo sean: si dos salidas difieren en un solo carácter, la integración continua se pone roja y el cambio no entra. La equivalencia deja de ser una afirmación editorial y pasa a ser una propiedad verificada del repositorio.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué contiene `casos.json` y qué contrato define para una clase.
2. Ejecutar el verificador sobre una clase e interpretar cada línea de su salida.
3. Entender por qué algunos lenguajes se omiten y por qué otros se marcan como ilustrativos.
4. Reconocer las causas típicas de una divergencia entre implementaciones (formato, locale, redondeo).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El contrato de una clase | Entrada por stdin, salida por stdout, casos esperados |
| 2 | El verificador | Alimenta cada caso a cada implementación y compara |
| 3 | Degradación silenciosa | Si falta un toolchain, se omite e informa |
| 4 | Divergencias típicas | Decimales, locale y saltos de línea |

## 📖 Definiciones y características

**`casos.json`** es el contrato de la clase. Contiene una descripción del problema, la fórmula o regla que lo resuelve en forma neutral y una lista de pares `{stdin, esperado}`: para esta entrada exacta, esta salida exacta. Su virtud es que está escrito **antes y por encima** de cualquier lenguaje: no menciona Python ni Go, solo texto que entra y texto que debe salir. Eso lo convierte en la fuente de verdad de la equivalencia, y también en la mejor forma de estudiar una clase, porque leerlo te dice qué hay que resolver sin contaminarte con cómo lo resuelve un lenguaje concreto. Es la misma separación que hacen Cormen y sus coautores entre el enunciado de un problema computacional y los algoritmos que lo satisfacen.

El **verificador de equivalencia** es el programa que da vida a ese contrato. Para cada implementación de la clase, la ejecuta con el toolchain que le corresponde —`python main.py`, `go run main.go`, `cc main.c -o main && ./main`—, le entrega cada `stdin` del archivo de casos y compara la salida obtenida con la esperada como **texto exacto**, sin tolerancias ni interpretaciones. Esa dureza es deliberada: una comparación numérica "aproximada" escondería precisamente los fenómenos que el curso quiere enseñar, como que un lenguaje redondee a la mitad par y otro hacia arriba, o que uno imprima `1e+06` donde otro imprime `1000000`. El verificador no juzga si el programa es bonito ni si es idiomático; juzga si observa el contrato, y solo eso.

Dos comportamientos del verificador merecen explicación aparte porque suelen malinterpretarse. El primero es la **degradación silenciosa**: si en tu máquina no está instalado el compilador de Rust, el verificador no falla, sino que omite esa implementación e informa de la omisión. Es la diferencia entre "esta implementación está mal" y "no pude comprobarla", y confundirlas haría el curso inutilizable para quien no tenga los diez toolchains. El segundo es la marca **ilustrativa**, que se aplica a implementaciones que no participan del contrato por stdin: SQL es el caso obvio, porque es declarativo y no lee un flujo de entrada como los demás, sino que consulta datos que ya están ahí. Su implementación muestra la misma idea sobre una tabla de casos y se exhibe sin compararse igual, no porque valga menos, sino porque su paradigma cambia el contrato. Esa es, en el vocabulario de la clase 002, una diferencia paradigmática, y el verificador la reconoce en lugar de fingir que no existe.

## 🔎 Ejemplo

Salida real del verificador sobre la clase 041 en una máquina donde falta el toolchain de Go:

```text
✅ python      3/3 casos
✅ javascript  3/3 casos
✅ java        3/3 casos
⏭️  go          omitido (toolchain 'go' no disponible)
ℹ️  sql         ilustrativa (declarativa, sin stdin)
```

Comando: `python scripts/verificar_equivalencia.py 041`

Léela línea a línea, porque cada símbolo significa algo distinto. El ✅ dice que la implementación se ejecutó con los tres casos y las tres salidas coincidieron carácter a carácter con lo esperado. El ⏭️ no es un aprobado ni un suspenso: es un "no comprobado", y conviene tenerlo presente al leer un informe con muchas omisiones, porque una clase verde en tu máquina con seis omisiones está mucho menos verificada que la misma clase en el servidor de integración continua, donde están los diez toolchains. El ℹ️ marca la implementación ilustrativa. Un fallo, en cambio, se vería así: `❌ rust 2/3 casos — esperado '27000.00', obtenido '27000'`, y ese mensaje ya contiene el diagnóstico completo, porque te dice qué caso, qué querías y qué obtuviste.

## ✍️ Práctica

Ejecuta `python scripts/verificar_equivalencia.py 041` en tu máquina y responde tres preguntas por escrito:

1. ¿Qué lenguajes verificó de verdad y cuáles omitió por falta de toolchain? Anota el número real de implementaciones comprobadas: es la medida honesta de cuánto verificó tu ejecución.
2. Abre el `casos.json` de esa clase y localiza, para cada caso, la entrada y la salida esperada. Predice mentalmente la salida antes de mirarla: estás haciendo a mano lo que el verificador hace en milisegundos.
3. Copia una implementación a un archivo aparte y estropéala a propósito, por ejemplo imprimiendo un decimal de más. Vuelve a correr el verificador sobre el original para confirmar que sigue en verde y observa qué aspecto tendría el rojo.

## ⚠️ Errores comunes

| Síntoma / creencia | Causa y cómo corregirlo |
|--------------------|--------------------------|
| "Seguro que son equivalentes, se parecen mucho" | El ojo humano perdona diferencias que una comparación de texto no perdona. Ejecuta el verificador: la máquina no se cansa de comparar |
| Una implementación imprime `27000,00` y las demás `27000.00` | El programa tomó el separador decimal del idioma del sistema. Fija la cultura invariante y el número de decimales en todas las implementaciones |
| Salida con un salto de línea de más o de menos | Un `println` donde tocaba `print`, o `\r\n` en Windows. La comparación es exacta: cuida también los caracteres invisibles |
| Interpretar un ⏭️ como un aprobado | Omitido significa no comprobado. Cuenta cuántas implementaciones se verificaron realmente antes de dar la clase por buena |
| Cambiar `casos.json` para que la implementación pase | Es invertir el contrato: el código debe satisfacer la especificación, no al revés. Corrige el programa |

## ❓ Preguntas frecuentes

**❓ ¿Qué NO verifica el verificador?** El texto de las clases y del Atlas, que es material de lectura y no se ejecuta. Tampoco juzga la calidad, la eficiencia ni el carácter idiomático del código: solo comprueba el comportamiento observable en la frontera stdin/stdout. Un programa lento y feo que produzca la salida correcta pasa; uno elegante que imprima un decimal de más, no.

**❓ ¿Por qué SQL es ilustrativa y no se compara igual?** Porque es declarativo: no consume un flujo de entrada línea a línea, sino que expresa el resultado como una consulta sobre datos existentes. Forzarlo al contrato de stdin exigiría envolverlo en otro lenguaje y ya no estaríamos mostrando SQL, sino ese envoltorio. Se prefiere exhibir la misma fórmula como consulta y ser explícitos sobre la diferencia.

**❓ ¿Por qué comparar texto exacto y no valores numéricos con tolerancia?** Porque una comparación tolerante escondería justo lo que el curso quiere enseñar. Las diferencias de formato, redondeo y localización entre lenguajes son contenido, no ruido: si el verificador las perdonara, la clase 045 sobre punto flotante perdería su mejor evidencia.

**❓ ¿Esto es lo mismo que una prueba unitaria?** En esencia sí, y la clase 038 lo desarrolla: hay una entrada fija, una salida esperada y una comparación automática. La particularidad aquí es que la misma prueba se aplica a diez programas escritos en diez lenguajes, de modo que no comprueba solo la corrección de cada uno, sino la **equivalencia** entre todos.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), cuarta fase: revisar la solución obtenida.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre automatizar toda comprobación repetible.
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. 1: especificación de un problema frente a algoritmo.

---

> [⏮️ Clase 011](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/011-anatomia-de-una-ficha-de-transferencia-y-como-estudiarla/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 013 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/013-el-concepto-en-la-familia-leer-un-lenguaje-que-no-conoces/README.md)
