# Clase 034 — Compilar y construir: gcc/clang, cargo, go build, javac, dotnet build

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Distinguir 'ejecutar' de 'construir': construir produce un artefacto (binario, jar, dll) listo para distribuir o desplegar, sin ejecutarlo. Cada lenguaje compilado tiene su comando de construcción, y los proyectos reales se apoyan en un sistema de construcción (cargo, gradle, msbuild) que gestiona dependencias y pasos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar ejecutar de construir/compilar a un artefacto.
2. Usar el comando de construcción de cada lenguaje del núcleo.
3. Explicar el papel de un sistema de construcción (build system).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ejecutar vs. construir | Correr ahora vs. producir un artefacto |
| 2 | Compilador directo | gcc/clang, javac, rustc |
| 3 | Sistema de construcción | cargo, go build, dotnet build, gradle |
| 4 | Artefactos | Binarios, .jar, .dll listos para desplegar |

## 📖 Definiciones y características

- **Construir (build)** — producir el artefacto final (ejecutable, librería) a partir del código. Clave: el resultado se distribuye o despliega.
- **Artefacto** — salida de la construcción: binario, .jar, .dll, wheel. Clave: es lo que se entrega, no el código fuente.
- **Sistema de construcción** — herramienta que orquesta compilación y dependencias (cargo, gradle, msbuild). Clave: automatiza builds reproducibles.
- **Compilación separada** — compilar módulos por separado y enlazarlos. Clave: acelera recompilaciones (solo lo que cambió).

## 🧩 Situación

Durante el desarrollo usas `go run`; para desplegar en el servidor usas `go build`, que produce un binario que copias y ejecutas sin necesitar el toolchain. Ejecutar y construir sirven a momentos distintos.

## 🔎 Ejemplo

Comandos de construcción del núcleo:

```text
C:     gcc main.c -o programa
Rust:  cargo build --release      → target/release/programa
Go:    go build -o programa
Java:  javac Main.java            → Main.class
C#:    dotnet build -c Release    → bin/Release/...
```

## ✍️ Práctica

Si tienes Go o Rust, construye un binario y ejecútalo directamente (sin `run`). Observa que ya no necesitas el código fuente para correrlo.

## ⚠️ Errores comunes

- **Desplegar el código fuente en vez del artefacto** → causa: confundir build con run → solución: construir y distribuir el binario/artefacto, no las fuentes
- **Recompilar todo cada vez** → causa: no aprovechar la compilación incremental → solución: dejar que el build system recompile solo lo cambiado

## ❓ Preguntas frecuentes

- **¿Cuál es la diferencia entre debug y release?** Release optimiza y quita información de depuración: más rápido, más difícil de depurar.
- **¿Los interpretados se 'construyen'?** Suelen empaquetarse (wheel, tarball) más que compilarse; el concepto de artefacto sigue aplicando.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 033](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/033-ejecutar-python-node-tsx-java-dotnet-go-run-rustc-cc-php-sqlite3/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 035 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/035-paquetes-y-dependencias-pip-pnpm-cargo-maven-gradle-nuget-go-mod-composer/README.md)
