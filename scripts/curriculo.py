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

# --------------------------------------------------------------------------- #
# Bibliografía: los libros que sostienen cada parte (columna vertebral del
# contenido). Cada clase cita las fuentes de su parte + el libro del lenguaje.
# --------------------------------------------------------------------------- #

BIBLIO = {
    0: [  # Pensamiento computacional y método
        "G. Polya — *How to Solve It* (Princeton University Press).",
        "H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).",
        "A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).",
        "T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).",
    ],
    1: [  # Atlas y genealogía de los lenguajes
        "R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).",
        "M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).",
        "B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).",
        "P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).",
    ],
    2: [  # Toolchains y comandos
        "W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).",
        "B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).",
        "A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).",
    ],
    3: [  # Valores, tipos y variables
        "R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.",
        "B. C. Pierce — *Types and Programming Languages* (MIT Press).",
        "M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).",
    ],
    4: [  # Control del programa
        "O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).",
        "R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.",
    ],
    5: [  # Funciones y modularidad
        "H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).",
        "R. C. Martin — *Clean Code* (Prentice Hall).",
        "S. McConnell — *Code Complete* (2ª ed., Microsoft Press).",
    ],
    6: [  # Datos y estructuras
        "T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).",
        "R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).",
    ],
    7: [  # Paradigmas
        "P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).",
        "H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).",
        "R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).",
    ],
    8: [  # Cómo funcionan los lenguajes
        "R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).",
        "A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).",
        "R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).",
    ],
    9: [  # Ingeniería de software políglota
        "S. McConnell — *Code Complete* (2ª ed., Microsoft Press).",
        "A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).",
        "M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).",
        "E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).",
        "K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).",
    ],
    10: [  # Interoperabilidad y fronteras
        "M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).",
        "S. Newman — *Building Microservices* (2ª ed., O'Reilly).",
        "A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).",
    ],
    11: [  # Proyecto integrador
        "S. Newman — *Building Microservices* (2ª ed., O'Reilly).",
        "M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf).",
        "A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).",
    ],
}

# Libro de referencia por lenguaje del núcleo (se cita en las clases de código).
LIBROS_NUCLEO = {
    "python": "L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).",
    "javascript": "M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).",
    "typescript": "B. Cherny — *Programming TypeScript* (O'Reilly).",
    "java": "J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).",
    "csharp": "J. Skeet — *C# in Depth* (4ª ed., Manning).",
    "go": "A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).",
    "rust": "S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).",
    "c": "B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).",
    "sql": "C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).",
    "php": "J. Lockhart — *Modern PHP* (O'Reilly).",
}


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
# Parte 1 — Atlas y genealogía de los lenguajes (tipo "metodo")
# --------------------------------------------------------------------------- #

