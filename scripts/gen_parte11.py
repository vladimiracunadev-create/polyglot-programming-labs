"""Parte 11 — Proyecto integrador políglota (clases 165-176). Cierre del programa."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[165] = {
    "descripcion": "Describir el sistema: contar sus componentes y listar sus nombres.",
    "objetivo": "Arrancar el **proyecto integrador**: un sistema real hecho de componentes en varios lenguajes. El primer paso es inventariar los componentes que lo forman.",
    "resultados": ["Inventariar los componentes de un sistema.", "Nombrar cada pieza.", "Entender el proyecto como suma de componentes."],
    "temas": [("Sistema", "El todo integrado"), ("Componente", "Cada pieza con su lenguaje"), ("Inventario", "Qué partes lo forman")],
    "definiciones": [("Sistema integrador", "producto compuesto por varios componentes que colaboran. Clave: cada uno en su lenguaje idóneo."), ("Componente", "pieza con una responsabilidad. Clave: se integra con las demás."), ("Inventario", "lista de las partes del sistema. Clave: primer paso del diseño.")],
    "situacion": "Antes de construir, se enumeran los componentes: CLI, API, web, datos. Ese inventario define el alcance del proyecto integrador y qué lenguaje usará cada pieza.",
    "entrada": "una línea con nombres de componentes (palabras)",
    "salida": "`componentes=<N> nombres=<unidos por ->`",
    "formula": "contar y listar los componentes",
    "algoritmo": "LEER componentes ; ESCRIBIR conteo y nombres unidos",
    "casos": [("cli api web", "componentes=3 nombres=cli-api-web"), ("app", "componentes=1 nombres=app"), ("web api datos cache", "componentes=4 nombres=web-api-datos-cache")],
    "comparacion": [("Sintáctica", "Contar y unir en cada lenguaje."), ("Semántica", "Cada componente puede estar en otro lenguaje."), ("Paradigmática", "SQL agrega con group_concat.")],
    "familia": "Todo sistema real es un inventario de componentes con responsabilidades y lenguajes propios.",
    "errores": [("Componentes sin responsabilidad clara", "solapamientos", "una responsabilidad por componente"), ("Olvidar un componente", "integración incompleta", "inventariar todas las piezas")],
    "faq": [("¿Cuántos componentes?", "Los que el problema justifique; ni de más ni de menos."), ("¿Por dónde empezar?", "Por el inventario y los contratos entre componentes.")],
    "reto": "Marca cuál componente es el de datos y resuélvelo en **Python**.",
    "impls": {
        "python": "import sys\n\nc = sys.stdin.read().split()\nprint(f\"componentes={len(c)} nombres={'-'.join(c)}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst c = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`componentes=${c.length} nombres=${c.join(\"-\")}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst c: string[] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`componentes=${c.length} nombres=${c.join(\"-\")}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] c = br.readLine().trim().split(\"\\\\s+\");\n        System.out.println(\"componentes=\" + c.length + \" nombres=\" + String.join(\"-\", c));\n    }\n}\n",
        "csharp": "using System;\n\nstring[] c = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nConsole.WriteLine($\"componentes={c.Length} nombres={string.Join(\"-\", c)}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tc := strings.Fields(line)\n\tfmt.Printf(\"componentes=%d nombres=%s\\n\", len(c), strings.Join(c, \"-\"))\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let c: Vec<&str> = s.split_whitespace().collect();\n    println!(\"componentes={} nombres={}\", c.len(), c.join(\"-\"));\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    char t[64];\n    int n = 0;\n    printf(\"componentes=\");\n    char buf[4096] = \"\";\n    while (scanf(\"%63s\", t) == 1) {\n        if (n > 0) { buf[0] = buf[0]; }\n        if (n > 0) snprintf(buf + 0, 0, \"\");\n        n++;\n    }\n    /* segunda pasada no trivial en C: reconstruimos abajo */\n    return 0;\n}\n",
        "php": "<?php\n$c = preg_split('/\\s+/', trim(fgets(STDIN)));\necho \"componentes=\" . count($c) . \" nombres=\" . implode(\"-\", $c) . \"\\n\";\n",
        "sql": "-- SQL cuenta y une los componentes.\nWITH c(nombre) AS (VALUES ('cli'), ('api'), ('web'))\nSELECT printf('componentes=%d nombres=%s', count(*), group_concat(nombre, '-')) AS resultado FROM c;\n",
    },
}

# Corrección de la implementación C de 165 (una sola pasada guardando en un buffer).
S[165]["impls"]["c"] = (
    "#include <stdio.h>\n#include <string.h>\n\n"
    "int main(void) {\n"
    "    char t[64];\n"
    "    char buf[4096];\n"
    "    buf[0] = '\\0';\n"
    "    int n = 0;\n"
    "    while (scanf(\"%63s\", t) == 1) {\n"
    "        if (n > 0) strcat(buf, \"-\");\n"
    "        strcat(buf, t);\n"
    "        n++;\n"
    "    }\n"
    "    printf(\"componentes=%d nombres=%s\\n\", n, buf);\n"
    "    return 0;\n"
    "}\n"
)

S[166] = {
    "descripcion": "Verificar que dos componentes son compatibles en su frontera comparando sus valores de contrato.",
    "objetivo": "Diseñar el sistema definiendo **responsabilidades y contratos entre componentes**. Dos componentes encajan si respetan el mismo contrato en su frontera; aquí se comprueba comparando sus valores.",
    "resultados": ["Comprobar la compatibilidad de un contrato.", "Explicar el papel de los contratos.", "Reconocer fronteras entre componentes."],
    "temas": [("Contrato", "El acuerdo en la frontera"), ("Compatibilidad", "Ambos lados coinciden"), ("Responsabilidad", "Qué hace cada componente")],
    "definiciones": [("Contrato de frontera", "acuerdo de datos y formato entre dos componentes. Clave: permite evolucionar por separado."), ("Compatibilidad", "que emisor y receptor esperan lo mismo. Clave: sin ella, la integración falla."), ("Responsabilidad", "la tarea única de un componente. Clave: define qué expone en el contrato.")],
    "situacion": "El backend produce un formato que el frontend consume. Si ambos respetan el contrato, encajan; si uno cambia sin avisar, se rompen. Comprobar la compatibilidad evita sorpresas en la integración.",
    "entrada": "una línea `a b` (los valores de contrato de cada componente)",
    "salida": "`contrato=<compatible|incompatible>`",
    "formula": "compatible si a == b",
    "algoritmo": "LEER a, b ; compatible <- (a == b)",
    "casos": [("5 5", "contrato=compatible"), ("5 6", "contrato=incompatible"), ("0 0", "contrato=compatible")],
    "comparacion": [("Sintáctica", "Comparación en cada lenguaje."), ("Semántica", "El contrato desacopla los componentes."), ("Paradigmática", "SQL compara valores.")],
    "familia": "Los tests de contrato (Pact) verifican que servicios independientes respetan su frontera.",
    "errores": [("Cambiar el contrato sin versionar", "romper al otro lado", "versionar y evolucionar con compatibilidad"), ("Fronteras implícitas", "malentendidos", "documentar el contrato explícitamente")],
    "faq": [("¿Cómo verificar contratos?", "Con tests de contrato entre el consumidor y el proveedor."), ("¿Contrato o integración total?", "El contrato permite probar cada lado por separado, más barato.")],
    "reto": "Compara dos versiones de contrato y di cuál es más nueva; resuélvelo en **Go**.",
    "impls": {
        "python": "import sys\n\na, b = sys.stdin.readline().split()\nprint(f\"contrato={'compatible' if a == b else 'incompatible'}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`contrato=${a === b ? \"compatible\" : \"incompatible\"}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`contrato=${a === b ? \"compatible\" : \"incompatible\"}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        System.out.println(\"contrato=\" + (p[0].equals(p[1]) ? \"compatible\" : \"incompatible\"));\n    }\n}\n",
        "csharp": "using System;\n\nstring[] p = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nConsole.WriteLine($\"contrato={(p[0] == p[1] ? \"compatible\" : \"incompatible\")}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf := strings.Fields(line)\n\tres := \"incompatible\"\n\tif f[0] == f[1] {\n\t\tres = \"compatible\"\n\t}\n\tfmt.Printf(\"contrato=%s\\n\", res)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let v: Vec<&str> = s.split_whitespace().collect();\n    let res = if v[0] == v[1] { \"compatible\" } else { \"incompatible\" };\n    println!(\"contrato={res}\");\n}\n",
        "c": "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char a[64], b[64];\n    if (scanf(\"%63s %63s\", a, b) != 2) return 1;\n    printf(\"contrato=%s\\n\", strcmp(a, b) == 0 ? \"compatible\" : \"incompatible\");\n    return 0;\n}\n",
        "php": "<?php\n[$a, $b] = preg_split('/\\s+/', trim(fgets(STDIN)));\necho \"contrato=\" . ($a === $b ? \"compatible\" : \"incompatible\") . \"\\n\";\n",
        "sql": "-- SQL compara los valores de contrato.\nWITH t(a, b) AS (VALUES (5, 5))\nSELECT printf('contrato=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;\n",
    },
}

S[167] = {
    "descripcion": "Componente CLI: parsear un comando y contar sus argumentos.",
    "objetivo": "Construir el **componente CLI** del sistema (idóneo para un lenguaje de sistemas): una interfaz de línea de comandos que recibe un comando y argumentos. Aquí se parsea el comando y se cuentan sus argumentos.",
    "resultados": ["Parsear una invocación de CLI.", "Separar comando de argumentos.", "Explicar el rol del componente CLI."],
    "temas": [("CLI", "Interfaz de línea de comandos"), ("Comando y argumentos", "Qué hacer y con qué"), ("Parseo", "Interpretar la invocación")],
    "definiciones": [("Componente CLI", "interfaz por terminal del sistema. Clave: automatizable y componible."), ("Comando", "la acción a ejecutar (el primer token). Clave: selecciona qué hacer."), ("Argumento", "dato que modifica la acción. Clave: se cuentan tras el comando.")],
    "situacion": "La CLI del sistema recibe `run a b`: el comando es `run` y hay 2 argumentos. Parsear bien la invocación es la base de cualquier herramienta de línea de comandos, a menudo escrita en Go o Rust.",
    "entrada": "una línea `comando arg1 arg2 ...` (al menos el comando)",
    "salida": "`comando=<comando> args=<número de argumentos>`",
    "formula": "primer token = comando; resto = argumentos",
    "algoritmo": "LEER tokens ; comando <- tokens[0] ; args <- tokens - 1",
    "casos": [("run a b", "comando=run args=2"), ("build", "comando=build args=0"), ("deploy x y z", "comando=deploy args=3")],
    "comparacion": [("Sintáctica", "Separar el primer token del resto en cada lenguaje."), ("Semántica", "El comando decide la acción; los argumentos, los datos."), ("Paradigmática", "SQL no tiene CLI de argumentos; se consulta.")],
    "familia": "clap (Rust), cobra (Go), argparse (Python), commander (JS) construyen CLIs robustas.",
    "errores": [("No validar los argumentos", "errores al ejecutar", "comprobar cantidad y tipo de argumentos"), ("Mensajes de ayuda ausentes", "CLI difícil de usar", "ofrecer --help y errores claros")],
    "faq": [("¿Qué lenguaje para una CLI?", "Go y Rust por sus binarios únicos y rápidos; Python para scripts."), ("¿Argumentos posicionales o con nombre?", "Nombrados (--flag) para claridad; posicionales para lo esencial.")],
    "reto": "Distingue las opciones (que empiezan por -) de los argumentos y resuélvelo en **Go**.",
    "impls": {
        "python": "import sys\n\nt = sys.stdin.read().split()\nprint(f\"comando={t[0]} args={len(t) - 1}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst t = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`comando=${t[0]} args=${t.length - 1}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst t: string[] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconsole.log(`comando=${t[0]} args=${t.length - 1}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] t = br.readLine().trim().split(\"\\\\s+\");\n        System.out.println(\"comando=\" + t[0] + \" args=\" + (t.length - 1));\n    }\n}\n",
        "csharp": "using System;\n\nstring[] t = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nConsole.WriteLine($\"comando={t[0]} args={t.Length - 1}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tt := strings.Fields(line)\n\tfmt.Printf(\"comando=%s args=%d\\n\", t[0], len(t)-1)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let t: Vec<&str> = s.split_whitespace().collect();\n    println!(\"comando={} args={}\", t[0], t.len() - 1);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    char comando[64], t[64];\n    if (scanf(\"%63s\", comando) != 1) return 1;\n    int args = 0;\n    while (scanf(\"%63s\", t) == 1) args++;\n    printf(\"comando=%s args=%d\\n\", comando, args);\n    return 0;\n}\n",
        "php": "<?php\n$t = preg_split('/\\s+/', trim(fgets(STDIN)));\necho \"comando={$t[0]} args=\" . (count($t) - 1) . \"\\n\";\n",
        "sql": "-- SQL no tiene CLI; se ilustra con valores.\nWITH t(comando, args) AS (VALUES ('run', 2))\nSELECT printf('comando=%s args=%d', comando, args) AS resultado FROM t;\n",
    },
}

S[168] = {
    "descripcion": "Componente de API: responder a una petición con un código 200 y el dato solicitado.",
    "objetivo": "Construir el **componente de API/servicio** (backend): recibe una petición y devuelve una respuesta con un código de estado y datos. Aquí responde 200 (OK) con el dato recibido.",
    "resultados": ["Producir una respuesta de API con estado.", "Explicar el rol del backend.", "Reconocer los códigos de estado."],
    "temas": [("Servicio/API", "Responde peticiones"), ("Código de estado", "200 OK, 404, 500"), ("Respuesta", "Estado + datos")],
    "definiciones": [("Componente de API", "servicio que atiende peticiones y devuelve respuestas. Clave: la lógica del sistema."), ("Código de estado", "número que indica el resultado (200 OK, 404 no encontrado). Clave: comunica el desenlace."), ("Respuesta", "estado más datos que el servicio devuelve. Clave: lo que consume el cliente.")],
    "situacion": "El frontend pide un dato; el backend responde `200` con el dato o un error. El componente de API es el cerebro del sistema, a menudo en Go, Java o C# por su rendimiento y ecosistema.",
    "entrada": "un entero `n` (el dato solicitado)",
    "salida": "`respuesta=200 datos=<n>`",
    "formula": "responder 200 con el dato",
    "algoritmo": "LEER n ; ESCRIBIR estado 200 y datos=n",
    "casos": [("5", "respuesta=200 datos=5"), ("0", "respuesta=200 datos=0"), ("42", "respuesta=200 datos=42")],
    "comparacion": [("Sintáctica", "Formatear la respuesta en cada lenguaje."), ("Semántica", "El código de estado comunica el resultado."), ("Paradigmática", "SQL devuelve filas, no códigos HTTP.")],
    "familia": "Express (JS), Spring (Java), ASP.NET (C#), Gin (Go), FastAPI (Python) construyen APIs.",
    "errores": [("Devolver 200 en un error", "el cliente no detecta el fallo", "usar el código correcto (4xx/5xx)"), ("Respuestas sin formato acordado", "el cliente no las interpreta", "seguir el contrato de la API")],
    "faq": [("¿Qué código para 'no encontrado'?", "404; 200 es OK, 500 es error del servidor."), ("¿Qué lenguaje para el backend?", "Depende: Go/Java/C# por rendimiento; Python por rapidez de desarrollo.")],
    "reto": "Devuelve 404 si n es negativo y resuélvelo en **Go**.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"respuesta=200 datos={n}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`respuesta=200 datos=${n}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`respuesta=200 datos=${n}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(\"respuesta=200 datos=\" + n);\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"respuesta=200 datos={n}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tfmt.Printf(\"respuesta=200 datos=%d\\n\", n)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"respuesta=200 datos={n}\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"respuesta=200 datos=%ld\\n\", n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho \"respuesta=200 datos=$n\\n\";\n",
        "sql": "-- SQL devuelve filas; aqui, la respuesta simulada.\nWITH t(n) AS (VALUES (5))\nSELECT printf('respuesta=200 datos=%d', n) AS resultado FROM t;\n",
    },
}

S[169] = {
    "descripcion": "Componente web/frontend: indicar cuántos elementos se renderizan y confirmar el render.",
    "objetivo": "Construir el **componente web/frontend** (JS/TS): la interfaz que el usuario ve. Aquí se simula el renderizado de una lista de n elementos, confirmando que el render fue correcto.",
    "resultados": ["Simular el renderizado de una vista.", "Explicar el rol del frontend.", "Reconocer JS/TS como su lenguaje."],
    "temas": [("Frontend", "La interfaz de usuario"), ("Renderizar", "Mostrar datos como UI"), ("Componentes de UI", "Piezas visuales")],
    "definiciones": [("Componente web", "la interfaz que interactúa con el usuario. Clave: consume la API y muestra datos."), ("Renderizar", "convertir datos en elementos visuales. Clave: lo que el usuario ve."), ("Estado de la UI", "los datos que la interfaz muestra en un momento. Clave: cambia con la interacción.")],
    "situacion": "El frontend recibe n elementos de la API y los renderiza como una lista. Confirmar que el render fue correcto cierra el flujo. Este componente vive en el navegador, en JavaScript o TypeScript.",
    "entrada": "un entero `n` (número de elementos a renderizar)",
    "salida": "`items=<n> render=ok`",
    "formula": "renderizar n elementos y confirmar",
    "algoritmo": "LEER n ; renderizar n items ; confirmar render",
    "casos": [("3", "items=3 render=ok"), ("0", "items=0 render=ok"), ("10", "items=10 render=ok")],
    "comparacion": [("Sintáctica", "Formatear la salida en cada lenguaje."), ("Semántica", "El frontend transforma datos en UI."), ("Paradigmática", "SQL no renderiza; provee datos.")],
    "familia": "React, Vue, Svelte (JS/TS) y Flutter (Dart) construyen interfaces; el frontend es su terreno.",
    "errores": [("Bloquear la UI con cálculo pesado", "interfaz congelada", "mover el cómputo a un worker o al backend"), ("Renderizar sin manejar el estado vacío", "vista rota con 0 elementos", "considerar el caso de lista vacía")],
    "faq": [("¿Frontend en qué lenguaje?", "JavaScript/TypeScript en el navegador; Dart con Flutter para móvil."), ("¿Lógica en el frontend o backend?", "La presentación en el frontend; la de negocio, en el backend.")],
    "reto": "Renderiza los elementos como una lista con guiones y resuélvelo en **TypeScript**.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"items={n} render=ok\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`items=${n} render=ok`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`items=${n} render=ok`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(\"items=\" + n + \" render=ok\");\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"items={n} render=ok\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tfmt.Printf(\"items=%d render=ok\\n\", n)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"items={n} render=ok\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"items=%ld render=ok\\n\", n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho \"items=$n render=ok\\n\";\n",
        "sql": "-- SQL provee datos; aqui, el render simulado.\nWITH t(n) AS (VALUES (3))\nSELECT printf('items=%d render=ok', n) AS resultado FROM t;\n",
    },
}

S[170] = {
    "descripcion": "Componente de datos: agregar (sumar) los valores de una consulta.",
    "objetivo": "Construir el **componente de datos y consultas** (SQL): la capa de persistencia responde consultas. Aquí agrega (suma) un conjunto de valores, como haría una consulta de agregación.",
    "resultados": ["Agregar un conjunto de datos.", "Explicar el rol de la capa de datos.", "Reconocer SQL como su lenguaje."],
    "temas": [("Capa de datos", "Persistencia y consultas"), ("Agregación", "Resumir muchos en uno"), ("Consulta", "Pedir datos declarativamente")],
    "definiciones": [("Componente de datos", "la capa que almacena y consulta la información. Clave: fuente de verdad del sistema."), ("Agregación", "combinar muchas filas en un valor (SUM, AVG). Clave: resumen de datos."), ("Consulta declarativa", "describir qué datos se quieren, no cómo obtenerlos. Clave: propio de SQL.")],
    "situacion": "El backend pide 'el total de ventas': la capa de datos ejecuta una consulta de agregación (`SELECT SUM(...)`) y devuelve el número. SQL es el lenguaje natural de este componente.",
    "entrada": "una línea con enteros separados por espacio (valores a agregar)",
    "salida": "`total=<suma de los valores>`",
    "formula": "total = suma de los valores",
    "algoritmo": "LEER valores ; total <- suma ; ESCRIBIR total",
    "casos": [("10 20 30", "total=60"), ("5", "total=5"), ("1 2 3 4", "total=10")],
    "comparacion": [("Sintáctica", "Suma en el núcleo; SUM en SQL."), ("Semántica", "La agregación resume el conjunto."), ("Paradigmática", "SQL es declarativo: SELECT SUM(x).")],
    "familia": "Bases de datos relacionales (PostgreSQL, SQLite) y sus consultas SQL dominan este componente.",
    "errores": [("Agregar en el backend lo que la BD hace mejor", "traer todos los datos", "delegar la agregación a la base de datos"), ("Consultas sin índices", "lentitud", "indexar las columnas de filtrado/orden")],
    "faq": [("¿Agregar en la BD o en el backend?", "En la BD: es más eficiente y evita mover datos."), ("¿Por qué SQL para datos?", "Es declarativo y el motor optimiza las consultas.")],
    "reto": "Calcula también el promedio y resuélvelo en **SQL**.",
    "impls": {
        "python": "import sys\n\nnums = [int(x) for x in sys.stdin.read().split()]\nprint(f\"total={sum(nums)}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst nums = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`total=${nums.reduce((a, b) => a + b, 0)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst nums: number[] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`total=${nums.reduce((a, b) => a + b, 0)}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        long total = 0;\n        for (String s : p) total += Integer.parseInt(s);\n        System.out.println(\"total=\" + total);\n    }\n}\n",
        "csharp": "using System;\nusing System.Linq;\n\nlong total = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries)\n    .Sum(x => (long) int.Parse(x));\nConsole.WriteLine($\"total={total}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\ttotal := 0\n\tfor _, s := range strings.Fields(line) {\n\t\tn, _ := strconv.Atoi(s)\n\t\ttotal += n\n\t}\n\tfmt.Printf(\"total=%d\\n\", total)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let total: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();\n    println!(\"total={total}\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long total = 0, x;\n    while (scanf(\"%ld\", &x) == 1) total += x;\n    printf(\"total=%ld\\n\", total);\n    return 0;\n}\n",
        "php": "<?php\n$nums = array_map('intval', preg_split('/\\s+/', trim(fgets(STDIN))));\necho \"total=\" . array_sum($nums) . \"\\n\";\n",
        "sql": "-- SQL: agregacion declarativa con SUM.\nWITH datos(x) AS (VALUES (10), (20), (30))\nSELECT printf('total=%d', sum(x)) AS resultado FROM datos;\n",
    },
}

S[171] = {
    "descripcion": "Componente de automatización: procesar n tareas y confirmar que se completaron.",
    "objetivo": "Construir el **componente de automatización/scripting**: tareas repetitivas que se ejecutan sin intervención (limpieza, despliegue, informes). Aquí se procesan n tareas y se confirma su finalización.",
    "resultados": ["Procesar un lote de tareas.", "Confirmar la finalización.", "Reconocer el rol de la automatización."],
    "temas": [("Automatización", "Tareas sin intervención"), ("Scripting", "Pegamento entre componentes"), ("Lote de tareas", "Procesar en serie")],
    "definiciones": [("Automatización", "ejecutar tareas repetitivas sin intervención humana. Clave: fiabilidad y ahorro de tiempo."), ("Script", "programa que orquesta o automatiza pasos. Clave: pegamento del sistema."), ("Lote", "conjunto de tareas procesadas juntas. Clave: eficiencia.")],
    "situacion": "Un script nocturno procesa las tareas pendientes (limpiar, respaldar, notificar) y confirma su finalización. La automatización, a menudo en Python o Bash, mantiene el sistema funcionando solo.",
    "entrada": "un entero `n` (número de tareas)",
    "salida": "`tareas=<n> estado=completado`",
    "formula": "procesar n tareas y confirmar",
    "algoritmo": "LEER n ; procesar n tareas ; ESCRIBIR completado",
    "casos": [("5", "tareas=5 estado=completado"), ("0", "tareas=0 estado=completado"), ("3", "tareas=3 estado=completado")],
    "comparacion": [("Sintáctica", "Formatear la salida en cada lenguaje."), ("Semántica", "La automatización procesa y confirma."), ("Paradigmática", "SQL automatiza con procedimientos/trabajos.")],
    "familia": "Python y Bash dominan el scripting; herramientas como cron y Airflow orquestan tareas.",
    "errores": [("Automatizar sin registrar", "no saber si falló", "loggear el resultado de cada tarea"), ("Sin manejo de errores", "una tarea rota detiene todo", "aislar fallos y reintentar")],
    "faq": [("¿Qué lenguaje para automatizar?", "Python y Bash por su rapidez de escritura y ubicuidad."), ("¿Automatizar todo?", "Lo repetitivo y propenso a error; lo puntual, a mano.")],
    "reto": "Marca 'con errores' si n es 0 y resuélvelo en **Python**.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"tareas={n} estado=completado\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`tareas=${n} estado=completado`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`tareas=${n} estado=completado`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(\"tareas=\" + n + \" estado=completado\");\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"tareas={n} estado=completado\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tfmt.Printf(\"tareas=%d estado=completado\\n\", n)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"tareas={n} estado=completado\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"tareas=%ld estado=completado\\n\", n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho \"tareas=$n estado=completado\\n\";\n",
        "sql": "-- SQL automatiza con procedimientos/trabajos; aqui, el conteo.\nWITH t(n) AS (VALUES (5))\nSELECT printf('tareas=%d estado=completado', n) AS resultado FROM t;\n",
    },
}

S[172] = {
    "descripcion": "Persistencia: guardar un par clave/valor y confirmar lo almacenado.",
    "objetivo": "Construir la **persistencia y el almacenamiento**: guardar datos para recuperarlos después. Aquí se almacena un par clave/valor y se confirma lo guardado, como haría un almacén clave-valor.",
    "resultados": ["Guardar un par clave/valor.", "Confirmar el almacenamiento.", "Reconocer tipos de almacenamiento."],
    "temas": [("Persistencia", "Sobrevivir al reinicio"), ("Clave/valor", "Almacén simple"), ("Almacenamiento", "Dónde viven los datos")],
    "definiciones": [("Persistencia", "guardar datos de forma duradera (disco, base de datos). Clave: sobreviven al reinicio."), ("Almacén clave-valor", "guarda valores indexados por una clave (Redis, mapas persistentes). Clave: acceso rápido por clave."), ("Durabilidad", "garantía de que lo guardado no se pierde. Clave: propiedad clave del almacenamiento.")],
    "situacion": "El sistema guarda la configuración y el estado: un almacén clave-valor mapea `usuario → sesión`. Persistir bien es lo que permite apagar y volver a encender sin perder datos.",
    "entrada": "una línea `clave valor`",
    "salida": "`guardado=<clave>=<valor>`",
    "formula": "almacenar el par y confirmar",
    "algoritmo": "LEER clave, valor ; guardar ; confirmar clave=valor",
    "casos": [("x 5", "guardado=x=5"), ("nombre ada", "guardado=nombre=ada"), ("n 100", "guardado=n=100")],
    "comparacion": [("Sintáctica", "Un mapa/diccionario en cada lenguaje; una tabla en SQL."), ("Semántica", "La persistencia hace duraderos los datos."), ("Paradigmática", "SQL persiste en tablas con INSERT.")],
    "familia": "Redis (clave-valor), PostgreSQL (relacional), sistemas de archivos: opciones de persistencia según el caso.",
    "errores": [("Guardar sin durabilidad garantizada", "pérdida ante caídas", "usar almacenamiento que confirme la escritura"), ("Claves sin convención", "colisiones y confusión", "definir un esquema de claves claro")],
    "faq": [("¿Clave-valor o relacional?", "Clave-valor para acceso simple y rápido; relacional para datos estructurados y consultas."), ("¿Persistir en disco o memoria?", "Memoria para caché rápida; disco para durabilidad.")],
    "reto": "Recupera el valor tras guardarlo (leer de vuelta) y resuélvelo en **Python**.",
    "impls": {
        "python": "import sys\n\nclave, valor = sys.stdin.readline().split()\nalmacen = {}\nalmacen[clave] = valor\nprint(f\"guardado={clave}={almacen[clave]}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [clave, valor] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconst almacen = new Map();\nalmacen.set(clave, valor);\nconsole.log(`guardado=${clave}=${almacen.get(clave)}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [clave, valor] = readFileSync(0, \"utf8\").trim().split(/\\s+/);\nconst almacen = new Map<string, string>();\nalmacen.set(clave, valor);\nconsole.log(`guardado=${clave}=${almacen.get(clave)}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\nimport java.util.HashMap;\nimport java.util.Map;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        Map<String, String> almacen = new HashMap<>();\n        almacen.put(p[0], p[1]);\n        System.out.println(\"guardado=\" + p[0] + \"=\" + almacen.get(p[0]));\n    }\n}\n",
        "csharp": "using System;\nusing System.Collections.Generic;\n\nstring[] p = Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries);\nvar almacen = new Dictionary<string, string>();\nalmacen[p[0]] = p[1];\nConsole.WriteLine($\"guardado={p[0]}={almacen[p[0]]}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tp := strings.Fields(line)\n\talmacen := map[string]string{}\n\talmacen[p[0]] = p[1]\n\tfmt.Printf(\"guardado=%s=%s\\n\", p[0], almacen[p[0]])\n}\n",
        "rust": "use std::collections::HashMap;\nuse std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let p: Vec<&str> = s.split_whitespace().collect();\n    let mut almacen: HashMap<&str, &str> = HashMap::new();\n    almacen.insert(p[0], p[1]);\n    println!(\"guardado={}={}\", p[0], almacen[p[0]]);\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    char clave[64], valor[64];\n    if (scanf(\"%63s %63s\", clave, valor) != 2) return 1;\n    printf(\"guardado=%s=%s\\n\", clave, valor);\n    return 0;\n}\n",
        "php": "<?php\n[$clave, $valor] = preg_split('/\\s+/', trim(fgets(STDIN)));\n$almacen = [];\n$almacen[$clave] = $valor;\necho \"guardado=$clave={$almacen[$clave]}\\n\";\n",
        "sql": "-- SQL persiste en tablas; aqui, el par guardado.\nWITH t(clave, valor) AS (VALUES ('x', '5'))\nSELECT 'guardado=' || clave || '=' || valor AS resultado FROM t;\n",
    },
}

S[173] = {
    "descripcion": "Prueba end-to-end: verificar que el sistema completo produce el resultado esperado para una entrada.",
    "objetivo": "Realizar una **prueba end-to-end (e2e)**: ejercitar el sistema completo, de la entrada a la salida, como lo haría un usuario real. Aquí se comprueba que, dadas dos entradas, el sistema devuelve el total esperado.",
    "resultados": ["Ejecutar una prueba end-to-end.", "Distinguir e2e de unitaria e integración.", "Reconocer su valor y su coste."],
    "temas": [("End-to-end", "El sistema completo"), ("Flujo de usuario", "De la entrada a la salida"), ("Pirámide de pruebas", "Muchas unitarias, pocas e2e")],
    "definiciones": [("Prueba end-to-end", "verifica el sistema completo desde la perspectiva del usuario. Clave: cubre todos los componentes juntos."), ("Flujo", "el recorrido de una acción a través del sistema. Clave: lo que se ejercita en e2e."), ("Pirámide de pruebas", "muchas unitarias, algunas de integración, pocas e2e. Clave: equilibrio coste/valor.")],
    "situacion": "Tras construir todos los componentes, una prueba e2e comprueba el flujo completo: el usuario introduce datos y obtiene el resultado correcto. Son valiosas pero costosas: se usan con moderación.",
    "entrada": "una línea `a b esperado`",
    "salida": "`e2e=<pasa|falla>`",
    "formula": "pasa si el sistema (a + b) da el esperado",
    "algoritmo": "LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla",
    "casos": [("3 4 7", "e2e=pasa"), ("2 2 5", "e2e=falla"), ("10 5 15", "e2e=pasa")],
    "comparacion": [("Sintáctica", "Comparación tras ejecutar el flujo."), ("Semántica", "Se prueba el sistema completo, no una unidad."), ("Paradigmática", "SQL prueba con consultas sobre datos de prueba.")],
    "familia": "Cypress, Playwright, Selenium ejecutan pruebas e2e sobre la aplicación real.",
    "errores": [("Solo pruebas e2e", "lentas y frágiles", "seguir la pirámide: base de unitarias"), ("e2e sin datos controlados", "resultados no reproducibles", "usar datos de prueba fijos")],
    "faq": [("¿e2e o unitaria?", "Unitarias para la base rápida; e2e para verificar el flujo completo, con moderación."), ("¿Por qué son costosas?", "Ejercitan todo el sistema: lentas y más frágiles ante cambios.")],
    "reto": "Prueba un flujo con tres pasos encadenados y resuélvelo en **Python**.",
    "impls": {
        "python": "import sys\n\na, b, esperado = map(int, sys.stdin.readline().split())\nprint(f\"e2e={'pasa' if a + b == esperado else 'falla'}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b, esperado] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`e2e=${a + b === esperado ? \"pasa\" : \"falla\"}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst [a, b, esperado] = readFileSync(0, \"utf8\").trim().split(/\\s+/).map(Number);\nconsole.log(`e2e=${a + b === esperado ? \"pasa\" : \"falla\"}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String[] p = br.readLine().trim().split(\"\\\\s+\");\n        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), e = Integer.parseInt(p[2]);\n        System.out.println(\"e2e=\" + (a + b == e ? \"pasa\" : \"falla\"));\n    }\n}\n",
        "csharp": "using System;\n\nint[] p = Array.ConvertAll(Console.In.ReadToEnd()\n    .Split(new[] { ' ', '\\t', '\\n', '\\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);\nConsole.WriteLine($\"e2e={(p[0] + p[1] == p[2] ? \"pasa\" : \"falla\")}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tf := strings.Fields(line)\n\ta, _ := strconv.Atoi(f[0])\n\tb, _ := strconv.Atoi(f[1])\n\te, _ := strconv.Atoi(f[2])\n\tres := \"falla\"\n\tif a+b == e {\n\t\tres = \"pasa\"\n\t}\n\tfmt.Printf(\"e2e=%s\\n\", res)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();\n    let res = if v[0] + v[1] == v[2] { \"pasa\" } else { \"falla\" };\n    println!(\"e2e={res}\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long a, b, e;\n    if (scanf(\"%ld %ld %ld\", &a, &b, &e) != 3) return 1;\n    printf(\"e2e=%s\\n\", a + b == e ? \"pasa\" : \"falla\");\n    return 0;\n}\n",
        "php": "<?php\n[$a, $b, $e] = array_map('intval', preg_split('/\\s+/', trim(fgets(STDIN))));\necho \"e2e=\" . ($a + $b === $e ? \"pasa\" : \"falla\") . \"\\n\";\n",
        "sql": "-- SQL prueba con una consulta de comprobacion.\nWITH t(a, b, esperado) AS (VALUES (3, 4, 7))\nSELECT printf('e2e=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;\n",
    },
}

S[174] = {
    "descripcion": "Empaquetar el sistema en una imagen de contenedor etiquetada con su versión.",
    "objetivo": "Realizar el **empaquetado, los contenedores y el despliegue**: meter el sistema y su entorno en una imagen de contenedor reproducible. Aquí se construye el nombre de la imagen a partir de la versión.",
    "resultados": ["Etiquetar una imagen de contenedor.", "Explicar qué resuelve un contenedor.", "Relacionar imagen con despliegue."],
    "temas": [("Contenedor", "Programa + su entorno"), ("Imagen etiquetada", "app:version"), ("Despliegue", "Correr la imagen")],
    "definiciones": [("Contenedor", "empaqueta el programa con su entorno mínimo. Clave: elimina el 'funciona en mi máquina'."), ("Imagen", "plantilla de la que se crean contenedores, etiquetada con una versión. Clave: `app:1.2.3`."), ("Despliegue", "poner en marcha la imagen en un entorno. Clave: reproducible y versionado.")],
    "situacion": "El sistema políglota (frontend, backend, datos) se empaqueta en imágenes de contenedor etiquetadas por versión y se despliega. La imagen lleva el entorno consigo, así corre igual en cualquier lado.",
    "entrada": "una línea con una versión `mayor.menor.parche`",
    "salida": "`imagen=app:<versión>`",
    "formula": "construir el nombre de imagen app:version",
    "algoritmo": "LEER version ; ESCRIBIR 'imagen=app:' + version",
    "casos": [("1.2.3", "imagen=app:1.2.3"), ("0.9.0", "imagen=app:0.9.0"), ("2.1.5", "imagen=app:2.1.5")],
    "comparacion": [("Sintáctica", "Concatenación en cada lenguaje."), ("Semántica", "La etiqueta identifica la versión de la imagen."), ("Paradigmática", "SQL concatena con ||.")],
    "familia": "Docker y OCI empaquetan en imágenes; Kubernetes las despliega y orquesta.",
    "errores": [("Imágenes sin versión (:latest)", "no saber qué corre", "etiquetar con la versión concreta"), ("Imágenes enormes", "despliegues lentos", "usar imágenes base mínimas y multi-stage")],
    "faq": [("¿Contenedor o máquina virtual?", "El contenedor comparte el kernel y es más ligero; empaqueta el entorno, no un SO completo."), ("¿Por qué etiquetar?", "Para saber exactamente qué versión está desplegada y poder revertir.")],
    "reto": "Añade el registro (`registro/app:1.2.3`) y resuélvelo en **Go**.",
    "impls": {
        "python": "import sys\n\nversion = sys.stdin.readline().strip()\nprint(f\"imagen=app:{version}\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst version = readFileSync(0, \"utf8\").trim();\nconsole.log(`imagen=app:${version}`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst version: string = readFileSync(0, \"utf8\").trim();\nconsole.log(`imagen=app:${version}`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        String version = br.readLine().trim();\n        System.out.println(\"imagen=app:\" + version);\n    }\n}\n",
        "csharp": "using System;\n\nstring version = Console.In.ReadToEnd().Trim();\nConsole.WriteLine($\"imagen=app:{version}\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tversion := strings.TrimSpace(line)\n\tfmt.Printf(\"imagen=app:%s\\n\", version)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let version = s.trim();\n    println!(\"imagen=app:{version}\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    char version[64];\n    if (scanf(\"%63s\", version) != 1) return 1;\n    printf(\"imagen=app:%s\\n\", version);\n    return 0;\n}\n",
        "php": "<?php\n$version = trim(fgets(STDIN));\necho \"imagen=app:$version\\n\";\n",
        "sql": "-- SQL concatena el nombre de la imagen.\nWITH t(v) AS (VALUES ('1.2.3'))\nSELECT 'imagen=app:' || v AS resultado FROM t;\n",
    },
}

S[175] = {
    "descripcion": "Documentar el proyecto: informar cuántas secciones tiene la documentación.",
    "objetivo": "Realizar la **documentación y la defensa de las decisiones de lenguaje**: explicar por qué cada componente usa su lenguaje y cómo encajan. Aquí se mide la documentación por su número de secciones.",
    "resultados": ["Medir la cobertura de la documentación.", "Explicar por qué documentar las decisiones.", "Reconocer qué documentar."],
    "temas": [("Documentación", "Explicar el porqué"), ("Defensa de decisiones", "Justificar cada lenguaje"), ("Secciones", "Cobertura del documento")],
    "definiciones": [("Documentación", "explicación escrita del sistema y sus decisiones. Clave: el porqué, no solo el qué."), ("Defensa de decisiones", "justificar por qué cada componente usa su lenguaje. Clave: hace revisables las elecciones."), ("Cobertura", "cuánto del sistema está documentado. Clave: una métrica de calidad.")],
    "situacion": "Al cerrar el proyecto, se documenta: por qué Rust en el núcleo, TypeScript en el frontend, SQL en los datos, y cómo se comunican. Esa defensa razonada es lo que distingue una decisión de ingeniería de un capricho.",
    "entrada": "un entero `n` (número de secciones documentadas)",
    "salida": "`documentado=<n> secciones`",
    "formula": "informar el número de secciones",
    "algoritmo": "LEER n ; ESCRIBIR documentado=n secciones",
    "casos": [("5", "documentado=5 secciones"), ("1", "documentado=1 secciones"), ("8", "documentado=8 secciones")],
    "comparacion": [("Sintáctica", "Formatear la salida en cada lenguaje."), ("Semántica", "La documentación explica el porqué de las decisiones."), ("Paradigmática", "SQL se documenta con comentarios y vistas.")],
    "familia": "Markdown, docstrings, ADR (Architecture Decision Records) documentan sistemas y decisiones.",
    "errores": [("Documentar el qué en vez del porqué", "comentarios redundantes", "explicar las decisiones y sus razones"), ("Documentación desactualizada", "engaña más que ayuda", "mantenerla junto al código")],
    "faq": [("¿Qué documentar?", "Las decisiones y el porqué; el qué suele leerse en el código."), ("¿Qué es un ADR?", "Un registro breve de una decisión de arquitectura y su justificación.")],
    "reto": "Marca 'completa' si hay al menos 5 secciones y resuélvelo en **Python**.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"documentado={n} secciones\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`documentado=${n} secciones`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`documentado=${n} secciones`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(\"documentado=\" + n + \" secciones\");\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"documentado={n} secciones\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tfmt.Printf(\"documentado=%d secciones\\n\", n)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"documentado={n} secciones\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"documentado=%ld secciones\\n\", n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho \"documentado=$n secciones\\n\";\n",
        "sql": "-- SQL se documenta con comentarios; aqui, el conteo.\nWITH t(n) AS (VALUES (5))\nSELECT printf('documentado=%d secciones', n) AS resultado FROM t;\n",
    },
}

S[176] = {
    "descripcion": "Cierre del programa: informar cuántas lecciones se llevan y confirmar que el conocimiento es transferible.",
    "objetivo": "Cerrar el programa con una **retrospectiva y la transferencia a nuevos lenguajes**. Tras 176 clases, la lección central es que el conocimiento de la programación es transferible: lo aprendido se aplica a cualquier lenguaje, incluso a los que aún no conoces.",
    "resultados": ["Cerrar el proyecto con una retrospectiva.", "Afirmar la transferibilidad del conocimiento.", "Mirar hacia el siguiente lenguaje."],
    "temas": [("Retrospectiva", "Qué aprendimos"), ("Transferencia", "Aplicar a lo nuevo"), ("Siguiente lenguaje", "Aprender por familia")],
    "definiciones": [("Retrospectiva", "reflexión sobre lo hecho para mejorar. Clave: cierra el ciclo de aprendizaje."), ("Transferencia", "aplicar lo aprendido a un contexto nuevo. Clave: la tesis del programa."), ("Aprendizaje por familia", "usar el Atlas para leer un lenguaje nuevo por su parentesco. Clave: amplía sin empezar de cero.")],
    "situacion": "Has recorrido pensamiento computacional, el Atlas de familias, toolchains, valores, control, funciones, datos, paradigmas, runtime, ingeniería, interoperabilidad y un proyecto integrador. La lección final: el próximo lenguaje ya no te asusta, porque reconoces sus conceptos.",
    "entrada": "un entero `n` (número de lecciones que te llevas)",
    "salida": "`lecciones=<n> transferible=si`",
    "formula": "informar las lecciones y confirmar la transferibilidad",
    "algoritmo": "LEER n ; ESCRIBIR lecciones=n transferible=si",
    "casos": [("5", "lecciones=5 transferible=si"), ("12", "lecciones=12 transferible=si"), ("1", "lecciones=1 transferible=si")],
    "comparacion": [("Sintáctica", "Una última vez, la misma idea en diez formas."), ("Semántica", "El concepto permanece; la forma cambia."), ("Paradigmática", "Del imperativo al declarativo, todo cabe en la misma tesis.")],
    "familia": "Con el Atlas y estas 176 clases, cualquier lenguaje nuevo se aprende reconociendo su familia y sus deltas.",
    "errores": [("Creer que hay que empezar de cero con cada lenguaje", "desaprovechar lo transferible", "reconocer los conceptos y aprender solo las diferencias"), ("Detener el aprendizaje aquí", "el campo evoluciona", "seguir aplicando el método a lenguajes nuevos")],
    "faq": [("¿Y ahora qué?", "Elige un lenguaje del Atlas que no conozcas y léelo por su familia: comprobarás la transferencia."), ("¿Se acabó el aprendizaje?", "Nunca: el método políglota es una forma de seguir aprendiendo cualquier lenguaje.")],
    "reto": "Elige un lenguaje que no domines, lee su ficha en el Atlas y resuelve la clase 041 en él. Ese es el verdadero cierre del programa.",
    "impls": {
        "python": "import sys\n\nn = int(sys.stdin.readline())\nprint(f\"lecciones={n} transferible=si\")\n",
        "javascript": "import { readFileSync } from \"node:fs\";\n\nconst n = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`lecciones=${n} transferible=si`);\n",
        "typescript": "import { readFileSync } from \"node:fs\";\n\nconst n: number = parseInt(readFileSync(0, \"utf8\").trim(), 10);\nconsole.log(`lecciones=${n} transferible=si`);\n",
        "java": "import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class Main {\n    public static void main(String[] args) throws IOException {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        int n = Integer.parseInt(br.readLine().trim());\n        System.out.println(\"lecciones=\" + n + \" transferible=si\");\n    }\n}\n",
        "csharp": "using System;\n\nint n = int.Parse(Console.In.ReadToEnd().Trim());\nConsole.WriteLine($\"lecciones={n} transferible=si\");\n",
        "go": "package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"os\"\n\t\"strconv\"\n\t\"strings\"\n)\n\nfunc main() {\n\tline, _ := bufio.NewReader(os.Stdin).ReadString('\\n')\n\tn, _ := strconv.Atoi(strings.TrimSpace(line))\n\tfmt.Printf(\"lecciones=%d transferible=si\\n\", n)\n}\n",
        "rust": "use std::io::Read;\n\nfn main() {\n    let mut s = String::new();\n    std::io::stdin().read_to_string(&mut s).unwrap();\n    let n: i64 = s.trim().parse().unwrap();\n    println!(\"lecciones={n} transferible=si\");\n}\n",
        "c": "#include <stdio.h>\n\nint main(void) {\n    long n;\n    if (scanf(\"%ld\", &n) != 1) return 1;\n    printf(\"lecciones=%ld transferible=si\\n\", n);\n    return 0;\n}\n",
        "php": "<?php\n$n = (int) trim(fgets(STDIN));\necho \"lecciones=$n transferible=si\\n\";\n",
        "sql": "-- SQL, la ultima vez: la misma idea, otra forma.\nWITH t(n) AS (VALUES (5))\nSELECT printf('lecciones=%d transferible=si', n) AS resultado FROM t;\n",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
