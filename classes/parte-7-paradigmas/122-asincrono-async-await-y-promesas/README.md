# Clase 122 — Asíncrono: async/await y promesas

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Asomarse al paradigma **asíncrono**: iniciar una operación que tardará y continuar sin bloquear, esperando su resultado con `async/await`. Aquí una tarea calcula el doble y se espera su valor.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir y esperar una tarea asíncrona.
2. Explicar por qué no bloquea.
3. Reconocer async/await por lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Asíncrono | No bloquear mientras se espera |
| 2 | async/await | Esperar sin bloquear el hilo |
| 3 | Tarea/promesa/future | El resultado que llegará |

## 📖 Definiciones y características

- **Asíncrono** — iniciar algo que tarda y seguir sin bloquear. Clave: eficiente para I/O.
- **async/await** — sintaxis para escribir código asíncrono como si fuera secuencial. Clave: legible.
- **Promesa/Future/Task** — objeto que representa un resultado futuro. Clave: se espera con await.

## 🧩 Situación

Leer de la red, de disco o de una base de datos tarda. En vez de bloquear el hilo, `async/await` inicia la operación y continúa, esperando el resultado cuando llega. Clave en servidores y UI.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** await doble(n) = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `6` | `resultado=12` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
async doble(x): DEVOLVER 2x ; resultado <- await doble(n)
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
| Sintáctica | `async/await` (JS/TS/Python/C#/Rust), goroutines+canales (Go). |
| Semántica | await no bloquea el hilo; libera para otras tareas. |
| Paradigmática | SQL no tiene async a nivel de lenguaje. |

## 🧬 El concepto en la familia

JavaScript popularizó async/await; hoy está en Python, C#, Rust y otros. Go usa goroutines en su lugar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 122
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquear en vez de esperar** → causa: desperdiciar la ventaja asíncrona → solución: usar await, no una espera activa
- **Olvidar await** → causa: obtener la promesa, no el valor → solución: esperar el resultado antes de usarlo

## ❓ Preguntas frecuentes

- **¿Async es paralelismo?** No: es no bloquear mientras se espera; puede usar un solo hilo.
- **¿Y Go?** Usa goroutines y canales en lugar de async/await, con un modelo distinto.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 121](../../parte-7-paradigmas/121-concurrente-hilos-tareas-y-canales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 123 ⏭️](../../parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md)
