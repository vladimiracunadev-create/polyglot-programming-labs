# Clase 162 — WebAssembly como objetivo común

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **WebAssembly (Wasm)** como objetivo común: un formato binario portable al que compilan muchos lenguajes (Rust, C, Go) y que corre en el navegador o en runtimes. Es un 'punto de encuentro' entre lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es WebAssembly.
2. Reconocer qué lenguajes compilan a Wasm.
3. Ver Wasm como objetivo común.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | WebAssembly | Binario portable y rápido |
| 2 | Objetivo de compilación | Muchos lenguajes compilan a Wasm |
| 3 | Runtime | Navegador o fuera de él (WASI) |

## 📖 Definiciones y características

- **WebAssembly** — formato binario portable y eficiente, objetivo de compilación de varios lenguajes. Clave: corre en el navegador y en runtimes.
- **Objetivo (target)** — el formato al que compila un lenguaje. Clave: Rust, C, Go pueden apuntar a Wasm.
- **WASI** — interfaz de sistema para Wasm fuera del navegador. Clave: Wasm del lado servidor.

## 🧩 Situación

Un módulo de cálculo escrito en Rust se compila a Wasm y corre en el navegador junto a JavaScript, o en un runtime del servidor. Wasm es el objetivo común que deja a varios lenguajes convivir.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<n²>`
- **Regla:** calcular n al cuadrado (como en un módulo Wasm)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=25` |
| `0` | `resultado=0` |
| `7` | `resultado=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n*n
```

## 🌐 Implementaciones idiomáticas

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`:

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
| Python | `implementaciones/python/main.py` | `python main.py` |
| JavaScript | `implementaciones/javascript/main.mjs` | `node main.mjs` |
| TypeScript | `implementaciones/typescript/main.ts` | `pnpm exec tsx main.ts` |
| Java | `implementaciones/java/Main.java` | `java Main.java` |
| C# | `implementaciones/csharp/Program.cs` | `dotnet run` |
| Go | `implementaciones/go/main.go` | `go run main.go` |
| Rust | `implementaciones/rust/main.rs` | `rustc main.rs -o main && ./main` |
| C | `implementaciones/c/main.c` | `cc main.c -o main && ./main` |
| SQL | `implementaciones/sql/main.sql` | `sqlite3 :memory: < main.sql` |
| PHP | `implementaciones/php/main.php` | `php main.php` |

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El cálculo es idéntico; lo distinto es el objetivo de compilación. |
| Semántica | Wasm ejecuta el mismo cálculo de forma portable y rápida. |
| Paradigmática | SQL corre en su propio motor, no en Wasm. |

## 🧬 El concepto en la familia

Rust, C/C++, Go, C# (Blazor) compilan a WebAssembly; runtimes como Wasmtime lo ejecutan.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 162
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar acceso directo al sistema en Wasm del navegador** → causa: el sandbox lo limita → solución: usar las APIs disponibles (o WASI en servidor)
- **Módulos Wasm enormes** → causa: carga lenta → solución: optimizar el tamaño del binario

## ❓ Preguntas frecuentes

- **¿Wasm reemplaza a JavaScript?** No: lo complementa para cargas de cómputo intensivo.
- **¿Wasm solo en el navegador?** No: con WASI también en el servidor y en la nube.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 161](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 163 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)
