"""Segunda división de la Parte 3: clases 047-056. Reutiliza la maquinaria de
gen_parte3.py (render + write_class) y solo aporta los contratos e impls.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

# ---- 047 Caracteres, texto y Unicode ----
S[47] = {
    "descripcion": "Dado un carácter, mostrar el propio carácter y su punto de código (code point).",
    "objetivo": "Entender que un **carácter** es, por dentro, un número: su punto de código. Verás cómo cada lenguaje lee un carácter y obtiene su código, y por qué el texto es, en el fondo, una secuencia de números.",
    "resultados": ["Obtener el punto de código de un carácter.", "Leer un único carácter de la entrada.", "Explicar la relación entre carácter y número."],
    "temas": [("Carácter como número", "Cada carácter tiene un código (ASCII/Unicode)"), ("Leer un carácter", "Distinto de leer una línea"), ("ASCII y Unicode", "Del código 0-127 a todo el texto humano"), ("char vs. string", "Un carácter no es una cadena de longitud 1 en todos")],
    "definiciones": [("Carácter", "símbolo textual (letra, dígito, signo). Clave: internamente es un número."), ("Punto de código", "número que identifica un carácter en Unicode/ASCII. Clave: 'A' es 65."), ("ASCII", "codificación de 0-127 para el inglés básico. Clave: subconjunto de Unicode."), ("Unicode", "estándar que asigna un código a cada carácter de todo idioma. Clave: el texto moderno.")],
    "situacion": "La letra 'A' y el número 65 son, para la máquina, lo mismo. Comprender que el texto son códigos numéricos explica el orden alfabético, las conversiones y por qué 'a' y 'A' son distintos.",
    "entrada": "un único carácter (ASCII)",
    "salida": "`char=<c> codigo=<punto de código>`",
    "formula": "codigo = punto_de_codigo(c)",
    "algoritmo": "LEER c\nESCRIBIR \"char=\" c \" codigo=\" CODIGO(c)",
    "casos": [("A", "char=A codigo=65"), ("z", "char=z codigo=122"), ("0", "char=0 codigo=48")],
    "comparacion": [("Sintáctica", "`ord(c)` (Python/PHP), `charCodeAt` (JS), `c as u32` (Rust)."), ("Semántica", "Java/C leen un byte/char; en C el carácter ya es un `int`."), ("Paradigmática", "SQL usa la función `unicode(c)` sobre una columna de texto.")],
    "familia": "En Ruby `c.ord`. En Haskell `Data.Char.ord c`. En C++ un `char` es directamente convertible a `int`, como en C.",
    "errores": [("Confundir carácter con cadena", "tratar 'A' como texto de longitud 1", "usar el tipo carácter y su código donde corresponde"), ("Asumir solo ASCII", "fallar con acentos o emoji", "recordar que Unicode va más allá de 0-127 (aquí usamos ASCII)")],
    "faq": [("¿'A' y 'a' tienen el mismo código?", "No: 65 y 97. Por eso las comparaciones distinguen mayúsculas."), ("¿Un emoji es un carácter?", "Un punto de código Unicode, sí; pero puede ocupar varios bytes al codificarse.")],
    "reto": "Muestra también `mayuscula=<C en mayúscula>` y resuélvelo en **Ruby** con `c.upcase`.",
    "impls": {
        "python": "import sys\n\nc = sys.stdin.readline().rstrip(\"\\n\")[0]\nprint(f\"char={c} codigo={ord(c)}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst data = readFileSync(0, \"utf8\");\nconst c = data[0];\nconsole.log(`char=${c} codigo=${data.charCodeAt(0)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst data: string = readFileSync(0, \"utf8\");\nconst c: string = data[0];\nconsole.log(`char=${c} codigo=${data.charCodeAt(0)}`);\n",
        "java": "import java.io.IOException;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        int r = System.in.read();\n        char c = (char) r;\n        System.out.println(\"char=\" + c + \" codigo=\" + r);\n    }\n}\n",
        "csharp": "using System;\n\nint r = Console.In.Read();\nchar c = (char) r;\nConsole.WriteLine($\"char={c} codigo={r}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n)\n\nfunc main() {\n\tb, _ := bufio.NewReader(os.Stdin).ReadByte()\n\tfmt.Printf(\"char=%c codigo=%d\\n\", b, b)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let c = s.chars().next().unwrap();\n    println!(\"char={} codigo={}\", c, c as u32);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    int c = getchar();\n    printf(\"char=%c codigo=%d\\n\", c, c);\n    return 0;\n}\n",
        "php": "<?php\n$c = fgetc(STDIN);\nprintf(\"char=%s codigo=%d\\n\", $c, ord($c));\n",
        "sql": "-- SQL: unicode(c) devuelve el punto de código de un carácter.\nWITH chars(c) AS (VALUES ('A'), ('z'), ('0'))\nSELECT printf('char=%s codigo=%d', c, unicode(c)) AS resultado\nFROM chars;\n",
    },
}

# ---- 048 Cadenas ----
S[48] = {
    "descripcion": "Dada una palabra, saludar e informar su longitud.",
    "objetivo": "Trabajar con **cadenas**: leer texto, interpolarlo en un saludo y medir su longitud. Verás que la longitud puede significar 'bytes' o 'caracteres' según el lenguaje (aquí, ASCII, coinciden).",
    "resultados": ["Interpolar una variable de texto en una cadena.", "Obtener la longitud de una cadena.", "Reconocer la inmutabilidad de las cadenas donde aplica."],
    "temas": [("Interpolación", "Insertar valores dentro de una cadena"), ("Longitud", "Cuántos caracteres tiene"), ("Inmutabilidad", "En muchos lenguajes la cadena no se modifica, se recrea"), ("Bytes vs. caracteres", "La longitud puede medir distinto")],
    "definiciones": [("Cadena", "secuencia de caracteres. Clave: el tipo para todo texto."), ("Interpolación", "insertar el valor de una variable dentro de una cadena. Clave: `f\"...{x}\"`, `${x}`, etc."), ("Longitud", "número de unidades (caracteres/bytes) de la cadena. Clave: en ASCII coinciden."), ("Inmutabilidad de cadenas", "en Java, C#, Python las cadenas no se modifican in situ. Clave: se crea una nueva.")],
    "situacion": "Saludar por nombre y contar caracteres son de las operaciones más comunes. Cómo se interpola y cómo se mide la longitud revela decisiones de diseño de cada lenguaje.",
    "entrada": "una palabra (ASCII, sin espacios)",
    "salida": "`hola=<palabra> longitud=<número de caracteres>`",
    "formula": "longitud = |palabra|",
    "algoritmo": "LEER w\nESCRIBIR \"hola=\" w \" longitud=\" LONGITUD(w)",
    "casos": [("Ada", "hola=Ada longitud=3"), ("Bo", "hola=Bo longitud=2"), ("polyglot", "hola=polyglot longitud=8")],
    "comparacion": [("Sintáctica", "`len(w)` (Python), `w.length` (JS/Java), `len(w)` (Go, bytes), `w.len()` (Rust, bytes)."), ("Semántica", "En Go/Rust `len` cuenta bytes; en Java/JS cuenta unidades UTF-16 (aquí ASCII: igual)."), ("Paradigmática", "SQL usa la función `length(w)` sobre una columna.")],
    "familia": "En Ruby `w.length`. En Haskell `length w`. En C++ `w.size()`. Todos miden lo mismo en ASCII; difieren con Unicode multibyte.",
    "errores": [("Asumir que longitud = caracteres siempre", "olvidar Unicode multibyte", "en Go/Rust `len` es bytes; usar el conteo de caracteres si hace falta"), ("Modificar una cadena in situ", "esperar mutación en Java/Python", "recordar que la cadena es inmutable: se crea una nueva")],
    "faq": [("¿Por qué las cadenas son inmutables?", "Seguridad y optimización (compartir, hashear). Modificar crea una copia."), ("¿`len` en Go da caracteres?", "Da bytes; para caracteres Unicode se usa `utf8.RuneCountInString`.")],
    "reto": "Muestra también `mayus=<palabra en mayúsculas>` y resuélvelo en **Kotlin** con `w.uppercase()`.",
    "impls": {
        "python": "import sys\n\nw = sys.stdin.readline().strip()\nprint(f\"hola={w} longitud={len(w)}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst w = readFileSync(0, \"utf8\").trim();\nconsole.log(`hola=${w} longitud=${w.length}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst w: string = readFileSync(0, \"utf8\").trim();\nconsole.log(`hola=${w} longitud=${w.length}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String w = br.readLine().trim();\n        System.out.println(\"hola=\" + w + \" longitud=\" + w.length());\n    }\n}\n",
        "csharp": "using System;\n\nstring w = Console.In.ReadToEnd().Trim();\nConsole.WriteLine($\"hola={w} longitud={w.Length}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tw := strings.TrimSpace(line)\n\tfmt.Printf(\"hola=%s longitud=%d\\n\", w, len(w))\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let w = s.trim();\n    println!(\"hola={} longitud={}\", w, w.len());\n}\n",
        "c": "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char buf[256];\n    if (scanf(\"%255s\", buf) != 1) return 1;\n    printf(\"hola=%s longitud=%d\\n\", buf, (int) strlen(buf));\n    return 0;\n}\n",
        "php": "<?php\n$w = trim(fgets(STDIN));\nprintf(\"hola=%s longitud=%d\\n\", $w, strlen($w));\n",
        "sql": "-- SQL: length(w) cuenta los caracteres de una cadena.\nWITH palabras(w) AS (VALUES ('Ada'), ('Bo'), ('polyglot'))\nSELECT printf('hola=%s longitud=%d', w, length(w)) AS resultado\nFROM palabras;\n",
    },
}

# ---- 049 Conversión de tipos ----
S[49] = {
    "descripcion": "Dado un número real como texto, mostrar su parte entera (truncada) y el valor con dos decimales.",
    "objetivo": "Distinguir **conversión explícita** (casting) de **coerción implícita**. Convertir un texto a real, y ese real a entero (truncando), muestra cómo cada lenguaje exige o realiza la conversión.",
    "resultados": ["Convertir texto a número.", "Convertir un real a entero por truncamiento.", "Diferenciar casting explícito de coerción implícita."],
    "temas": [("De texto a número", "Parsear la entrada"), ("Truncamiento", "Quitar la parte decimal hacia cero"), ("Casting explícito", "El programador ordena la conversión"), ("Coerción implícita", "El lenguaje convierte solo")],
    "definiciones": [("Conversión (casting)", "cambiar el tipo de un valor explícitamente. Clave: `int(x)`, `(long)f`."), ("Coerción", "conversión automática que hace el lenguaje. Clave: fuente de sorpresas en los débilmente tipados."), ("Truncamiento", "descartar la parte decimal hacia cero. Clave: distinto de redondear."), ("Parseo", "interpretar un texto como un número. Clave: primer paso de casi toda entrada.")],
    "situacion": "Un formulario entrega '3.7' como texto. Para calcular hay que convertirlo a número, y quizá a entero. Cada lenguaje exige un grado distinto de explicitud, y truncar no es redondear.",
    "entrada": "un número real como texto",
    "salida": "`entero=<parte entera truncada> real=<valor con 2 decimales>`",
    "formula": "entero = truncar(real) ; real formateado a 2 decimales",
    "algoritmo": "LEER texto\nreal <- A_REAL(texto)\nentero <- TRUNCAR(real)\nESCRIBIR \"entero=\" entero \" real=\" FORMATEAR(real,2)",
    "casos": [("3.7", "entero=3 real=3.70"), ("5.0", "entero=5 real=5.00"), ("8.9", "entero=8 real=8.90")],
    "comparacion": [("Sintáctica", "`int(f)` (Python), `Math.trunc` (JS), `(long)f` (Java/C/C#), `f as i64` (Rust)."), ("Semántica", "El truncamiento va hacia cero; no confundir con redondeo (`round`)."), ("Paradigmática", "SQL usa `CAST(x AS INTEGER)`.")],
    "familia": "En Ruby `f.to_i` trunca. En Haskell `truncate f`. En C++ `static_cast<long>(f)`. Todos truncan hacia cero (para positivos, igual que floor).",
    "errores": [("Confundir truncar con redondear", "esperar 4 de 3.7", "usar la conversión a entero (trunca), no round"), ("Sumar texto y número", "olvidar convertir la entrada", "parsear siempre el texto antes de operar")],
    "faq": [("¿Truncar y floor son lo mismo?", "Para positivos sí; para negativos no (trunc va a cero, floor hacia abajo)."), ("¿Qué es coerción implícita?", "Que el lenguaje convierta sin pedirlo (p. ej. PHP suma '3'+4). Puede sorprender.")],
    "reto": "Añade `redondeo=<real redondeado a entero>` y resuélvelo en **Go** con `math.Round`.",
    "impls": {
        "python": "import sys\n\nf = float(sys.stdin.readline().strip())\nprint(f\"entero={int(f)} real={f:.2f}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst f = parseFloat(readFileSync(0, \"utf8\").trim());\nconsole.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst f: number = parseFloat(readFileSync(0, \"utf8\").trim());\nconsole.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\nimport java.util.Locale;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        double f = Double.parseDouble(br.readLine().trim());\n        System.out.printf(Locale.US, \"entero=%d real=%.2f%n\", (long) f, f);\n    }\n}\n",
        "csharp": "using System;\nusing System.Globalization;\n\nvar inv = CultureInfo.InvariantCulture;\ndouble f = double.Parse(Console.In.ReadToEnd().Trim(), inv);\nConsole.WriteLine($\"entero={(long)f} real={f.ToString(\"F2\", inv)}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf, _ := strconv.ParseFloat(strings.TrimSpace(line), 64)\n\tfmt.Printf(\"entero=%d real=%.2f\\n\", int64(f), f)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let f: f64 = s.trim().parse().unwrap();\n    println!(\"entero={} real={:.2}\", f as i64, f);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    double f;\n    if (scanf(\"%lf\", &f) != 1) return 1;\n    printf(\"entero=%ld real=%.2f\\n\", (long) f, f);\n    return 0;\n}\n",
        "php": "<?php\n$f = (float) trim(fgets(STDIN));\nprintf(\"entero=%d real=%.2f\\n\", (int) $f, $f);\n",
        "sql": "-- SQL: CAST(x AS INTEGER) trunca hacia cero.\nWITH nums(x) AS (VALUES (3.7), (5.0), (8.9))\nSELECT printf('entero=%d real=%.2f', CAST(x AS INTEGER), x) AS resultado\nFROM nums;\n",
    },
}

# ---- 050 Tipado estático vs dinámico ----
S[50] = {
    "descripcion": "Sumar un entero y un real y mostrar el resultado con dos decimales.",
    "objetivo": "Ver la diferencia entre **tipado estático** (el tipo se fija y comprueba al compilar) y **dinámico** (se resuelve al ejecutar). Sumar un entero con un real obliga, en los estáticos, a una conversión explícita que en los dinámicos ocurre sola.",
    "resultados": ["Sumar valores de tipos distintos (entero + real).", "Reconocer dónde hace falta convertir explícitamente.", "Explicar estático vs. dinámico con un ejemplo."],
    "temas": [("Tipado estático", "El compilador conoce y comprueba los tipos"), ("Tipado dinámico", "El tipo se conoce al ejecutar"), ("Promoción numérica", "Entero que se convierte a real para operar"), ("Errores en compilación vs. ejecución", "Cuándo se detecta un tipo mal usado")],
    "definiciones": [("Tipado estático", "los tipos se fijan y comprueban en compilación (Java, C#, Go, Rust, C). Clave: errores antes de ejecutar."), ("Tipado dinámico", "los tipos se resuelven en ejecución (Python, PHP, JS). Clave: flexible, errores más tarde."), ("Promoción", "convertir un entero a real para operar con otro real. Clave: en estáticos suele ser explícita."), ("Comprobación de tipos", "verificar que las operaciones son válidas para los tipos. Clave: estática o dinámica.")],
    "situacion": "Sumar `2 + 3.5`: en Python simplemente da `5.5`; en Go debes convertir el entero a `float64` primero. La misma operación revela la filosofía de tipos de cada lenguaje.",
    "entrada": "una línea `a b` (a entero, b real)",
    "salida": "`suma=<a+b con 2 decimales>`",
    "formula": "suma = a + b (a entero promovido a real)",
    "algoritmo": "LEER a (entero), b (real)\nESCRIBIR \"suma=\" FORMATEAR(a+b, 2)",
    "casos": [("2 3.5", "suma=5.50"), ("10 0.25", "suma=10.25"), ("0 0", "suma=0.00")],
    "comparacion": [("Sintáctica", "Python/PHP suman directo; Go exige `float64(a)+b`."), ("Semántica", "En estáticos el tipo del resultado se decide en compilación; en dinámicos, al ejecutar."), ("Paradigmática", "SQL trata los números de forma uniforme en la expresión.")],
    "familia": "En Ruby `a + b` funciona por coerción numérica. En Haskell (estático fuerte) hace falta `fromIntegral a + b`, similar a Go pero más estricto.",
    "errores": [("Sumar int y float sin convertir en Go/Rust", "el compilador rechaza tipos mezclados", "convertir el entero a real explícitamente"), ("Confiar en el tipo en un dinámico", "un dato inesperado rompe en ejecución", "validar la entrada donde el compilador no ayuda")],
    "faq": [("¿Cuál es mejor?", "Estático atrapa errores antes; dinámico itera más rápido. Depende del proyecto."), ("¿Por qué Go obliga a convertir?", "Para que la promoción sea visible y no haya conversiones silenciosas.")],
    "reto": "Añade `tipo_a=entero tipo_b=real` a la salida y resuélvelo en **Python** usando `type(...).__name__`.",
    "impls": {
        "python": "import sys\n\np = sys.stdin.readline().split()\na = int(p[0])\nb = float(p[1])\nprint(f\"suma={a + b:.2f}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [x, y] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconst a = parseInt(x, 10);\nconst b = parseFloat(y);\nconsole.log(`suma=${(a + b).toFixed(2)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [x, y]: string[] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconst a: number = parseInt(x, 10);\nconst b: number = parseFloat(y);\nconsole.log(`suma=${(a + b).toFixed(2)}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\nimport java.util.Locale;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        int a = Integer.parseInt(p[0]);\n        double b = Double.parseDouble(p[1]);\n        System.out.printf(Locale.US, \"suma=%.2f%n\", a + b);\n    }\n}\n",
        "csharp": "using System;\nusing System.Globalization;\n\nvar inv = CultureInfo.InvariantCulture;\nstring[] p = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nint a = int.Parse(p[0], inv);\ndouble b = double.Parse(p[1], inv);\nConsole.WriteLine($\"suma={(a + b).ToString(\"F2\", inv)}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf := strings.Fields(line)\n\ta, _ := strconv.Atoi(f[0])\n\tb, _ := strconv.ParseFloat(f[1], 64)\n\tfmt.Printf(\"suma=%.2f\\n\", float64(a)+b)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let v: Vec<&str> = s.split_whitespace().collect();\n    let a: i64 = v[0].parse().unwrap();\n    let b: f64 = v[1].parse().unwrap();\n    println!(\"suma={:.2}\", a as f64 + b);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long a;\n    double b;\n    if (scanf(\"%ld %lf\", &a, &b) != 2) return 1;\n    printf(\"suma=%.2f\\n\", (double) a + b);\n    return 0;\n}\n",
        "php": "<?php\n[$x, $y] = preg_split('/\\s+/', trim(fgets(STDIN)));\n$a = (int) $x;\n$b = (float) $y;\nprintf(\"suma=%.2f\\n\", $a + $b);\n",
        "sql": "-- SQL evalúa la expresión numérica de forma uniforme.\nWITH pares(a, b) AS (VALUES (2, 3.5), (10, 0.25), (0, 0))\nSELECT printf('suma=%.2f', a + b) AS resultado\nFROM pares;\n",
    },
}

# ---- 051 Tipado fuerte vs débil ----
S[51] = {
    "descripcion": "Dado un entero, mostrar su suma consigo mismo (número) y su concatenación consigo mismo (texto).",
    "objetivo": "Distinguir **tipado fuerte** (no mezcla tipos sin permiso) de **débil** (convierte soluto). El mismo `+` puede sumar números o concatenar texto: verlo lado a lado aclara por qué `'5' + '5'` puede ser `10` o `'55'` según el lenguaje.",
    "resultados": ["Diferenciar suma numérica de concatenación de texto.", "Explicar tipado fuerte vs. débil con `+`.", "Producir ambos resultados de forma explícita."],
    "temas": [("Suma vs. concatenación", "El mismo símbolo, dos operaciones"), ("Tipado fuerte", "No convierte tipos sin que lo pidas"), ("Tipado débil", "Convierte automáticamente (a veces sorprende)"), ("El operador +", "Sobrecargado en muchos lenguajes")],
    "definiciones": [("Tipado fuerte", "no permite operar entre tipos incompatibles sin conversión (Python, Java). Clave: menos sorpresas."), ("Tipado débil", "convierte tipos automáticamente para operar (PHP, JS). Clave: `'5'+5` puede dar cosas raras."), ("Concatenación", "unir dos cadenas. Clave: en muchos lenguajes también con `+`."), ("Sobrecarga de operador", "un operador con distinto significado según los tipos. Clave: `+` suma o concatena.")],
    "situacion": "En JavaScript `'5' + 5` da `'55'` (concatena) y `'5' - 5` da `0` (resta). Esa es la marca del tipado débil. Verlo explícito evita bugs difíciles de rastrear.",
    "entrada": "un entero `n`",
    "salida": "`suma=<n+n> texto=<n concatenado consigo mismo>`",
    "formula": "suma = n + n ; texto = str(n) ++ str(n)",
    "algoritmo": "LEER n\nESCRIBIR \"suma=\" (n+n) \" texto=\" (TEXTO(n) ++ TEXTO(n))",
    "casos": [("5", "suma=10 texto=55"), ("3", "suma=6 texto=33"), ("12", "suma=24 texto=1212")],
    "comparacion": [("Sintáctica", "`str(n)+str(n)` (Python) vs. `n + \"\" + n` (Java) vs. `$n.$n` (PHP)."), ("Semántica", "Python (fuerte) exige `str(n)` para concatenar; JS/PHP (débil) convierten solos."), ("Paradigmática", "SQL usa `||` para concatenar y `+` no existe para texto.")],
    "familia": "En Ruby (fuerte) `n.to_s + n.to_s`. En JS (débil) `n + '' + n` concatena por coerción. Haskell (muy fuerte) obliga `show n ++ show n`.",
    "errores": [("Esperar que `n + n` concatene", "confundir suma con concatenación", "convertir a texto explícitamente para concatenar"), ("Confiar en la coerción débil", "resultados inesperados con `+`", "convertir de forma explícita para que la intención sea clara")],
    "faq": [("¿Por qué `'5'+5` es `'55'` en JS?", "Tipado débil: ante texto y número, `+` concatena convirtiendo el número a texto."), ("¿Python es fuerte o débil?", "Fuerte: `'5' + 5` es un error; hay que convertir explícitamente.")],
    "reto": "Muestra también `resta=<n-n>` (siempre 0) y explica por qué la resta no concatena. Resuélvelo en **JavaScript**.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"suma={n + n} texto={str(n) + str(n)}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`suma=${n + n} texto=${String(n) + String(n)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`suma=${n + n} texto=${String(n) + String(n)}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        String t = Integer.toString(n) + Integer.toString(n);\n        System.out.printf(\"suma=%d texto=%s%n\", n + n, t);\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"suma={n + n} texto={n.ToString() + n.ToString()}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\ts := strconv.Itoa(n)\n\tfmt.Printf(\"suma=%d texto=%s%s\\n\", n+n, s, s)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"suma={} texto={}{}\", n + n, n, n);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"suma=%ld texto=%ld%ld\\n\", n + n, n, n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\nprintf(\"suma=%d texto=%s\\n\", $n + $n, (string) $n . (string) $n);\n",
        "sql": "-- SQL concatena con || (no con +).\nWITH nums(n) AS (VALUES (5), (3), (12))\nSELECT printf('suma=%d texto=%s', n + n, n || n) AS resultado\nFROM nums;\n",
    },
}

# ---- 052 Inferencia de tipos ----
S[52] = {
    "descripcion": "Multiplicar dos enteros y mostrar el producto.",
    "objetivo": "Ver la **inferencia de tipos**: el compilador deduce el tipo sin que lo anotes. Un producto de dos enteros basta para comparar `x = a*b` (Python), `var`/`:=` (C#/Go), `let` (Rust) frente a la anotación explícita de Java o C.",
    "resultados": ["Reconocer dónde el lenguaje infiere el tipo.", "Comparar inferencia con anotación explícita.", "Escribir el mismo cálculo con y sin anotar tipos."],
    "temas": [("Inferencia", "El compilador deduce el tipo del valor"), ("Anotación explícita", "El programador escribe el tipo"), ("var/:=/let", "Palabras de inferencia por lenguaje"), ("Inferencia no es dinámico", "El tipo sigue siendo fijo, solo no se escribe")],
    "definiciones": [("Inferencia de tipos", "el compilador deduce el tipo a partir del valor. Clave: menos ruido, mismo tipado estático."), ("Anotación de tipo", "escribir el tipo explícitamente (`int x`). Clave: obligatoria donde no hay inferencia."), ("var / := / let", "formas de declarar con inferencia (C#, Go, Rust). Clave: el tipo se fija igual."), ("Estático con inferencia", "tipos fijos que no hace falta anotar. Clave: no confundir con dinámico.")],
    "situacion": "`var total = a * b;` en C# infiere que `total` es entero. No es tipado dinámico: el tipo es fijo, solo no lo escribiste. Distinguir inferencia de dinamismo evita malentendidos.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`producto=<a*b>`",
    "formula": "producto = a * b",
    "algoritmo": "LEER a, b\nESCRIBIR \"producto=\" (a*b)",
    "casos": [("3 4", "producto=12"), ("0 9", "producto=0"), ("-2 5", "producto=-10")],
    "comparacion": [("Sintáctica", "`p = a*b` (Python), `p := a*b` (Go), `let p = a*b` (Rust), `int p = a*b` (Java/C)."), ("Semántica", "En Go/Rust/C# el tipo se infiere pero es fijo; en Java/C se anota."), ("Paradigmática", "SQL no declara variables: la expresión produce el valor.")],
    "familia": "En Kotlin `val p = a * b` infiere. En C++ `auto p = a * b`. En Haskell la inferencia (Hindley-Milner) es total: casi nunca anotas tipos.",
    "errores": [("Creer que inferencia = dinámico", "confundir no-anotar con no-tipar", "recordar que el tipo inferido es fijo y se comprueba"), ("No anotar donde hace falta", "Java/C exigen el tipo", "anotar cuando el lenguaje no infiere")],
    "faq": [("¿La inferencia hace el código más lento?", "No: ocurre en compilación; el binario es idéntico al anotado."), ("¿Siempre puede inferir?", "No siempre; a veces el tipo es ambiguo y hay que anotar.")],
    "reto": "Resuélvelo en **Kotlin** con `val` y observa que no escribes ningún tipo, pero el compilador los conoce.",
    "impls": {
        "python": "import sys\n\na, b = map(int, sys.stdin.readline().split())\nprint(f\"producto={a * b}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`producto=${a * b}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b]: number[] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`producto=${a * b}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        int a = Integer.parseInt(p[0]);\n        int b = Integer.parseInt(p[1]);\n        System.out.println(\"producto=\" + (a * b));\n    }\n}\n",
        "csharp": "using System;\n\nstring[] p = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nvar a = int.Parse(p[0]);\nvar b = int.Parse(p[1]);\nConsole.WriteLine($\"producto={a * b}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf := strings.Fields(line)\n\ta, _ := strconv.Atoi(f[0])\n\tb, _ := strconv.Atoi(f[1])\n\tproducto := a * b\n\tfmt.Printf(\"producto=%d\\n\", producto)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();\n    let producto = v[0] * v[1];\n    println!(\"producto={producto}\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long a, b;\n    if (scanf(\"%ld %ld\", &a, &b) != 2) return 1;\n    printf(\"producto=%ld\\n\", a * b);\n    return 0;\n}\n",
        "php": "<?php\n[$a, $b] = preg_split('/\\s+/', trim(fgets(STDIN)));\n$producto = (int) $a * (int) $b;\nprintf(\"producto=%d\\n\", $producto);\n",
        "sql": "-- SQL: la expresión produce el valor sin declarar variables.\nWITH pares(a, b) AS (VALUES (3, 4), (0, 9), (-2, 5))\nSELECT printf('producto=%d', a * b) AS resultado\nFROM pares;\n",
    },
}

# ---- 053 Nulabilidad ----
S[53] = {
    "descripcion": "Dado un entero donde 0 representa 'ausente', informar si hay valor o no.",
    "objetivo": "Modelar la **ausencia de valor**: null, nil, None, Option. Usando 0 como centinela de 'ausente', verás cómo cada lenguaje representa y maneja la falta de un dato, y por qué las opciones tipadas (Option/Result) evitan el temido puntero nulo.",
    "resultados": ["Distinguir un valor presente de uno ausente.", "Nombrar cómo cada lenguaje representa la ausencia.", "Explicar por qué Option/None es más seguro que null."],
    "temas": [("Ausencia de valor", "No todo dato existe siempre"), ("null / nil / None", "Nombres del 'nada' por lenguaje"), ("Option / Maybe", "Ausencia tipada y segura"), ("El error del billón de dólares", "Los NullPointerException")],
    "definiciones": [("Nulabilidad", "posibilidad de que un valor esté ausente. Clave: fuente clásica de errores."), ("null / nil / None", "representación de 'sin valor'. Clave: cada lenguaje lo llama distinto."), ("Option / Maybe", "tipo que envuelve 'hay valor' o 'no hay' (Rust, Haskell). Clave: obliga a manejar la ausencia."), ("Valor centinela", "un valor normal usado para significar 'ausente' (aquí, 0). Clave: sencillo pero frágil.")],
    "situacion": "Buscar un usuario que no existe: ¿qué devuelves? null puede reventar el programa más tarde con un NullPointerException. Modelar la ausencia explícitamente (Option/None) obliga a tratarla.",
    "entrada": "un entero `n` (0 significa ausente)",
    "salida": "`valor=<n>` si hay valor, o `valor=ausente` si n es 0",
    "formula": "si n == 0 → 'ausente'; si no → n",
    "algoritmo": "LEER n\nSI n == 0: ESCRIBIR \"valor=ausente\"\nSINO: ESCRIBIR \"valor=\" n",
    "casos": [("5", "valor=5"), ("0", "valor=ausente"), ("42", "valor=42")],
    "comparacion": [("Sintáctica", "Operador ternario o `if` para decidir presente/ausente."), ("Semántica", "Rust modela la ausencia con `Option<T>`; Java/C con null o un centinela."), ("Paradigmática", "SQL tiene `NULL` nativo y `CASE WHEN` para tratarlo.")],
    "familia": "En Rust idiomático sería `Option<i64>` y un `match`. En Haskell `Maybe Int`. En Kotlin el tipo `Int?` marca la nulabilidad en el propio tipo.",
    "errores": [("Usar un valor ausente como si existiera", "el NullPointerException clásico", "comprobar la ausencia antes de usar el valor"), ("Elegir un centinela que es un dato válido", "0 podría ser legítimo", "preferir un tipo Option explícito cuando el lenguaje lo ofrece")],
    "faq": [("¿Por qué null es peligroso?", "Se cuela sin avisar y estalla al usarlo. Los tipos Option obligan a manejarlo."), ("¿Qué lenguajes del núcleo tienen Option?", "Rust (`Option`). Otros usan null/nil; Kotlin (primo JVM) marca nulabilidad en el tipo.")],
    "reto": "Cambia el centinela de 'ausente' a `-1` y resuélvelo en **Rust** usando `Option<i64>` de verdad.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(\"valor=ausente\" if n == 0 else f\"valor={n}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(n === 0 ? \"valor=ausente\" : `valor=${n}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(n === 0 ? \"valor=ausente\" : `valor=${n}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(n == 0 ? \"valor=ausente\" : \"valor=\" + n);\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine(n == 0 ? \"valor=ausente\" : $\"valor={n}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tif n == 0 {\n\t\tfmt.Println(\"valor=ausente\")\n\t} else {\n\t\tfmt.Printf(\"valor=%d\\n\", n)\n\t}\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    let valor: Option<i64> = if n == 0 { None } else { Some(n) };\n    match valor {\n        None => println!(\"valor=ausente\"),\n        Some(v) => println!(\"valor={v}\"),\n    }\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    if (n == 0) {\n        printf(\"valor=ausente\\n\");\n    } else {\n        printf(\"valor=%ld\\n\", n);\n    }\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho $n === 0 ? \"valor=ausente\\n\" : \"valor=$n\\n\";\n",
        "sql": "-- SQL tiene NULL nativo; aquí 0 modela la ausencia con CASE WHEN.\nWITH nums(n) AS (VALUES (5), (0), (42))\nSELECT CASE WHEN n = 0 THEN 'valor=ausente' ELSE printf('valor=%d', n) END AS resultado\nFROM nums;\n",
    },
}

# ---- 054 Mutabilidad e inmutabilidad ----
S[54] = {
    "descripcion": "Dado un entero n, construir la secuencia '1-2-...-n'.",
    "objetivo": "Ver la diferencia entre construir un resultado **mutando** un acumulador (StringBuilder, lista que crece) y hacerlo de forma **inmutable**. Construir una secuencia numérica muestra el patrón acumulador en cada lenguaje.",
    "resultados": ["Construir un resultado acumulando en un bucle.", "Reconocer estructuras mutables (builder, lista).", "Explicar el coste de concatenar cadenas inmutables."],
    "temas": [("Acumulador", "Una variable que crece en cada vuelta"), ("Mutable vs. inmutable", "Modificar en sitio o crear nuevo"), ("StringBuilder", "Construir texto eficientemente"), ("Coste de la inmutabilidad", "Concatenar cadenas puede recrear todo")],
    "definiciones": [("Mutabilidad", "capacidad de cambiar un valor in situ. Clave: eficiente para construir por partes."), ("Inmutabilidad", "el valor no cambia; toda 'modificación' crea uno nuevo. Clave: más seguro, a veces más caro."), ("Acumulador", "variable que reúne el resultado a lo largo de un bucle. Clave: patrón universal."), ("Builder", "estructura mutable para construir cadenas/colecciones (StringBuilder). Clave: evita recrear en cada paso.")],
    "situacion": "Concatenar 10.000 cadenas con `+` en un bucle puede ser lentísimo si cada `+` recrea toda la cadena. Por eso existen los builders mutables. Construir '1-2-...-n' ilustra el patrón.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`sec=1-2-...-n` (números de 1 a n separados por guiones)",
    "formula": "sec = unir([1..n], separador='-')",
    "algoritmo": "LEER n\nacc <- vacío\nPARA i de 1 a n: añadir i a acc\nESCRIBIR \"sec=\" UNIR(acc, \"-\")",
    "casos": [("3", "sec=1-2-3"), ("1", "sec=1"), ("5", "sec=1-2-3-4-5")],
    "comparacion": [("Sintáctica", "`'-'.join(...)` (Python), `StringBuilder` (Java/C#), `strings.Builder` (Go)."), ("Semántica", "Java/C#/Go usan builders mutables; Python/Rust juntan una lista al final."), ("Paradigmática", "SQL usa `group_concat` sobre filas generadas, no un bucle.")],
    "familia": "En Ruby `(1..n).to_a.join('-')`. En Haskell `intercalate \"-\" (map show [1..n])`, puramente inmutable. En C++ un `std::ostringstream`.",
    "errores": [("Concatenar con `+` en bucle grande", "recrear la cadena cada vuelta (O(n²))", "usar un builder mutable o juntar al final"), ("Olvidar el caso n=1", "poner un guion de más", "no añadir separador antes del primer elemento")],
    "faq": [("¿Siempre es mejor mutar?", "Para construir por partes, el builder es eficiente; para compartir datos, la inmutabilidad es más segura."), ("¿Por qué las cadenas suelen ser inmutables?", "Seguridad y para poder compartirlas/hashearlas sin copiar.")],
    "reto": "Construye la secuencia al revés (`n-...-1`) y resuélvelo en **Go** con `strings.Builder`.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(\"sec=\" + \"-\".join(str(i) for i in range(1, n + 1)))\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconst parts = [];\nfor (let i = 1; i <= n; i++) parts.push(i);\nconsole.log(`sec=${parts.join(\"-\")}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconst parts: number[] = [];\nfor (let i = 1; i <= n; i++) parts.push(i);\nconsole.log(`sec=${parts.join(\"-\")}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        StringBuilder sb = new StringBuilder();\n        for (int i = 1; i <= n; i++) {\n            if (i > 1) sb.append(\"-\");\n            sb.append(i);\n        }\n        System.out.println(\"sec=\" + sb);\n    }\n}\n",
        "csharp": "using System;\nusing System.Text;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nvar sb = new StringBuilder();\nfor (int i = 1; i <= n; i++) {\n    if (i > 1) sb.Append(\"-\");\n    sb.Append(i);\n}\nConsole.WriteLine($\"sec={sb}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tvar sb strings.Builder\n\tfor i := 1; i <= n; i++ {\n\t\tif i > 1 {\n\t\t\tsb.WriteString(\"-\")\n\t\t}\n\t\tsb.WriteString(strconv.Itoa(i))\n\t}\n\tfmt.Printf(\"sec=%s\\n\", sb.String())\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    let parts: Vec<String> = (1..=n).map(|i| i.to_string()).collect();\n    println!(\"sec={}\", parts.join(\"-\"));\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"sec=\");\n    for (long i = 1; i <= n; i++) {\n        if (i > 1) printf(\"-\");\n        printf(\"%ld\", i);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\n$parts = [];\nfor ($i = 1; $i <= $n; $i++) {\n    $parts[] = $i;\n}\necho \"sec=\" . implode(\"-\", $parts) . \"\\n\";\n",
        "sql": "-- SQL construye la secuencia con un CTE recursivo y group_concat (ilustrativo, n=5).\nWITH RECURSIVE seq(i) AS (\n    VALUES (1)\n    UNION ALL SELECT i + 1 FROM seq WHERE i < 5\n)\nSELECT 'sec=' || group_concat(i, '-') AS resultado FROM seq;\n",
    },
}

# ---- 055 Operadores y expresiones ----
S[55] = {
    "descripcion": "Dados dos enteros positivos, mostrar su suma, resta, producto, división entera y resto.",
    "objetivo": "Repasar los **operadores aritméticos** y ver diferencias sutiles: la división entera y el módulo se comportan distinto con negativos según el lenguaje (aquí usamos positivos para que coincidan). Es la base del cálculo en todo programa.",
    "resultados": ["Aplicar los cinco operadores aritméticos básicos.", "Distinguir división entera de división real.", "Reconocer que el módulo con negativos varía entre lenguajes."],
    "temas": [("Operadores aritméticos", "+, -, *, / y %"), ("División entera", "Descarta la parte decimal"), ("Módulo (resto)", "Lo que sobra de la división"), ("Precedencia", "El orden en que se evalúan")],
    "definiciones": [("Operador", "símbolo que combina valores para producir otro (+, *, %). Clave: bloque de las expresiones."), ("División entera", "cociente sin decimales. Clave: `7/2 = 3`, no 3.5."), ("Módulo", "resto de la división entera. Clave: `7 % 2 = 1`."), ("Precedencia", "el orden de evaluación (`*` antes que `+`). Clave: los paréntesis mandan.")],
    "situacion": "Repartir 7 caramelos entre 2 niños: cada uno recibe 3 (división entera) y sobra 1 (módulo). Estos operadores están en todo cálculo; sus reglas con negativos son una trampa clásica entre lenguajes.",
    "entrada": "una línea `a b` (enteros positivos, b != 0)",
    "salida": "`suma=<a+b> resta=<a-b> mult=<a*b> div=<a/b entera> mod=<a%b>`",
    "formula": "las cinco operaciones aritméticas sobre a y b",
    "algoritmo": "LEER a, b\nESCRIBIR suma, resta, mult, división entera y módulo",
    "casos": [("10 3", "suma=13 resta=7 mult=30 div=3 mod=1"), ("20 4", "suma=24 resta=16 mult=80 div=5 mod=0"), ("7 2", "suma=9 resta=5 mult=14 div=3 mod=1")],
    "comparacion": [("Sintáctica", "`//` (Python) vs. `/` entre enteros (C/Java/Go); `%` en casi todos."), ("Semántica", "Con negativos, el módulo difiere: Python da signo del divisor; C/Java, del dividendo."), ("Paradigmática", "SQL evalúa la expresión aritmética en la propia consulta.")],
    "familia": "En Ruby `a / b` es entero si ambos lo son, como C. En Haskell `div` y `mod` (y `quot`/`rem` con otra regla de signo).",
    "errores": [("Esperar decimales de `/` entre enteros", "en C/Java la división de enteros trunca", "usar reales si quieres decimales, o `//` en Python"), ("Asumir el mismo módulo con negativos", "Python y C difieren en el signo del resto", "usar entradas positivas o conocer la regla de cada lenguaje")],
    "faq": [("¿`7/2` es 3 o 3.5?", "Entre enteros, 3 (división entera). Con un real, 3.5."), ("¿Por qué el módulo varía con negativos?", "Cada lenguaje elige el signo del resto; por eso aquí usamos positivos.")],
    "reto": "Añade `potencia=<a elevado a b>` y resuélvelo en **Python** con `a ** b`.",
    "impls": {
        "python": "import sys\n\na, b = map(int, sys.stdin.readline().split())\nprint(f\"suma={a + b} resta={a - b} mult={a * b} div={a // b} mod={a % b}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`suma=${a + b} resta=${a - b} mult=${a * b} div=${Math.trunc(a / b)} mod=${a % b}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b]: number[] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`suma=${a + b} resta=${a - b} mult=${a * b} div=${Math.trunc(a / b)} mod=${a % b}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        int a = Integer.parseInt(p[0]);\n        int b = Integer.parseInt(p[1]);\n        System.out.printf(\"suma=%d resta=%d mult=%d div=%d mod=%d%n\", a + b, a - b, a * b, a / b, a % b);\n    }\n}\n",
        "csharp": "using System;\n\nstring[] p = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nint a = int.Parse(p[0]);\nint b = int.Parse(p[1]);\nConsole.WriteLine($\"suma={a + b} resta={a - b} mult={a * b} div={a / b} mod={a % b}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf := strings.Fields(line)\n\ta, _ := strconv.Atoi(f[0])\n\tb, _ := strconv.Atoi(f[1])\n\tfmt.Printf(\"suma=%d resta=%d mult=%d div=%d mod=%d\\n\", a+b, a-b, a*b, a/b, a%b)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();\n    let (a, b) = (v[0], v[1]);\n    println!(\"suma={} resta={} mult={} div={} mod={}\", a + b, a - b, a * b, a / b, a % b);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long a, b;\n    if (scanf(\"%ld %ld\", &a, &b) != 2) return 1;\n    printf(\"suma=%ld resta=%ld mult=%ld div=%ld mod=%ld\\n\", a + b, a - b, a * b, a / b, a % b);\n    return 0;\n}\n",
        "php": "<?php\n[$a, $b] = preg_split('/\\s+/', trim(fgets(STDIN)));\n$a = (int) $a;\n$b = (int) $b;\nprintf(\"suma=%d resta=%d mult=%d div=%d mod=%d\\n\", $a + $b, $a - $b, $a * $b, intdiv($a, $b), $a % $b);\n",
        "sql": "-- SQL evalúa las operaciones aritméticas en la consulta (/ entre enteros es división entera).\nWITH pares(a, b) AS (VALUES (10, 3), (20, 4), (7, 2))\nSELECT printf('suma=%d resta=%d mult=%d div=%d mod=%d', a + b, a - b, a * b, a / b, a % b) AS resultado\nFROM pares;\n",
    },
}

# ---- 056 Entrada y salida básica ----
S[56] = {
    "descripcion": "Leer una línea de texto y devolverla con el prefijo 'eco: '.",
    "objetivo": "Cerrar la Parte 3 con lo más elemental: **leer de la entrada estándar y escribir en la salida estándar**. Todo el curso se apoya en este contrato (stdin → stdout), y aquí se ve desnudo en los 10 lenguajes.",
    "resultados": ["Leer una línea completa de stdin.", "Escribir en stdout con un formato dado.", "Reconocer el contrato stdin/stdout usado en todo el curso."],
    "temas": [("Entrada estándar (stdin)", "El canal por defecto de entrada"), ("Salida estándar (stdout)", "El canal por defecto de salida"), ("Leer una línea", "Distinto de leer un token o un carácter"), ("El contrato del curso", "stdin → stdout, verificable")],
    "definiciones": [("stdin", "canal de entrada estándar de un programa. Clave: de donde se leen los datos por defecto."), ("stdout", "canal de salida estándar. Clave: donde se escribe el resultado que se verifica."), ("Leer una línea", "obtener texto hasta el salto de línea. Clave: incluye espacios internos."), ("Eco", "devolver la entrada tal cual (con un prefijo). Clave: el ejemplo mínimo de E/S.")],
    "situacion": "Todo programa de este curso lee de stdin y escribe en stdout; por eso el verificador puede comprobarlos a todos igual. El 'eco' es la forma más simple de ese contrato.",
    "entrada": "una línea de texto",
    "salida": "`eco: <la línea leída>`",
    "formula": "salida = 'eco: ' + entrada",
    "algoritmo": "LEER linea\nESCRIBIR \"eco: \" linea",
    "casos": [("hola", "eco: hola"), ("Polyglot", "eco: Polyglot"), ("123", "eco: 123")],
    "comparacion": [("Sintáctica", "`input()`/`readline` (Python), `readFileSync(0)` (JS), `fgets` (C)."), ("Semántica", "Hay que quitar el salto de línea final para que el eco sea exacto."), ("Paradigmática", "SQL no lee stdin: se muestra el eco sobre una tabla de textos.")],
    "familia": "En Ruby `gets.chomp`. En Haskell `getLine`. En C++ `std::getline(std::cin, s)`. Todos leen una línea y recortan el salto.",
    "errores": [("Dejar el salto de línea pegado", "no recortar el `\\n` final", "usar trim/chomp/TrimSpace antes de imprimir"), ("Leer un token en vez de la línea", "perder el texto tras el primer espacio", "leer la línea completa cuando el dato puede tener espacios")],
    "faq": [("¿stdin y un archivo son distintos?", "Conceptualmente no: stdin es un flujo; puede venir del teclado o redirigido de un archivo."), ("¿Por qué el curso usa stdin/stdout?", "Es el contrato común que permite verificar los 10 lenguajes con los mismos casos.")],
    "reto": "Haz que el eco convierta el texto a mayúsculas y resuélvelo en **PHP** con `strtoupper`.",
    "impls": {
        "python": "import sys\n\nlinea = sys.stdin.readline().rstrip(\"\\n\")\nprint(f\"eco: {linea}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst linea = readFileSync(0, \"utf8\").replace(/\\r?\\n$/, \"\");\nconsole.log(`eco: ${linea}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst linea: string = readFileSync(0, \"utf8\").replace(/\\r?\\n$/, \"\");\nconsole.log(`eco: ${linea}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String linea = br.readLine();\n        System.out.println(\"eco: \" + linea);\n    }\n}\n",
        "csharp": "using System;\n\nstring linea = Console.In.ReadToEnd().TrimEnd('\\r', '\\n');\nConsole.WriteLine($\"eco: {linea}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tline = strings.TrimRight(line, \"\\r\\n\")\n\tfmt.Printf(\"eco: %s\\n\", line)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let linea = s.trim_end_matches(['\\r', '\\n']);\n    println!(\"eco: {linea}\");\n}\n",
        "c": "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char buf[1024];\n    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;\n    buf[strcspn(buf, \"\\r\\n\")] = '\\0';\n    printf(\"eco: %s\\n\", buf);\n    return 0;\n}\n",
        "php": "<?php\n$linea = rtrim(fgets(STDIN), \"\\r\\n\");\necho \"eco: $linea\\n\";\n",
        "sql": "-- SQL no lee stdin: se muestra el eco sobre una tabla de textos.\nWITH lineas(x) AS (VALUES ('hola'), ('Polyglot'), ('123'))\nSELECT printf('eco: %s', x) AS resultado\nFROM lineas;\n",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
