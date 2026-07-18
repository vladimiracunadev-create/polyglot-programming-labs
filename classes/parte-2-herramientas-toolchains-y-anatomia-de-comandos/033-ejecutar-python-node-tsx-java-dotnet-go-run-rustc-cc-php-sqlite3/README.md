# Clase 033 — Ejecutar: python, node, tsx, java, dotnet, go run, rustc, cc, php, sqlite3

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender el comando de 'ejecutar un programa' en cada lenguaje del núcleo, y por qué difieren. Unos ejecutan la fuente directamente (python, node, php), otros compilan y corren en un paso (go run), y otros requieren compilar primero (rustc, cc). Es la tabla de referencia que usarás en cada clase.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ejecutar un 'hola mundo' en cada lenguaje del núcleo.
2. Explicar por qué unos comandos son de un paso y otros de dos.
3. Relacionar el comando de ejecución con el modelo (compilado/interpretado).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ejecutar la fuente | Interpretados: python, node, php |
| 2 | Compilar y ejecutar | En un paso (go run) o en dos (rustc, cc) |
| 3 | Bytecode + VM | java, dotnet run |
| 4 | El caso SQL | Se ejecuta dentro de un motor (sqlite3) |

## 📖 Definiciones y características

- **Ejecutar** — poner en marcha un programa. Clave: el comando exacto depende del modelo del lenguaje.
- **Un paso vs. dos pasos** — compilar+correr juntos (go run) o separados (rustc; luego ./main). Clave: dos pasos dan un binario reutilizable.
- **tsx** — ejecutor que compila y corre TypeScript al vuelo. Clave: evita transpilar a mano en desarrollo.
- **sqlite3** — motor de base de datos que ejecuta SQL desde un archivo o la entrada estándar. Clave: cómo 'corre' SQL en el curso.

## 🧩 Situación

Al abrir la clase 041, cada implementación trae su comando de ejecución. Tenerlos memorizados —o a mano— convierte el estudio en algo fluido en vez de una búsqueda constante.

## 🔎 Ejemplo

La tabla de ejecución del núcleo (misma que en cada clase):

```text
Python      python main.py
JavaScript  node main.mjs
TypeScript  pnpm exec tsx main.ts
Java        java Main.java
C#          dotnet run
Go          go run main.go
Rust        rustc main.rs -o main && ./main
C           cc main.c -o main && ./main
PHP         php main.php
SQL         sqlite3 :memory: < main.sql
```

## ✍️ Práctica

Ejecuta el 'hola mundo' de dos lenguajes que tengas instalados. Fíjate cuál da un binario (archivo `main`) y cuál no.

## ⚠️ Errores comunes

- **Buscar un binario tras `python main.py`** → causa: esperar comportamiento de compilado → solución: recordar que los interpretados no generan ejecutable
- **Olvidar el segundo paso en Rust/C** → causa: compilar y no ejecutar → solución: encadenar la ejecución (`&& ./main`) o correrlo aparte

## ❓ Preguntas frecuentes

- **¿`java Main.java` no necesita compilar?** Desde Java 11 puede ejecutar un único archivo fuente directamente; compila en memoria.
- **¿Por qué `go run` y no `go build`?** `run` compila y ejecuta al vuelo; `build` genera el binario para distribuir.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 032](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/032-instalacion-y-gestion-de-versiones-pyenv-nvm-rustup-sdkman-phpenv/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 034 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/034-compilar-y-construir-gcc-clang-cargo-go-build-javac-dotnet-build/README.md)
