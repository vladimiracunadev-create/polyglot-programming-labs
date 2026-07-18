# 🌐 Atlas y genealogía de los lenguajes

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md)

El Atlas es la **segunda capa** del programa. Mientras el **núcleo** (10 lenguajes) se implementa y
se verifica, el Atlas te deja **comprender ~40 lenguajes más por sus características**: su historia,
su familia, su paradigma, su modelo de memoria y con qué software se ejecutan. La tesis:
**aprende el representante, reconoce la familia entera.**

> Este material es **de lectura** (historia, características, toolchain). No se ejecuta en CI. Cada
> ficha se fecha y enlaza a la documentación oficial, porque las versiones y herramientas cambian.

## 🌳 El árbol, en una tabla

| Familia | Representante del núcleo | Primos (se comprenden por características) | Idea que aporta |
|---|---|---|---|
| C / llaves | **C** | C++, Objective-C | Memoria, punteros, sintaxis brace |
| Scripting dinámico | **Python** / **PHP** | Ruby, Perl, Lua, Tcl | Tipado dinámico, rapidez de escritura |
| JavaScript / web | **JavaScript** → **TypeScript** | Dart, ActionScript | Prototipos, asincronía, web |
| JVM | **Java** | Kotlin, Scala, Groovy, Clojure | OO nominal en máquina virtual |
| .NET | **C#** | F#, VB.NET | Multiparadigma sobre el CLR |
| Sistemas | **Go**, **Rust**, **C** | C++, Zig, Nim | Rendimiento y control de memoria |
| Funcional tipada (ML) | — (influye en **Rust**) | Haskell, OCaml, F# | Pureza, tipos algebraicos, inferencia |
| Lisp | — | Scheme, Racket, Clojure, Emacs Lisp | Homoiconicidad, macros |
| Lógica y declarativa | **SQL** | Prolog, Datalog | Describir el qué, no el cómo |
| Concurrente / actor | — (CSP en **Go**) | Erlang, Elixir | Procesos, mensajes, tolerancia a fallos |
| Array / científica | — | APL, J, R, Julia, Fortran, MATLAB | Operar sobre vectores completos |
| Históricos / shell | — | COBOL, Pascal, BASIC, Bash | Contexto histórico y automatización |

## 📇 Fichas de lenguaje

Cada familia tendrá una **ficha** (`atlas/<lenguaje>.md`) con:

- **Historia** — autor, año, motivo, de quién hereda (posición en el árbol).
- **Características** — paradigma, modelo de tipos, modelo de memoria/ejecución.
- **Con qué software se ejecuta** — compilador o intérprete, instalación, "hola mundo", ecosistema.
- **"Si ya sabes X, esto te sonará a…"** — mapa de similitud con su familia.
- **Estado** — vivo / legado / nicho, y dónde se usa hoy.

> Las fichas se construyen junto con la **Parte 1 — Atlas y genealogía de los lenguajes**
> ([clases 015–028](../classes/parte-1-atlas-y-genealogia-de-los-lenguajes/README.md)).

## Por qué esta capa existe

Meter 40 lenguajes con implementación completa multiplicaría el mantenimiento sin multiplicar el
aprendizaje: **muchos son casi el mismo lenguaje con otra piel**. El Atlas captura esa amplitud por
comprensión; el núcleo captura la profundidad por práctica verificada.
