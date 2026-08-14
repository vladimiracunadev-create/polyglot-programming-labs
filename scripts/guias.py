"""Contenido pedagógico de las partes: la narrativa que el índice no puede dar.

`curriculo.py` dice QUÉ clases hay; este módulo dice QUÉ SE APRENDE en cada una
y POR QUÉ están en ese orden. `build.py` lo usa para generar el README de cada
parte (y el índice general) con materia real en vez de una tabla de enlaces.

Estructura:

    GUIA[idx] = {
        "gancho":        una frase que responde "¿de qué va esta parte?",
        "resumen":       2-3 párrafos: qué problema resuelve y por qué va aquí,
        "asume":         qué hay que traer de las partes anteriores,
        "logros":        resultados verificables al terminar,
        "bloques":       [(título, por qué van juntas, primera, última), ...],
        "malentendidos": [(creencia extendida, corrección), ...],
        "abre":          qué hace posible la parte siguiente,
    }
    CLASES[num] = descripción pedagógica de la clase (1-2 frases).

Las descripciones se escriben a mano, ancladas en el objetivo real de cada
clase. No se generan: un resumen automático produciría texto plausible y vacío,
que es justo lo que este módulo existe para evitar.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Datos operativos por parte (horas del syllabus, tipo y nivel).
# --------------------------------------------------------------------------- #

HORAS = {0: 21, 1: 21, 2: 18, 3: 40, 4: 40, 5: 40,
         6: 45, 7: 40, 8: 40, 9: 40, 10: 25, 11: 36}

TIPO = {0: "método", 1: "método", 2: "método", 3: "código", 4: "código",
        5: "código", 6: "código", 7: "código", 8: "código", 9: "código",
        10: "código", 11: "proyecto"}

# Cómo se estudia según el tipo de clase. Se declara una vez porque es
# honestamente el mismo procedimiento en todas las partes del mismo tipo:
# repetirlo con variaciones cosméticas sería relleno.
ESTUDIAR = {
    "método": [
        "**Lee la clase entera antes de opinar.** Son clases de razonamiento: el valor está en el argumento completo, no en la definición suelta.",
        "**Contesta la pregunta que abre cada clase** con tus palabras antes de seguir a la siguiente. Si no puedes, vuelve al párrafo del objetivo.",
        "**Aplícalo a un problema tuyo.** Estas clases no se verifican con una máquina; se verifican usándolas sobre código real que ya escribiste.",
        "**Anota los términos nuevos.** Aparecen otra vez, con código delante, a partir de la Parte 3 — y están todos en el [glosario](../../glosario/README.md).",
    ],
    "código": [
        "**Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.",
        "**Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.",
        "**Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.",
        "**Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.",
        "**Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.",
    ],
    "proyecto": [
        "**Trabaja el proyecto de corrido, no clase a clase suelta.** Cada clase añade un componente al mismo sistema; saltarse una deja un hueco en el siguiente.",
        "**Escribe el contrato antes que el código** de cada componente: entradas, salidas, errores y quién es responsable de qué.",
        "**Ejecuta el sistema completo al cerrar cada clase**, aunque la pieza nueva sea mínima. Un sistema políglota que solo funciona por partes no funciona.",
        "**Justifica cada elección de lenguaje por escrito.** La defensa razonada es parte entregable del proyecto, no un adorno.",
    ],
}


# --------------------------------------------------------------------------- #
# Descripción pedagógica de cada clase: qué aprendes y por qué importa.
# --------------------------------------------------------------------------- #

CLASES = {
    # --- Parte 0 · Pensamiento computacional -------------------------------- #
    1: "Separa programar de «saber la sintaxis de un lenguaje»: programar es expresar la solución de un problema con precisión suficiente para que una máquina, que no entiende nada, la ejecute sin ambigüedad. De ahí sale la tesis del curso: si lo esencial es el problema y el algoritmo, el lenguaje es la forma — y compararlo con otros es lo que revela cuál es cuál.",
    2: "Instala la brújula que se usa en las 175 clases restantes: toda diferencia entre dos lenguajes es **sintáctica** (cómo se escribe), **semántica** (qué ocurre al ejecutarse) o **paradigmática** (qué considera una pieza legítima de solución). Confundirlas es la causa número uno de las discusiones estériles sobre lenguajes.",
    3: "Modelar antes de teclear: decidir qué datos entran, qué resultado sale, bajo qué reglas ocurre la transformación y en qué contexto tiene sentido. Ese modelo es exactamente lo que después se escribe como `casos.json` y lo que diez implementaciones deben satisfacer por igual.",
    4: "Partir un problema grande en subproblemas manejables y reconocer cuándo un subproblema ya lo resolviste antes con otra forma. Es la habilidad que separa a quien programa cosas pequeñas de quien construye sistemas, y la que evita reescribir tres veces la misma solución sin notarlo.",
    5: "Tres herramientas que trabajan juntas: **abstraer** (quedarse con lo esencial y descartar el resto), **restringir** (declarar las reglas que la solución debe cumplir) y buscar deliberadamente los **casos límite** —el vacío, el cero, el negativo, el máximo— que es donde los programas se rompen de verdad.",
    6: "Un algoritmo no vale por «parece que funciona»: necesita **corrección** (produce el resultado esperado para toda entrada válida) y **terminación** (garantiza que acaba). Aquí aprendes a argumentar ambas con invariantes y variantes en lugar de con intuición.",
    7: "El **pseudocódigo neutral** es la notación que hace posible todo el curso: describe el algoritmo sin comprometerse con ningún lenguaje real, de modo que las diez implementaciones sean traducciones de un mismo texto y no diez invenciones distintas.",
    8: "Ejecutar el algoritmo con papel y lápiz, siguiendo el valor de cada variable paso a paso. Es la habilidad de depuración más fundamental que existe: la única que funciona antes de tener código, y la que convierte un bug en una hipótesis comprobable.",
    9: "Pasar de «¿funciona?» a «¿cuánto **cuesta** cuando la entrada crece?». Intuición de órdenes de magnitud —constante, logarítmico, lineal, cuadrático— suficiente para elegir estructura de datos antes de medir, sin necesidad de formalismo pesado.",
    10: "El código se lee muchas más veces de las que se escribe. Aquí se distingue **estilo** (convención de forma, automatizable) de **idiomática** (la manera natural de decir algo en ese lenguaje concreto), que es justo lo que hace que el mismo algoritmo se vea distinto en Python y en Go sin que ninguno esté peor escrito.",
    11: "El manual de instrucciones del curso: cómo está montada una clase de código —modelo, pseudocódigo, diez implementaciones, comparación, `casos.json`, primos y reto— y en qué orden conviene leerla para que el contraste enseñe en vez de abrumar.",
    12: "La afirmación «estas diez implementaciones resuelven el mismo problema» es fácil de escribir y facilísima de equivocar. Aquí ves el mecanismo que la comprueba por máquina: mismo stdin, misma salida esperada, ejecutado en CI para los diez lenguajes.",
    13: "La habilidad más rentable del enfoque políglota: **leer con provecho código de un lenguaje que nunca estudiaste**. No escribirlo bien ni dominarlo — leerlo: entender qué hace y seguir su lógica apoyándote en la familia a la que pertenece.",
    14: "Cierra la parte con la pregunta que solo ahora se puede responder: dado un problema y su contexto —equipo, plataforma, ecosistema, plazo, riesgo—, qué lenguaje conviene y con qué argumentos se defiende esa elección ante otros.",

    # --- Parte 1 · Atlas y genealogía --------------------------------------- #
    15: "El mapa completo de familias y antepasados comunes. Sirve para dejar de percibir la programación como una lista inabarcable de tecnologías rivales y empezar a verla como lo que es: un puñado de linajes descendientes de unos pocos experimentos fundacionales.",
    16: "Un lenguaje no es un objeto fijo sino un proceso: nace de una necesidad, se formaliza en un **estándar**, se materializa en **implementaciones** y publica **versiones** con reglas de compatibilidad. Distinguir esas cuatro cosas explica por qué «Python» y «CPython» no son sinónimos.",
    17: "La familia que fijó la sintaxis dominante de la programación actual: llaves, punto y coma, `for` de tres partes. Si dominas C, ya lees la superficie de Java, C#, JavaScript, Go y PHP — aquí se explica exactamente por qué, y dónde el parecido deja de serlo.",
    18: "Los lenguajes **dinámicos**: interpretados, sin declaración obligatoria de tipos, diseñados para que un humano escriba la solución en minutos. Python y PHP están en el núcleo; Ruby, Perl y Lua son los primos cercanos que además se ejecutan en CI en cada clase de código.",
    19: "Una familia que no se define por la sintaxis sino por la **plataforma de ejecución**: todo lo que corre sobre la JVM. Java representa al núcleo; Kotlin, Scala, Groovy y Clojure comparten bytecode y biblioteca con sintaxis y paradigmas radicalmente distintos.",
    20: "El mismo fenómeno de la JVM, ahora sobre el CLR de .NET: **C#** (núcleo, multiparadigma), **F#** (funcional, de la familia ML) y **VB.NET** conviven sobre un runtime común. Dos plataformas distintas llegando a la misma idea genealógica.",
    21: "La familia que domina la web. JavaScript nació en 1995 para animar páginas y hoy corre en navegador, servidor, móvil y embebidos; TypeScript le añade tipos sin cambiar su semántica de ejecución. Aquí se entiende por qué ambos están en el núcleo y no como uno solo.",
    22: "Ningún miembro clásico de la familia ML —Haskell, OCaml, Standard ML— está en el núcleo, pero su **influencia** sí lo está y de forma profunda: los tipos algebraicos, `Option`/`Result` y la inferencia de Rust vienen de aquí. Explica por qué Rust «se siente» distinto a C.",
    23: "La familia viva más antigua (1958) y una de las más influyentes: su rasgo único es la **homoiconicidad**, el código escrito con la misma estructura que los datos. Aunque nunca escribas Lisp, sus ideas están en los cierres, las comprensiones y la metaprogramación de tu lenguaje.",
    24: "Los lenguajes donde describes **QUÉ** quieres y no **CÓMO** obtenerlo: SQL en el núcleo, Prolog y Datalog como primos. Es el primer choque frontal con un paradigma que no es una variante del imperativo, sino su opuesto.",
    25: "Lenguajes diseñados desde su base para hacer muchas cosas a la vez: el modelo de **actores** de Erlang y Elixir (procesos aislados, sin memoria compartida) frente al **CSP** de Go (canales). Aquí queda claro que «concurrencia» no es una técnica sino varios modelos incompatibles entre sí.",
    26: "Los lenguajes hechos para escribir sistemas operativos, drivers, motores de bases de datos y runtimes: C, C++, Rust y Zig. Control explícito de la memoria, sin runtime pesado y con el coste puesto donde el programador pueda verlo.",
    27: "APL, R, Julia, Fortran y MATLAB traen un estilo de pensamiento distinto: la **vectorización**, operar sobre arreglos completos de una vez en lugar de elemento a elemento con bucles. Cambia la unidad de razonamiento, no solo la sintaxis.",
    28: "COBOL, Fortran, Pascal, BASIC y Bash no forman familia por parentesco sino por destino: marcaron una época y, en vez de desaparecer, se replegaron a un nicho donde siguen siendo insustituibles. Explican decisiones de diseño que todavía heredamos.",

    # --- Parte 2 · Toolchains ------------------------------------------------ #
    29: "Entre el archivo de texto que escribes y un proceso vivo consumiendo CPU hay una cadena de herramientas. Nombrar cada eslabón —preprocesador, compilador, enlazador, cargador, intérprete— es lo que convierte un error de build en un problema localizable.",
    30: "«¿Es compilado o interpretado?» está casi siempre mal planteada: la realidad tiene cuatro respuestas —compilado a máquina, interpretado, transpilado y bytecode sobre VM— y muchos lenguajes usan varias a la vez. Aquí se corrige la dicotomía.",
    31: "La línea de comandos parece un idioma secreto y es una gramática muy regular: nombre, subcomando, flags, argumentos. Aprender el esquema permite leer un comando que nunca viste en lugar de copiarlo de un foro sin entenderlo.",
    32: "El día en que dos proyectos exigen versiones distintas del mismo lenguaje en la misma máquina, instalar deja de ser trivial. `pyenv`, `nvm`, `rustup`, SDKMAN y `phpenv` resuelven el mismo problema con la misma idea; aquí se ve el patrón común.",
    33: "El comando de ejecución de cada lenguaje del núcleo, comprendido y no memorizado: qué hace realmente `python`, `node`, `java`, `dotnet`, `go run`, `rustc`, `cc`, `php` y `sqlite3` con tu archivo antes de que aparezca la primera línea de salida.",
    34: "Ejecutar y **construir** se confunden con facilidad y sirven a momentos distintos: ejecutar es correrlo ahora; construir es producir un **artefacto** —binario, jar, wheel— que sobrevive a la sesión y viaja a otra máquina.",
    35: "Nadie escribe todo el software desde cero. Aquí se ve el mecanismo universal detrás de `pip`, `pnpm`, `cargo`, Maven/Gradle, NuGet, `go mod` y Composer: manifiesto, resolución, lockfile y caché — el mismo esquema con siete vocabularios.",
    36: "El **REPL** convierte una duda en un experimento de tres segundos: escribir una expresión, pulsar Enter y ver el resultado sin crear archivo ni compilar. Es la herramienta de aprendizaje más infrautilizada de todas.",
    37: "El **formateador** elimina la discusión sobre la forma reescribiendo el código a una convención; el **linter** detecta construcciones sospechosas antes de ejecutarlas. Automatizan justo la legibilidad que la clase 010 defendió a mano.",
    38: "Ejecutar pruebas desde la terminal en cada lenguaje: `pytest`, `node --test`, `go test`, `cargo test`, `dotnet test`, PHPUnit. Cambia el comando; no cambia la idea de dar entradas conocidas y afirmar la salida esperada.",
    39: "Un programa que funciona en tu máquina todavía no es un producto. El **empaquetado** —wheels, jars, binarios, contenedores— es el paso entre «compila aquí» y «otra persona lo ejecuta allá», y decide buena parte del éxito de un proyecto.",
    40: "Cuando escribes `python` y pulsas Enter, el sistema no sabe dónde está Python: lo busca recorriendo el **PATH**. Entender esa lista, y las variables de entorno en general, explica la mitad de los «en mi máquina sí funciona».",

    # --- Parte 3 · Valores, tipos y variables -------------------------------- #
    41: "Un valor puro —el número `27000`, la cadena `\"hola\"`— no tiene nombre ni domicilio: existe solo mientras alguien lo sostiene. Literal, valor, variable y constante son cuatro nociones distintas que el lenguaje cotidiano funde en una sola palabra.",
    42: "**Declarar** es introducir un nombre en un ámbito, **inicializar** es darle su primer valor y **asignar** es cambiárselo después. Separarlos explica por qué Java se queja de una variable «posiblemente no inicializada» y Python no puede hacerlo.",
    43: "Enteros, reales, booleanos y caracteres son los átomos con los que se construye todo dato compuesto: primitivos porque el lenguaje los trae incorporados y porque suelen corresponder a algo que la CPU sabe manejar directamente.",
    44: "La distinción entre **valor** y **representación**: `255`, `0xff`, `0o377` y `0b11111111` son cuatro formas de escribir un mismo número. Debajo aparecen el tamaño en bits, el signo en complemento a dos y el desbordamiento — y el hueco de C, que no tiene especificador para binario.",
    45: "Un real matemático tiene infinitos vecinos infinitamente cercanos; la máquina solo tiene bits finitos. IEEE 754 explica por qué `0.1 + 0.2 != 0.3` en casi todos los lenguajes, y qué hacer con el dinero, donde ese error no es aceptable.",
    46: "En 1854 Boole demostró que la lógica es un álgebra de dos valores. De ahí salen las condiciones de todo programa — y la pregunta incómoda de qué considera «verdadero» cada lenguaje: `0`, la cadena vacía, la lista vacía y `null` no votan lo mismo en todas partes.",
    47: "Toda la escritura humana que una computadora manipula es, por dentro, una sucesión de números. Unicode, punto de código, UTF-8 y la diferencia entre «carácter», «byte» y «lo que se ve en pantalla»: la fuente de los bugs más difíciles de reproducir.",
    48: "La cadena es el tipo compuesto que más usarás y el que más decisiones de diseño esconde: mutable o inmutable, indexada por bytes o por caracteres, con o sin interpolación. Cada lenguaje eligió distinto y todos tienen su razón.",
    49: "Los datos del mundo exterior llegan casi siempre como **texto**. Convertirlos tiene dos formas muy distintas: el **casting explícito**, que tú pides, y la **coerción implícita**, que el lenguaje hace por su cuenta — y que es donde nacen los resultados sorprendentes.",
    50: "El primero de los dos grandes ejes de todo sistema de tipos: **cuándo** se comprueban. Estático es antes de ejecutar (el compilador rechaza); dinámico es durante (el programa falla en el momento). No es una jerarquía de calidad: es una elección con costes en ambos lados.",
    51: "El segundo eje: **cuántas** conversiones inseguras tolera el lenguaje cuando una operación recibe tipos que no encajan. Fuerte y débil no es lo mismo que estático y dinámico, y confundir los dos ejes es el error de vocabulario más repetido del campo.",
    52: "La **inferencia** permite no escribir el tipo sin renunciar a tenerlo: `var` en C#, `let` en Rust, `:=` en Go, `auto` en C++. El compilador lo deduce, y entender hasta dónde llega esa deducción evita tanto ruido como sorpresas.",
    53: "La ausencia de valor parece trivial hasta que tumba un servicio en producción. `null`, `nil`, `None`, `Option` y `Maybe` son respuestas distintas al mismo problema, y la diferencia entre «puede fallar» declarado en el tipo o descubierto en ejecución.",
    54: "Detrás de una pregunta doméstica —¿cómo construyo la cadena `1-2-3-…-n`?— se esconde una decisión profunda de diseño: si un valor puede cambiar después de creado. La inmutabilidad no es purismo funcional: es lo que hace seguro compartir un dato entre hilos.",
    55: "`a + b * c` esconde más decisiones de las que parece: precedencia, asociatividad, orden de evaluación y qué ocurre si un operando tiene efectos colaterales. Aquí entran también los operadores bit a bit, que son los mismos en casi todos los lenguajes por herencia de C.",
    56: "La parte cierra con lo que ha sostenido en silencio a todas las clases anteriores: leer de la entrada estándar y escribir en la salida estándar. Es el contrato exacto que hace verificable la equivalencia entre diez lenguajes.",

    # --- Parte 4 · Control del programa -------------------------------------- #
    57: "Todo programa que decide algo fabrica antes un valor de verdad. El **cortocircuito** (`&&`, `||`) no es una optimización: es semántica observable, porque determina si el segundo operando —y sus efectos— llega a evaluarse.",
    58: "Una **guarda** atiende primero todo lo que puede salir mal y sale de inmediato, dejando el resto del cuerpo para un solo camino: el correcto. Es la técnica más barata para eliminar anidamiento y la que más legibilidad devuelve por línea escrita.",
    59: "La cadena `if` / `else if` / `else` elige entre alternativas mutuamente excluyentes. Aquí se ve por qué el anidamiento profundo es un problema de comprensión y no de estilo, y cómo cada lenguaje lo aplana con recursos distintos.",
    60: "Muchas veces no queremos *ejecutar* una de dos acciones sino *elegir* uno de dos valores. La diferencia entre `if` como sentencia y como **expresión** separa a Rust y Kotlin de C y Java, y explica por qué unos necesitan el operador ternario y otros no.",
    61: "El `switch` nace de una necesidad concreta: elegir entre muchos valores exactos sin una escalera ilegible de `else if`. El **fallthrough** —caer al siguiente caso— es la trampa clásica, y los lenguajes modernos la han invertido por defecto.",
    62: "La coincidencia de patrones da un salto conceptual sobre el `switch`: en vez de preguntar «¿es igual a esta constante?», pregunta «¿tiene esta **forma**?», y desestructura al mismo tiempo que decide. Es la puerta de entrada a los tipos algebraicos.",
    63: "El `while` es el bucle en su forma más pura: repetir mientras algo siga siendo cierto, sin presuponer contador ni número de vueltas. Es más fundamental que el `for`, y por eso es donde se estudian el invariante y la condición de parada.",
    64: "El bucle `for` cubre el caso más común: saber de antemano cuántas veces o sobre qué rango. La distancia entre el `for` clásico de C y el `for-range` de Go o Python muestra cuánta ceremonia era accidental.",
    65: "«Para cada elemento de esto, haz aquello»: sin índices, sin contadores, sin la posibilidad de equivocarse en el límite. Detrás está el **iterador**, el protocolo que cada lenguaje implementa a su manera y que conviene conocer.",
    66: "La evaluación **perezosa** invierte una suposición tan arraigada que casi nunca se enuncia: que para trabajar con una secuencia hay que tenerla entera en memoria. Generadores y flujos permiten procesar lo infinito y lo enorme con memoria constante.",
    67: "Una **comprensión** construye una colección describiéndola en lugar de fabricarla paso a paso. Su forma —«los `x` de la lista tales que `x` es par»— viene de la notación matemática de conjuntos, y es el punto donde lo imperativo empieza a ceder terreno.",
    68: "`map`, `filter` y `reduce` son la prueba de que una función puede recibir otra función. Con esos tres verbos se expresa la mayoría de los bucles que escribes, y se hace visible qué parte era recorrido y qué parte era lógica.",
    69: "La recursión existe porque hay estructuras que son recursivas por naturaleza —árboles, listas, gramáticas—. Aquí se ve también su coste real en la pila y qué lenguajes optimizan la **recursión de cola** (spoiler: menos de los que se cree).",
    70: "`break`, `continue`, `return` y el proscrito `goto` son salidas del flujo natural. Ninguno es malo por sí mismo: lo que importa es si hacen el código más fácil o más difícil de razonar, y esa evaluación se puede argumentar.",
    71: "Una excepción es una transferencia de control **no local**: el flujo salta hasta el manejador más cercano en la pila. Potente y peligrosa a partes iguales, porque su camino no se ve leyendo la función donde ocurre el fallo.",
    72: "El enfoque opuesto: si una función puede fallar, que lo diga en su **tipo de retorno**. `Result` en Rust, `error` en Go, `Either` en la familia ML. El error deja de ser un canal aparte y pasa a ser un valor que el compilador te obliga a mirar.",

    # --- Parte 5 · Funciones y modularidad ----------------------------------- #
    73: "La función es la primera y más importante herramienta de abstracción: dar **nombre** a un proceso para poder olvidarse de cómo está hecho. Su **firma** es un contrato — y leer contratos ajenos es la mitad del trabajo de programar.",
    74: "Un parámetro que trae su propio valor por defecto simplifica la llamada común sin cerrar la puerta al caso especial. Cuándo se evalúa ese valor por defecto es una diferencia semántica real entre lenguajes, y una fuente clásica de bugs en Python.",
    75: "Pasar los argumentos diciendo a qué parámetro corresponde cada uno, en vez de confiar en el orden. Convierte `crear(true, false, true)` en algo legible, y es una de las diferencias más visibles entre Python y la familia C.",
    76: "Una función que no fija de antemano cuántos argumentos recibe: acepta uno, tres o cuarenta. Es lo que hay detrás de `print`, `printf` y `format`, y cada lenguaje lo resuelve con un mecanismo distinto (empaquetado, arreglo, slice).",
    77: "Que una función entregue **más de un valor de una vez**, y que quien la llama reparta esos valores en variables. Tuplas en Python y Rust, retornos múltiples en Go, `out` en C#: el mismo problema con soluciones que revelan el diseño de cada lenguaje.",
    78: "Escribir la función **una sola vez** y que sirva para muchos tipos sin renunciar a la comprobación del compilador. Los genéricos son la respuesta tipada a la duplicación, y su coste —monomorfización o borrado— cambia por completo entre Rust, Java y Go.",
    79: "El paso **por valor** entrega una copia: la función no recibe *tu* variable sino un duplicado. Simple de enunciar y responsable de la mitad de las confusiones sobre por qué «la modifiqué y afuera no cambió».",
    80: "El paso **por referencia** entrega acceso al original: la función puede alcanzar y modificar la variable de quien la llamó. Distinguir esto de «pasar un objeto por valor» resuelve la confusión más persistente de la programación.",
    81: "El modelo con el que Rust gestiona memoria sin recolector y sin `malloc`/`free`: **propiedad**, **movimiento** y **préstamo**. Es la tercera respuesta a un problema que C y Java resolvieron de forma opuesta, y se entiende mejor comparada que sola.",
    82: "Cada vez que escribes `x`, el lenguaje decide a qué variable te refieres siguiendo una regla precisa: el **alcance**. El **sombreado** —redeclarar un nombre que ya existía— es legal en unos lenguajes, un error en otros y una fuente de bugs en todos.",
    83: "Un **cierre** es una función que se lleva consigo un pedazo del entorno donde nació. Capturar por valor o por referencia cambia el resultado del programa, y ahí es donde JavaScript, Rust y C++ toman decisiones incompatibles.",
    84: "Una función es **pura** cuando su resultado depende solo de sus argumentos y no observa ni cambia nada más. La distinción no es doctrinal: las funciones puras son las únicas trivialmente comprobables, cacheables y seguras entre hilos.",
    85: "Dejar de ver la función como una construcción especial del lenguaje y verla como **un valor más**: que se guarda en una variable, se pasa como argumento y se devuelve. Es el requisito de todo lo funcional que viene después.",
    86: "El **módulo** es el escalón siguiente a la función: una abstracción sobre un grupo de funciones y datos, con un nombre y una frontera. Paquete, namespace, crate y módulo nombran cosas parecidas pero no iguales en cada lenguaje.",
    87: "La encapsulación no es etiqueta («no toques los campos ajenos») sino el mecanismo que hace **confiable** a un tipo: si el estado interno solo cambia por operaciones que preservan sus invariantes, esos invariantes se pueden dar por ciertos.",
    88: "La contracara de escribir funciones: saber **traer** las que ya existen, y decidir la estructura de carpetas de un proyecto real en cada lenguaje. Importar es también una decisión de acoplamiento, no solo una línea al principio del archivo.",

    # --- Parte 6 · Datos y estructuras --------------------------------------- #
    89: "El **arreglo de tamaño fijo** es la estructura primitiva de la que descienden casi todas las demás: un bloque contiguo de memoria con acceso en tiempo constante por índice. Entenderlo es entender por qué todo lo demás cuesta lo que cuesta.",
    90: "El **arreglo dinámico** —`list`, `Vec`, `ArrayList`, slice— no crece por arte de magia: reserva de más y se recopia cuando se llena. Ese detalle explica su coste amortizado y por qué invalida referencias en algunos lenguajes.",
    91: "La **tupla** es la colección de tamaño fijo y heterogénea cuyos elementos se identifican por posición. Es la estructura mínima para devolver dos cosas a la vez, y el escalón previo al registro con nombres.",
    92: "El **rango** describe «todos los enteros de a hasta b» sin materializarlos: una representación perezosa que ahorra memoria y expresa la intención. Aquí se ve además el eterno detalle de si el extremo es inclusivo o exclusivo.",
    93: "Dejar de ver la cadena como un escalar «que guarda texto» y verla como una **estructura de datos**: secuencia indexable de caracteres o bytes, con coste real en cada operación de concatenación, corte o búsqueda.",
    94: "El **conjunto** no es «una lista que rechaza repetidos»: es una idea matemática en código, con pertenencia en tiempo constante y operaciones de unión, intersección y diferencia que expresan lógica que en bucles quedaría ilegible.",
    95: "El **mapa** —diccionario, tabla hash— asocia claves con valores y, junto con el arreglo, sostiene buena parte de la programación real. Entender el hash y la colisión explica por qué el orden de iteración no es el que insertaste.",
    96: "**Pila** y **cola** no son dos colecciones más: son dos **disciplinas de acceso** que restringen deliberadamente dónde se inserta y de dónde se saca. LIFO y FIFO son decisiones de diseño, no limitaciones.",
    97: "El **árbol** es el salto de lo lineal a lo jerárquico: raíz, hijos, hojas y recorridos. Aparece en todas partes —sistemas de archivos, DOM, AST, índices de base de datos— y es la primera estructura donde la recursión resulta natural.",
    98: "El **grafo** es la estructura más general: vértices y aristas modelando cualquier relación. Con él llegan los recorridos en anchura y profundidad, y la conciencia de que muchos problemas «difíciles» son grafos mal reconocidos.",
    99: "El **registro** —struct, clase, record— agrupa campos heterogéneos accedidos por **nombre**. Es el complemento exacto de la tupla y el punto donde el programa empieza a hablar el vocabulario del dominio y no el de la máquina.",
    100: "Dos ideas confundidas bajo la palabra «enum»: el conjunto cerrado de valores con nombre, y el **tipo algebraico** que además lleva datos en cada variante. La segunda es la que hace posible `Option`/`Result` y el `match` exhaustivo.",
    101: "**Igualdad** (mismo valor) e **identidad** (mismo objeto en memoria) son dos preguntas distintas que la sintaxis suele disfrazar con símbolos parecidos. `==` frente a `equals`, `is` frente a `==`: la respuesta correcta depende del lenguaje.",
    102: "¿`b = a` duplica el dato o le da un segundo nombre? Y si duplica, ¿copia también lo que hay dentro? Copia superficial, copia profunda y referencia compartida son la causa de los bugs de aliasing más caros de diagnosticar.",
    103: "La pregunta más callada y consecuente de la programación de sistemas: **quién es responsable de liberar un recurso y cuándo**. Aquí se prepara el terreno para las tres respuestas —manual, GC y propiedad— que la Parte 8 desarrolla.",
    104: "La entrada/salida de archivos es un **flujo** de bytes entre tu proceso y el mundo. Texto frente a binario, buffering, codificación y cierre del descriptor: cuatro decisiones que casi todos los tutoriales omiten.",
    105: "**JSON** es el formato universal de intercambio: convertir estructuras vivas del proceso en texto que otro programa —en otro lenguaje— pueda reconstruir. Serializar es donde los tipos de cada lenguaje se encuentran con un vocabulario común y pierden algo por el camino.",
    106: "Cierra la parte con persistencia: CSV, YAML, formatos binarios y bases de datos. Elegir representación externa es decidir quién más podrá leer tus datos, con qué coste y durante cuánto tiempo.",

    # --- Parte 7 · Paradigmas ------------------------------------------------ #
    107: "Un **paradigma** no es un lenguaje ni una sintaxis: es un marco mental que decide qué cuenta como una pieza legítima de la solución. Por eso el mismo problema resuelto en dos paradigmas no se parece ni en la forma ni en el vocabulario.",
    108: "El paradigma **imperativo** describe la computación como una secuencia de comandos que modifican un estado; el **estructurado** le impone tres construcciones (secuencia, selección, iteración) y prohíbe el salto arbitrario. Es la base sobre la que discuten todos los demás.",
    109: "Cuando un programa deja de caber en la cabeza, la respuesta clásica es dar nombre a las partes: **procedimientos** y **módulos**. Es el imperativo que crece y descubre que necesita fronteras internas.",
    110: "La orientación a objetos responde a una pregunta abierta: si el estado mutable es tan poderoso como peligroso, ¿cómo se domestica? Su respuesta es encapsularlo junto a las operaciones que lo respetan.",
    111: "El problema que la OO resuelve de verdad no es «modelar el mundo con clases»: es **eliminar los condicionales que preguntan de qué tipo es un valor**. El polimorfismo sustituye el `if` por despacho, y la composición suele batir a la herencia.",
    112: "Una **interfaz** desacopla lo que un cliente necesita de cómo alguien decide dárselo. Interfaces de Java y Go, traits de Rust y clases abstractas de C++ resuelven lo mismo con reglas distintas: nominal frente a estructural, explícito frente a implícito.",
    113: "Casi todo lo que aprendiste de OO asume un modelo que JavaScript **no tiene por debajo**: no hay clases, hay **prototipos**. Entender la cadena de prototipos explica la sintaxis `class` de ES6 y por qué a veces se comporta de forma inesperada.",
    114: "La programación funcional no empieza por `map` ni por las lambdas: empieza por una decisión sobre el **estado**. Sustituir la celda que se modifica por el valor que se transforma cambia lo que se puede razonar y lo que se puede paralelizar.",
    115: "Una función pura es un ladrillo; la **composición** es el cemento. Con currying y aplicación parcial se fabrican funciones nuevas a partir de las que ya tienes, en vez de escribir otra función casi igual.",
    116: "*Functor* y *mónada* arrastran fama de dificultad que aquí se desmonta con una visión práctica: son patrones para encadenar operaciones sobre valores envueltos —opcionales, resultados, listas, asincronía— sin desenvolverlos a mano en cada paso.",
    117: "El paradigma **declarativo** invierte la pregunta: no «qué pasos doy» sino «qué propiedades tiene el resultado». SQL es la implementación más usada del mundo, y compararla con el bucle equivalente hace visible el trabajo que hace el optimizador.",
    118: "La forma más radical de lo declarativo: describir **hechos** y **reglas** y dejar que un motor de inferencia busque las soluciones por unificación y backtracking. Prolog cambia hasta lo que significa «llamar» a algo.",
    119: "En el paradigma **orientado a eventos** tu código deja de mandar: registra callbacks y espera a ser llamado. Esa inversión del control es la base de toda interfaz de usuario y de todo servidor, y explica por qué el orden de ejecución deja de leerse de arriba abajo.",
    120: "Tratar el dato como una **corriente** que pasa por una tubería de transformaciones, en lugar de una colección que se recorre. Cambia la pregunta que le haces a los datos y permite trabajar con lo que aún no ha llegado.",
    121: "El paradigma **concurrente** rompe el supuesto de una sola línea de ejecución: hilos, tareas y canales. Aquí aparece por primera vez la necesidad de sincronizar, y con ella la clase de bugs que no se reproducen al depurar.",
    122: "El asíncrono persigue lo mismo que la concurrencia —no quedarse esperando— con otra filosofía: un solo hilo que suspende y reanuda. `async`/`await` y promesas, y el famoso «color» de las funciones que contagia a todo lo que las llama.",

    # --- Parte 8 · Cómo funcionan los lenguajes ------------------------------ #
    123: "Toda ejecución arranca con el mismo viaje: texto plano → tokens → árbol sintáctico → análisis semántico → código. Conocer las fases convierte cada mensaje de error en una coordenada del pipeline, no en un misterio.",
    124: "Qué se hace con el árbol después: compilar a máquina, interpretar directamente o compilar en caliente con un **JIT**. Estas tres respuestas explican la mayoría de las diferencias de rendimiento y de arranque entre lenguajes.",
    125: "`javac` no produce código de máquina sino **bytecode** para una máquina virtual imaginaria. JVM, CLR y V8 comparten esa idea, y con ella la portabilidad, el JIT y las herramientas de introspección que la acompañan.",
    126: "**AOT** frente a **JIT**, cara a cara: el compromiso entre tiempo de arranque, rendimiento sostenido, tamaño del artefacto y capacidad de optimizar con información de ejecución. Es una decisión de ingeniería que se paga en cada despliegue.",
    127: "Toda función llamada necesita recordar sus datos locales y a dónde volver. La **pila de llamadas** y su marco lo hacen posible — y explican el desbordamiento de pila, el coste de la recursión profunda y el contenido de un stack trace.",
    128: "El **heap** es donde viven los datos cuyo tamaño o vida no se conocen al compilar. Más flexible que la pila y bastante más caro: cada asignación implica buscar espacio y cada olvido implica una fuga.",
    129: "A los datos del heap se accede *a través* de algo que dice dónde están: dirección, puntero o referencia. Distinguir esos tres términos —y el aritmético puntero de C de la referencia segura de Java— desactiva media docena de confusiones.",
    130: "En C el contrato es explícito: cada `malloc` exitoso exige un `free`. De ahí salen las fugas, el *use-after-free* y el *double free*, tres fallos que aquí se ven provocados a propósito para reconocerlos después.",
    131: "El **recolector de basura** invierte la pregunta: en vez de «¿cuándo puedo liberar esto?», el runtime averigua qué ya no es alcanzable. Cómodo y no gratuito: pausas, memoria extra y comportamiento difícil de predecir bajo carga.",
    132: "La tercera vía: **RAII** en C++ y **propiedad con préstamos** en Rust liberan de forma determinista sin recolector, moviendo la comprobación al compilador. Es el punto donde las tres respuestas de la parte quedan comparables lado a lado.",
    133: "`cuenta += 1` no es atómico: son tres pasos, y en cuanto dos hilos los intercalan aparece la **condición de carrera**. Aquí se ve el problema real de la memoria compartida antes de estudiar cualquier solución.",
    134: "Los hilos del sistema operativo son caros y limitados. **Corrutinas**, tareas y canales permiten decenas de miles de unidades concurrentes ligeras — goroutines de Go, `async` de Rust — con un modelo mental distinto del hilo clásico.",
    135: "El modelo de **actores** elimina lo compartido: procesos aislados que solo se comunican por mensajes, con supervisión y reinicio. El BEAM de Erlang/Elixir muestra que la tolerancia a fallos puede ser una propiedad del lenguaje.",
    136: "Una idea incómoda: **el código que escribes no es el código que se ejecuta**. Compilador y CPU reordenan, y en un programa multihilo eso es observable. Aquí entran el modelo de memoria, la visibilidad y por qué `volatile` no es lo que parece.",
    137: "Un error no es solo un mensaje: es una **coordenada** en el pipeline de la clase 123. De sintaxis, de tipos, de enlace o de ejecución — saber en qué fase nace cada uno reduce el diagnóstico a la mitad.",
    138: "Cierra la parte devolviendo todo a la práctica: depurar es cerrar la distancia entre tu modelo mental del programa y lo que el programa realmente hace, con las herramientas que cada runtime ofrece para mirar dentro.",

    # --- Parte 9 · Ingeniería de software políglota -------------------------- #
    139: "Una **prueba unitaria** ejerce un trozo de código y afirma que el resultado observado es el esperado. Modesto de enunciar y la pieza que sostiene todo lo demás: sin ella, refactorizar es apostar.",
    140: "La prueba de **integración** mira qué ocurre cuando las partes se encuentran. En este curso hay un ejemplo poco común y muy literal: el verificador de equivalencia es una prueba de integración entre diez lenguajes.",
    141: "El **depurador** congela un programa vivo y te deja mirar dentro: puntos de ruptura, inspección de variables, ejecución paso a paso. `gdb`, `lldb`, `pdb` y los de IDE cambian de comandos, no de modelo mental.",
    142: "En producción no puedes pausar nada: tu única ventana es lo que el sistema haya decidido contar de sí mismo. Registro estructurado, niveles, trazas y métricas — y la diferencia entre registrar y observar.",
    143: "Ningún proyecto serio se sostiene solo con el código propio. Versionado semántico, resolución y **lockfile**: sin fijar versiones exactas, «funciona» es una afirmación sobre hoy y sobre esta máquina.",
    144: "Entre el fuente y el artefacto de producción media la *build*. Que sea **reproducible** —mismo fuente, mismo resultado, byte a byte— es lo que permite auditar qué se está ejecutando realmente.",
    145: "Git aplicado a un repositorio con siete lenguajes: qué se versiona y qué no, cómo se organizan los artefactos de compilación de cada toolchain y por qué el historial es documentación de las decisiones, no solo respaldo.",
    146: "Los datos de McConnell sobre inspecciones de código son contundentes: revisar a conciencia detecta una fracción enorme de los defectos, más barata que cualquier otra fase. Aquí se ve qué mirar y cómo dar la crítica.",
    147: "La **integración continua** nace de una observación incómoda: cuanto más tarda un cambio en fundirse con el trabajo de los demás, más caro es integrarlo. En un repo políglota hay que orquestar además siete toolchains.",
    148: "Separar **entrega** de **despliegue**: que un artefacto esté listo no obliga a ponerlo delante de los usuarios hoy. Estrategias, reversión y por qué desplegar debería ser aburrido.",
    149: "El **diseño** reparte el sistema en piezas y define cómo se hablan; la **arquitectura** es ese diseño a la escala más alta. Comparar cómo distintos lenguajes empujan hacia estilos distintos evita copiar arquitecturas fuera de contexto.",
    150: "Refactorizar es **cambiar la estructura interna sin alterar el comportamiento observable**. Las dos mitades de la definición importan: sin pruebas que sostengan la segunda, no estás refactorizando, estás reescribiendo con los ojos cerrados.",
    151: "Los patrones del *GoF* no son leyes: son soluciones recurrentes en un contexto. Compararlos entre lenguajes revela que varios patrones clásicos son andamios para suplir algo que otro lenguaje ya trae de serie.",
    152: "«Measure, don't guess». La intuición sobre rendimiento es sistemáticamente mala; el perfilado la sustituye por datos y casi siempre señala un lugar distinto al que habrías optimizado.",
    153: "La seguridad no es una capa final sino una postura desde la primera línea: validar toda entrada externa, tratar la memoria con cuidado en los lenguajes que lo exigen y vigilar la cadena de dependencias.",
    154: "El software se lee, se modifica y se reescribe durante años. Documentación que envejece bien, y **deuda técnica** entendida como lo que es: una decisión de financiación, no un pecado.",

    # --- Parte 10 · Interoperabilidad ---------------------------------------- #
    155: "Cambia la pregunta del curso: hasta aquí un problema resuelto en diez lenguajes que no se hablaban; a partir de ahora, cómo esos lenguajes **conviven dentro de un mismo sistema** y qué se paga en cada frontera.",
    156: "La frontera más íntima: llamar, dentro del mismo proceso, una función compilada por otro lenguaje. La **FFI** convierte a C en el idioma franco — y en el punto donde se pierden las garantías de seguridad del lenguaje que llama.",
    157: "Bajo la firma de la FFI hay un contrato silencioso: la **ABI**. Convención de llamada, alineación, tamaño de tipos y decoración de nombres — cuando no coinciden, el programa no falla con un error claro sino con corrupción.",
    158: "La FFI cruda es peligrosa, y nadie quiere programar así a diario. Los **bindings** y *wrappers* envuelven esa frontera para devolver al lenguaje anfitrión sus tipos, sus errores y su gestión de recursos.",
    159: "La mayoría de las fronteras reales no comparten proceso ni memoria. Serializar —JSON, Protobuf, MessagePack— es acordar cómo se escriben los datos en el cable, con un compromiso claro entre legibilidad, tamaño y velocidad.",
    160: "El formato resuelve *cómo* viajan los datos; el **contrato de API** resuelve *qué* datos y *qué* operaciones. REST, gRPC y esquemas versionados: sin contrato explícito, la integración funciona hasta el primer cambio.",
    161: "Falta el canal: por dónde salen los bytes de un proceso y entran en otro. `stdin`/`stdout`, sockets y colas de mensajes determinan el acoplamiento temporal —si ambos extremos deben estar vivos a la vez— más que cualquier otra decisión.",
    162: "**WebAssembly** ofrece un punto de encuentro que la ABI de C no puede dar: independiente de arquitectura y de sistema operativo, con aislamiento por defecto. Un objetivo común al que compilan hoy Rust, C, Go y varios más.",
    163: "Incrustar invierte la relación y la vuelve jerárquica: un programa anfitrión hospeda un intérprete y le expone funciones. Es como Lua entró en los motores de juego y como Python se usa para extender aplicaciones grandes.",
    164: "Cierra la parte con la decisión que todo lo anterior hace informada: qué lenguaje merece cada componente, con qué criterios explícitos y qué coste de frontera se acepta a cambio.",

    # --- Parte 11 · Proyecto integrador -------------------------------------- #
    165: "Arranca el proyecto integrador con la última idea del programa: un sistema real casi nunca es un programa monolítico sino una **federación de componentes** que colaboran. Aquí se inventaría qué piezas hacen falta.",
    166: "Con el inventario en la mano, definir **responsabilidades** y **contratos** entre piezas: qué entra, qué sale, qué errores son posibles y quién es dueño de cada dato. El diseño se hace antes, no se documenta después.",
    167: "El primer componente concreto: la **CLI**, territorio natural de los lenguajes de sistemas que compilan a un binario sin runtime. Argumentos, códigos de salida y salida legible por humanos y por máquinas.",
    168: "El corazón del sistema: el **servicio backend** donde vive la lógica de negocio. Recibe una petición y devuelve una respuesta con dos partes que conviene no mezclar: el dato y el estado de la operación.",
    169: "La cara visible: el **frontend** en JavaScript o TypeScript, único lenguaje que el navegador ejecuta de forma nativa. Consume el contrato definido en la clase 166 y demuestra si ese contrato era bueno.",
    170: "El **componente de datos**: la fuente de verdad del sistema, en SQL. Modelar el esquema y escribir consultas es ejercer el paradigma declarativo de la Parte 7 sobre datos que ahora son del proyecto.",
    171: "El **pegamento**: los scripts que ejecutan tareas repetitivas sin que nadie mire —limpiar, respaldar, desplegar, informar—. Poco glamuroso y decisivo, porque es lo que hace que el sistema se opere solo.",
    172: "Guardar un dato para recuperarlo cuando el proceso que lo escribió ya no exista. Dónde vive el estado, qué se persiste y qué se recalcula, y las garantías que se están asumiendo sin decirlo.",
    173: "Ejercitar el sistema **completo**, de la entrada a la salida, como lo haría un usuario real. Es la única prueba que puede fallar por un contrato mal entendido entre dos componentes que individualmente pasaban sus pruebas.",
    174: "Empaquetar el sistema y su entorno en un artefacto reproducible y ponerlo a correr. Es el momento en que un proyecto políglota deja de ser un problema y pasa a ser una ventaja: cada componente trae su propio toolchain, aislado.",
    175: "Escribir la parte que no se ejecuta y decide si el sistema sobrevive: la **defensa razonada** de cada elección de lenguaje. Un sistema con cinco lenguajes sin justificación escrita es un sistema que nadie querrá mantener.",
    176: "Cierre del programa: mirar atrás las 176 clases y, sobre todo, adelante — hacia el lenguaje que todavía no conoces. La tesis de la clase 001 se cierra aquí, convertida en un método de transferencia que puedes aplicar solo.",
}


# --------------------------------------------------------------------------- #
# Narrativa de cada parte.
# --------------------------------------------------------------------------- #

GUIA = {
    0: {
        "gancho": "Aprender a pensar el problema antes de elegir con qué escribirlo.",
        "resumen": [
            "Esta parte existe porque la mayor parte de lo que hace bueno a un programador **no está dentro de ningún lenguaje**. Modelar un problema, descomponerlo, escribir un algoritmo que se sepa correcto y estimar lo que costará son habilidades que sobreviven a cualquier cambio de tecnología, y son exactamente las que un curso «de Python» o «de Java» da por supuestas mientras enseña sintaxis.",
            "Aquí no se escribe código en ningún lenguaje del núcleo. Se escribe **pseudocódigo neutral**, se traza a mano y se discute qué significa que dos programas hagan «lo mismo». Ese vocabulario es el que hace posible que a partir de la Parte 3 se pongan diez implementaciones lado a lado y la comparación enseñe algo en vez de ser un desfile de sintaxis.",
            "La parte cierra con el método del propio curso —la ficha de transferencia, el `casos.json`, el verificador— para que sepas exactamente qué estás leyendo en cada clase posterior y qué garantía tiene cada afirmación.",
        ],
        "asume": "Nada. Es el punto de entrada del programa y no requiere haber programado antes, aunque haber peleado con algún lenguaje hace que varias clases resuenen más.",
        "logros": [
            "Modelar un problema como entradas, proceso, salidas, reglas y restricciones.",
            "Escribir un algoritmo en pseudocódigo neutral y trazarlo a mano sobre un caso concreto.",
            "Argumentar corrección y terminación en lugar de confiar en que «parece funcionar».",
            "Clasificar cualquier diferencia entre dos lenguajes como sintáctica, semántica o paradigmática.",
            "Estimar el orden de coste de un algoritmo antes de escribirlo.",
            "Leer una clase de código del curso sacándole todo el partido, y saber qué verifica la máquina.",
        ],
        "bloques": [
            ("La tesis y la brújula", "Las dos clases que fijan de qué va el curso y con qué criterio se compara. Todo lo demás las usa.", 1, 2),
            ("Modelar el problema", "Antes del algoritmo está el modelo: qué entra, qué sale, qué se descarta y qué casos lo rompen.", 3, 6),
            ("Del papel al algoritmo", "Escribirlo sin lenguaje, comprobarlo a mano, estimar su coste y hacerlo legible.", 7, 10),
            ("El método del curso en la práctica", "Cómo está hecha una clase de código, cómo se verifica y cómo se lee un lenguaje ajeno.", 11, 14),
        ],
        "malentendidos": [
            ("«Aprender a programar es aprender un lenguaje.»", "El lenguaje es la última decisión, no la primera: sin modelo ni algoritmo, la sintaxis no te lleva a ninguna parte."),
            ("«Los lenguajes son todos iguales, solo cambia la sintaxis.»", "Falso en el eje semántico y en el paradigmático. Lo que cambia de verdad es qué se puede expresar y qué garantiza el lenguaje."),
            ("«El pseudocódigo es una pérdida de tiempo.»", "Es la única forma de escribir una vez lo que después se traduce diez veces — y de detectar que el problema estaba mal planteado antes de codificarlo."),
        ],
        "abre": "Con el método fijado, la Parte 1 lo aplica al mapa completo de los lenguajes: de dónde viene cada uno y a qué familia pertenece.",
    },

    1: {
        "gancho": "El árbol genealógico completo: por qué diez lenguajes bastan para leer decenas.",
        "resumen": [
            "La programación se percibe como una lista inabarcable de tecnologías rivales, y esa percepción es un accidente de cómo se enseña. En realidad hay un puñado de **linajes** con antepasados comunes: cuando ves de dónde salió cada lenguaje y qué problema vino a resolver, sus decisiones dejan de parecer arbitrarias.",
            "Esta parte recorre las familias una a una: la de C y las llaves, la del scripting dinámico, la de la JVM, la de .NET, la de la web, la funcional tipada, Lisp, la lógica, la de actores, la de sistemas, la científica y la de los lenguajes que sobreviven en su nicho. Cada una aporta una **idea** que el resto del curso reencuentra con código delante.",
            "Es la parte que sostiene la tesis del Atlas: *aprende el representante, reconoce la familia entera*. Si dominas C lees la superficie de cinco lenguajes más; si entiendes por qué existe la JVM entiendes de golpe a Kotlin, Scala, Groovy y Clojure.",
        ],
        "asume": "La Parte 0 completa, sobre todo las tres clases de diferencia (002): sin ese criterio, comparar familias degenera en preferencias.",
        "logros": [
            "Situar cualquier lenguaje conocido en su familia y nombrar a sus parientes cercanos.",
            "Distinguir estándar, implementación, versión y ecosistema al hablar de un lenguaje.",
            "Explicar qué idea aporta cada familia y qué problema histórico vino a resolver.",
            "Predecir qué te resultará familiar y qué te sorprenderá al abrir un lenguaje nuevo.",
            "Usar el [Atlas](../../atlas/README.md) como material de consulta durante el resto del programa.",
        ],
        "bloques": [
            ("Cómo se lee el árbol", "El mapa general y el ciclo de vida de un lenguaje: sin esto, las familias son una lista de nombres.", 15, 16),
            ("Las familias con representante en el núcleo", "Cinco familias cuyos representantes vas a implementar y verificar a partir de la Parte 3.", 17, 21),
            ("Las familias que aportan ideas", "ML, Lisp, la lógica y los actores: poco código propio en el curso, influencia enorme en el resto.", 22, 25),
            ("Sistemas, cálculo y legado", "Los lenguajes cercanos a la máquina, los del cálculo numérico y los que sobreviven en su nicho.", 26, 28),
        ],
        "malentendidos": [
            ("«Una familia se define por la sintaxis.»", "A veces se define por la plataforma: Kotlin y Clojure no se parecen en nada escritos y comparten JVM, bytecode y bibliotecas."),
            ("«Los lenguajes viejos están muertos.»", "COBOL mueve transacciones bancarias hoy y Fortran sigue en cálculo científico. Sobreviven donde son insustituibles, no por inercia."),
            ("«Aprender más lenguajes es acumular sintaxis.»", "Es reconocer familias. El undécimo lenguaje cuesta una fracción del primero si sabes de qué linaje viene."),
        ],
        "abre": "Sabiendo qué lenguajes existen y de dónde vienen, la Parte 2 responde a la pregunta práctica: cómo se ejecutan.",
    },

    2: {
        "gancho": "Del archivo de texto al proceso que corre: el toolchain de cada lenguaje.",
        "resumen": [
            "El código fuente es un archivo de texto que no hace nada por sí mismo. Entre ese texto y un proceso vivo hay una cadena de herramientas —el **toolchain**— que casi nadie enseña y que todo el mundo necesita: instalar, ejecutar, compilar, gestionar dependencias, formatear, probar y empaquetar.",
            "Esta parte es deliberadamente práctica y transversal: cubre los diez lenguajes del núcleo a la vez, mostrando que bajo diez vocabularios distintos hay unos pocos conceptos idénticos. `pip`, `cargo`, `pnpm`, Maven y Composer hacen lo mismo con nombres distintos; entender el patrón ahorra volver a aprender desde cero en cada lenguaje.",
            "Es también la parte que hace ejecutable el resto del curso: aquí se instala y comprueba lo necesario para que el verificador de equivalencia pueda correr en tu máquina y no solo en CI.",
        ],
        "asume": "Las Partes 0 y 1. Conviene tener acceso a una terminal y permisos para instalar software; sin ello, varias clases se quedan en lectura.",
        "logros": [
            "Nombrar cada eslabón entre tu archivo fuente y el proceso en ejecución.",
            "Leer un comando desconocido descomponiéndolo en nombre, subcomando, flags y argumentos.",
            "Instalar y convivir con varias versiones del mismo lenguaje en una máquina.",
            "Ejecutar, construir, probar y empaquetar en cualquiera de los diez lenguajes del núcleo.",
            "Diagnosticar el clásico «en mi máquina sí funciona» mirando PATH y variables de entorno.",
        ],
        "bloques": [
            ("Qué hay entre tu texto y un proceso", "El toolchain, los cuatro modelos de ejecución y la gramática de un comando.", 29, 31),
            ("Instalar y ejecutar", "Gestión de versiones y el comando de ejecución de cada lenguaje del núcleo.", 32, 33),
            ("Construir, depender y explorar", "Artefactos, gestores de paquetes y la consola interactiva como herramienta de estudio.", 34, 36),
            ("Calidad, empaquetado y entorno", "Formateadores, linters, pruebas desde terminal, distribución y PATH.", 37, 40),
        ],
        "malentendidos": [
            ("«Python es interpretado y Java compilado.»", "Ambos compilan a bytecode y lo ejecutan sobre una VM. La dicotomía compilado/interpretado tiene cuatro respuestas, no dos."),
            ("«Ejecutar y compilar son lo mismo con otro comando.»", "Ejecutar es correrlo ahora; construir produce un artefacto que sobrevive a la sesión y viaja a otra máquina."),
            ("«El lockfile es un archivo generado que se puede borrar.»", "Es la diferencia entre una build reproducible y una que depende del día en que se ejecute."),
        ],
        "abre": "Con las herramientas instaladas y entendidas, la Parte 3 empieza el código: la primera clase con diez implementaciones verificadas.",
    },

    3: {
        "gancho": "La materia prima de todo programa: cómo cada lenguaje nombra, tipa, convierte y muta un valor.",
        "resumen": [
            "Aquí empiezan las **clases de código**: cada una trae el mismo problema resuelto en los diez lenguajes del núcleo, con el código a la vista y verificado contra un `casos.json` común. La Parte 3 elige el terreno más elemental posible —valores, tipos y variables— justamente porque es donde las diferencias entre lenguajes son más profundas de lo que parecen.",
            "El recorrido es deliberado: primero qué es un valor y qué es un nombre, luego los tipos primitivos uno por uno (con sus trampas reales: desbordamiento, punto flotante, Unicode), después los **dos ejes** con los que se clasifica cualquier sistema de tipos —estático/dinámico y fuerte/débil— y por último las tres decisiones que más consecuencias tienen: la ausencia de valor, la mutabilidad y la evaluación de expresiones.",
            "Al terminar dispondrás del vocabulario que las ocho partes siguientes dan por sabido, y de algo más incómodo y más útil: la conciencia de que `0.1 + 0.2`, `\"5\" + 3` y una cadena vacía dentro de un `if` no significan lo mismo en todos los lenguajes.",
        ],
        "asume": "Las Partes 0–2. En particular el pseudocódigo (007), el `casos.json` y el verificador (012), y tener al menos un toolchain instalado para ejecutar las implementaciones.",
        "logros": [
            "Distinguir literal, valor, variable y constante, y declarar cada uno en los diez lenguajes.",
            "Explicar el rango, el signo y el desbordamiento de un entero, y por qué el punto flotante no es exacto.",
            "Situar cualquier lenguaje en los ejes estático/dinámico y fuerte/débil, con un ejemplo que lo demuestre.",
            "Elegir entre `null`, `Option` y un valor centinela sabiendo qué garantiza cada uno.",
            "Predecir el resultado de una conversión implícita antes de ejecutarla.",
            "Leer y escribir por entrada y salida estándar en los diez lenguajes del núcleo.",
        ],
        "bloques": [
            ("Nombres y valores", "Qué es un valor sin nombre y qué añade la variable: declarar, inicializar y asignar como tres actos distintos.", 41, 42),
            ("Los tipos primitivos, uno por uno", "Enteros, reales, booleanos, caracteres y cadenas, cada uno con la trampa que esconde.", 43, 48),
            ("Los dos ejes del sistema de tipos", "Conversión, cuándo se comprueba, cuánto se tolera y cuánto deduce el compilador.", 49, 52),
            ("Ausencia, mutación y expresión", "Las tres decisiones con más consecuencias, y el cierre con entrada/salida estándar.", 53, 56),
        ],
        "malentendidos": [
            ("«Tipado fuerte y tipado estático son sinónimos.»", "Son ejes independientes: Python es dinámico y fuerte; C es estático y relativamente débil."),
            ("«Los decimales fallan por un bug del lenguaje.»", "Es IEEE 754, y ocurre igual en los diez. Lo que cambia es qué ofrece cada lenguaje para el dinero."),
            ("«Una cadena es un tipo simple.»", "Es una estructura de datos con codificación, coste por operación y una decisión de mutabilidad detrás."),
        ],
        "abre": "Con valores que nombrar y tipar, la Parte 4 les añade lo único que falta para tener un programa: decidir y repetir.",
    },

    4: {
        "gancho": "Decidir, repetir y fallar: el flujo del programa y sus formas en diez lenguajes.",
        "resumen": [
            "Un programa que solo calcula expresiones no es todavía un programa. La Parte 4 añade las dos operaciones que lo convierten en uno —**decidir** y **repetir**— y termina con la tercera que nadie llama control de flujo y lo es: **fallar**.",
            "El recorrido va de lo más concreto a lo más expresivo. Empieza por la condición y sus formas (`if`, ternario, `switch`, `match`), sigue por los bucles en sus tres sabores (por condición, por rango, por colección) y llega a la iteración perezosa y a las comprensiones, donde el «cómo recorro» empieza a desaparecer del código. Después, `map`/`filter`/`reduce` y la recursión muestran que se puede repetir sin escribir un solo bucle.",
            "El cierre son las dos filosofías del error: la **excepción**, que salta por la pila hasta quien sepa atenderla, y el **resultado como valor**, que obliga a mirarlo en el sitio. Es una de las divisiones más profundas entre los lenguajes del núcleo y se ve mejor con las dos implementadas lado a lado.",
        ],
        "asume": "La Parte 3 completa: booleanos (046), operadores (055) y entrada/salida (056) se usan en todas las clases de esta parte.",
        "logros": [
            "Elegir entre `if`, `switch` y `match` con un criterio explícito y no por costumbre.",
            "Escribir un bucle con su invariante y su condición de parada argumentadas.",
            "Reescribir un bucle imperativo como comprensión o como `map`/`filter`/`reduce`.",
            "Explicar qué hace el cortocircuito y por qué es semántica y no optimización.",
            "Implementar el mismo fallo con excepciones y con `Result`, y defender cuál conviene.",
            "Reconocer cuándo la recursión es la forma natural y cuándo va a desbordar la pila.",
        ],
        "bloques": [
            ("Decidir", "De la condición booleana a la coincidencia de patrones, pasando por las guardas y el `switch`.", 57, 62),
            ("Repetir", "Los tres sabores de bucle, la evaluación perezosa y las comprensiones.", 63, 67),
            ("Repetir sin bucles", "Funciones de orden superior y recursión: el mismo trabajo sin escribir el recorrido.", 68, 69),
            ("Salir del flujo y fallar bien", "Saltos controlados y las dos grandes filosofías del manejo de errores.", 70, 72),
        ],
        "malentendidos": [
            ("«`match` es un `switch` más bonito.»", "El `switch` compara con constantes; el `match` compara **formas** y desestructura. Son operaciones distintas."),
            ("«La recursión siempre es más elegante.»", "Es más natural sobre estructuras recursivas y desastrosa sobre secuencias largas en lenguajes sin optimización de cola."),
            ("«Las excepciones son el manejo de errores moderno.»", "Go y Rust demuestran lo contrario: el error como valor es igual de moderno y mucho más visible en la firma."),
        ],
        "abre": "Con flujo y datos elementales, la Parte 5 introduce la abstracción que lo ordena todo: la función y el módulo.",
    },

    5: {
        "gancho": "La función como contrato: firma, paso de parámetros, cierres y fronteras de módulo.",
        "resumen": [
            "La función es la primera herramienta de abstracción real: permite dar nombre a un proceso y, con ese nombre, dejar de pensar en cómo está hecho. Esta parte la estudia como **contrato** —qué promete la firma y qué garantiza— y no como una forma de ahorrar líneas repetidas.",
            "La sección más importante es la que casi todos los cursos despachan en un párrafo: **qué recibe realmente una función**. Paso por valor, paso por referencia y el modelo de propiedad y préstamo de Rust son tres respuestas incompatibles a la misma pregunta, y verlas juntas resuelve de una vez la confusión sobre por qué a veces «se modifica afuera» y a veces no.",
            "Después vienen los nombres —alcance, sombreado, cierres, pureza— y el salto de la función al **módulo**: fronteras, visibilidad e importación. Es el punto en que el curso deja de hablar de programas de un archivo y empieza a hablar de proyectos.",
        ],
        "asume": "Las Partes 3 y 4. La mutabilidad (054) y el control de flujo son requisito directo; los genéricos (078) se apoyan en el sistema de tipos de la Parte 3.",
        "logros": [
            "Leer una firma como un contrato y detectar qué no promete.",
            "Predecir si una función puede modificar el argumento que recibió, en cada uno de los diez lenguajes.",
            "Explicar movimiento y préstamo de Rust comparándolos con copia y referencia.",
            "Escribir una función genérica y explicar el coste de su implementación en cada lenguaje.",
            "Identificar qué captura un cierre y por qué eso cambia el resultado del programa.",
            "Organizar un proyecto en módulos con fronteras y visibilidad explícitas.",
        ],
        "bloques": [
            ("La firma como contrato", "Parámetros, valores por defecto, argumentos nombrados, variádicos, retornos múltiples y genéricos.", 73, 78),
            ("Qué recibe realmente la función", "Las tres respuestas al paso de parámetros: valor, referencia y propiedad.", 79, 81),
            ("Dónde viven los nombres", "Alcance, sombreado, cierres, pureza y la función como valor de primera clase.", 82, 85),
            ("De la función al proyecto", "Módulos, visibilidad, encapsulación e importación: las fronteras del código propio.", 86, 88),
        ],
        "malentendidos": [
            ("«En Java los objetos se pasan por referencia.»", "Se pasa por valor la **referencia**. La diferencia se nota en cuanto reasignas el parámetro dentro de la función."),
            ("«Un cierre es solo una función anónima.»", "Lo que lo define no es no tener nombre, sino llevarse consigo el entorno donde nació."),
            ("«`private` es una regla de cortesía.»", "Es el mecanismo que permite dar por ciertos los invariantes de un tipo. Sin él, no hay nada que garantizar."),
        ],
        "abre": "Con funciones y módulos, la Parte 6 se ocupa de lo que esas funciones manipulan: las estructuras de datos.",
    },

    6: {
        "gancho": "Dónde se guardan los datos, qué cuesta cada operación y qué significa realmente copiar.",
        "resumen": [
            "Es la parte más larga del programa (18 clases) porque es la que más se transfiere: las estructuras de datos son las mismas en todos los lenguajes, cambian los nombres y las garantías. Un `dict` de Python, un `HashMap` de Java y un `map` de Go son la misma idea con tres contratos distintos sobre orden, nulidad y concurrencia.",
            "El recorrido sube de lo contiguo a lo enlazado —arreglo, arreglo dinámico, tupla, rango, cadena, conjunto, mapa, pila, cola, árbol, grafo— y luego cambia de plano: cómo modelar un dato **propio** con registros y tipos algebraicos. Cada clase declara el coste real de sus operaciones, porque elegir estructura es elegir qué será barato y qué será caro.",
            "El tramo final es el más peligroso de la programación cotidiana: **igualdad frente a identidad**, **copia superficial frente a profunda** y **propiedad de los datos**. Ahí nacen los bugs de aliasing que no se reproducen. La parte cierra sacando los datos del proceso: archivos, JSON y persistencia.",
        ],
        "asume": "Las Partes 3–5. La mutabilidad (054), el paso de parámetros (079–081) y los genéricos (078) son requisito directo.",
        "logros": [
            "Elegir la estructura adecuada a partir del coste de las operaciones que vas a hacer.",
            "Explicar por qué un arreglo dinámico tiene coste amortizado y qué pasa al recrecerse.",
            "Modelar un dato del dominio con registros y tipos algebraicos en lugar de con banderas sueltas.",
            "Distinguir igualdad de identidad y copia superficial de profunda en los diez lenguajes.",
            "Serializar y deserializar a JSON sabiendo qué información del tipo se pierde en el viaje.",
            "Persistir datos eligiendo formato con criterio de interoperabilidad y longevidad.",
        ],
        "bloques": [
            ("Secuencias", "De la memoria contigua a la cadena: las estructuras lineales y su coste real.", 89, 93),
            ("Colecciones por clave y por disciplina", "Conjuntos, mapas y las estructuras que restringen el acceso a propósito.", 94, 96),
            ("Estructuras enlazadas", "El salto a lo jerárquico y a lo relacional: árboles y grafos.", 97, 98),
            ("Modelar un dato propio", "Registros y tipos algebraicos: el vocabulario del dominio dentro del sistema de tipos.", 99, 100),
            ("Qué significa copiar", "Igualdad, identidad, copia superficial y profunda, y quién es dueño del dato.", 101, 103),
            ("Sacar los datos del proceso", "Archivos, JSON y persistencia: la vida del dato más allá de la ejecución.", 104, 106),
        ],
        "malentendidos": [
            ("«Una lista y un arreglo son lo mismo.»", "Uno tiene tamaño fijo y coste predecible; el otro recrece, recopia y a veces invalida referencias."),
            ("«El diccionario conserva el orden de inserción.»", "Solo en algunos lenguajes y por decisión explícita de la implementación. Depender de ello sin comprobarlo es una bomba de relojería."),
            ("«Copiar un objeto copia lo que hay dentro.»", "Casi nunca: la copia por defecto es superficial y comparte lo interno. De ahí el bug que aparece «solo a veces»."),
        ],
        "abre": "Con datos y funciones dominados, la Parte 7 sube al nivel de las decisiones de estilo: los paradigmas.",
    },

    7: {
        "gancho": "Los ocho estilos de resolver: qué considera cada paradigma una pieza legítima de solución.",
        "resumen": [
            "Un paradigma no es una sintaxis: es un **marco mental** que decide cómo se descompone un problema y qué cuenta como pieza válida de la solución. Por eso el mismo problema resuelto en dos paradigmas no se parece ni en la forma ni en el vocabulario, aunque produzca la misma salida — que es justo lo que el verificador de equivalencia demuestra en cada clase.",
            "La parte recorre imperativo y estructurado, procedimental, orientado a objetos (con su variante de prototipos, que JavaScript usa por debajo), funcional en tres escalones, declarativo, lógico, orientado a eventos, reactivo, concurrente y asíncrono. Ninguno se presenta como superior: cada uno se explica por el problema que vino a resolver y por el que crea.",
            "Es la parte donde el curso rentabiliza toda su estructura comparada: ver la misma tarea como objetos, como composición de funciones puras y como consulta declarativa es lo que convierte los paradigmas en herramientas elegibles en vez de en banderas.",
        ],
        "asume": "Las Partes 5 y 6. Funciones de primera clase (085), cierres (083), pureza (084) y registros (099) son requisito; sin ellos lo funcional y lo OO quedan en eslóganes.",
        "logros": [
            "Identificar el paradigma dominante de un fragmento de código ajeno y sus consecuencias.",
            "Sustituir un condicional por polimorfismo, y saber cuándo no conviene hacerlo.",
            "Explicar la orientación a objetos por prototipos de JavaScript sin recurrir a la analogía de clases.",
            "Componer funciones y aplicar currying para fabricar funciones nuevas en vez de duplicarlas.",
            "Escribir la misma transformación en versión imperativa, funcional y declarativa (SQL).",
            "Distinguir concurrencia de asincronía y elegir el modelo adecuado a un problema real.",
        ],
        "bloques": [
            ("Qué es un paradigma", "La clase que da el criterio con el que se leen las quince siguientes.", 107, 107),
            ("Imperativo y sus herederos", "El estilo más antiguo y su evolución hacia el orden: estructurado, procedimental y modular.", 108, 109),
            ("Orientación a objetos", "Estado encapsulado, polimorfismo, interfaces y el modelo de prototipos de JavaScript.", 110, 113),
            ("Funcional", "Inmutabilidad y pureza, composición y currying, y los patrones para encadenar efectos.", 114, 116),
            ("Declarativo y lógico", "Describir el qué en vez del cómo: SQL y el motor de inferencia de Prolog.", 117, 118),
            ("Eventos, flujos y concurrencia", "Cuando el control se invierte: callbacks, streams, hilos y `async`/`await`.", 119, 122),
        ],
        "malentendidos": [
            ("«La programación funcional es usar `map` y lambdas.»", "Empieza por una decisión sobre el estado, no por una sintaxis. Se puede escribir código imperativo lleno de lambdas."),
            ("«JavaScript tiene clases desde ES6.»", "Tiene azúcar sintáctico sobre prototipos. La diferencia se nota en cuanto inspeccionas la cadena de prototipos."),
            ("«Concurrente y asíncrono son sinónimos.»", "La concurrencia reparte trabajo entre líneas de ejecución; la asincronía evita esperar bloqueado, a menudo en un solo hilo."),
        ],
        "abre": "Vistos los estilos, la Parte 8 baja al nivel que los explica: qué hace realmente la máquina con tu código.",
    },

    8: {
        "gancho": "Lo que ocurre bajo el código: compilación, memoria, concurrencia y por qué falla lo que falla.",
        "resumen": [
            "Esta es la parte que convierte la explicación en comprensión. Todo lo estudiado hasta aquí —tipos, funciones, estructuras, paradigmas— descansa sobre un conjunto de mecanismos concretos: un pipeline de compilación, una pila, un heap, una estrategia para liberar memoria y un modelo de ejecución concurrente.",
            "El recorrido baja por capas. Primero el viaje del texto a la acción y las tres respuestas —compilador, intérprete, JIT— con su comparación AOT/JIT. Después, dónde viven los datos: pila, heap y las referencias que los alcanzan. Luego, las **tres respuestas a «quién libera la memoria»**: manual en C, recolector en Java o Go, y propiedad con préstamos en Rust y C++, comparadas por fin en el mismo sitio.",
            "El tramo final es la concurrencia vista desde abajo: por qué `cuenta += 1` no es atómico, qué son las corrutinas y los canales, cómo el modelo de actores elimina lo compartido y por qué el código que escribes no es el que se ejecuta. Cierra con el diagnóstico: clasificar un error por la fase en que nace y depurar en cada runtime.",
        ],
        "asume": "Las Partes 5 y 6, en particular propiedad y ciclo de vida (103), paso de parámetros (079–081) y la Parte 7 para la concurrencia (121–122).",
        "logros": [
            "Situar cualquier mensaje de error en la fase del pipeline donde nace.",
            "Explicar la diferencia práctica entre AOT y JIT en arranque, rendimiento y tamaño.",
            "Decir qué vive en la pila y qué en el heap para un programa dado, en cada lenguaje.",
            "Comparar gestión manual, recolector y propiedad nombrando qué garantiza y qué cuesta cada uno.",
            "Reproducir una condición de carrera y explicar por qué la reordenación la hace posible.",
            "Depurar con el instrumental nativo de cada runtime en lugar de a base de imprimir.",
        ],
        "bloques": [
            ("Del texto a la acción", "El pipeline de compilación y las tres formas de ejecutar lo que produce.", 123, 126),
            ("Dónde viven los datos", "Pila, marco de llamada, heap y las referencias que lo enlazan todo.", 127, 129),
            ("Las tres respuestas a «quién libera»", "Manual, recolector y propiedad: el mismo problema con tres contratos incompatibles.", 130, 132),
            ("Hacer varias cosas a la vez", "Memoria compartida, corrutinas y canales, actores y el modelo de memoria.", 133, 136),
            ("Cuando algo falla", "Clasificar el error por su fase y diagnosticarlo con las herramientas del runtime.", 137, 138),
        ],
        "malentendidos": [
            ("«El recolector de basura evita las fugas de memoria.»", "Evita las clásicas, no las lógicas: una referencia viva que ya no necesitas es una fuga que el GC nunca recogerá."),
            ("«Rust es seguro porque no deja hacer cosas.»", "Es seguro porque mueve una comprobación que en C hace el programador —y a veces olvida— al compilador."),
            ("«Si el código es correcto, no hay condiciones de carrera.»", "Compilador y CPU reordenan. Sin sincronización explícita, «correcto» leído de arriba abajo no significa correcto al ejecutarse."),
        ],
        "abre": "Entendida la máquina, la Parte 9 se ocupa de la otra mitad del oficio: construir software que otras personas puedan mantener.",
    },

    9: {
        "gancho": "Que funcione, que se construya igual siempre, que llegue a producción y que se pueda cambiar.",
        "resumen": [
            "Escribir código que funciona hoy en tu máquina es la parte fácil. Esta parte trata todo lo demás: pruebas, depuración, observabilidad, dependencias, builds reproducibles, control de versiones, revisión, CI, despliegue, diseño, refactorización, patrones, rendimiento, seguridad y deuda técnica — cada práctica comparada entre los diez lenguajes.",
            "El hilo conductor es la evidencia. Cada práctica responde a una pregunta comprobable: ¿cómo sé que funciona? ¿cómo sé que la build de hoy es la de ayer? ¿cómo sé qué está pasando en producción? ¿cómo sé que este refactor no rompió nada? Las herramientas cambian de nombre en cada lenguaje; las preguntas no.",
            "El repositorio que estás leyendo es su propio caso de estudio: el verificador de equivalencia es literalmente una prueba de integración entre diez lenguajes, y su CI orquesta siete toolchains. Cuando la clase 147 habla de integración continua multi-lenguaje, habla de un problema que este repo tuvo que resolver de verdad.",
        ],
        "asume": "Las Partes 2 y 5–8. Las herramientas de la Parte 2 (pruebas, paquetes, formateadores) se dan aquí por instaladas y comprendidas.",
        "logros": [
            "Escribir pruebas unitarias y de integración en los diez lenguajes del núcleo.",
            "Diagnosticar con depurador y con registro estructurado, y saber cuándo toca cada uno.",
            "Fijar dependencias con lockfile y explicar por qué una build sin ellos no es reproducible.",
            "Montar una CI que valide varios lenguajes en paralelo sin duplicar la lógica.",
            "Refactorizar apoyándote en pruebas y argumentar por qué el comportamiento no cambió.",
            "Perfilar antes de optimizar y defender la decisión con datos en vez de con intuición.",
        ],
        "bloques": [
            ("Comprobar que funciona", "Pruebas unitarias y de integración, depuradores y observabilidad en producción.", 139, 142),
            ("Que se construya igual siempre", "Dependencias con lockfile, builds reproducibles y control de versiones políglota.", 143, 145),
            ("Que llegue a producción", "Revisión de código, integración continua multi-lenguaje, entrega y despliegue.", 146, 148),
            ("Que se pueda cambiar", "Diseño y arquitectura, refactorización segura y patrones comparados entre lenguajes.", 149, 151),
            ("Que aguante", "Rendimiento medido, seguridad desde la primera línea y deuda técnica gestionada.", 152, 154),
        ],
        "malentendidos": [
            ("«Las pruebas son para proyectos grandes.»", "Son lo que permite cambiar el código sin miedo. En un proyecto pequeño el miedo simplemente se nota antes."),
            ("«Refactorizar es mejorar el código.»", "Es cambiar la estructura **sin alterar el comportamiento observable**. Si el comportamiento cambia, es otra cosa y necesita otras precauciones."),
            ("«Optimizo esto que se ve lento.»", "«Measure, don't guess»: el perfilador casi siempre señala un sitio distinto al que habrías tocado."),
        ],
        "abre": "Con el oficio cubierto, la Parte 10 aborda lo que ningún curso de un solo lenguaje puede enseñar: qué ocurre en la frontera entre dos.",
    },

    10: {
        "gancho": "Las fronteras entre lenguajes: FFI, ABI, serialización, contratos, Wasm e incrustación.",
        "resumen": [
            "Hasta aquí el curso estudiaba un problema resuelto en diez lenguajes que no se hablaban entre sí. Esta parte cambia la pregunta: cómo esos lenguajes **conviven dentro de un mismo sistema**. Es el territorio que justifica el enfoque políglota, porque todo sistema real de cierto tamaño lo es.",
            "Las fronteras se ordenan de la más íntima a la más laxa. La **FFI** llama una función de otro lenguaje dentro del mismo proceso, con la ABI como contrato silencioso que, cuando no coincide, no da error sino corrupción. Los **bindings** envuelven esa frontera para hacerla habitable. Después, las fronteras por datos: serialización, contratos de API y el canal por el que viajan los bytes.",
            "Cierra con dos terrenos comunes —WebAssembly como objetivo independiente de arquitectura, y la incrustación de un intérprete dentro de un anfitrión— y con la decisión que todo lo anterior vuelve informada: qué lenguaje merece cada componente y qué coste de frontera se acepta a cambio.",
        ],
        "asume": "Las Partes 6, 8 y 9. Propiedad y ciclo de vida (103), memoria y punteros (128–130) y contratos de módulo (087) son requisito directo.",
        "logros": [
            "Llamar a una función de C desde otro lenguaje y explicar qué garantías se pierden al cruzar.",
            "Diagnosticar un fallo de ABI distinguiéndolo de un error de tipos en el código fuente.",
            "Elegir entre JSON, Protobuf y MessagePack con un criterio de tamaño, velocidad y legibilidad.",
            "Definir un contrato de API versionado que sobreviva a un cambio en uno de los dos lados.",
            "Decidir el canal de comunicación según el acoplamiento temporal que quieras aceptar.",
            "Justificar por escrito la elección de lenguaje de cada componente de un sistema.",
        ],
        "bloques": [
            ("La frontera íntima: mismo proceso", "Por qué los sistemas son políglotas, la FFI, la ABI que la sostiene y los bindings que la hacen usable.", 155, 158),
            ("La frontera por datos", "Serialización, contratos de API y los canales por los que viajan los bytes.", 159, 161),
            ("Terrenos comunes", "WebAssembly como objetivo compartido e incrustar un lenguaje dentro de otro.", 162, 163),
            ("La decisión", "Elegir el lenguaje de cada componente con criterios explícitos.", 164, 164),
        ],
        "malentendidos": [
            ("«Si la firma está bien declarada, la FFI funciona.»", "Bajo la firma está la ABI: convención de llamada, alineación y tamaños. Cuando no coinciden, el fallo es corrupción silenciosa."),
            ("«Un formato común basta para integrar dos servicios.»", "El formato dice cómo se escriben los datos; el contrato dice cuáles y qué operaciones. Sin contrato, la integración dura hasta el primer cambio."),
            ("«Políglota significa usar muchos lenguajes.»", "Significa pagar conscientemente el coste de cada frontera a cambio de una ventaja concreta y defendible."),
        ],
        "abre": "Con las fronteras comprendidas, la Parte 11 construye un sistema real que las usa todas.",
    },

    11: {
        "gancho": "Un sistema real con cinco componentes en cinco lenguajes, construido, probado, desplegado y defendido.",
        "resumen": [
            "El proyecto integrador reúne las once partes anteriores en un solo sistema: una CLI en un lenguaje de sistemas, un servicio backend, un frontend web, una capa de datos en SQL y scripts de automatización. No es un ejercicio ilustrativo — es la forma que tiene de verdad un sistema profesional.",
            "El orden reproduce el de un proyecto real: primero el inventario de componentes, después los **contratos** entre ellos (antes de escribir código), luego cada pieza, después la persistencia, las pruebas end-to-end y el empaquetado, y por último la documentación. Cada clase añade al mismo sistema, así que saltarse una deja un hueco visible en la siguiente.",
            "El cierre no es el despliegue sino la **defensa razonada**: un sistema con cinco lenguajes sin justificación escrita es un sistema que nadie querrá mantener. La clase 176 devuelve la tesis del programa convertida en método: cómo abordar solo el lenguaje número once.",
        ],
        "asume": "Todo el programa anterior. En particular la Parte 9 (pruebas, CI, despliegue) y la Parte 10 (contratos y fronteras), que aquí se aplican en vez de estudiarse.",
        "logros": [
            "Descomponer un sistema en componentes con responsabilidades disjuntas y contratos explícitos.",
            "Implementar cada componente en el lenguaje adecuado y justificar la elección con criterios.",
            "Hacer que cinco componentes en cinco lenguajes se comuniquen sin acoplarse innecesariamente.",
            "Probar el sistema completo de extremo a extremo y detectar los fallos de contrato entre piezas.",
            "Empaquetar y desplegar un sistema políglota de forma reproducible.",
            "Defender por escrito cada decisión de lenguaje ante alguien que no participó en el proyecto.",
        ],
        "bloques": [
            ("Diseño", "Inventario de componentes y definición de responsabilidades y contratos antes de codificar.", 165, 166),
            ("Los cinco componentes", "CLI, servicio, frontend, datos y automatización: cada pieza en su lenguaje natural.", 167, 171),
            ("Datos, pruebas y despliegue", "Persistencia, pruebas end-to-end y empaquetado en contenedores.", 172, 174),
            ("Defender y transferir", "La documentación de decisiones y el cierre del programa con el método de transferencia.", 175, 176),
        ],
        "malentendidos": [
            ("«Un sistema políglota es una decisión estética.»", "Cada frontera cuesta: serialización, despliegue, depuración y equipo. Solo se justifica si la ventaja del lenguaje elegido supera ese coste."),
            ("«Si cada componente pasa sus pruebas, el sistema funciona.»", "Los fallos de un sistema distribuido viven en los contratos entre piezas, que ninguna prueba unitaria mira."),
            ("«La documentación se escribe al final si sobra tiempo.»", "La defensa de las decisiones es lo que permite que otro equipo mantenga el sistema. Sin ella, el sistema se reescribe."),
        ],
        "abre": "El programa termina donde empezó, en la clase 001, pero con una diferencia: ahora el método de transferencia lo aplicas tú, sobre el lenguaje que elijas.",
    },
}
