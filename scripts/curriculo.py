"""Fuente de verdad del currículo de Polyglot Programming Labs.

Describe las 12 partes y las 176 clases. Los scripts generadores lo importan.
Cada clase es un título (str) o una tupla (título, datos). Las clases de la
Parte 0 llevan datos completos con tipo "metodo" (contenido conceptual, sin
implementaciones de código); el generador las renderiza al README completo.
"""

from __future__ import annotations

import re
import unicodedata

NUCLEO = ["python", "javascript", "typescript", "java", "csharp",
          "go", "rust", "c", "sql", "php"]

FAMILIAS_ATLAS = [
    "C / llaves", "scripting dinámico", "JVM", ".NET", "JavaScript / web",
    "funcional tipada (ML)", "Lisp", "lógica y declarativa",
    "concurrente / actor", "sistemas", "array / científica", "históricos",
]


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    t = t.replace("+", " plus ").replace("#", " sharp ").replace("/", " ")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


# --------------------------------------------------------------------------- #
# Parte 0 — contenido completo (tipo "metodo")
# --------------------------------------------------------------------------- #

P0 = [
    ("Qué es programar y por qué comparar lenguajes: la tesis políglota", {
        "tipo": "metodo",
        "objetivo": "Entender que programar es resolver problemas con instrucciones precisas, y que ese conocimiento es **transferible**: un mismo concepto (una variable, un bucle, una función) existe en todos los lenguajes; lo que cambia es la forma. Aprenderlo una vez permite reconocerlo, compararlo y aplicarlo en cualquier lenguaje.",
        "resultados": [
            "Explicar la diferencia entre aprender *un* lenguaje y aprender *a programar*.",
            "Enunciar la tesis políglota: concepto → forma neutral → implementaciones → comparación → transferencia.",
            "Distinguir el conocimiento transferible del detalle sintáctico de un lenguaje.",
            "Justificar por qué comparar lenguajes acelera el aprendizaje en vez de dispersarlo.",
        ],
        "temas": [
            ("Programar = resolver con precisión", "Separa la idea (algoritmo) de su escritura (lenguaje)"),
            ("Concepto vs. sintaxis", "Lo que perdura frente a lo que cambia entre lenguajes"),
            ("Los 10 lenguajes del núcleo", "El terreno práctico que se implementa y verifica"),
            ("Las ~40 familias del Atlas", "Amplían la comprensión sin multiplicar el mantenimiento"),
            ("Reconocer, comparar, aplicar", "El ciclo que convierte teoría en habilidad"),
        ],
        "definiciones": [
            ("Programar", "expresar la solución de un problema como instrucciones que una máquina ejecuta. Clave: la idea es independiente del lenguaje."),
            ("Conocimiento transferible", "idea que sobrevive al cambio de lenguaje (p. ej. 'iterar una colección'). Clave: es lo que de verdad se aprende."),
            ("Núcleo", "los 10 lenguajes que se implementan y verifican en CI. Clave: profundidad práctica."),
            ("Atlas", "cobertura de ~40 lenguajes por sus características. Clave: amplitud de comprensión."),
        ],
        "situacion": "Alguien aprende Python, hace 50 ejercicios y se siente capaz. Le piden mantener un servicio en Go. Se bloquea: cree que no sabe programar, cuando en realidad **sí** sabe — solo no reconoce los mismos conceptos con otra piel. Este programa ataca justamente eso.",
        "ejemplo": "El mismo concepto (\"guardar un valor con nombre\") en tres lenguajes:\n\n```text\nPython:  total = 27000\nGo:      total := 27000\nRust:    let total = 27000;\n```\n\nCambia la escritura, **no** la idea: un nombre apunta a un valor. Eso es lo transferible.",
        "practica": "Escribe en una frase, sin usar ningún lenguaje, qué hace este programa: `precio * cantidad`. Luego búscalo escrito en dos lenguajes que conozcas y subraya qué es idéntico y qué cambia.",
        "errores": [
            ("Creer que \"sé Python\" = \"sé programar\"", "confundir el lenguaje con la disciplina", "estudiar el concepto y luego reconocerlo en otro lenguaje"),
            ("Memorizar sintaxis sin el concepto detrás", "aprender la forma sin el fondo", "para cada línea, preguntar \"¿qué idea neutral expresa?\""),
        ],
        "faq": [
            ("¿Necesito saber los 10 lenguajes antes de empezar?", "No. Empiezas por el concepto; los lenguajes se introducen comparándolos."),
            ("¿No es más fácil dominar uno solo?", "Para tu primer empleo, quizá. Para entender de verdad la programación, comparar revela por qué cada lenguaje decide lo que decide."),
        ],
    }),
    ("Las tres clases de diferencia: sintáctica, semántica y paradigmática", {
        "tipo": "metodo",
        "objetivo": "Dar el marco que se usa en **cada** comparación del curso. Cuando dos lenguajes difieren, la diferencia es de una de tres clases: sintáctica (se escribe distinto pero significa lo mismo), semántica (cambia el comportamiento, el tipo, la memoria) o paradigmática (invita a estructurar la solución de otra manera).",
        "resultados": [
            "Clasificar una diferencia entre lenguajes como sintáctica, semántica o paradigmática.",
            "Dar ejemplos propios de cada clase de diferencia.",
            "Explicar por qué confundirlas lleva a traducir mecánicamente en vez de programar idiomáticamente.",
        ],
        "temas": [
            ("Diferencia sintáctica", "La más superficial: solo cambia cómo se escribe"),
            ("Diferencia semántica", "Cambia qué ocurre: tipos, mutabilidad, memoria, errores"),
            ("Diferencia paradigmática", "Cambia cómo se piensa la solución"),
            ("Traducción vs. idiomática", "Por qué copiar sintaxis produce código antinatural"),
        ],
        "definiciones": [
            ("Diferencia sintáctica", "distinta escritura, mismo significado esencial. Clave: la más fácil de salvar."),
            ("Diferencia semántica", "distinto comportamiento observable. Clave: la que causa bugs al portar código."),
            ("Diferencia paradigmática", "distinta forma de estructurar el problema. Clave: exige cambiar de mentalidad."),
            ("Código idiomático", "solución escrita como la escribiría un experto de ese lenguaje. Clave: aprovecha el paradigma."),
        ],
        "situacion": "Portas un bucle de JavaScript a Rust cambiando solo las llaves y los `;`. Compila… pero el programa se comporta distinto porque en Rust el valor se *movió* y ya no puedes usarlo. No era una diferencia sintáctica: era semántica.",
        "ejemplo": "```text\nSintáctica:   for (i=0;i<n;i++)      vs   for i in range(n)\n              (mismo bucle, otra escritura)\n\nSemántica:    x = y (copia en C)     vs   x = y (mueve en Rust)\n              (misma escritura, otro comportamiento)\n\nParadigmática: recorrer una lista con un bucle\n              vs   describir el resultado con SQL (SELECT ...)\n```",
        "practica": "Toma `a == b`. En Java compara referencias para objetos; en Python compara valor. ¿De qué clase de diferencia se trata? (Respuesta: semántica.)",
        "errores": [
            ("Portar código cambiando solo la sintaxis", "asumir que todo es sintáctico", "verificar siempre si hay diferencia semántica (tipos, memoria, mutabilidad)"),
            ("Forzar el estilo de un lenguaje en otro", "ignorar el paradigma destino", "escribir idiomático: adaptar la estructura, no solo las palabras"),
        ],
        "faq": [
            ("¿Cuál es la más peligrosa?", "La semántica: el código compila y parece correcto, pero se comporta distinto."),
            ("¿Y la paradigmática se puede evitar?", "A veces sí (imperativo en casi todos), pero perderías la ventaja del lenguaje destino."),
        ],
    }),
    ("Problema, contexto, entradas, proceso y salidas", {
        "tipo": "metodo",
        "objetivo": "Antes de escribir una línea de código hay que **modelar** el problema: qué entra, qué sale, bajo qué reglas y en qué contexto. Ese modelo es independiente del lenguaje y es lo primero que define cada ficha del curso.",
        "resultados": [
            "Descomponer un problema en entradas, proceso y salidas.",
            "Identificar el contexto y las restricciones que condicionan la solución.",
            "Escribir la especificación de un problema sin mencionar ningún lenguaje.",
        ],
        "temas": [
            ("Entradas", "Qué datos recibe el programa y de qué tipo"),
            ("Proceso", "Qué transformación ocurre entre entrada y salida"),
            ("Salidas", "Qué produce y cómo se observa el resultado"),
            ("Contexto y restricciones", "Condiciones que limitan las soluciones válidas"),
        ],
        "definiciones": [
            ("Especificación", "descripción de *qué* debe hacer un programa, no *cómo*. Clave: neutral al lenguaje."),
            ("Entrada", "dato que el programa recibe. Clave: define el dominio del problema."),
            ("Salida", "resultado observable. Clave: es lo que se verifica con casos.json."),
            ("Restricción", "condición que la solución debe respetar. Clave: acota el espacio de soluciones."),
        ],
        "situacion": "\"Calcula el total de una venta.\" Suena trivial, pero: ¿el descuento es porcentaje o monto? ¿la cantidad puede ser 0? ¿el total lleva impuesto? Sin modelar entradas, proceso y salidas, dos personas resuelven problemas distintos.",
        "ejemplo": "Especificación del problema de la venta (neutral al lenguaje):\n\n```text\nEntrada:  precio_unitario (real ≥ 0), cantidad (entero ≥ 0), descuento (real 0..1)\nProceso:  total = precio_unitario * cantidad * (1 - descuento)\nSalida:   \"Total: <total con 2 decimales>\"\nLímite:   cantidad = 0  ⇒  total = 0.00\n```\n\nEsta es la base de la clase 041, idéntica para los 10 lenguajes.",
        "practica": "Especifica (entrada/proceso/salida/límite) el problema \"contar cuántas palabras tiene una frase\". No escribas código.",
        "errores": [
            ("Empezar a codificar sin especificar", "saltarse el modelo", "escribir entrada/proceso/salida antes de tocar el teclado"),
            ("Olvidar los casos límite", "pensar solo el caso feliz", "listar valores extremos (0, vacío, negativo) en la especificación"),
        ],
        "faq": [
            ("¿Por qué no empezar a programar directo?", "Porque el 80% de los bugs nacen de un problema mal entendido, no de mala sintaxis."),
            ("¿La especificación cambia por lenguaje?", "No: es la parte que permanece. Por eso los casos.json sirven para los 10."),
        ],
    }),
    ("Descomposición y reconocimiento de patrones", {
        "tipo": "metodo",
        "objetivo": "Aprender a partir un problema grande en subproblemas manejables (descomposición) y a notar cuándo un subproblema ya lo resolviste antes con otra forma (reconocimiento de patrones). Son las dos habilidades que hacen escalable la programación.",
        "resultados": [
            "Descomponer un problema en subproblemas independientes.",
            "Reconocer un patrón repetido y nombrarlo.",
            "Explicar cómo la descomposición se traduce en funciones y módulos.",
        ],
        "temas": [
            ("Descomposición", "Divide y vencerás: partes pequeñas se resuelven y prueban solas"),
            ("Reconocimiento de patrones", "Reutilizar una solución conocida ahorra trabajo y errores"),
            ("De subproblema a función", "La descomposición prefigura la modularidad (Parte 5)"),
        ],
        "definiciones": [
            ("Descomposición", "dividir un problema en subproblemas más simples. Clave: cada parte se resuelve y verifica por separado."),
            ("Patrón", "estructura de solución que reaparece en problemas distintos. Clave: reconocerlo evita reinventar."),
            ("Abstracción de subproblema", "tratar un subproblema resuelto como una caja negra. Clave: reduce la carga mental."),
        ],
        "situacion": "\"Genera un reporte de ventas en PDF.\" Enorme. Descompuesto: (1) leer datos, (2) calcular totales, (3) dar formato, (4) exportar a PDF. Cada pieza es un problema conocido; el patrón \"leer → transformar → escribir\" reaparece en casi todo software.",
        "ejemplo": "```text\nProblema: promedio de las notas aprobadas\nDescomposición:\n  1. filtrar las notas >= 4      (patrón: filtrar)\n  2. sumar las que quedaron      (patrón: reducir)\n  3. dividir entre cuántas son   (patrón: contar)\n```\n\nLos patrones filtrar/reducir/contar reaparecen en la Parte 4 (map/filter/reduce).",
        "practica": "Descompón \"corregir automáticamente un test de opción múltiple\" en 3-4 subproblemas y nombra el patrón de cada uno.",
        "errores": [
            ("Resolver todo en una sola función gigante", "no descomponer", "extraer cada subproblema a su propia función"),
            ("No ver que dos partes son el mismo patrón", "falta de reconocimiento", "preguntar \"¿esto se parece a algo que ya resolví?\""),
        ],
        "faq": [
            ("¿Cuánto descomponer?", "Hasta que cada parte quepa en tu cabeza y se pueda probar sola."),
            ("¿Los patrones son los 'patrones de diseño'?", "Aquí es más básico: estructuras de solución. Los patrones de diseño formales llegan en la Parte 9."),
        ],
    }),
    ("Abstracción, restricciones y casos límite", {
        "tipo": "metodo",
        "objetivo": "Dominar tres herramientas del pensamiento: la abstracción (quedarse con lo esencial e ignorar el detalle), las restricciones (las reglas que la solución debe cumplir) y los casos límite (las entradas extremas donde los programas suelen fallar).",
        "resultados": [
            "Abstraer un problema quedándote con lo relevante.",
            "Enumerar las restricciones explícitas e implícitas de un problema.",
            "Identificar los casos límite antes de programar.",
        ],
        "temas": [
            ("Abstracción", "Ignorar el ruido para razonar sobre lo esencial"),
            ("Restricciones", "Definen qué soluciones son válidas"),
            ("Casos límite", "El vacío, el cero, el negativo, el máximo: donde se rompen los programas"),
        ],
        "definiciones": [
            ("Abstracción", "representar solo los aspectos relevantes de algo. Clave: un mapa no es el territorio, y por eso es útil."),
            ("Restricción", "condición que la solución debe respetar (rango, formato, rendimiento). Clave: acota lo válido."),
            ("Caso límite", "entrada extrema o inusual (vacío, 0, negativo, enorme). Clave: donde nacen la mayoría de los bugs."),
        ],
        "situacion": "Un programa suma precios y funciona perfecto en las demos. En producción falla: llegó una lista vacía y dividió entre cero al calcular el promedio. El caso límite \"lista vacía\" no se pensó.",
        "ejemplo": "```text\nProblema: promedio de una lista de números\nAbstracción: solo importan los números, no de dónde vienen\nRestricción: el resultado es un real\nCasos límite:\n  - lista vacía      ⇒ ¿0? ¿error? (¡hay que decidirlo!)\n  - un solo elemento ⇒ el promedio es ese elemento\n  - números enormes  ⇒ ¿desbordamiento?\n```",
        "practica": "Para \"buscar el mayor de una lista\", enumera 3 casos límite y decide qué hace el programa en cada uno.",
        "errores": [
            ("Probar solo el caso feliz", "olvidar los extremos", "escribir los casos límite en casos.json desde el inicio"),
            ("Abstraer de más o de menos", "quedarse sin datos clave o con ruido", "revisar que la abstracción conserve lo que el problema necesita"),
        ],
        "faq": [
            ("¿Los casos límite son los tests?", "Son la semilla de los tests: cada caso límite debería ser un caso de prueba."),
            ("¿Cómo sé si abstraje bien?", "Si puedes resolver el problema con tu abstracción sin volver a los detalles, está bien."),
        ],
    }),
    ("Algoritmos: corrección y terminación", {
        "tipo": "metodo",
        "objetivo": "Entender qué es un algoritmo y las dos propiedades que lo hacen fiable: **corrección** (produce el resultado correcto para toda entrada válida) y **terminación** (siempre acaba, no se queda en un bucle infinito).",
        "resultados": [
            "Definir algoritmo y sus propiedades esenciales.",
            "Argumentar informalmente por qué un algoritmo es correcto.",
            "Detectar por qué un bucle podría no terminar.",
        ],
        "temas": [
            ("Qué es un algoritmo", "Una receta precisa y finita de pasos"),
            ("Corrección", "Da la respuesta correcta para toda entrada válida"),
            ("Terminación", "Siempre acaba; el bucle avanza hacia su fin"),
            ("Invariante y variante", "Herramientas para razonar sobre bucles"),
        ],
        "definiciones": [
            ("Algoritmo", "secuencia finita y precisa de pasos que resuelve un problema. Clave: finita y sin ambigüedad."),
            ("Corrección", "el algoritmo produce la salida especificada para toda entrada válida. Clave: se argumenta, no se supone."),
            ("Terminación", "el algoritmo acaba en un número finito de pasos. Clave: algo debe decrecer hacia un límite."),
            ("Invariante de bucle", "condición verdadera en cada vuelta del bucle. Clave: prueba la corrección."),
        ],
        "situacion": "Un algoritmo de búsqueda binaria es rapidísimo… hasta que alguien escribe `fin = medio` en vez de `fin = medio - 1` y el bucle deja de decrecer: nunca termina. Terminación no es un detalle.",
        "ejemplo": "```text\nALGORITMO mayor(lista):\n    mayor <- lista[0]           # invariante: 'mayor' es el máximo de lo visto\n    PARA cada x en lista[1..]:\n        SI x > mayor: mayor <- x\n    DEVOLVER mayor\n\nTerminación: la lista es finita ⇒ el bucle da pasos finitos.\nCorrección: el invariante garantiza que al final 'mayor' es el máximo total.\n```",
        "practica": "Escribe un algoritmo que cuente cuántos números pares hay en una lista y argumenta en una frase por qué termina.",
        "errores": [
            ("Bucle que no decrece", "el índice o la condición no avanzan hacia el fin", "asegurar que algo cambia en cada vuelta acercándose al límite"),
            ("Asumir corrección sin argumentar", "confiar en que 'parece bien'", "buscar el invariante que lo garantiza"),
        ],
        "faq": [
            ("¿Hay que demostrar formalmente todo?", "No en este curso: basta un argumento informal claro de por qué es correcto y termina."),
            ("¿Un programa que no termina siempre es un bug?", "Casi siempre. Excepción: servicios que corren en un bucle eventos a propósito."),
        ],
    }),
    ("Pseudocódigo neutral: escribir sin lenguaje", {
        "tipo": "metodo",
        "objetivo": "Aprender a expresar un algoritmo en **pseudocódigo**: una notación legible, independiente de cualquier lenguaje, que captura la lógica sin comprometerse con una sintaxis. Es el puente entre la idea y las 10 implementaciones.",
        "resultados": [
            "Escribir un algoritmo en pseudocódigo claro y neutral.",
            "Traducir pseudocódigo a cualquier lenguaje del núcleo.",
            "Evitar el 'pseudocódigo' que en realidad es un lenguaje disfrazado.",
        ],
        "temas": [
            ("Convenciones del pseudocódigo", "Un vocabulario mínimo y consistente"),
            ("Neutralidad", "No favorecer la sintaxis de ningún lenguaje"),
            ("Del pseudocódigo al código", "Cómo cada lenguaje 'rellena' la misma lógica"),
        ],
        "definiciones": [
            ("Pseudocódigo", "descripción de un algoritmo en lenguaje estructurado pero informal. Clave: legible por humanos, neutral."),
            ("Notación neutral", "sin sintaxis específica de un lenguaje real. Clave: se traduce igual de fácil a los 10."),
            ("Asignación (<-)", "dar un valor a un nombre. Clave: convención neutral en vez de `=`, `:=` o `let`."),
        ],
        "situacion": "En una entrevista te piden 'resolverlo en el lenguaje que quieras'. Si primero escribes el pseudocódigo, la traducción a Python, Java o Go es mecánica; si vas directo al código, te enredas con la sintaxis y pierdes la lógica.",
        "ejemplo": "El mismo algoritmo en pseudocódigo neutral, listo para traducir:\n\n```text\nLEER precio, cantidad, descuento\nsubtotal <- precio * cantidad\ntotal    <- subtotal * (1 - descuento)\nESCRIBIR \"Total: \" + FORMATEAR(total, 2 decimales)\n```\n\nCompara con las implementaciones reales en la [clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md).",
        "practica": "Escribe en pseudocódigo el algoritmo \"invertir una cadena de texto\". No uses funciones específicas de ningún lenguaje.",
        "errores": [
            ("Pseudocódigo que es Python disfrazado", "usar `for i in range` y métodos reales", "usar PARA/MIENTRAS/SI y verbos neutrales (LEER, ESCRIBIR)"),
            ("Demasiado detalle o demasiado vago", "perder la lógica en ruido o en ambigüedad", "capturar cada paso esencial, sin sintaxis"),
        ],
        "faq": [
            ("¿Hay un estándar de pseudocódigo?", "No universal. Este curso usa <-, PARA, MIENTRAS, SI, LEER, ESCRIBIR de forma consistente."),
            ("¿Siempre debo escribirlo?", "Para problemas nuevos o difíciles, sí. Para triviales, va en tu cabeza."),
        ],
    }),
    ("Trazado manual y ejecución simbólica", {
        "tipo": "metodo",
        "objetivo": "Aprender a 'ejecutar' un algoritmo con papel y lápiz: seguir el valor de cada variable paso a paso (trazado) para verificar que hace lo que crees, antes de ejecutarlo en una máquina. Es la habilidad de depuración más fundamental.",
        "resultados": [
            "Trazar la ejecución de un algoritmo con una tabla de variables.",
            "Detectar un error de lógica sin ejecutar el programa.",
            "Predecir la salida de un fragmento leyéndolo.",
        ],
        "temas": [
            ("Tabla de trazado", "Registrar el estado de las variables vuelta a vuelta"),
            ("Ejecución simbólica", "Razonar con valores generales, no solo concretos"),
            ("Trazar para depurar", "Encontrar el error donde el estado se desvía"),
        ],
        "definiciones": [
            ("Trazado", "seguir a mano el valor de cada variable en cada paso. Clave: revela dónde se desvía la lógica."),
            ("Estado", "el conjunto de valores de todas las variables en un instante. Clave: el programa avanza cambiando el estado."),
            ("Ejecución simbólica", "trazar con símbolos (x, n) en vez de números concretos. Clave: cubre todos los casos a la vez."),
        ],
        "situacion": "Tu bucle debería sumar 1+2+3 = 6 pero devuelve 3. En vez de ejecutar 20 veces cambiando cosas al azar, trazas a mano: descubres que inicializas `suma` dentro del bucle, reiniciándola cada vuelta.",
        "ejemplo": "Trazado de `suma <- 0; PARA i en 1..3: suma <- suma + i`:\n\n```text\npaso | i | suma\n-----|---|-----\ninic | - | 0\n  1  | 1 | 1\n  2  | 2 | 3\n  3  | 3 | 6   ⇐ salida\n```",
        "practica": "Traza a mano `x <- 5; MIENTRAS x > 0: ESCRIBIR x; x <- x - 2`. ¿Qué imprime? ¿Termina?",
        "errores": [
            ("Depurar cambiando cosas al azar", "no entender el estado real", "trazar a mano hasta ver dónde se desvía"),
            ("Trazar solo un caso concreto", "no generalizar", "usar ejecución simbólica para cubrir todos los casos"),
        ],
        "faq": [
            ("¿No es más rápido usar el debugger?", "El debugger traza por ti, pero si no sabes trazar, no entiendes lo que muestra."),
            ("¿Cuándo trazar?", "Cuando un resultado te sorprende: el trazado localiza el paso exacto del error."),
        ],
    }),
    ("Complejidad y eficiencia: intuición de coste", {
        "tipo": "metodo",
        "objetivo": "Desarrollar la intuición de cuánto 'cuesta' un algoritmo en tiempo y memoria según crece la entrada, usando la notación O-grande de forma práctica. No es matemática por deporte: es saber por qué un programa que va bien con 100 datos se cae con 10 millones.",
        "resultados": [
            "Estimar el orden de crecimiento (O(1), O(n), O(n²)) de un algoritmo simple.",
            "Comparar dos soluciones por su coste, no solo por si funcionan.",
            "Reconocer el bucle anidado como fuente típica de O(n²).",
        ],
        "temas": [
            ("Crecimiento con la entrada", "Lo que importa es cómo escala, no el tiempo en un caso"),
            ("O(1), O(n), O(n²), O(log n)", "El vocabulario para comparar costes"),
            ("Tiempo vs. memoria", "A veces se cambia uno por el otro"),
        ],
        "definiciones": [
            ("Complejidad temporal", "cómo crece el número de operaciones con el tamaño de la entrada. Clave: se mide el orden, no los segundos."),
            ("O-grande", "cota superior del crecimiento (O(n), O(n²)…). Clave: describe el peor caso al escalar."),
            ("Bucle anidado", "un bucle dentro de otro. Clave: suele producir O(n²); vigílalo."),
        ],
        "situacion": "Dos funciones ordenan una lista. Con 10 elementos ambas tardan 'nada'. Con un millón, una tarda 1 segundo y la otra, 3 horas. La diferencia no se ve en la demo: se ve en el orden de complejidad, O(n log n) vs. O(n²).",
        "ejemplo": "```text\nBuscar en lista NO ordenada  ⇒ recorrer todo        ⇒ O(n)\nBuscar en lista ordenada     ⇒ búsqueda binaria    ⇒ O(log n)\nComparar todos con todos     ⇒ bucle dentro de bucle ⇒ O(n²)\nAcceder a lista[i]           ⇒ directo             ⇒ O(1)\n```",
        "practica": "¿Cuál es el orden de un algoritmo que, para cada persona de una lista, la compara con todas las demás? (Pista: bucle anidado.)",
        "errores": [
            ("Medir con entradas pequeñas", "el coste solo se nota al escalar", "razonar el orden, no cronometrar un caso chico"),
            ("Optimizar sin medir", "atacar lo que no es el cuello de botella", "primero identificar el orden dominante, luego optimizar"),
        ],
        "faq": [
            ("¿Siempre gana el de menor O?", "Para entradas grandes, sí. Para pequeñas, un O(n²) simple puede ganar a un O(n log n) complejo."),
            ("¿Necesito las matemáticas formales?", "Aquí basta la intuición: contar cuántas veces se repite el trabajo al crecer n."),
        ],
    }),
    ("Legibilidad, estilo e idiomática", {
        "tipo": "metodo",
        "objetivo": "Entender que el código se lee muchas más veces de las que se escribe, y que cada lenguaje tiene su forma 'idiomática' (la que un experto reconoce como natural). Escribir legible e idiomático no es estética: es mantenibilidad.",
        "resultados": [
            "Explicar por qué la legibilidad importa más que la brevedad.",
            "Reconocer código idiomático frente a una traducción mecánica.",
            "Aplicar nombres y estructura que comuniquen intención.",
        ],
        "temas": [
            ("El código se lee más que se escribe", "Optimizar para quien lo lea (incluido tu yo futuro)"),
            ("Idiomática por lenguaje", "Lo natural en Python no lo es en Go"),
            ("Nombres que comunican", "Un buen nombre ahorra un comentario"),
        ],
        "definiciones": [
            ("Legibilidad", "facilidad con que un humano entiende el código. Clave: prima sobre la astucia."),
            ("Idiomática", "escribir como lo haría un experto del lenguaje. Clave: aprovecha sus convenciones y su paradigma."),
            ("Código listo (clever)", "código ingenioso pero difícil de leer. Clave: casi siempre es un error de criterio."),
        ],
        "situacion": "Un desarrollador escribe en Python un bucle `for i in range(len(lista))` para acceder por índice, como haría en C. Funciona, pero cualquier pythonista escribiría `for x in lista`. La versión idiomática se lee y se mantiene mejor.",
        "ejemplo": "```text\nNo idiomático (Python, estilo C):\n    for i in range(len(nombres)):\n        print(nombres[i])\n\nIdiomático (Python):\n    for nombre in nombres:\n        print(nombre)\n```\n\nMismo resultado; el segundo comunica la intención sin ruido.",
        "practica": "Busca un fragmento tuyo de hace meses. ¿Lo entiendes en 10 segundos? Reescríbelo para que sí, cambiando nombres y estructura.",
        "errores": [
            ("Priorizar líneas cortas sobre claridad", "confundir brevedad con calidad", "preferir lo legible aunque ocupe una línea más"),
            ("Escribir todos los lenguajes con el mismo estilo", "ignorar la idiomática", "aprender las convenciones de cada lenguaje del núcleo"),
        ],
        "faq": [
            ("¿La idiomática es subjetiva?", "Menos de lo que parece: cada comunidad tiene guías de estilo (PEP 8, gofmt, rustfmt)."),
            ("¿Legible o rápido?", "Legible por defecto; rápido solo donde midas que hace falta."),
        ],
    }),
    ("Anatomía de una ficha de transferencia y cómo estudiarla", {
        "tipo": "metodo",
        "objetivo": "Conocer la unidad de estudio del curso: la **ficha de transferencia** (cada clase de código). Verás qué secciones tiene, en qué orden estudiarlas y cómo usarlas para aprender un concepto una vez y aplicarlo en 10 lenguajes.",
        "resultados": [
            "Nombrar las secciones de una clase y para qué sirve cada una.",
            "Seguir el flujo de estudio: concepto → pseudocódigo → implementaciones → comparación → transferencia.",
            "Usar casos.json y el verificador para comprobar tu comprensión.",
        ],
        "temas": [
            ("Estructura de una clase", "Objetivo, modelo, algoritmo, implementaciones, comparación, reto"),
            ("Orden de estudio recomendado", "Del concepto neutral a la transferencia"),
            ("Los archivos de la ficha", "concepto.md, comparacion.md, reto.md, casos.json, implementaciones/"),
        ],
        "definiciones": [
            ("Ficha de transferencia", "una clase de código: mismo problema resuelto y comparado en los 10 lenguajes. Clave: es la unidad de estudio."),
            ("casos.json", "entradas y salidas comunes para todas las implementaciones. Clave: define la equivalencia."),
            ("Reto de transferencia", "resolver una variante en un lenguaje no explicado. Clave: prueba que el conocimiento se transfirió."),
        ],
        "situacion": "Abres la clase 041 y ves diez implementaciones. El impulso es leerlas todas en paralelo. El método correcto es otro: primero el concepto y el algoritmo neutral, luego una implementación, luego comparar — y solo al final, el reto.",
        "ejemplo": "Flujo de estudio de una ficha:\n\n```text\n1. 🎯 Objetivo + 🧮 Modelo   → entiende QUÉ se resuelve\n2. 📐 Algoritmo neutral       → entiende CÓMO, sin lenguaje\n3. 🌐 Una implementación      → ve la forma en TU lenguaje\n4. 🔬 Comparación             → nota qué cambia y por qué\n5. ✅ casos.json + verificador → comprueba equivalencia\n6. 🧪 Reto de transferencia   → aplícalo en un lenguaje nuevo\n```\n\nRevisa la [clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md) con este flujo.",
        "practica": "Abre la clase 041 y estúdiala siguiendo los 6 pasos. Al llegar al reto, intenta la variante en un lenguaje que no domines.",
        "errores": [
            ("Leer las 10 implementaciones a la vez", "saturarse sin fijar el concepto", "empezar por el algoritmo neutral y una sola implementación"),
            ("Saltarse la comparación", "quedarse con la forma, no con el porqué", "leer siempre comparacion.md: ahí está el aprendizaje"),
        ],
        "faq": [
            ("¿Debo implementar en los 10 siempre?", "No. Domina 2-3, lee el resto para comparar, y usa el reto para forzar uno nuevo."),
            ("¿Y las clases de la Parte 0?", "Son de método (como esta): no tienen 10 implementaciones, sino ideas que se aplican a todas."),
        ],
    }),
    ("casos.json y el verificador de equivalencia", {
        "tipo": "metodo",
        "objetivo": "Entender el mecanismo que hace único a este programa: un archivo `casos.json` con entradas y salidas comunes, y un verificador que ejecuta todas las implementaciones y comprueba que producen la **misma** salida. Es equivalencia demostrada por máquina, no prometida.",
        "resultados": [
            "Explicar qué contiene casos.json y qué define.",
            "Ejecutar el verificador sobre una clase e interpretar su salida.",
            "Entender por qué algunos lenguajes se omiten o se marcan como ilustrativos.",
        ],
        "temas": [
            ("El contrato de una clase", "Entrada por stdin, salida por stdout, casos esperados"),
            ("El verificador", "Alimenta cada caso a cada implementación y compara"),
            ("Degradación silenciosa", "Si falta un toolchain, se omite e informa"),
        ],
        "definiciones": [
            ("casos.json", "contrato de la clase: descripción, fórmula y lista de {stdin, esperado}. Clave: es la fuente de verdad de la equivalencia."),
            ("Verificador de equivalencia", "script que corre las implementaciones contra casos.json. Clave: falla si dos difieren."),
            ("Ilustrativa", "implementación que no participa en la comparación por stdin (p. ej. SQL). Clave: se muestra pero no se compara igual."),
        ],
        "situacion": "Afirmar 'estas 10 implementaciones hacen lo mismo' es fácil de decir y fácil de equivocar. El verificador lo convierte en algo comprobable: si la de Rust imprime `27000.0` y las demás `27000.00`, el CI se pone rojo.",
        "ejemplo": "Salida real del verificador sobre la clase 041:\n\n```text\n✅ python      3/3 casos\n✅ javascript  3/3 casos\n✅ java        3/3 casos\n⏭️  go          omitido (toolchain 'go' no disponible)\nℹ️  sql         ilustrativa (declarativa, sin stdin)\n```\n\nComando: `python scripts/verificar_equivalencia.py 041`",
        "practica": "Ejecuta `python scripts/verificar_equivalencia.py 041` en tu máquina. ¿Qué lenguajes verifica y cuáles omite según tus toolchains instalados?",
        "errores": [
            ("Confiar en que 'seguro son equivalentes'", "no verificar", "correr el verificador: la máquina no se cansa de comparar"),
            ("Formatear distinto en un lenguaje", "locale o decimales diferentes", "fijar el formato (cultura invariante, 2 decimales) en todas las implementaciones"),
        ],
        "faq": [
            ("¿Qué NO verifica?", "El texto de las clases y el Atlas: son material de lectura, no se ejecutan en CI."),
            ("¿Por qué SQL es ilustrativa?", "Es declarativa: no lee stdin como las demás; se muestra la misma fórmula como consulta."),
        ],
    }),
    ("El concepto en la familia: leer un lenguaje que no conoces", {
        "tipo": "metodo",
        "objetivo": "Adquirir la habilidad central del enfoque políglota: poder **leer** código de un lenguaje que nunca estudiaste, apoyándote en la familia a la que pertenece. Si sabes C, ya reconoces el 80% de Java, C#, JS, Go y PHP.",
        "resultados": [
            "Ubicar un lenguaje desconocido en su familia a partir de su aspecto.",
            "Leer y explicar un fragmento de un lenguaje no estudiado usando su parecido con uno conocido.",
            "Distinguir qué parte es familiar y qué parte exige atención (la diferencia semántica).",
        ],
        "temas": [
            ("Familias y parecidos", "Lenguajes primos comparten sintaxis y modelo"),
            ("Leer por analogía", "Mapear lo nuevo a lo conocido"),
            ("Dónde poner atención", "Las diferencias semánticas, no las cosméticas"),
        ],
        "definiciones": [
            ("Familia de lenguajes", "grupo con antepasado y rasgos comunes (sintaxis, paradigma). Clave: conocer una abre la puerta a las demás."),
            ("Lectura por analogía", "entender lo nuevo mapeándolo a lo que ya sabes. Clave: acelera enormemente el aprendizaje."),
            ("Delta", "lo que cambia respecto del representante de la familia. Clave: es lo único que hay que aprender de nuevo."),
        ],
        "situacion": "Te toca revisar un pull request en Kotlin y nunca lo escribiste. En vez de bloquearte, reconoces que es familia JVM (como Java): `val` es una constante, `fun` una función, la inferencia se parece a Rust. Lees el 90% sin estudiarlo.",
        "ejemplo": "Leer Kotlin sabiendo Java (misma familia JVM):\n\n```text\nKotlin:  val precio = 15000.0        // 'val' = final (constante)\n         fun total(c: Int) = ...     // 'fun' = método\nJava:    final double precio = 15000.0;\n         double total(int c) { ... }\n```\n\nEl delta: `val`/`fun` e inferencia. Todo lo demás ya lo sabías.",
        "practica": "Mira la sección '🧬 El concepto en la familia' de la clase 041. Elige un primo (Ruby, Kotlin o Haskell) y explica su línea apoyándote en un lenguaje del núcleo.",
        "errores": [
            ("Asumir que 'no sé este lenguaje' = 'no puedo leerlo'", "ignorar el parecido de familia", "identificar la familia y leer por analogía"),
            ("Confiar en la analogía sin verificar el delta", "pasar por alto una diferencia semántica", "marcar explícitamente qué cambia respecto del representante"),
        ],
        "faq": [
            ("¿Esto reemplaza estudiar el lenguaje?", "No para escribirlo bien, pero sí para leerlo y entenderlo, que es el 90% del trabajo real."),
            ("¿Dónde veo las familias?", "En el [Atlas](../../../atlas/README.md) y en la Parte 1 del programa."),
        ],
    }),
    ("Cómo elegir lenguaje para un problema", {
        "tipo": "metodo",
        "objetivo": "Cerrar la Parte 0 con criterio de ingeniería: dado un problema y su contexto, saber elegir el lenguaje adecuado según sus fortalezas, su ecosistema y las restricciones del proyecto — y justificar la decisión.",
        "resultados": [
            "Enumerar criterios para elegir lenguaje (rendimiento, ecosistema, equipo, plataforma).",
            "Asociar tipos de problema con familias adecuadas.",
            "Justificar una elección de lenguaje con argumentos, no por moda.",
        ],
        "temas": [
            ("Criterios de elección", "Rendimiento, seguridad, ecosistema, equipo, plazo"),
            ("Problema → familia", "Cada tipo de problema tiene familias que encajan"),
            ("Sistemas políglotas", "Elegir por componente, no un solo lenguaje para todo"),
        ],
        "definiciones": [
            ("Criterio de selección", "factor que inclina la elección de lenguaje (rendimiento, plataforma, talento disponible). Clave: se ponderan, no hay uno absoluto."),
            ("Ecosistema", "librerías, herramientas y comunidad de un lenguaje. Clave: a veces pesa más que el lenguaje en sí."),
            ("Sistema políglota", "software que usa varios lenguajes, uno por componente. Clave: es lo normal en producción."),
        ],
        "situacion": "Un equipo quiere un servicio web con una parte de cálculo numérico intenso y un frontend interactivo. 'Usemos un solo lenguaje' suena simple, pero la respuesta real es políglota: TypeScript en el frontend, un backend en Go o Java, y quizá Rust o C para el núcleo numérico.",
        "ejemplo": "```text\nProblema                         Familias que encajan\n-------------------------------  ----------------------------\nScript rápido / automatización   Python, Bash, PHP\nServicio web de alto tráfico     Go, Java, C#\nNúcleo de rendimiento crítico    C, Rust, C++\nInteractividad en el navegador   JavaScript, TypeScript\nConsulta y análisis de datos     SQL, Python (con librerías)\n```",
        "practica": "Para 'una app móvil con sincronización en la nube', propón un lenguaje por componente (cliente, backend, base de datos) y justifica cada uno en una frase.",
        "errores": [
            ("Elegir por moda o por comodidad", "ignorar el problema y el contexto", "ponderar criterios reales: rendimiento, ecosistema, equipo, plataforma"),
            ("Forzar un solo lenguaje para todo", "creer que uniformidad = simplicidad", "aceptar que los sistemas reales son políglotas y elegir por componente"),
        ],
        "faq": [
            ("¿Hay un 'mejor lenguaje'?", "No. Hay lenguajes mejores para un problema y contexto dados. Ese es todo el punto del curso."),
            ("¿Y si el equipo solo sabe uno?", "El talento disponible es un criterio legítimo y a menudo decisivo."),
        ],
    }),
]