P1 = [
    ("El árbol genealógico de los lenguajes: mapa general", {
        "tipo": "metodo",
        "objetivo": "Ver el mapa completo de las familias de lenguajes y sus antepasados comunes. Casi todos los lenguajes actuales descienden de tres troncos de los años 50-60: Fortran (cálculo), Lisp (funcional/simbólico) y ALGOL (estructurado, del que nace la familia de llaves). Entender el árbol convierte 'decenas de lenguajes' en 'unas pocas familias con variaciones'.",
        "resultados": [
            "Ubicar los tres troncos históricos (Fortran, Lisp, ALGOL) y qué aportó cada uno.",
            "Situar cada lenguaje del núcleo en su rama del árbol.",
            "Explicar por qué conocer una familia acelera aprender a sus miembros.",
        ],
        "temas": [
            ("Los tres troncos", "Fortran, Lisp y ALGOL originan casi todo lo demás"),
            ("Ramas principales", "Llaves, dinámicos, funcionales, declarativos, lógicos"),
            ("Herencia de rasgos", "Sintaxis, tipos y paradigma se heredan de los ancestros"),
            ("Representante y primos", "Un lenguaje del núcleo por rama abre la puerta a las demás"),
        ],
        "definiciones": [
            ("Tronco", "lenguaje raíz del que desciende una familia (Fortran, Lisp, ALGOL). Clave: define rasgos que perduran décadas."),
            ("Familia", "grupo de lenguajes con ancestro y rasgos comunes. Clave: aprender uno facilita los demás."),
            ("ALGOL", "lenguaje de 1958-60 que introdujo la programación estructurada y los bloques. Clave: padre de C, y por tanto de casi toda la sintaxis de llaves."),
            ("Influencia", "rasgo que un lenguaje toma de otro sin ser de su familia (p. ej. Rust toma tipos de ML). Clave: el árbol tiene cruces, no solo ramas."),
        ],
        "situacion": "Un principiante ve una lista de 50 lenguajes y se abruma. Un veterano ve cinco familias y sabe que dominar un representante de cada una cubre el 90% de lo que encontrará. El árbol es lo que separa una visión de la otra.",
        "ejemplo": "Árbol simplificado (año de nacimiento aproximado):\n\n```text\nFortran (1957) ── cálculo numérico ── Fortran, MATLAB, Julia\nLisp (1958) ───── simbólico/funcional ─ Scheme, Clojure, (influye en ML)\nALGOL (1958) ──── estructurado ──┬── C (1972) ── C++, Java, C#, Go, Rust\n                                 ├── Pascal (1970)\n                                 └── (influye en casi todo)\nML (1973) ─────── funcional tipado ── OCaml, Haskell, F#, (influye en Rust)\nProlog (1972) ─── lógico ──────────── Datalog\n```",
        "practica": "Dibuja tu propio árbol con los 10 lenguajes del núcleo. ¿Cuáles comparten la sintaxis de llaves de C? ¿Cuál no encaja en ninguna rama imperativa? (Pista: SQL.)",
        "errores": [
            ("Tratar cada lenguaje como algo aislado y nuevo", "no ver la familia", "identificar el ancestro y estudiar los rasgos heredados"),
            ("Creer que el árbol son ramas puras sin cruces", "ignorar las influencias", "recordar que Rust toma de C y de ML a la vez"),
        ],
        "faq": [
            ("¿Hay un árbol 'oficial'?", "No único, pero las relaciones históricas son bien conocidas y consistentes entre fuentes."),
            ("¿Dónde va SQL?", "Fuera del tronco imperativo: es declarativo, primo de la rama lógica (Prolog)."),
        ],
    }),
    ("Cómo nace y evoluciona un lenguaje: estándares, versiones y ecosistemas", {
        "tipo": "metodo",
        "objetivo": "Entender que un lenguaje no es estático: nace por una necesidad, se estandariza, publica versiones y crece con un ecosistema (librerías, herramientas, comunidad). Saber leer 'C11', 'ES2023' o 'Python 3.12' te dice qué features puedes usar y qué compatibilidad esperar.",
        "resultados": [
            "Distinguir el lenguaje (estándar) de su implementación (compilador/intérprete).",
            "Interpretar una versión y saber qué implica para la compatibilidad.",
            "Explicar el papel del ecosistema y la gobernanza (PEP, JEP, ECMA, RFC).",
        ],
        "temas": [
            ("Estándar vs. implementación", "El lenguaje se especifica; varios compiladores lo implementan"),
            ("Versionado", "Mayor/menor indica compatibilidad y features nuevas"),
            ("Gobernanza", "Quién decide los cambios (comités, fundaciones, empresas)"),
            ("Ecosistema", "Librerías y herramientas que hacen útil al lenguaje"),
        ],
        "definiciones": [
            ("Estándar", "documento que define el lenguaje (ISO C, ECMAScript). Clave: separa la idea de sus implementaciones."),
            ("Implementación", "compilador o intérprete concreto (GCC, CPython, V8). Clave: puede haber varias del mismo estándar."),
            ("Proceso de evolución", "mecanismo formal de cambios (PEP en Python, JEP en Java, TC39 en JS). Clave: el lenguaje cambia con reglas, no al azar."),
            ("Ecosistema", "conjunto de librerías, gestores de paquetes y comunidad. Clave: a menudo decide la elección más que el lenguaje."),
        ],
        "situacion": "Copias un ejemplo de internet y no compila: usa una feature de C++20 y tu compilador aún es C++17. El problema no es tu código: es la versión. Saber esto ahorra horas.",
        "ejemplo": "Cómo se nombran y gobiernan algunos lenguajes:\n\n```text\nLenguaje    Estándar/versión   Gobernanza         Implementación\n--------    ----------------   ----------------   --------------\nC           ISO C23            comité ISO/WG14    GCC, Clang\nJavaScript  ECMAScript 2023    TC39 (Ecma)        V8, SpiderMonkey\nPython      3.12 (PEP)         Steering Council   CPython, PyPy\nJava        JDK 21 (JEP)       OpenJDK / Oracle   HotSpot, GraalVM\nRust        edición 2021       RFC / Rust team    rustc\n```",
        "practica": "Averigua la última versión estable de dos lenguajes del núcleo y una feature que introdujeron. ¿Cómo se propuso ese cambio (PEP, JEP, RFC…)?",
        "errores": [
            ("Confundir el lenguaje con su compilador", "creer que 'C = GCC'", "recordar que un estándar tiene varias implementaciones"),
            ("Ignorar la versión al copiar código", "asumir que todo el código de un lenguaje es intercambiable", "verificar la versión mínima que exige un ejemplo"),
        ],
        "faq": [
            ("¿Por qué hay varias implementaciones?", "Distintos objetivos: rendimiento, portabilidad, tamaño. Todas siguen el mismo estándar."),
            ("¿'Edición' de Rust es una versión?", "Es un mecanismo de compatibilidad: permite cambios sin romper código viejo."),
        ],
    }),
    ("Familia C y de las llaves: C, C++, Objective-C", {
        "tipo": "metodo",
        "objetivo": "Conocer la familia más influyente en la sintaxis actual: C y sus descendientes directos. C (1972) definió las llaves `{}`, el `;`, los tipos y la cercanía a la memoria que hoy reconoces en Java, C#, JavaScript, Go y muchos más. Aprender a leer C es aprender a leer media programación.",
        "resultados": [
            "Reconocer los rasgos de C que heredaron docenas de lenguajes.",
            "Distinguir C de C++ (OO + plantillas) y Objective-C (mensajes al estilo Smalltalk).",
            "Explicar por qué 'saber C' facilita leer casi cualquier lenguaje de llaves.",
        ],
        "temas": [
            ("C: el ancestro", "Llaves, punteros, memoria manual, tipos primitivos"),
            ("C++: C con objetos", "Clases, plantillas y RAII sobre la base de C"),
            ("Objective-C: C con mensajes", "OO al estilo Smalltalk; base de macOS/iOS clásico"),
            ("La herencia sintáctica", "Por qué Java, C#, JS y Go 'se parecen a C'"),
        ],
        "definiciones": [
            ("C", "lenguaje de 1972 (Dennis Ritchie, Bell Labs) para sistemas. Clave: control total de la memoria; en el núcleo del curso."),
            ("C++", "extensión de C (1985, Bjarne Stroustrup) con OO, plantillas y RAII. Clave: potencia y complejidad; primo directo."),
            ("Objective-C", "C + mensajería estilo Smalltalk (1984, Brad Cox). Clave: lenguaje histórico de Apple, hoy sustituido por Swift."),
            ("Sintaxis de llaves", "bloques delimitados por `{}` y sentencias con `;`. Clave: la marca de la familia, heredada por decenas de lenguajes."),
        ],
        "situacion": "Alguien que solo sabe JavaScript abre por primera vez código en C y, para su sorpresa, entiende los bucles, los `if`, las llaves y las funciones. No es casualidad: JavaScript heredó esa sintaxis de C a través de Java.",
        "ejemplo": "El mismo bucle revela el parentesco de la familia de llaves:\n\n```text\nC:     for (int i = 0; i < 3; i++) { printf(\"%d\", i); }\nC++:   for (int i = 0; i < 3; i++) { std::cout << i; }\nJava:  for (int i = 0; i < 3; i++) { System.out.print(i); }\nJS:    for (let i = 0; i < 3; i++) { console.log(i); }\n```",
        "practica": "Toma un `for` en un lenguaje que conozcas y reescríbelo en C mentalmente. ¿Qué cambia (semántica) más allá de la escritura (sintaxis)?",
        "errores": [
            ("Creer que C++ es 'solo C con clases'", "subestimar su complejidad (plantillas, RAII, sobrecarga)", "tratarlo como un lenguaje propio, no como C decorado"),
            ("Asumir que llaves iguales = comportamiento igual", "confundir sintaxis con semántica", "verificar la gestión de memoria y tipos de cada miembro"),
        ],
        "faq": [
            ("¿Por qué C sigue vivo tras 50 años?", "Es la base de sistemas operativos, drivers y del runtime de casi todo. Rápido y portable."),
            ("¿Objective-C está muerto?", "En desuso frente a Swift, pero aún corre en mucho software de Apple existente."),
        ],
    }),
    ("Familia scripting dinámico: Python, Ruby, Perl, PHP, Lua", {
        "tipo": "metodo",
        "objetivo": "Conocer la familia de los lenguajes dinámicos: sin declarar tipos, interpretados, pensados para escribir rápido. Python y PHP están en el núcleo; Ruby, Perl y Lua son sus primos. Comparten la filosofía 'el programador antes que la máquina', con distintos acentos.",
        "resultados": [
            "Explicar qué comparte esta familia (tipado dinámico, interpretado, expresividad).",
            "Distinguir el acento de cada uno (claridad, felicidad del dev, texto, web, embebido).",
            "Reconocer código de un primo apoyándote en Python o PHP.",
        ],
        "temas": [
            ("Rasgos comunes", "Tipado dinámico, interpretado, poca ceremonia"),
            ("Python y PHP", "Los representantes del núcleo: claridad y web"),
            ("Ruby, Perl, Lua", "Felicidad del dev, procesamiento de texto, embebido"),
            ("Cuándo brillan", "Prototipos, scripting, web, automatización"),
        ],
        "definiciones": [
            ("Python", "1991 (Guido van Rossum), prioriza la legibilidad. Clave: núcleo del curso; el más usado para enseñar y para datos."),
            ("Ruby", "1995 (Matz), diseñado para la felicidad del programador. Clave: bloques y metaprogramación; base de Rails."),
            ("Perl", "1987 (Larry Wall), rey del procesamiento de texto y las expresiones regulares. Clave: 'hay más de una forma de hacerlo'."),
            ("Lua", "1993 (PUC-Rio), minimalista y embebible. Clave: tablas como única estructura; scripting en juegos y sistemas embebidos."),
        ],
        "situacion": "Un equipo necesita un script para renombrar 10.000 archivos. Nadie propone C: se hace en Python en 10 líneas. Esa inmediatez es la razón de ser de toda la familia dinámica.",
        "ejemplo": "'Hola, X' revela el aire de familia (todos dinámicos, sin declarar tipos):\n\n```text\nPython:  nombre = \"Ada\"; print(f\"Hola, {nombre}\")\nRuby:    nombre = \"Ada\"; puts \"Hola, #{nombre}\"\nPHP:     $nombre = \"Ada\"; echo \"Hola, $nombre\";\nLua:     nombre = \"Ada\"; print(\"Hola, \" .. nombre)\n```",
        "practica": "Compara la interpolación de cadenas en Python (`f\"{x}\"`), Ruby (`#{x}`) y PHP (`$x`). ¿De qué clase es la diferencia entre ellas?",
        "errores": [
            ("Creer que 'dinámico' significa 'sin reglas'", "confundir tipado dinámico con débil", "recordar que Python es dinámico pero fuerte: no suma texto y número sin más"),
            ("Usar la familia para todo", "ignorar su coste en rendimiento", "reservarla para scripting/prototipos, no para núcleos críticos"),
        ],
        "faq": [
            ("¿Python es lento?", "Comparado con C/Rust, sí; pero para la mayoría de tareas su velocidad de desarrollo compensa."),
            ("¿Por qué PHP tiene mala fama?", "Por su historia caótica; las versiones modernas (8.x) son un lenguaje sólido y tipado opcionalmente."),
        ],
    }),
    ("Familia JVM: Java, Kotlin, Scala, Groovy, Clojure", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes que corren sobre la Máquina Virtual de Java (JVM). Java es el representante del núcleo; Kotlin, Scala, Groovy y Clojure comparten la misma plataforma (bytecode, GC, librerías) pero ofrecen paradigmas distintos. Un mismo runtime, varias formas de programar.",
        "resultados": [
            "Explicar qué comparten los lenguajes JVM (bytecode, GC, interoperabilidad).",
            "Distinguir el paradigma de cada uno (OO nominal, moderno, funcional-OO, Lisp).",
            "Entender por qué se puede mezclar Java y Kotlin en un mismo proyecto.",
        ],
        "temas": [
            ("La JVM como plataforma", "Compilan a bytecode; comparten GC y librerías"),
            ("Java: el estándar", "OO nominal, verboso pero robusto"),
            ("Kotlin y Scala", "Java moderno (null-safety, corrutinas) y funcional-OO"),
            ("Clojure", "Un Lisp sobre la JVM: datos inmutables y macros"),
        ],
        "definiciones": [
            ("JVM", "máquina virtual que ejecuta bytecode Java. Clave: da portabilidad ('escribe una vez, corre en todas partes') y GC."),
            ("Java", "1995 (Gosling, Sun), OO nominal sobre la JVM. Clave: núcleo del curso; pilar del backend empresarial."),
            ("Kotlin", "2011 (JetBrains), Java moderno con null-safety y corrutinas. Clave: oficial para Android; interopera 100% con Java."),
            ("Clojure", "2007 (Rich Hickey), dialecto de Lisp sobre la JVM. Clave: inmutabilidad y homoiconicidad en una plataforma mainstream."),
        ],
        "situacion": "Un proyecto Android en Java quiere adoptar corrutinas y null-safety sin reescribir todo. Migra archivo a archivo a Kotlin, que convive con Java en el mismo proyecto porque ambos compilan al mismo bytecode.",
        "ejemplo": "Cuatro maneras de sumar sobre la MISMA plataforma:\n\n```text\nJava:    int r = a + b;\nKotlin:  val r = a + b            // inferencia, inmutable\nScala:   val r = a + b            // funcional-OO\nClojure: (def r (+ a b))          // Lisp: paréntesis y prefijo\n```",
        "practica": "Kotlin usa `val` (inmutable) y `var` (mutable). ¿A qué lenguaje del núcleo se parece esa distinción? (Pista: Rust.)",
        "errores": [
            ("Creer que 'lenguaje JVM' = 'Java'", "ignorar la diversidad de paradigmas sobre la misma VM", "recordar que Clojure (Lisp) y Java conviven en la JVM"),
            ("Asumir arranque instantáneo", "la JVM tiene tiempo de calentamiento", "considerarlo en herramientas de línea de comandos de vida corta"),
        ],
        "faq": [
            ("¿Puedo llamar a Java desde Kotlin?", "Sí, y viceversa: comparten bytecode y librerías; la interoperabilidad es total."),
            ("¿Clojure es raro?", "Su sintaxis Lisp asusta al principio, pero su modelo de datos inmutables es muy elegante."),
        ],
    }),
    ("Familia .NET: C#, F#, VB.NET", {
        "tipo": "metodo",
        "objetivo": "Conocer la plataforma .NET de Microsoft y sus tres lenguajes: C# (el representante del núcleo, multiparadigma), F# (funcional) y VB.NET (heredero de Visual Basic). Todos compilan a un lenguaje intermedio común (IL) que corre sobre el CLR, el equivalente de la JVM en el mundo Microsoft.",
        "resultados": [
            "Explicar el rol del CLR y el IL (análogo a la JVM y su bytecode).",
            "Distinguir C# (multiparadigma), F# (funcional) y VB.NET (accesible).",
            "Entender qué significa que .NET hoy sea multiplataforma y de código abierto.",
        ],
        "temas": [
            ("El CLR y el IL", "Runtime y lenguaje intermedio comunes a los tres"),
            ("C#: el buque insignia", "Multiparadigma, moderno, gran ecosistema"),
            ("F#: el funcional", "ML sobre .NET: inmutabilidad y tipos algebraicos"),
            (".NET multiplataforma", "De Windows a Linux/macOS, open source"),
        ],
        "definiciones": [
            ("CLR", "Common Language Runtime: la máquina virtual de .NET. Clave: ejecuta el IL, gestiona memoria (GC); análogo a la JVM."),
            ("C#", "2000 (Anders Hejlsberg, Microsoft), multiparadigma sobre el CLR. Clave: núcleo del curso; empresa, juegos (Unity) y web."),
            ("F#", "2005 (Don Syme), funcional tipado derivado de OCaml, sobre .NET. Clave: pureza y tipos algebraicos en la plataforma Microsoft."),
            ("IL (bytecode de .NET)", "código intermedio al que compilan todos los lenguajes .NET. Clave: permite mezclarlos en una solución."),
        ],
        "situacion": "Un estudio de videojuegos usa Unity, cuyo scripting es C#. El mismo lenguaje sirve luego para el backend web con ASP.NET y para una herramienta de escritorio: una plataforma, muchos destinos.",
        "ejemplo": "Los tres lenguajes .NET, mismo runtime:\n\n```text\nC#:      int r = a + b;\nF#:      let r = a + b            // funcional, inmutable por defecto\nVB.NET:  Dim r As Integer = a + b  ' sintaxis verbosa, accesible\n```",
        "practica": "F# es a .NET lo que Kotlin/Clojure son a la JVM: otro paradigma sobre el mismo runtime. Enumera dos lenguajes del núcleo comparables a C# por su modelo (Pista: Java).",
        "errores": [
            ("Creer que .NET es solo Windows", "quedarse con la imagen antigua", "recordar que .NET moderno corre en Linux y macOS y es open source"),
            ("Confundir C# con Java por parecerse", "asumir que son intercambiables", "notar diferencias reales: propiedades, LINQ, structs por valor"),
        ],
        "faq": [
            ("¿C# o Java?", "Muy parecidos en modelo; la elección suele depender del ecosistema (Microsoft vs. JVM) y del equipo."),
            ("¿VB.NET sigue vivo?", "En mantenimiento: existe y funciona, pero Microsoft ya no lo evoluciona activamente."),
        ],
    }),
    ("Familia JavaScript y web: JS, TypeScript, Dart", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes de la web. JavaScript (1995) nació para animar páginas y hoy corre en todas partes; TypeScript le añade tipos estáticos; Dart (Google) es su primo para apps (Flutter). Comparten sintaxis de llaves y un modelo asíncrono basado en eventos.",
        "resultados": [
            "Explicar por qué JavaScript es omnipresente (navegador, servidor, móvil).",
            "Entender qué añade TypeScript sobre JavaScript y por qué.",
            "Reconocer el modelo asíncrono/eventos común a la familia.",
        ],
        "temas": [
            ("JavaScript: el lenguaje de la web", "Único en el navegador; también en servidor (Node)"),
            ("TypeScript: tipos sobre JS", "Comprobación estática que transpila a JS"),
            ("Prototipos y asincronía", "Herencia por prototipos; eventos y promesas"),
            ("Dart y otros primos", "Alternativas que compilan a/para la web y móvil"),
        ],
        "definiciones": [
            ("JavaScript", "1995 (Brendan Eich, Netscape), dinámico y basado en prototipos. Clave: el único lenguaje nativo del navegador; núcleo del curso."),
            ("TypeScript", "2012 (Microsoft), superset de JS con tipos estáticos. Clave: se comprueba al compilar y transpila a JS; núcleo del curso."),
            ("Dart", "2011 (Google), tipado y compilable a JS o nativo. Clave: motor de Flutter para apps multiplataforma."),
            ("Prototipos", "modelo de OO donde los objetos heredan de otros objetos, no de clases. Clave: rasgo distintivo de JavaScript."),
        ],
        "situacion": "Un proyecto JavaScript crece a 50.000 líneas y los errores de 'undefined is not a function' se disparan. Adoptar TypeScript hace que el compilador atrape esos fallos antes de ejecutar: la misma familia, con red de seguridad.",
        "ejemplo": "TypeScript es JavaScript con tipos: mismo código, más garantías.\n\n```text\nJavaScript:  function doble(x) { return x * 2; }\nTypeScript:  function doble(x: number): number { return x * 2; }\n```\n\nEl segundo falla al compilar si alguien llama `doble(\"hola\")`.",
        "practica": "TypeScript infiere y comprueba tipos como Java o Rust, pero desaparece al ejecutar (transpila a JS). ¿A qué modelo del núcleo se parece más y en qué se diferencia?",
        "errores": [
            ("Creer que TypeScript es un lenguaje distinto de JS", "no ver que es un superset", "recordar que todo JS válido es TS válido; TS solo añade tipos"),
            ("Ignorar la asincronía", "programar como si todo fuera secuencial", "entender el bucle de eventos, callbacks y async/await desde el inicio"),
        ],
        "faq": [
            ("¿TypeScript reemplaza a JavaScript?", "No: lo complementa. Al final se convierte en JavaScript para poder ejecutarse."),
            ("¿Por qué JS corre en el servidor?", "Node.js incrustó el motor V8 fuera del navegador; hizo de JS un lenguaje de propósito general."),
        ],
    }),
    ("Familia funcional tipada (ML): Haskell, OCaml, F# y la influencia en Rust", {
        "tipo": "metodo",
        "objetivo": "Conocer la familia ML: lenguajes funcionales con sistemas de tipos potentes e inferencia. Aunque ninguno está en el núcleo, su influencia sí: Rust tomó de aquí los tipos algebraicos, el `match` y `Option`/`Result`. Entender ML explica por qué Rust se siente distinto a C.",
        "resultados": [
            "Explicar los rasgos de la familia ML (funciones puras, inmutabilidad, inferencia, ADT).",
            "Reconocer qué tomó Rust de ML frente a lo que tomó de C.",
            "Leer una expresión funcional simple (match sobre un tipo suma).",
        ],
        "temas": [
            ("Raíces: ML (1973)", "Inferencia de tipos y funciones como valores"),
            ("Haskell: pureza y pereza", "Sin efectos secundarios por defecto; evaluación perezosa"),
            ("OCaml y F#", "ML práctico; F# lleva ML a .NET"),
            ("La huella en Rust", "ADT, match exhaustivo, Option/Result"),
        ],
        "definiciones": [
            ("ML", "familia de 1973 (Robin Milner) con inferencia de tipos Hindley-Milner. Clave: raíz de OCaml, Haskell y F#."),
            ("Haskell", "1990, funcional puro y perezoso. Clave: los efectos se modelan con tipos (mónadas); el más 'purista' de la familia."),
            ("Tipo algebraico (ADT)", "tipo compuesto por alternativas (suma) o productos. Clave: Rust los tomó de aquí como `enum`."),
            ("Inferencia de tipos", "el compilador deduce los tipos sin anotarlos. Clave: rasgo de ML heredado por Rust, Kotlin, Go y otros."),
        ],
        "situacion": "Un programador de C prueba Rust y se sorprende con `match` exhaustivo y `Option<T>` en vez de punteros nulos. Eso no viene de C: viene de ML. Reconocer la herencia hace que Rust deje de parecer arbitrario.",
        "ejemplo": "El `match` sobre un tipo suma, de ML a Rust:\n\n```text\nHaskell:  case forma of\n            Circulo r -> pi * r * r\n            Cuadrado l -> l * l\nRust:     match forma {\n            Forma::Circulo(r) => PI * r * r,\n            Forma::Cuadrado(l) => l * l,\n          }\n```",
        "practica": "Busca en la clase 041 (o en material de Rust) un `Option`/`Result`. Explica por qué esa idea es más segura que un puntero nulo, y de qué familia proviene.",
        "errores": [
            ("Ver Rust como 'C moderno' solamente", "ignorar su mitad ML", "reconocer que su seguridad de tipos viene de la familia funcional"),
            ("Creer que funcional = académico e inútil", "prejuicio", "notar que sus ideas ya están en lenguajes mainstream (Rust, Kotlin, Swift)"),
        ],
        "faq": [
            ("¿Necesito aprender Haskell?", "No para el núcleo, pero entender sus ideas mejora tu Rust, tu Kotlin y tu forma de pensar."),
            ("¿Qué es la 'pereza' de Haskell?", "Evalúa una expresión solo cuando se necesita su valor; permite listas infinitas, entre otras cosas."),
        ],
    }),
    ("Familia Lisp: Scheme, Racket, Clojure, Emacs Lisp", {
        "tipo": "metodo",
        "objetivo": "Conocer la familia más antigua todavía viva: Lisp (1958). Su rasgo único es la homoiconicidad: el código se escribe con la misma estructura que los datos (listas entre paréntesis), lo que permite macros que reescriben el propio lenguaje. Ninguno está en el núcleo, pero sus ideas (funciones de primera clase, GC, REPL) hoy están en todos.",
        "resultados": [
            "Explicar la homoiconicidad y por qué habilita macros potentes.",
            "Leer una expresión Lisp (notación prefija entre paréntesis).",
            "Reconocer ideas nacidas en Lisp que hoy son universales.",
        ],
        "temas": [
            ("Homoiconicidad", "Código y datos comparten forma (listas)"),
            ("Notación prefija", "(operador operando operando)"),
            ("Macros", "Programas que escriben programas"),
            ("Herencia universal", "GC, REPL, funciones de primera clase nacieron aquí"),
        ],
        "definiciones": [
            ("Lisp", "1958 (John McCarthy), segundo lenguaje de alto nivel más antiguo. Clave: introdujo ideas hoy universales (GC, funciones de primera clase)."),
            ("Homoiconicidad", "el código tiene la misma estructura que los datos que manipula. Clave: permite macros que transforman el lenguaje."),
            ("Scheme", "1975, dialecto minimalista y elegante de Lisp. Clave: usado en enseñanza (SICP)."),
            ("Clojure", "2007, Lisp moderno sobre la JVM. Clave: acerca la familia Lisp al mundo mainstream con datos inmutables."),
        ],
        "situacion": "Un programador ve `(+ 1 2 3)` y lo descarta por 'raro'. Pero esa uniformidad —todo es una lista— es justo lo que permite a Lisp extenderse con macros que otros lenguajes no pueden igualar.",
        "ejemplo": "La notación prefija: el operador va primero, todo entre paréntesis.\n\n```text\nInfija (C):    (1 + 2) * 3\nLisp:          (* (+ 1 2) 3)\nDefinir función (Scheme):\n               (define (doble x) (* x 2))\n```",
        "practica": "Traduce `(* (+ 2 3) (- 10 4))` a notación infija y calcula el resultado. (Respuesta: (2+3)*(10-4) = 30.)",
        "errores": [
            ("Rechazar Lisp por los paréntesis", "juzgar la forma, no las ideas", "ver que su uniformidad es su superpoder (macros)"),
            ("Creer que Lisp es cosa del pasado", "ignorar Clojure y Racket", "reconocer que sigue vivo e influyente"),
        ],
        "faq": [
            ("¿Para qué sirve hoy?", "Clojure en backend/datos, Racket y Scheme en enseñanza e investigación, Emacs Lisp en el editor Emacs."),
            ("¿Qué idea de Lisp uso sin saberlo?", "Las funciones de primera clase (pasar funciones como valores) y el recolector de basura."),
        ],
    }),
    ("Familia lógica y declarativa: SQL, Prolog, Datalog", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes donde describes QUÉ quieres, no CÓMO obtenerlo. SQL (en el núcleo) describe conjuntos de datos; Prolog describe hechos y reglas y deja que el motor deduzca. Es el salto paradigmático más grande respecto de los lenguajes imperativos del curso.",
        "resultados": [
            "Distinguir programación declarativa de imperativa con un ejemplo.",
            "Explicar el modelo de SQL (consultas sobre conjuntos) y de Prolog (hechos, reglas, unificación).",
            "Reconocer cuándo el enfoque declarativo simplifica un problema.",
        ],
        "temas": [
            ("Declarativo vs. imperativo", "Describir el resultado vs. describir los pasos"),
            ("SQL: consultas sobre datos", "El motor decide cómo ejecutar la consulta"),
            ("Prolog: hechos y reglas", "Deducción por unificación y backtracking"),
            ("Datalog", "Subconjunto de Prolog para consultas de datos"),
        ],
        "definiciones": [
            ("Declarativo", "paradigma en el que se describe el resultado deseado, no el algoritmo. Clave: el motor decide el 'cómo'."),
            ("SQL", "1974 (IBM), lenguaje de consulta de bases de datos relacionales. Clave: núcleo del curso; declarativo sobre conjuntos."),
            ("Prolog", "1972 (Colmerauer, Kowalski), programación lógica. Clave: describes hechos y reglas; el motor deduce por unificación."),
            ("Unificación", "mecanismo que hace coincidir términos para satisfacer una consulta lógica. Clave: motor de la deducción en Prolog."),
        ],
        "situacion": "Para obtener 'los clientes con más de 3 pedidos', un lenguaje imperativo recorre listas y acumula contadores. SQL lo dice en una frase (`GROUP BY ... HAVING COUNT(*) > 3`) y el motor se encarga del cómo. Ese cambio de mentalidad es el corazón de lo declarativo.",
        "ejemplo": "Mismo objetivo, dos mentalidades:\n\n```text\nImperativo (pseudocódigo):\n  PARA cada cliente: contar pedidos; SI > 3, añadir a resultado\n\nDeclarativo (SQL):\n  SELECT cliente FROM pedidos GROUP BY cliente HAVING COUNT(*) > 3;\n\nLógico (Prolog):\n  abuelo(X, Z) :- padre(X, Y), padre(Y, Z).\n```",
        "practica": "Escribe en una frase, sin código, qué resultado pides (no cómo). Luego nota que eso es 'pensar declarativamente'. Compáralo con cómo lo harías con un bucle.",
        "errores": [
            ("Programar SQL como si fuera imperativo", "querer controlar el 'cómo'", "confiar en el optimizador y describir solo el 'qué'"),
            ("Creer que lo declarativo sirve para todo", "forzarlo donde el control paso a paso es necesario", "usarlo donde el problema es 'describir un resultado'"),
        ],
        "faq": [
            ("¿SQL es 'de verdad' un lenguaje de programación?", "Es un lenguaje declarativo especializado; Turing-completo con extensiones, pero su fuerte es consultar datos."),
            ("¿Dónde se usa Prolog hoy?", "IA simbólica, sistemas expertos, análisis de lenguaje y verificación; nicho pero potente."),
        ],
    }),
    ("Familia concurrente/actor: Erlang, Elixir y el CSP de Go", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes diseñados para hacer muchas cosas a la vez de forma segura. Erlang y Elixir usan el modelo de actores (procesos aislados que se comunican por mensajes, con supervisión y 'let it crash'); Go (en el núcleo) usa CSP (goroutines y canales). Dos respuestas al mismo problema: la concurrencia.",
        "resultados": [
            "Explicar el modelo de actores y por qué favorece la tolerancia a fallos.",
            "Distinguir actores (Erlang/Elixir) de CSP (Go).",
            "Entender la filosofía 'let it crash' y la supervisión.",
        ],
        "temas": [
            ("El problema de la concurrencia", "Hacer muchas cosas a la vez sin corromper datos"),
            ("Modelo de actores", "Procesos aislados que solo se comunican por mensajes"),
            ("Let it crash y supervisión", "Dejar morir un proceso y reiniciarlo desde arriba"),
            ("CSP en Go", "Goroutines y canales: 'comparte comunicando'"),
        ],
        "definiciones": [
            ("Modelo de actores", "concurrencia mediante procesos aislados que intercambian mensajes. Clave: sin memoria compartida, no hay condiciones de carrera."),
            ("Erlang", "1986 (Ericsson, Joe Armstrong) para telecomunicaciones. Clave: tolerancia a fallos extrema; corre sobre la máquina BEAM."),
            ("Elixir", "2011 (José Valim), sintaxis moderna sobre la BEAM de Erlang. Clave: actores + productividad; base de Phoenix."),
            ("CSP", "Communicating Sequential Processes (Hoare, 1978): procesos que se sincronizan por canales. Clave: modelo de la concurrencia de Go."),
        ],
        "situacion": "Un sistema de mensajería debe seguir funcionando aunque parte de él falle. En vez de evitar todos los errores, Erlang deja que un proceso muera y un supervisor lo reinicia limpio. La resiliencia nace de aislar, no de blindar.",
        "ejemplo": "Dos modelos de concurrencia:\n\n```text\nActores (Elixir):  send(pid, {:hola, \"Ada\"})     # mensaje a un proceso\nCSP (Go):          canal <- \"hola\"                // enviar por un canal\n                   msg := <-canal                 // recibir\n```",
        "practica": "Go está en el núcleo y usa CSP. Busca 'goroutine' y 'channel'. ¿En qué se parece un canal de Go a enviar un mensaje a un actor, y en qué se diferencia?",
        "errores": [
            ("Compartir memoria entre hilos sin protección", "condiciones de carrera", "preferir el paso de mensajes (actores/canales) al estado compartido"),
            ("Intentar prevenir todos los fallos", "código defensivo frágil", "adoptar 'let it crash': aislar y supervisar en vez de blindar"),
        ],
        "faq": [
            ("¿Qué es la BEAM?", "La máquina virtual de Erlang/Elixir, optimizada para millones de procesos ligeros y tolerancia a fallos."),
            ("¿Go es de actores?", "No exactamente: usa CSP (canales), un primo cercano del modelo de actores."),
        ],
    }),
    ("Familia de sistemas: C, C++, Rust, Zig", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes para escribir software cercano a la máquina: sistemas operativos, drivers, motores y runtimes. C, C++ y Rust están en el núcleo o son primos directos; Zig es el recién llegado. Comparten el control de la memoria y la ausencia (o control) de recolector de basura.",
        "resultados": [
            "Explicar qué distingue a un lenguaje de sistemas (control de memoria, sin GC obligatorio).",
            "Comparar cómo cada uno gestiona la seguridad de memoria.",
            "Situar a Rust y Zig como respuestas modernas a los peligros de C.",
        ],
        "temas": [
            ("Qué es un lenguaje de sistemas", "Control fino de memoria y rendimiento predecible"),
            ("C y C++: potencia sin red", "Máximo control, máxima responsabilidad"),
            ("Rust: seguridad sin GC", "Propiedad y préstamos comprobados al compilar"),
            ("Zig: C moderno", "Simplicidad, comptime, sin GC"),
        ],
        "definiciones": [
            ("Lenguaje de sistemas", "diseñado para software cercano al hardware, con control de memoria y sin GC obligatorio. Clave: rendimiento predecible."),
            ("Rust", "2010/2015 (Mozilla, Graydon Hoare), seguridad de memoria sin GC vía propiedad. Clave: núcleo del curso; evita clases enteras de bugs."),
            ("Zig", "2016 (Andrew Kelley), alternativa moderna y minimalista a C. Clave: `comptime`, sin GC, gestión manual explícita."),
            ("Seguridad de memoria", "garantía de no acceder a memoria inválida (use-after-free, desbordamientos). Clave: C no la da; Rust sí, al compilar."),
        ],
        "situacion": "El 70% de las vulnerabilidades graves en software de sistemas son errores de memoria de C/C++. Rust nació para eliminarlos de raíz: el compilador rechaza el código inseguro antes de ejecutarlo, sin coste en tiempo de ejecución.",
        "ejemplo": "Cómo cada familia gestiona la memoria:\n\n```text\nC:     malloc/free manuales        → potente, propenso a errores\nC++:   RAII (destructores)         → automático dentro de su ámbito\nRust:  propiedad + préstamos       → comprobado por el compilador\nZig:   asignadores explícitos      → manual pero visible y seguro-por-defecto\n```",
        "practica": "Busca en la implementación en C de la clase 041 dónde se reserva y libera memoria (o dónde podría hacer falta). ¿Qué garantiza Rust que C no?",
        "errores": [
            ("Creer que 'sistemas' = 'difícil e innecesario'", "evitar entender la memoria", "reconocer que estos lenguajes sostienen todo lo demás"),
            ("Pensar que Rust es 'C más lento'", "asumir que la seguridad cuesta rendimiento", "notar que sus comprobaciones son en tiempo de compilación, no de ejecución"),
        ],
        "faq": [
            ("¿Rust reemplazará a C?", "En proyectos nuevos gana terreno, pero C está en tantos cimientos que convivirán décadas."),
            ("¿Por qué sin recolector de basura?", "El GC introduce pausas impredecibles, inaceptables en drivers o sistemas de tiempo real."),
        ],
    }),
    ("Familia array y científica: APL, R, Julia, Fortran, MATLAB", {
        "tipo": "metodo",
        "objetivo": "Conocer los lenguajes hechos para el cálculo numérico y el trabajo con datos. Fortran (1957) inauguró la computación científica; MATLAB y R dominan ingeniería y estadística; Julia es la apuesta moderna; APL introdujo operar sobre arreglos completos de una vez. Ninguno está en el núcleo, pero definen un estilo: la vectorización.",
        "resultados": [
            "Explicar la vectorización (operar sobre arreglos completos sin bucles explícitos).",
            "Situar Fortran, MATLAB, R y Julia según su dominio.",
            "Reconocer por qué este estilo importa para datos y ciencia.",
        ],
        "temas": [
            ("Vectorización", "Operar sobre todo un arreglo de una vez"),
            ("Fortran: el pionero", "Cálculo numérico desde 1957, aún en HPC"),
            ("R y MATLAB", "Estadística e ingeniería, orientados a matrices"),
            ("Julia: lo moderno", "Rendimiento de C con comodidad de Python; multiple dispatch"),
        ],
        "definiciones": [
            ("Vectorización", "aplicar una operación a un arreglo entero sin escribir el bucle. Clave: código más corto y a menudo más rápido."),
            ("Fortran", "1957 (IBM, John Backus), primer lenguaje de alto nivel. Clave: sigue siendo rey del cálculo científico de alto rendimiento."),
            ("R", "1993, especializado en estadística y visualización. Clave: enorme ecosistema de análisis de datos."),
            ("Julia", "2012, cálculo científico con rendimiento cercano a C. Clave: multiple dispatch como paradigma central."),
        ],
        "situacion": "Un análisis en Python con un bucle sobre un millón de números tarda segundos; reescrito con operaciones vectorizadas (estilo de esta familia) tarda milisegundos. Pensar en arreglos completos, no en elementos, cambia el rendimiento.",
        "ejemplo": "Sumar dos vectores: con bucle vs. vectorizado.\n\n```text\nCon bucle (imperativo):\n  PARA i: c[i] <- a[i] + b[i]\n\nVectorizado (estilo array, p. ej. R/Julia/NumPy):\n  c <- a + b        # una sola operación sobre todo el arreglo\n```",
        "practica": "Piensa cómo calcular el promedio de un millón de números 'a la manera de bucle' y 'a la manera vectorizada'. ¿Cuál expresa mejor la intención?",
        "errores": [
            ("Escribir bucles donde cabe vectorizar", "traer la mentalidad imperativa a datos", "pensar en operaciones sobre arreglos completos"),
            ("Creer que estos lenguajes son 'de matemáticos'", "descartarlos", "reconocer que dominan datos, ciencia y buena parte de la IA"),
        ],
        "faq": [
            ("¿Fortran sigue en uso?", "Sí: mucho software de clima, física y HPC corre sobre Fortran altamente optimizado."),
            ("¿Julia sustituye a Python en datos?", "Compite en rendimiento; Python gana en ecosistema. Conviven según el caso."),
        ],
    }),
    ("Lenguajes históricos y de nicho: COBOL, Fortran, Pascal, BASIC, Bash", {
        "tipo": "metodo",
        "objetivo": "Cerrar el Atlas con lenguajes que marcaron época o dominan un nicho. COBOL aún mueve bancos; Fortran, la ciencia; Pascal enseñó a generaciones; BASIC democratizó programar; y Bash sigue siendo el pegamento de la administración de sistemas. Conocerlos da perspectiva histórica y práctica.",
        "resultados": [
            "Situar cada lenguaje en su época y su nicho actual.",
            "Explicar por qué algunos 'viejos' siguen en producción crítica.",
            "Reconocer Bash como habilidad transferible imprescindible hoy.",
        ],
        "temas": [
            ("COBOL: la banca", "Miles de millones de líneas aún en producción"),
            ("Pascal y BASIC", "Enseñaron a programar a generaciones enteras"),
            ("Fortran: la ciencia", "El pionero que no se jubila"),
            ("Bash: el pegamento vivo", "Automatización y orquestación en Unix"),
        ],
        "definiciones": [
            ("COBOL", "1959 (comité CODASYL, Grace Hopper influyente), para negocios. Clave: aún sostiene núcleos bancarios y de seguros."),
            ("Pascal", "1970 (Niklaus Wirth), diseñado para enseñar programación estructurada. Clave: claridad; padre de Delphi."),
            ("BASIC", "1964 (Kemeny y Kurtz), pensado para principiantes. Clave: llevó la programación a los ordenadores personales."),
            ("Bash", "1989 (Brian Fox, GNU), shell de Unix. Clave: automatización viva; su modelo de tuberías y procesos es muy transferible."),
        ],
        "situacion": "Un banco descubre que su sistema central corre en COBOL y quedan pocos que lo mantengan. No es una curiosidad: entender por qué el software 'viejo' persiste es entender la realidad de la industria.",
        "ejemplo": "Bash es el más vigente de este grupo: su modelo de tuberías es puro y transferible.\n\n```text\n# Contar cuántos archivos .md hay, en una línea:\nls *.md | wc -l\n\n# Tubería: la salida de un comando es la entrada del siguiente\ncat notas.txt | grep \"TODO\" | sort | uniq\n```",
        "practica": "Escribe una tubería de Bash que, dado un archivo de texto, cuente cuántas líneas contienen la palabra 'error'. (Pista: `grep` y `wc`.)",
        "errores": [
            ("Despreciar los lenguajes 'viejos'", "creer que lo antiguo es inútil", "reconocer que COBOL y Fortran mueven infraestructura crítica hoy"),
            ("Subestimar Bash", "verlo como comandos sueltos", "aprender su modelo de tuberías/procesos: es habilidad diaria del desarrollador"),
        ],
        "faq": [
            ("¿Vale la pena aprender COBOL?", "Como nicho bien pagado por la escasez de expertos, puede tener sentido; como base, no."),
            ("¿Bash cuenta como lenguaje?", "Sí: tiene variables, control de flujo y funciones; y su modelo de procesos es muy transferible."),
        ],
    }),
]


