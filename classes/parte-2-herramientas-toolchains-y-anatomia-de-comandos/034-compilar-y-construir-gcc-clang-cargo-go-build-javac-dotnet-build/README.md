# Clase 034 — Compilar y construir: gcc/clang, cargo, go build, javac, dotnet build

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Ejecutar y construir se parecen tanto que es fácil confundirlos, y sin embargo sirven a momentos completamente distintos del ciclo de vida de un programa. *Ejecutar* es correrlo ahora, para ver si funciona. *Construir* (build) es producir un **artefacto** —un binario, un `.jar`, un `.dll`— que se puede distribuir y ejecutar más tarde, en otra máquina, sin volver a tener el código fuente ni el compilador. El objetivo de esta clase es que dejes de mezclar ambas ideas: que sepas cuándo usas `go run` y cuándo `go build`, y que entiendas el papel de los **sistemas de construcción** (cargo, gradle, msbuild) que orquestan la compilación de proyectos reales con muchos archivos y dependencias.

La distinción tiene consecuencias directas en producción. Desplegar código fuente y pedir «que lo compilen allá» traslada la complejidad al usuario y multiplica los puntos de fallo. Construir un artefacto y desplegar *eso* es la práctica profesional: reproducible, versionable y auditable, en línea con la insistencia de *The Pragmatic Programmer* en automatizar la construcción para que sea repetible y no dependa de la memoria de nadie.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar ejecutar de construir/compilar a un artefacto distribuible.
2. Usar el comando de construcción de cada lenguaje compilado del núcleo.
3. Explicar qué es un sistema de construcción y qué problemas resuelve más allá de invocar el compilador.
4. Distinguir builds de depuración (debug) y de publicación (release) y cuándo usar cada uno.

## 🧩 Situación

Durante el desarrollo de un servicio en Go usas `go run` una y otra vez: cambias, corres, verificas. Llega el día de desplegar en el servidor de producción, que no tiene instalado el toolchain de Go ni tu código. Aquí `go run` no sirve: lo que haces es `go build -o servicio`, que produce un binario autónomo; copias ese único archivo al servidor y lo ejecutas. El servidor nunca ve tu código fuente ni necesita el compilador. Esa es la diferencia entre ejecutar y construir en la práctica: durante el desarrollo iteras, para el despliegue produces un artefacto que viaja solo. Confundirlas lleva a instalar toolchains en servidores de producción, algo que ni hace falta ni es buena idea.

## 📖 Del compilador al sistema de construcción

En su forma más básica, construir es invocar el compilador con la flag de salida: `gcc main.c -o programa` produce el ejecutable `programa`. Funciona perfecto para un archivo. Pero un proyecto real tiene decenas de archivos fuente, dependencias externas, distintas configuraciones y pasos previos y posteriores a la compilación. Invocar el compilador a mano para todo eso sería insostenible y propenso a errores. De ahí nacen los **sistemas de construcción**.

Un sistema de construcción hace tres cosas que el compilador solo no hace. Primero, **gestiona dependencias**: sabe qué bibliotecas necesita el proyecto y las trae (se solapa con la clase 035). Segundo, **orquesta la compilación incremental**: recompila solo lo que cambió desde la última vez, apoyándose en las marcas de tiempo de los archivos —la idea que popularizó `make` en Unix y que Kernighan y Pike ya trataban como pieza central del entorno de programación—. Tercero, **estandariza el proceso**: cualquiera del equipo construye con el mismo comando, sin conocer los detalles internos. `cargo build` en Rust, `dotnet build` en C#, `gradle build` en Java y `go build` en Go son esa capa: un comando único que esconde la complejidad y produce un build reproducible.

Otra distinción importante es entre **debug** y **release**. Un build de depuración incluye símbolos e información para el depurador y no optimiza, para que compilar sea rápido y depurar cómodo; es el modo por defecto mientras desarrollas. Un build de *release* activa las optimizaciones del compilador y elimina la información de depuración: el binario es más rápido y más pequeño, pero más difícil de inspeccionar. `cargo build` produce debug; `cargo build --release` produce el binario optimizado que enviarías a producción. La misma dualidad existe en `dotnet build -c Release` y en las flags de optimización de gcc (`-O2`).

## 🔬 Laboratorio guiado: construir en cada lenguaje

Compara el comando de construcción del núcleo y, sobre todo, *dónde* deja el artefacto cada uno:

```bash
cc    main.c   -o programa            # C:    -> ./programa (ejecutable nativo)
rustc main.rs  -o programa            # Rust: compilador directo, un archivo
cargo build                           # Rust: -> target/debug/<nombre> (sistema de build)
cargo build --release                 # Rust: -> target/release/<nombre> (optimizado)
go    build    -o programa main.go    # Go:   -> ./programa (binario autocontenido)
javac Main.java                       # Java: -> Main.class (bytecode, no ejecutable nativo)
dotnet build   -c Release             # C#:   -> bin/Release/.../<proyecto>.dll
```

Fíjate en que el compilador directo (`gcc`, `rustc`, `javac`) deja el artefacto donde tú digas o al lado del fuente, mientras que los sistemas de construcción (`cargo`, `dotnet`) lo colocan en una carpeta convenida (`target/`, `bin/`). Esa convención es deliberada: separa tu código fuente de lo generado, para que puedas borrar lo generado sin miedo y para no versionarlo.

Ahora comprueba con las manos la promesa del artefacto: que corre sin el toolchain ni el fuente. Construye un binario, mueve el fuente fuera de en medio y ejecuta:

```bash
go build -o programa main.go
mkdir _fuentes && mv main.go _fuentes/   # el código ya no está aquí
./programa                               # y sin embargo el binario sigue corriendo
```

Y observa la compilación incremental de un sistema de build: la primera vez compila todo, la segunda casi nada porque nada cambió:

```bash
cargo build          # primera vez: compila el proyecto y sus dependencias (lento)
cargo build          # otra vez sin cambios: "Finished" al instante (no recompila)
touch src/main.rs    # simula un cambio en un archivo
cargo build          # ahora sí recompila, pero solo lo afectado
```

## ✍️ Práctica

Si tienes Go o Rust, construye un binario y verifica que es autónomo: constrúyelo, aparta el código fuente a otra carpeta y ejecuta el binario; comprueba que sigue funcionando sin las fuentes presentes. Después, si usas Rust, construye en modo debug y luego en `--release` y compara el tamaño de ambos binarios con `ls -lh target/debug/` y `ls -lh target/release/`: el de release suele ser distinto por las optimizaciones. Ejecuta `cargo build` dos veces seguidas sin cambiar nada y observa que la segunda no recompila —esa es la compilación incremental en acción—. Anota, para tu lenguaje, cuál es el comando de construcción, dónde deja el artefacto y cómo pedirías un build de release.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Desplegar el código fuente y pedir «que lo compilen» | Confundir build con run. Construye el artefacto y distribuye *ese*, no las fuentes |
| Instalar el toolchain en el servidor de producción | No hace falta si despliegas un binario autocontenido. Construye en CI, despliega el artefacto |
| Recompilar todo el proyecto cada vez | No aprovechar la compilación incremental. Deja que el build system recompile solo lo cambiado |
| El binario va lento en producción | Compilaste en modo debug. Usa `--release` / `-c Release` / `-O2` para el artefacto final |
| Versionar `target/` o `bin/` en git | Son artefactos generados. Añádelos al `.gitignore`; se reconstruyen |

## ❓ Preguntas frecuentes

- **¿Cuál es la diferencia entre debug y release?** El build de release optimiza el código y quita la información de depuración: es más rápido y pequeño, pero difícil de depurar. El de debug es lo contrario: cómodo para desarrollar. Desarrolla en debug, distribuye en release.
- **¿Los lenguajes interpretados se «construyen»?** No compilan a un ejecutable nativo, pero sí se *empaquetan* en artefactos distribuibles (wheels, tarballs), que es la clase 039. El concepto de «producir algo listo para entregar» sigue aplicando.
- **¿`go build` y `cargo build` son compiladores?** No: son sistemas de construcción que *invocan* al compilador (el de Go, `rustc`) y además gestionan dependencias y compilación incremental. El compilador es una pieza de dentro.
- **¿Por qué `cargo` deja todo en `target/`?** Para separar limpiamente lo generado del código fuente. Puedes borrar `target/` entero (`cargo clean`) y reconstruir; nunca pierdes nada que no se pueda regenerar.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre `make` y la construcción automatizada.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre automatizar la construcción para que sea reproducible.

---

> [⏮️ Clase 033](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/033-ejecutar-python-node-tsx-java-dotnet-go-run-rustc-cc-php-sqlite3/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 035 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/035-paquetes-y-dependencias-pip-pnpm-cargo-maven-gradle-nuget-go-mod-composer/README.md)