# --------------------------------------------------------------------------- #
# Estructura completa
# --------------------------------------------------------------------------- #

PARTES = [
    ("Pensamiento computacional y el método políglota",
     "Cómo pensar un problema antes de elegir lenguaje, y el método de fichas de transferencia que sostiene todo el programa.",
     P0),

    ("Atlas y genealogía de los lenguajes",
     "El árbol genealógico: cada lenguaje del núcleo es el representante de una familia y abre la puerta a decenas de primos.",
     [
        "El árbol genealógico de los lenguajes: mapa general",
        "Cómo nace y evoluciona un lenguaje: estándares, versiones y ecosistemas",
        "Familia C y de las llaves: C, C++, Objective-C",
        "Familia scripting dinámico: Python, Ruby, Perl, PHP, Lua",
        "Familia JVM: Java, Kotlin, Scala, Groovy, Clojure",
        "Familia .NET: C#, F#, VB.NET",
        "Familia JavaScript y web: JS, TypeScript, Dart",
        "Familia funcional tipada (ML): Haskell, OCaml, F# y la influencia en Rust",
        "Familia Lisp: Scheme, Racket, Clojure, Emacs Lisp",
        "Familia lógica y declarativa: SQL, Prolog, Datalog",
        "Familia concurrente/actor: Erlang, Elixir y el CSP de Go",
        "Familia de sistemas: C, C++, Rust, Zig",
        "Familia array y científica: APL, R, Julia, Fortran, MATLAB",
        "Lenguajes históricos y de nicho: COBOL, Fortran, Pascal, BASIC, Bash",
     ]),

    ("Herramientas, toolchains y anatomía de comandos",
     "Del código fuente al programa que corre: instalar, ejecutar, compilar, empaquetar y probar en cada lenguaje, con el esquema completo de cada comando.",
     [
        "Qué es un toolchain: del código fuente al programa que corre",
        "Compilado vs. interpretado vs. transpilado vs. bytecode/VM",
        "Anatomía de un comando: nombre, subcomando, flags, argumentos y esquema",
        "Instalación y gestión de versiones (pyenv, nvm, rustup, SDKMAN, phpenv)",
        "Ejecutar: python, node, tsx, java, dotnet, go run, rustc, cc, php, sqlite3",
        "Compilar y construir: gcc/clang, cargo, go build, javac, dotnet build",
        "Paquetes y dependencias: pip, pnpm, cargo, maven/gradle, nuget, go mod, composer",
        "REPL e intérpretes interactivos por lenguaje",
        "Formateadores y linters: black, prettier, gofmt, rustfmt, clang-format, php-cs-fixer",
        "Pruebas desde la terminal: pytest, node --test, go test, cargo test, dotnet test, phpunit",
        "Empaquetado y distribución: wheels, jars, binarios, contenedores",
        "Variables de entorno, rutas y el PATH en Windows y Unix",
     ]),

    ("Valores, tipos y variables",
     "La materia prima de todo programa: cómo cada lenguaje nombra, tipa, convierte y muta los valores.",
     [
        "Literales, valores, variables y constantes",
        "Declaración, asignación e inicialización",
        "Tipos primitivos: enteros, reales, booleanos, caracteres",
        "Enteros: tamaño, signo, desbordamiento y bases",
        "Números reales: punto flotante, precisión y decimales",
        "Booleanos y valores de verdad",
        "Caracteres, texto y Unicode",
        "Cadenas: representación, inmutabilidad e interpolación",
        "Conversión de tipos: casting explícito vs. coerción implícita",
        "Tipado estático vs. dinámico",
        "Tipado fuerte vs. débil",
        "Inferencia de tipos",
        "Nulabilidad: null, nil, None, Option y valores ausentes",
        "Mutabilidad e inmutabilidad",
        "Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit",
        "Entrada y salida básica: leer y escribir",
     ]),

    ("Control del programa",
     "Decidir, repetir y manejar errores: el flujo de ejecución expresado en cada familia de lenguajes.",
     [
        "Booleanos, condiciones y cortocircuito",
        "Guardas y validación temprana",
        "if / else y anidamiento",
        "Expresiones condicionales: ternario e if como expresión",
        "switch, case y fallthrough",
        "Coincidencia de patrones: match / when",
        "Iteración por condición: while y do-while",
        "Iteración por rango: for clásico y for-range",
        "Iteración por colección: for-each e iteradores",
        "Iteradores y generadores perezosos (lazy)",
        "Comprensiones de listas y colecciones",
        "Funciones de orden superior: map, filter, reduce",
        "Recursión y recursión de cola",
        "Control de flujo: break, continue, return, goto",
        "Manejo de errores I: excepciones (try/catch/finally)",
        "Manejo de errores II: resultados y valores (Result/Either/error de Go)",
     ]),

    ("Funciones y modularidad",
     "Nombrar procesos, pasar datos y organizar el código en módulos con contratos claros.",
     [
        "Firma, parámetros, argumentos y retorno",
        "Parámetros por defecto y opcionales",
        "Argumentos nombrados y de palabra clave",
        "Parámetros variádicos",
        "Múltiples retornos y desestructuración",
        "Genéricos y polimorfismo paramétrico",
        "Paso por valor",
        "Paso por referencia",
        "Semántica de movimiento y préstamo (Rust)",
        "Alcance (scope) y sombreado (shadowing)",
        "Cierres (closures) y captura de variables",
        "Funciones puras y efectos secundarios",
        "Funciones de primera clase y como valores",
        "Módulos, paquetes y espacios de nombres",
        "Visibilidad, encapsulación y contratos (public/private)",
        "Importar, exportar y organizar un proyecto",
     ]),

    ("Datos y estructuras",
     "Modelar la información: colecciones, registros, tipos algebraicos, identidad, propiedad y persistencia.",
     [
        "Arreglos de tamaño fijo",
        "Listas, vectores y arreglos dinámicos",
        "Tuplas y registros posicionales",
        "Rangos y secuencias",
        "Cadenas como estructura de datos",
        "Conjuntos (sets) y unicidad",
        "Mapas / diccionarios / tablas hash",
        "Pilas y colas",
        "Árboles",
        "Grafos",
        "Registros, structs y clases",
        "Enumeraciones y tipos algebraicos (ADT / sum types)",
        "Igualdad vs. identidad",
        "Copia superficial vs. profunda; referencia vs. valor",
        "Propiedad y ciclo de vida de los datos",
        "Archivos: leer y escribir texto y binario",
        "JSON: serialización y deserialización",
        "Otros formatos y persistencia: CSV, YAML, binarios, bases de datos",
     ]),

    ("Paradigmas",
     "Las grandes formas de estructurar una solución: imperativo, objetos, funcional, declarativo, lógico, eventos y concurrencia.",
     [
        "Qué es un paradigma y por qué importa",
        "Imperativo y estructurado",
        "Procedimental y modular",
        "Orientado a objetos: clases, objetos y estado",
        "Herencia, composición y polimorfismo",
        "Interfaces, traits y clases abstractas",
        "OO basado en prototipos (JavaScript)",
        "Funcional I: inmutabilidad y funciones puras",
        "Funcional II: composición, currying y aplicación parcial",
        "Funcional III: functores, mónadas y efectos (visión práctica)",
        "Declarativo: consultas y transformación (SQL)",
        "Lógico: reglas, hechos y unificación (Prolog)",
        "Orientado a eventos y callbacks",
        "Reactivo y flujos de datos (streams)",
        "Concurrente: hilos, tareas y canales",
        "Asíncrono: async/await y promesas",
     ]),

    ("Cómo funcionan los lenguajes",
     "Qué ocurre por debajo: compilación, máquinas virtuales, memoria, concurrencia y diagnóstico de errores.",
     [
        "Del código a la ejecución: fases de compilación",
        "Compilador, intérprete y JIT",
        "Bytecode y máquinas virtuales (JVM, CLR, V8)",
        "AOT vs. JIT: costos y beneficios",
        "La pila (stack) y el marco de llamada",
        "El heap y la asignación dinámica",
        "Referencias, apuntadores y direcciones",
        "Gestión manual de memoria (C): malloc/free",
        "Recolección de basura (GC)",
        "RAII, propiedad y préstamos (Rust/C++)",
        "Concurrencia: procesos, hilos y memoria compartida",
        "Tareas, corrutinas y canales",
        "Actores y paso de mensajes (modelo BEAM)",
        "El modelo de memoria y las condiciones de carrera",
        "Errores: de sintaxis, de tipos, de enlace y de ejecución",
        "Depuración: cómo se diagnostica en cada runtime",
     ]),

    ("Ingeniería de software políglota",
     "Llevar el código a producción: pruebas, dependencias, Git, CI, rendimiento, seguridad y mantenibilidad en varios lenguajes.",
     [
        "Pruebas unitarias por lenguaje",
        "Pruebas de integración y el verificador de equivalencia",
        "Depuradores: gdb, lldb, pdb y los de IDE",
        "Registro (logging) y observabilidad",
        "Dependencias, versiones y lockfiles",
        "Compilación reproducible y empaquetado",
        "Git y control de versiones para proyectos políglotas",
        "Revisión de código y estándares",
        "Integración continua (CI) multi-lenguaje",
        "Entrega y despliegue",
        "Diseño y arquitectura comparada",
        "Refactorización segura",
        "Patrones de diseño comparados entre lenguajes",
        "Rendimiento y perfilado (profiling)",
        "Seguridad: entradas, memoria y dependencias",
        "Mantenibilidad, documentación y deuda técnica",
     ]),

    ("Interoperabilidad y fronteras entre lenguajes",
     "Por qué los sistemas reales son políglotas y cómo comunican sus piezas: FFI, ABI, serialización, APIs y WebAssembly.",
     [
        "Por qué los sistemas reales son políglotas",
        "La FFI (Foreign Function Interface): llamar a C desde todos",
        "ABI, enlace y convenciones de llamada",
        "Enlaces (bindings) y wrappers",
        "Serialización entre lenguajes: JSON, Protobuf, MessagePack",
        "Contratos de API: REST, gRPC y esquemas",
        "Procesos y comunicación: stdin/stdout, sockets, colas",
        "WebAssembly como objetivo común",
        "Incrustar un lenguaje en otro (Lua, Python embebido)",
        "Elegir el lenguaje correcto para cada componente",
     ]),

    ("Proyecto integrador políglota",
     "Construir un sistema real con componentes en varios lenguajes y defender cada decisión de lenguaje y contrato.",
     [
        "El proyecto: un sistema con componentes en varios lenguajes",
        "Diseño: responsabilidades y contratos entre componentes",
        "Componente CLI (lenguaje de sistemas)",
        "Componente de API/servicio (backend)",
        "Componente web/frontend (JS/TS)",
        "Componente de datos y consultas (SQL)",
        "Componente de automatización/scripting",
        "Persistencia y almacenamiento",
        "Pruebas end-to-end del sistema completo",
        "Empaquetado, contenedores y despliegue",
        "Documentación y defensa de las decisiones de lenguaje",
        "Cierre: retrospectiva y transferencia a nuevos lenguajes",
     ]),
]


def iter_clases():
    num = 0
    for idx, (_p, _s, clases) in enumerate(PARTES):
        for c in clases:
            num += 1
            titulo, datos = (c if isinstance(c, tuple) else (c, None))
            yield num, idx, titulo, datos


def total_clases():
    return sum(len(clases) for _, _, clases in PARTES)


if __name__ == "__main__":
    print(f"Partes: {len(PARTES)} · Clases: {total_clases()}")