# --------------------------------------------------------------------------- #
# Parte 2 — Herramientas, toolchains y anatomía de comandos (tipo "metodo")
# --------------------------------------------------------------------------- #

P2 = [
    ("Qué es un toolchain: del código fuente al programa que corre", {
        "tipo": "metodo",
        "objetivo": "Entender la cadena de herramientas (toolchain) que convierte el texto que escribes en un programa que se ejecuta: editor, compilador o intérprete, enlazador, gestor de paquetes y runtime. Cada lenguaje tiene su cadena, pero las etapas se repiten. Verlas como un flujo evita tratar los comandos como 'magia'.",
        "resultados": [
            "Nombrar las etapas típicas de un toolchain.",
            "Ubicar dónde encaja cada herramienta (compilador, enlazador, runtime, gestor de paquetes).",
            "Explicar por qué un mismo programa necesita pasos distintos en distintos lenguajes.",
        ],
        "temas": [
            ("Fuente → ejecutable", "Las etapas entre escribir y ejecutar"),
            ("Compilador/intérprete", "Traduce o ejecuta el código fuente"),
            ("Enlazador y dependencias", "Junta tu código con librerías"),
            ("Runtime", "El entorno donde el programa finalmente corre"),
        ],
        "definiciones": [
            ("Toolchain", "conjunto de herramientas que llevan el código fuente a un programa ejecutable. Clave: cada lenguaje tiene la suya, con etapas similares."),
            ("Compilador", "traduce el código fuente a otro lenguaje (máquina o bytecode) antes de ejecutar. Clave: los errores se ven en compilación."),
            ("Enlazador (linker)", "combina tu código compilado con librerías en un ejecutable. Clave: resuelve referencias a funciones externas."),
            ("Runtime", "entorno que ejecuta el programa (la CPU directamente, la JVM, Node…). Clave: define qué se necesita para correrlo."),
        ],
        "situacion": "Un principiante escribe `hola.c`, hace doble clic y no pasa nada. Le falta entender que C debe compilarse y enlazarse antes de existir como programa. Python sí 'se ejecuta al toque' porque su toolchain interpreta. La diferencia está en la cadena.",
        "ejemplo": "La misma meta, dos cadenas distintas:\n\n```text\nC (compilado):\n  main.c --[compilador]--> main.o --[enlazador]--> ejecutable --> corre\n\nPython (interpretado):\n  main.py --[intérprete]--> corre directamente\n```",
        "practica": "Para un lenguaje que uses, enumera qué herramienta interviene en cada etapa (editar, traducir, ejecutar). ¿Compila, interpreta o ambas?",
        "errores": [
            ("Tratar los comandos como magia", "no entender qué etapa ejecuta cada uno", "mapear cada comando a su etapa del toolchain"),
            ("Esperar que todos los lenguajes se ejecuten igual", "generalizar desde uno", "reconocer que compilados e interpretados difieren en la cadena"),
        ],
        "faq": [
            ("¿Python no se compila nunca?", "Compila a bytecode internamente (.pyc), pero lo hace de forma transparente al ejecutar."),
            ("¿Por qué tantas etapas en C?", "El control fino tiene coste: cada etapa es un punto donde optimizar o fallar."),
        ],
    }),
    ("Compilado vs. interpretado vs. transpilado vs. bytecode/VM", {
        "tipo": "metodo",
        "objetivo": "Clasificar cómo un lenguaje llega a ejecutarse: compilado a código máquina (C, Rust, Go), interpretado línea a línea (Python, PHP), transpilado a otro lenguaje (TypeScript → JavaScript) o compilado a bytecode para una máquina virtual (Java → JVM, C# → CLR). Esta clasificación explica el rendimiento, el arranque y los mensajes de error.",
        "resultados": [
            "Clasificar cada lenguaje del núcleo por su modelo de ejecución.",
            "Relacionar el modelo con el rendimiento y el momento en que aparecen los errores.",
            "Explicar qué es una máquina virtual y qué es transpilar.",
        ],
        "temas": [
            ("Compilado a máquina", "Rápido, errores en compilación (C, Rust, Go)"),
            ("Interpretado", "Flexible, errores en ejecución (Python, PHP)"),
            ("Bytecode + VM", "Portable, con calentamiento (Java, C#)"),
            ("Transpilado", "De un lenguaje a otro (TS → JS)"),
        ],
        "definiciones": [
            ("Compilación a código máquina", "traducción directa a instrucciones de la CPU. Clave: máximo rendimiento; errores antes de ejecutar."),
            ("Interpretación", "ejecución del código fuente sin traducirlo por adelantado. Clave: rápido de iterar; errores al llegar a la línea."),
            ("Bytecode", "código intermedio que ejecuta una máquina virtual (JVM, CLR). Clave: portabilidad entre sistemas operativos."),
            ("Transpilación", "compilar de un lenguaje de alto nivel a otro (TypeScript a JavaScript). Clave: aprovechar un runtime existente."),
        ],
        "situacion": "Un error tipográfico en un nombre de variable: en C, el compilador lo detiene antes de correr; en Python, el programa arranca y falla justo al llegar a esa línea. El modelo de ejecución decide cuándo te enteras del error.",
        "ejemplo": "Clasificación del núcleo:\n\n```text\nModelo               Lenguajes del núcleo\n-------------------  ---------------------------\nCompilado a máquina  C, Rust, Go\nInterpretado         Python, PHP, JavaScript*\nBytecode + VM        Java (JVM), C# (CLR)\nTranspilado          TypeScript (→ JavaScript)\nDeclarativo/motor    SQL (lo ejecuta el motor de BD)\n```\n\n*JavaScript usa un JIT: interpreta y compila sobre la marcha.",
        "practica": "Clasifica cada lenguaje que conozcas en una de las categorías. ¿Alguno encaja en más de una? (Pista: JavaScript y su JIT.)",
        "errores": [
            ("Creer que 'compilado' siempre es mejor", "ignorar el valor de iterar rápido", "elegir según el caso: rendimiento vs. velocidad de desarrollo"),
            ("Pensar que interpretado = sin compilación alguna", "simplificar de más", "recordar que muchos interpretan a bytecode internamente"),
        ],
        "faq": [
            ("¿Qué es un JIT?", "Just-In-Time: compila el código a máquina durante la ejecución, combinando flexibilidad y velocidad (V8, JVM)."),
            ("¿Por qué Java 'tarda en arrancar'?", "La JVM debe cargar y calentar (JIT) antes de alcanzar su velocidad máxima."),
        ],
    }),
    ("Anatomía de un comando: nombre, subcomando, flags, argumentos y esquema", {
        "tipo": "metodo",
        "objetivo": "Dominar la estructura universal de un comando de terminal para dejar de copiarlos a ciegas. Todo comando sigue el mismo esquema: nombre, subcomando opcional, opciones (flags) y argumentos. Entenderlo te permite leer, modificar y componer cualquier comando de cualquier toolchain.",
        "resultados": [
            "Descomponer un comando en nombre, subcomando, flags y argumentos.",
            "Distinguir flags cortas (-v), largas (--verbose) y con valor (-o salida).",
            "Leer la línea de uso ('usage') de la ayuda de un comando.",
        ],
        "temas": [
            ("El esquema general", "nombre [subcomando] [flags] [argumentos]"),
            ("Flags/opciones", "Cortas, largas, booleanas y con valor"),
            ("Argumentos posicionales", "Los datos sobre los que actúa el comando"),
            ("La ayuda como esquema", "--help revela la estructura exacta"),
        ],
        "definiciones": [
            ("Comando", "instrucción para el sistema o una herramienta, escrita en la terminal. Clave: sigue un esquema regular."),
            ("Subcomando", "acción específica dentro de una herramienta (git commit, dotnet build). Clave: agrupa funciones bajo un mismo programa."),
            ("Flag/opción", "modificador que cambia el comportamiento (-v, --output). Clave: puede ser booleana o llevar un valor."),
            ("Argumento posicional", "dato cuyo significado depende de su posición. Clave: distinto de las opciones con nombre."),
        ],
        "situacion": "Alguien copia `git commit -m \"fix\"` sin entenderlo y luego no sabe adaptarlo. Quien reconoce el esquema —programa `git`, subcomando `commit`, flag `-m` con valor— puede construir sus propios comandos con confianza.",
        "ejemplo": "El mismo esquema en varias herramientas:\n\n```text\n  git      commit     -m \"mensaje\"        (sin argumento posicional)\n  \\_/      \\____/     \\_______________/\n nombre  subcomando   flag con valor\n\n  cc       main.c     -o main            (compilar C)\n  docker   run        -it   ubuntu bash\n  dotnet   build      -c Release\n```",
        "practica": "Toma `rustc main.rs -o main` y etiqueta cada parte (nombre, argumento, flag, valor). Luego busca `git --help` y localiza el 'usage'.",
        "errores": [
            ("Copiar comandos sin entender sus partes", "no poder adaptarlos", "descomponer siempre en nombre/subcomando/flags/argumentos"),
            ("Confundir un argumento con una flag", "errores de sintaxis del comando", "recordar que las flags empiezan por - o --"),
        ],
        "faq": [
            ("¿Por qué unas flags llevan un guion y otras dos?", "Convención: un guion para la forma corta (-v), dos para la larga (--verbose)."),
            ("¿Cómo sé qué acepta un comando?", "Con `comando --help` o `man comando`: muestran el esquema y todas las opciones."),
        ],
    }),
    ("Instalación y gestión de versiones (pyenv, nvm, rustup, SDKMAN, phpenv)", {
        "tipo": "metodo",
        "objetivo": "Aprender a instalar cada lenguaje y, sobre todo, a manejar varias versiones en la misma máquina. Distintos proyectos necesitan distintas versiones; los gestores de versiones (pyenv, nvm, rustup, SDKMAN) permiten cambiar entre ellas sin conflictos. Es la base para no 'romper' tu entorno.",
        "resultados": [
            "Instalar un lenguaje del núcleo con su gestor recomendado.",
            "Cambiar entre versiones por proyecto.",
            "Explicar por qué un gestor de versiones evita conflictos.",
        ],
        "temas": [
            ("El problema de las versiones", "Proyectos que exigen versiones distintas"),
            ("Gestores por lenguaje", "pyenv, nvm, rustup, SDKMAN, phpenv"),
            ("Versión global vs. por proyecto", "Fijar la versión donde corresponde"),
            ("Entornos aislados", "Que un proyecto no afecte a otro"),
        ],
        "definiciones": [
            ("Gestor de versiones", "herramienta que instala y alterna versiones de un lenguaje (pyenv, nvm). Clave: varias versiones conviven sin chocar."),
            ("Versión por proyecto", "fijar qué versión usa una carpeta concreta (.python-version, .nvmrc). Clave: reproducibilidad entre máquinas."),
            ("rustup", "instalador y gestor oficial de Rust (toolchains, componentes). Clave: estándar de facto de la comunidad Rust."),
            ("SDKMAN", "gestor de versiones para el ecosistema JVM (Java, Kotlin, Gradle). Clave: cambia de JDK con un comando."),
        ],
        "situacion": "Un proyecto viejo necesita Node 16 y uno nuevo Node 22. Sin gestor, instalar uno rompe el otro. Con nvm, `nvm use 16` y `nvm use 22` conviven sin drama. Ese es el problema que resuelven los gestores.",
        "ejemplo": "Cada ecosistema tiene su gestor:\n\n```text\nPython:  pyenv install 3.12.4   ; pyenv local 3.12.4\nNode:    nvm install 22        ; nvm use 22\nRust:    rustup default stable\nJava:    sdk install java 21-tem\nPHP:     phpenv install 8.3\n```",
        "practica": "Comprueba qué versión de un lenguaje tienes instalada (`python --version`, `node --version`). Averigua cómo fijarías una versión distinta solo para un proyecto.",
        "errores": [
            ("Instalar una sola versión global para todo", "romper proyectos que exigen otra", "usar un gestor y fijar la versión por proyecto"),
            ("Editar el PATH a mano sin control", "entorno frágil e irreproducible", "dejar que el gestor de versiones administre las rutas"),
        ],
        "faq": [
            ("¿Necesito un gestor si solo tengo un proyecto?", "Aún así ayuda: cuando llegue el segundo proyecto, ya estarás preparado."),
            ("¿Docker no resuelve esto?", "También aísla versiones, a otro nivel (todo el sistema). Se complementan."),
        ],
    }),
    ("Ejecutar: python, node, tsx, java, dotnet, go run, rustc, cc, php, sqlite3", {
        "tipo": "metodo",
        "objetivo": "Aprender el comando de 'ejecutar un programa' en cada lenguaje del núcleo, y por qué difieren. Unos ejecutan la fuente directamente (python, node, php), otros compilan y corren en un paso (go run), y otros requieren compilar primero (rustc, cc). Es la tabla de referencia que usarás en cada clase.",
        "resultados": [
            "Ejecutar un 'hola mundo' en cada lenguaje del núcleo.",
            "Explicar por qué unos comandos son de un paso y otros de dos.",
            "Relacionar el comando de ejecución con el modelo (compilado/interpretado).",
        ],
        "temas": [
            ("Ejecutar la fuente", "Interpretados: python, node, php"),
            ("Compilar y ejecutar", "En un paso (go run) o en dos (rustc, cc)"),
            ("Bytecode + VM", "java, dotnet run"),
            ("El caso SQL", "Se ejecuta dentro de un motor (sqlite3)"),
        ],
        "definiciones": [
            ("Ejecutar", "poner en marcha un programa. Clave: el comando exacto depende del modelo del lenguaje."),
            ("Un paso vs. dos pasos", "compilar+correr juntos (go run) o separados (rustc; luego ./main). Clave: dos pasos dan un binario reutilizable."),
            ("tsx", "ejecutor que compila y corre TypeScript al vuelo. Clave: evita transpilar a mano en desarrollo."),
            ("sqlite3", "motor de base de datos que ejecuta SQL desde un archivo o la entrada estándar. Clave: cómo 'corre' SQL en el curso."),
        ],
        "situacion": "Al abrir la clase 041, cada implementación trae su comando de ejecución. Tenerlos memorizados —o a mano— convierte el estudio en algo fluido en vez de una búsqueda constante.",
        "ejemplo": "La tabla de ejecución del núcleo (misma que en cada clase):\n\n```text\nPython      python main.py\nJavaScript  node main.mjs\nTypeScript  pnpm exec tsx main.ts\nJava        java Main.java\nC#          dotnet run\nGo          go run main.go\nRust        rustc main.rs -o main && ./main\nC           cc main.c -o main && ./main\nPHP         php main.php\nSQL         sqlite3 :memory: < main.sql\n```",
        "practica": "Ejecuta el 'hola mundo' de dos lenguajes que tengas instalados. Fíjate cuál da un binario (archivo `main`) y cuál no.",
        "errores": [
            ("Buscar un binario tras `python main.py`", "esperar comportamiento de compilado", "recordar que los interpretados no generan ejecutable"),
            ("Olvidar el segundo paso en Rust/C", "compilar y no ejecutar", "encadenar la ejecución (`&& ./main`) o correrlo aparte"),
        ],
        "faq": [
            ("¿`java Main.java` no necesita compilar?", "Desde Java 11 puede ejecutar un único archivo fuente directamente; compila en memoria."),
            ("¿Por qué `go run` y no `go build`?", "`run` compila y ejecuta al vuelo; `build` genera el binario para distribuir."),
        ],
    }),
    ("Compilar y construir: gcc/clang, cargo, go build, javac, dotnet build", {
        "tipo": "metodo",
        "objetivo": "Distinguir 'ejecutar' de 'construir': construir produce un artefacto (binario, jar, dll) listo para distribuir o desplegar, sin ejecutarlo. Cada lenguaje compilado tiene su comando de construcción, y los proyectos reales se apoyan en un sistema de construcción (cargo, gradle, msbuild) que gestiona dependencias y pasos.",
        "resultados": [
            "Diferenciar ejecutar de construir/compilar a un artefacto.",
            "Usar el comando de construcción de cada lenguaje del núcleo.",
            "Explicar el papel de un sistema de construcción (build system).",
        ],
        "temas": [
            ("Ejecutar vs. construir", "Correr ahora vs. producir un artefacto"),
            ("Compilador directo", "gcc/clang, javac, rustc"),
            ("Sistema de construcción", "cargo, go build, dotnet build, gradle"),
            ("Artefactos", "Binarios, .jar, .dll listos para desplegar"),
        ],
        "definiciones": [
            ("Construir (build)", "producir el artefacto final (ejecutable, librería) a partir del código. Clave: el resultado se distribuye o despliega."),
            ("Artefacto", "salida de la construcción: binario, .jar, .dll, wheel. Clave: es lo que se entrega, no el código fuente."),
            ("Sistema de construcción", "herramienta que orquesta compilación y dependencias (cargo, gradle, msbuild). Clave: automatiza builds reproducibles."),
            ("Compilación separada", "compilar módulos por separado y enlazarlos. Clave: acelera recompilaciones (solo lo que cambió)."),
        ],
        "situacion": "Durante el desarrollo usas `go run`; para desplegar en el servidor usas `go build`, que produce un binario que copias y ejecutas sin necesitar el toolchain. Ejecutar y construir sirven a momentos distintos.",
        "ejemplo": "Comandos de construcción del núcleo:\n\n```text\nC:     gcc main.c -o programa\nRust:  cargo build --release      → target/release/programa\nGo:    go build -o programa\nJava:  javac Main.java            → Main.class\nC#:    dotnet build -c Release    → bin/Release/...\n```",
        "practica": "Si tienes Go o Rust, construye un binario y ejecútalo directamente (sin `run`). Observa que ya no necesitas el código fuente para correrlo.",
        "errores": [
            ("Desplegar el código fuente en vez del artefacto", "confundir build con run", "construir y distribuir el binario/artefacto, no las fuentes"),
            ("Recompilar todo cada vez", "no aprovechar la compilación incremental", "dejar que el build system recompile solo lo cambiado"),
        ],
        "faq": [
            ("¿Cuál es la diferencia entre debug y release?", "Release optimiza y quita información de depuración: más rápido, más difícil de depurar."),
            ("¿Los interpretados se 'construyen'?", "Suelen empaquetarse (wheel, tarball) más que compilarse; el concepto de artefacto sigue aplicando."),
        ],
    }),
    ("Paquetes y dependencias: pip, pnpm, cargo, maven/gradle, nuget, go mod, composer", {
        "tipo": "metodo",
        "objetivo": "Entender cómo cada lenguaje reutiliza código de terceros mediante un gestor de paquetes y un archivo de manifiesto que declara las dependencias. Nadie escribe todo desde cero: pip, pnpm, cargo, composer y sus primos descargan, versionan y bloquean librerías para que tu proyecto sea reproducible.",
        "resultados": [
            "Explicar qué es una dependencia y un gestor de paquetes.",
            "Identificar el manifiesto y el lockfile de cada lenguaje del núcleo.",
            "Entender por qué el lockfile garantiza builds reproducibles.",
        ],
        "temas": [
            ("Dependencias", "Código de terceros que tu proyecto reutiliza"),
            ("Manifiesto", "Declara qué dependencias y qué versiones"),
            ("Lockfile", "Fija las versiones exactas para reproducibilidad"),
            ("Repositorios de paquetes", "PyPI, npm, crates.io, Packagist…"),
        ],
        "definiciones": [
            ("Gestor de paquetes", "herramienta que descarga e instala dependencias (pip, cargo, composer). Clave: automatiza reutilizar código ajeno."),
            ("Manifiesto", "archivo que declara las dependencias (pyproject.toml, package.json, Cargo.toml). Clave: la lista de lo que el proyecto necesita."),
            ("Lockfile", "archivo con las versiones exactas resueltas (package-lock.json, Cargo.lock). Clave: mismo resultado en toda máquina."),
            ("Repositorio de paquetes", "servidor central de librerías (PyPI, npm, crates.io). Clave: de donde se descargan las dependencias."),
        ],
        "situacion": "Funciona en tu máquina pero falla en la del compañero: instalasteis versiones distintas de una librería. El lockfile resuelve exactamente esto, congelando las versiones para que ambos obtengáis lo mismo.",
        "ejemplo": "Manifiesto y gestor por lenguaje:\n\n```text\nPython   pip / pyproject.toml      (repos: PyPI)\nJS/TS    pnpm / package.json       (repos: npm)\nRust     cargo / Cargo.toml        (repos: crates.io)\nJava     gradle o maven / pom.xml  (repos: Maven Central)\nC#       nuget / .csproj           (repos: NuGet)\nGo       go mod / go.mod           (repos: proxy de módulos)\nPHP      composer / composer.json  (repos: Packagist)\n```",
        "practica": "Abre un manifiesto (package.json, Cargo.toml o pyproject.toml) de cualquier proyecto. Localiza la lista de dependencias y su versión. ¿Hay un lockfile al lado?",
        "errores": [
            ("No commitear el lockfile", "builds distintos en cada máquina", "versionar el lockfile junto al manifiesto"),
            ("Fijar versiones a '*' o 'latest'", "roturas por actualizaciones inesperadas", "acotar rangos de versión y confiar en el lockfile"),
        ],
        "faq": [
            ("¿pnpm o npm?", "Este curso usa pnpm en JS/TS por su eficiencia; el concepto (manifiesto + lockfile) es idéntico."),
            ("¿Go no tiene lockfile?", "Usa go.mod y go.sum (este último fija los hashes exactos, cumpliendo el rol de lock)."),
        ],
    }),
    ("REPL e intérpretes interactivos por lenguaje", {
        "tipo": "metodo",
        "objetivo": "Descubrir el REPL (Read-Eval-Print Loop): una consola interactiva donde escribes una expresión y ves su resultado al instante, sin crear un archivo ni compilar. Es la herramienta ideal para explorar, probar una idea o entender cómo se comporta un fragmento. Casi todos los lenguajes del núcleo tienen uno.",
        "resultados": [
            "Explicar qué es un REPL y cuándo usarlo.",
            "Abrir el REPL de al menos dos lenguajes del núcleo.",
            "Distinguir explorar en el REPL de escribir un programa en un archivo.",
        ],
        "temas": [
            ("Qué es un REPL", "Leer, evaluar, imprimir, repetir"),
            ("Para qué sirve", "Explorar y probar sin ceremonia"),
            ("REPL por lenguaje", "python, node, irb, ghci, dotnet fsi…"),
            ("Sus límites", "No sustituye a un archivo para programas reales"),
        ],
        "definiciones": [
            ("REPL", "consola interactiva que lee una expresión, la evalúa, imprime el resultado y repite. Clave: retroalimentación inmediata."),
            ("Evaluar", "calcular el valor de una expresión. Clave: en el REPL, cada línea se evalúa y muestra al instante."),
            ("Sesión interactiva", "el estado que acumula el REPL mientras trabajas. Clave: las variables persisten hasta cerrarlo."),
            ("Scratch/exploración", "uso del REPL para tantear ideas. Clave: complementa, no reemplaza, el código en archivos."),
        ],
        "situacion": "¿Qué devuelve `0.1 + 0.2` en JavaScript? En vez de escribir un archivo, abres el REPL de Node, lo tecleas y ves `0.30000000000000004` al instante. El REPL convierte una duda en un experimento de tres segundos.",
        "ejemplo": "Abrir el REPL de cada lenguaje:\n\n```text\nPython   python           >>> 2 + 2\nNode     node             > 2 + 2\nGo       (no oficial; usar 'gore' o el playground)\nRuby     irb              irb> 2 + 2\nHaskell  ghci             ghci> 2 + 2\n```",
        "practica": "Abre el REPL de Python o Node y prueba tres expresiones que te generen curiosidad (por ejemplo, mezclar tipos). Observa las respuestas al instante.",
        "errores": [
            ("Escribir un programa entero en el REPL", "perder el trabajo al cerrarlo", "usar el REPL para explorar; los programas van en archivos"),
            ("Creer que todos tienen REPL nativo", "asumir uniformidad", "saber que algunos (Go, C) no lo traen de serie"),
        ],
        "faq": [
            ("¿El REPL sirve para depurar?", "Para probar fragmentos, sí; para depurar un programa en marcha, se usa un debugger."),
            ("¿C tiene REPL?", "No de forma nativa; existen herramientas experimentales, pero no es habitual."),
        ],
    }),
    ("Formateadores y linters: black, prettier, gofmt, rustfmt, clang-format, php-cs-fixer", {
        "tipo": "metodo",
        "objetivo": "Conocer dos herramientas que elevan la calidad sin esfuerzo manual: el formateador, que reescribe el código con un estilo consistente, y el linter, que detecta problemas y malas prácticas. Automatizan la legibilidad e idiomática que estudiaste en la Parte 0, y evitan discusiones de estilo en los equipos.",
        "resultados": [
            "Distinguir formateador de linter.",
            "Nombrar el formateador de cada lenguaje del núcleo.",
            "Explicar por qué automatizar el estilo mejora el trabajo en equipo.",
        ],
        "temas": [
            ("Formateador", "Reescribe el código con un estilo único"),
            ("Linter", "Detecta errores probables y malas prácticas"),
            ("Herramientas por lenguaje", "black, prettier, gofmt, rustfmt, clippy…"),
            ("Integración", "En el editor y en el CI"),
        ],
        "definiciones": [
            ("Formateador", "herramienta que reescribe el código con un estilo consistente (black, gofmt). Clave: elimina las discusiones de formato."),
            ("Linter", "analiza el código en busca de errores probables y anti-patrones (clippy, ESLint). Clave: previene bugs antes de ejecutar."),
            ("Estilo consistente", "que todo el código luzca igual sin importar quién lo escribió. Clave: facilita leer y revisar."),
            ("gofmt", "formateador oficial de Go; no admite configuración. Clave: un solo estilo para toda la comunidad Go."),
        ],
        "situacion": "En una revisión de código, medio equipo discute si usar 2 o 4 espacios. Con un formateador (gofmt, black) la pregunta desaparece: la herramienta decide y todos aceptan. La energía se dedica a la lógica, no al formato.",
        "ejemplo": "Formateador y linter por lenguaje:\n\n```text\nPython   black (formato)      + ruff/flake8 (lint)\nJS/TS    prettier             + eslint\nGo       gofmt                + go vet\nRust     rustfmt              + clippy\nC/C++    clang-format\nPHP      php-cs-fixer\n```",
        "practica": "Si tienes uno instalado, pasa un formateador por un archivo desordenado y observa el 'antes y después'. ¿Qué reglas aplicó?",
        "errores": [
            ("Formatear a mano", "perder tiempo y ser inconsistente", "delegar el formato al formateador, integrado en el editor"),
            ("Ignorar los avisos del linter", "dejar pasar bugs latentes", "tratar los avisos como pistas y resolverlos o justificarlos"),
        ],
        "faq": [
            ("¿Formateador y linter son lo mismo?", "No: el formateador cambia el aspecto; el linter señala problemas de fondo. Se usan juntos."),
            ("¿gofmt se puede configurar?", "No, a propósito: Go impone un único estilo para toda la comunidad."),
        ],
    }),
    ("Pruebas desde la terminal: pytest, node --test, go test, cargo test, dotnet test, phpunit", {
        "tipo": "metodo",
        "objetivo": "Aprender a ejecutar pruebas automatizadas desde la línea de comandos en cada lenguaje. Las pruebas son código que verifica tu código: se corren con un comando y te dicen si algo se rompió. Es la base del verificador de equivalencia del curso y de cualquier proyecto profesional.",
        "resultados": [
            "Explicar qué es una prueba automatizada y para qué sirve.",
            "Nombrar el runner de pruebas de cada lenguaje del núcleo.",
            "Relacionar las pruebas con el verificador de equivalencia del curso.",
        ],
        "temas": [
            ("Qué es una prueba", "Código que comprueba que otro código funciona"),
            ("Runners por lenguaje", "pytest, go test, cargo test, dotnet test…"),
            ("Rojo/verde", "La prueba pasa o falla; el CI lo automatiza"),
            ("Conexión con el curso", "casos.json es una prueba de equivalencia"),
        ],
        "definiciones": [
            ("Prueba automatizada", "código que verifica que otro código produce el resultado esperado. Clave: se ejecuta con un comando y no depende de revisión manual."),
            ("Runner de pruebas", "herramienta que descubre y ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas."),
            ("Aserción", "comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo."),
            ("Verde/rojo", "estado de la suite de pruebas: todo pasa (verde) o algo falla (rojo). Clave: el CI lo usa para bloquear cambios."),
        ],
        "situacion": "Cambias una función y no sabes si rompiste algo más. Ejecutas `pytest` y en segundos sabes si las 200 pruebas siguen en verde. Sin pruebas, ese cambio sería un salto de fe; con ellas, una comprobación.",
        "ejemplo": "Comando de pruebas por lenguaje:\n\n```text\nPython   pytest\nJS       node --test\nGo       go test ./...\nRust     cargo test\nC#       dotnet test\nPHP      ./vendor/bin/phpunit\n```\n\nEn este curso, además: python scripts/verificar_equivalencia.py --all",
        "practica": "El verificador de equivalencia es, en el fondo, una prueba: compara la salida real con la esperada. Ejecútalo sobre la clase 041 y observa el 'verde' de cada implementación.",
        "errores": [
            ("Probar solo a mano ejecutando el programa", "verificación lenta y no repetible", "escribir pruebas automatizadas que corran con un comando"),
            ("No correr las pruebas antes de subir cambios", "romper el CI", "ejecutar la suite localmente antes de hacer push"),
        ],
        "faq": [
            ("¿Cuántas pruebas necesito?", "Al menos una por comportamiento importante y por caso límite; la calidad importa más que la cantidad."),
            ("¿casos.json es una prueba?", "Sí: define entradas y salidas esperadas; el verificador las comprueba como haría un runner."),
        ],
    }),
    ("Empaquetado y distribución: wheels, jars, binarios, contenedores", {
        "tipo": "metodo",
        "objetivo": "Entender cómo se entrega un programa a quien lo va a usar. Según el lenguaje, el artefacto es una wheel (Python), un jar (Java), un binario (Go/Rust/C) o una imagen de contenedor (Docker) que empaqueta el programa con su entorno. Empaquetar bien es la diferencia entre 'funciona en mi máquina' y 'funciona en cualquier parte'.",
        "resultados": [
            "Nombrar el formato de distribución típico de cada lenguaje.",
            "Explicar qué resuelve un contenedor frente a distribuir solo el artefacto.",
            "Relacionar el empaquetado con la reproducibilidad.",
        ],
        "temas": [
            ("Formatos de artefacto", "wheel, jar, binario, dll"),
            ("El binario autocontenido", "Go y Rust producen un solo archivo"),
            ("Contenedores", "Empaquetan el programa con su entorno"),
            ("Distribución", "Repositorios, registries y releases"),
        ],
        "definiciones": [
            ("Empaquetado", "preparar un programa y sus dependencias para distribuirlo. Clave: define cómo lo instala el usuario final."),
            ("wheel/jar", "formatos empaquetados de Python y Java. Clave: instalables sin recompilar."),
            ("Binario autocontenido", "un único ejecutable con todo dentro (típico de Go). Clave: se copia y corre sin instalar nada más."),
            ("Contenedor", "imagen que incluye el programa y su sistema operativo mínimo (Docker). Clave: elimina el 'funciona en mi máquina'."),
        ],
        "situacion": "Un servicio en Python funciona en desarrollo pero falla en producción por una versión distinta de una librería del sistema. Empaquetarlo en un contenedor lleva el entorno entero consigo, y el problema desaparece.",
        "ejemplo": "Formato de distribución por lenguaje:\n\n```text\nPython   wheel (.whl) / sdist       → pip install\nJava     jar (.jar)                → java -jar app.jar\nGo/Rust  binario único             → copiar y ejecutar\nC#       dll / ejecutable .NET\nCualquiera  imagen Docker          → docker run\n```",
        "practica": "Piensa cómo entregarías un programa a alguien sin tu entorno: ¿un binario, una wheel, un contenedor? Justifica según el lenguaje.",
        "errores": [
            ("Distribuir el código fuente y pedir 'que lo compilen'", "trasladar la complejidad al usuario", "entregar un artefacto o imagen lista para usar"),
            ("Asumir que el entorno destino es igual al tuyo", "el clásico 'en mi máquina funciona'", "empaquetar el entorno con un contenedor cuando importe"),
        ],
        "faq": [
            ("¿Un contenedor es una máquina virtual?", "No: comparte el kernel del host, es más ligero; empaqueta el entorno, no un SO completo."),
            ("¿Por qué Go es cómodo de distribuir?", "Compila a un binario estático único: se copia y funciona sin dependencias externas."),
        ],
    }),
    ("Variables de entorno, rutas y el PATH en Windows y Unix", {
        "tipo": "metodo",
        "objetivo": "Entender el entorno donde corren tus comandos: las variables de entorno (configuración que el sistema pasa a los programas) y en especial el PATH, la lista de carpetas donde el sistema busca los ejecutables. Dominar esto explica el 90% de los errores tipo 'command not found' y las diferencias entre Windows y Unix.",
        "resultados": [
            "Explicar qué es una variable de entorno y para qué sirve el PATH.",
            "Diagnosticar un 'command not found' a partir del PATH.",
            "Reconocer las diferencias de rutas entre Windows y Unix.",
        ],
        "temas": [
            ("Variables de entorno", "Configuración que reciben los programas"),
            ("El PATH", "Dónde busca el sistema los ejecutables"),
            ("Rutas Windows vs. Unix", "Separadores, mayúsculas, barras"),
            ("Diagnóstico", "Por qué 'command not found' y cómo resolverlo"),
        ],
        "definiciones": [
            ("Variable de entorno", "valor con nombre que el sistema pasa a los programas (PATH, HOME). Clave: configura sin tocar el código."),
            ("PATH", "lista de carpetas donde se buscan los ejecutables. Clave: si un programa no está en el PATH, 'no se encuentra'."),
            ("Ruta absoluta vs. relativa", "desde la raíz (/usr/bin) o desde la carpeta actual (./main). Clave: evita ambigüedad sobre qué se ejecuta."),
            ("Separador de rutas", "':' en Unix y ';' en Windows para el PATH; '/' vs. '\\' en las rutas. Clave: fuente de errores multiplataforma."),
        ],
        "situacion": "Instalas una herramienta y la terminal responde 'command not found'. No está rota: simplemente su carpeta no está en el PATH, así que el sistema no sabe dónde buscarla. Añadirla al PATH lo resuelve.",
        "ejemplo": "Ver y usar variables de entorno y el PATH:\n\n```text\nUnix (bash):\n  echo $PATH                    # ver el PATH\n  export API_KEY=\"abc123\"       # definir una variable\n\nWindows (PowerShell):\n  $env:PATH                     # ver el PATH\n  $env:API_KEY = \"abc123\"       # definir una variable\n```",
        "practica": "Muestra tu PATH (`echo $PATH` o `$env:PATH`). Cuenta cuántas carpetas incluye. ¿Está la del lenguaje que instalaste?",
        "errores": [
            ("Culpar al programa por 'command not found'", "no revisar el PATH", "verificar si la carpeta del ejecutable está en el PATH"),
            ("Escribir rutas con '/' en scripts de Windows (o al revés)", "ignorar el separador del sistema", "usar rutas relativas o herramientas que abstraigan el separador"),
        ],
        "faq": [
            ("¿Dónde guardo secretos como una API key?", "En variables de entorno, no en el código; nunca las subas al repositorio."),
            ("¿Por qué Windows y Unix difieren tanto?", "Herencias históricas distintas; por eso el curso muestra ambos y prefiere lo portable."),
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
     P1),

    ("Herramientas, toolchains y anatomía de comandos",
     "Del código fuente al programa que corre: instalar, ejecutar, compilar, empaquetar y probar en cada lenguaje, con el esquema completo de cada comando.",
     P2),

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
