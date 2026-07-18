# Clase 103 — Propiedad y ciclo de vida de los datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **propiedad y el ciclo de vida** de los datos: cuándo se crea y cuándo se libera un recurso. RAII (Rust/C++), `defer` (Go), `try-with-resources` (Java) y `using` (C#) atan la liberación al ámbito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el ciclo de vida de un recurso.
2. Liberar automáticamente al salir del ámbito.
3. Comparar RAII, defer y GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ciclo de vida | Crear → usar → liberar |
| 2 | RAII | La liberación va atada al ámbito |
| 3 | Liberación automática | defer, using, destructor |

## 📖 Definiciones y características

- **Ciclo de vida** — el tiempo entre que un recurso se crea y se libera. Clave: gestionarlo evita fugas.
- **RAII** — Resource Acquisition Is Initialization: el recurso se libera al destruirse el dueño. Clave: Rust/C++.
- **defer/using** — mecanismos que garantizan la liberación al salir del ámbito. Clave: Go, C#, Java.

## 🧩 Situación

Un archivo abierto debe cerrarse; una conexión, liberarse. RAII y defer garantizan que ocurra aunque haya un error, atando la liberación al fin del ámbito.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (valor del recurso)
- **Salida** (stdout): `valor=<n> estado=liberado`
- **Regla:** crear recurso(n), usarlo, liberarlo al salir

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5 estado=liberado` |
| `0` | `valor=0 estado=liberado` |
| `9` | `valor=9 estado=liberado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; crear recurso ; usar ; liberar al salir del ámbito
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
| Sintáctica | `Drop` (Rust), `defer` (Go), `using`/`try-with-resources` (C#/Java). |
| Semántica | Rust/C++ liberan determinísticamente; Java/Python dependen del GC salvo cierre explícito. |
| Paradigmática | SQL gestiona transacciones (COMMIT/ROLLBACK) como ciclo de vida. |

## 🧬 El concepto en la familia

En C++ el destructor libera al salir del ámbito, como el `Drop` de Rust. En Python, el `with` (context manager).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 103
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No liberar recursos** → causa: fugas de memoria/handles → solución: usar RAII/defer/using para atarlo al ámbito
- **Confiar solo en el GC para recursos no-memoria** → causa: archivos abiertos demasiado tiempo → solución: cerrar explícitamente archivos y conexiones

## ❓ Preguntas frecuentes

- **¿GC libera todo?** Libera memoria, pero no siempre a tiempo ni otros recursos (archivos): ciérralos tú.
- **¿RAII o defer?** RAII ata la liberación al tipo; defer, a la función. Ambos garantizan el cierre.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 102](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 104 ⏭️](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md)
