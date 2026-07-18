# Clase 081 — Semántica de movimiento y préstamo (Rust)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **semántica de movimiento y préstamo** de Rust: un valor tiene un dueño; se puede **prestar** (borrow) para leerlo sin copiar, o **mover** (move) transfiriendo la propiedad. Otros lenguajes copian o comparten referencias con GC.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar propiedad, préstamo y movimiento.
2. Leer un valor prestado sin copiarlo.
3. Comparar el modelo de Rust con el de los lenguajes con GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Propiedad (ownership) | Cada valor tiene un dueño |
| 2 | Préstamo (borrow) | Usar sin poseer |
| 3 | Movimiento (move) | Transferir la propiedad |
| 4 | Alternativas | Copia o GC en otros lenguajes |

## 📖 Definiciones y características

- **Propiedad** — cada valor tiene un único dueño responsable de liberarlo. Clave: base de la seguridad de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.
- **Movimiento** — transferir la propiedad a otra variable. Clave: la original deja de ser válida.
- **Copia vs. GC** — otros lenguajes copian o rastrean referencias con recolector. Clave: modelo distinto.

## 🧩 Situación

En Rust, medir la longitud del texto lo **presta** (`&s`); luego imprimirlo lo **mueve**. El compilador garantiza que nadie use un valor movido. Otros lenguajes lo resuelven con GC o copiando.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII)
- **Salida** (stdout): `movido=<palabra> longitud=<len>`
- **Regla:** longitud por préstamo; el texto se muestra tras moverse

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `movido=Ada longitud=3` |
| `Bo` | `movido=Bo longitud=2` |
| `hola` | `movido=hola longitud=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; len <- longitud(prestar w)
mostrar(mover w)
ESCRIBIR "movido=" w " longitud=" len
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
| Sintáctica | `&s` (préstamo) y move implícito en Rust; los demás copian o comparten referencia. |
| Semántica | Rust invalida el valor movido en compilación; con GC el valor sigue vivo mientras se use. |
| Paradigmática | SQL no tiene propiedad de memoria: opera sobre datos. |

## 🧬 El concepto en la familia

C++ tiene semántica de movimiento (`std::move`) y referencias, cercana a Rust pero sin comprobación en compilación. Java/Go/Python usan GC.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 081
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor tras moverlo (Rust)** → causa: el compilador lo rechaza → solución: prestar (`&`) si necesitas seguir usándolo
- **Asumir move en lenguajes con GC** → causa: allí no existe → solución: recordar que el GC mantiene el valor vivo mientras haya referencias

## ❓ Preguntas frecuentes

- **¿Por qué Rust mueve?** Para garantizar un único dueño y liberar memoria sin GC ni errores de uso tras liberar.
- **¿Prestar copia?** No: un préstamo es una referencia; no duplica el dato.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 080](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 082 ⏭️](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md)
