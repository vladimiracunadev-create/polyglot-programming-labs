"""Fuente de verdad del currículo de Polyglot Programming Labs.

Este módulo describe las 12 partes y las 176 clases del programa. Los scripts
generadores (manifest, índice, sitio, validación) lo importan para no repetir
datos. Cada clase es como mínimo un título; las clases "construidas" añaden un
diccionario con objetivo, resultados, temas y definiciones que el generador
expande al README completo.
"""

from __future__ import annotations

import re
import unicodedata

# Lenguajes del núcleo (se implementan y se verifican en CI).
NUCLEO = [
    "python", "javascript", "typescript", "java", "csharp",
    "go", "rust", "c", "sql", "php",
]

# Familias cubiertas por características en el Atlas (comprensión, no práctica).
FAMILIAS_ATLAS = [
    "C / llaves", "scripting dinámico", "JVM", ".NET", "JavaScript / web",
    "funcional tipada (ML)", "Lisp", "lógica y declarativa",
    "concurrente / actor", "sistemas", "array / científica", "históricos",
]


def slug(texto: str) -> str:
    """Convierte un título en un slug ASCII con guiones."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = t.lower()
    t = t.replace("+", " plus ").replace("#", " sharp ").replace("/", " ")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


# ---------------------------------------------------------------------------
# Estructura del currículo.
#   Cada parte: (título, subtítulo, [clases])
#   Cada clase: título (str)  o  (título, dict con contenido rico)
# ---------------------------------------------------------------------------

PARTES = [
    ("Pensamiento computacional y el método políglota",
     "Cómo pensar un problema antes de elegir lenguaje, y el método de fichas de transferencia que sostiene todo el programa.",
     [
        ("Qué es programar y por qué comparar lenguajes: la tesis políglota", {
            "objetivo": "Entender la tesis del programa: el conocimiento de la programación es transferible. Un mismo concepto (una variable, un bucle, una función) existe en todos los lenguajes; lo que cambia es la forma. Aprender el concepto una vez permite reconocerlo, compararlo y aplicarlo en cualquier lenguaje.",
            "resultados": [
                "Explicar la diferencia entre aprender un lenguaje y aprender a programar.",
                "Enunciar la tesis políglota: concepto → forma neutral → implementaciones → comparación → transferencia.",
                "Distinguir conocimiento transferible de detalle sintáctico.",
                "Justificar por qué comparar lenguajes acelera el aprendizaje en vez de dispersarlo.",
            ],
            "temas": [
                ("Concepto vs. sintaxis", "Separa lo que perdura de lo que cambia entre lenguajes"),
                ("Los 10 lenguajes del núcleo", "Definen el terreno práctico que se implementa y verifica"),
                ("Las ~40 familias del Atlas", "Amplían la comprensión sin multiplicar el mantenimiento"),
                ("La ficha de transferencia", "Es la unidad mínima de estudio del programa"),
                ("Reconocer, comparar, aplicar", "El ciclo que convierte teoría en habilidad transferible"),
            ],
            "definiciones": [
                ("Conocimiento transferible", "idea que sobrevive al cambio de lenguaje (p. ej. 'iterar una colección'). Clave: es lo que de verdad se aprende."),
                ("Núcleo", "los 10 lenguajes que se implementan y verifican en CI. Clave: profundidad práctica."),
                ("Atlas", "cobertura de ~40 lenguajes por sus características. Clave: amplitud de comprensión."),
                ("Ficha de transferencia", "unidad de estudio: concepto, algoritmo, implementaciones y comparación. Clave: mismo problema en todos los lenguajes."),
            ],
        }),
        ("Las tres clases de diferencia: sintáctica, semántica y paradigmática", {
            "objetivo": "Dar el marco que se usará en cada comparación del curso: cuando dos lenguajes difieren, la diferencia es de una de tres clases. Sintáctica (se escribe distinto pero significa lo mismo), semántica (cambia el comportamiento, el tipo, la memoria) o paradigmática (invita a estructurar la solución de otra manera).",
            "resultados": [
                "Clasificar una diferencia entre lenguajes como sintáctica, semántica o paradigmática.",
                "Dar ejemplos propios de cada clase de diferencia.",
                "Explicar por qué confundir las tres clases lleva a traducir mecánicamente en vez de programar idiomáticamente.",
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
                ("Diferencia paradigmática", "distinta forma de estructurar el problema. Clave: exige cambiar de mentalidad, no solo de sintaxis."),
                ("Código idiomático", "solución escrita como la escribiría un experto de ese lenguaje. Clave: aprovecha el paradigma, no lo combate."),
            ],
        }),
        ("Problema, contexto, entradas, proceso y salidas", {
            "objetivo": "Antes de escribir una línea de código hay que modelar el problema: qué entra, qué sale, bajo qué reglas y en qué contexto. Este modelo es independiente del lenguaje y es lo primero que define cada ficha del curso.",
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
                ("Especificación", "descripción de qué debe hacer un programa, no cómo. Clave: neutral al lenguaje."),
                ("Entrada", "dato que el programa recibe. Clave: define el dominio del problema."),
                ("Salida", "resultado observable. Clave: es lo que se verifica con casos.json."),
                ("Restricción", "condición que la solución debe respetar. Clave: acota el espacio de soluciones."),
            ],
        }),
        "Descomposición y reconocimiento de patrones",
        "Abstracción, restricciones y casos límite",
        "Algoritmos: corrección y terminación",
        "Pseudocódigo neutral: escribir sin lenguaje",
        "Trazado manual y ejecución simbólica",
        "Complejidad y eficiencia: intuición de coste",
        "Legibilidad, estilo e idiomática",
        "Anatomía de una ficha de transferencia y cómo estudiarla",
        "casos.json y el verificador de equivalencia",
        "El concepto en la familia: leer un lenguaje que no conoces",
        "Cómo elegir lenguaje para un problema",
     ]),

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
    """Genera tuplas (num_global, idx_parte, titulo, datos|None)."""
    num = 0
    for idx, (_ptitulo, _psub, clases) in enumerate(PARTES):
        for c in clases:
            num += 1
            if isinstance(c, tuple):
                titulo, datos = c
            else:
                titulo, datos = c, None
            yield num, idx, titulo, datos


def total_clases() -> int:
    return sum(len(clases) for _, _, clases in PARTES)


if __name__ == "__main__":
    print(f"Partes: {len(PARTES)}")
    print(f"Clases: {total_clases()}")
    for idx, (t, _s, clases) in enumerate(PARTES):
        ini = sum(len(PARTES[i][2]) for i in range(idx)) + 1
        fin = ini + len(clases) - 1
        print(f"  Parte {idx}: {t} · {len(clases)} clases · {ini:03d}-{fin:03d}")
