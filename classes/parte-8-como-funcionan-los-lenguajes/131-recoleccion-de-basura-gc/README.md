# Clase 131 — Recolección de basura (GC)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **recolección de basura (GC)**: el runtime libera automáticamente la memoria de los objetos que ya no son alcanzables. El programador no llama a free; el GC lo hace.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la recolección de basura.
2. Reconocer objetos inalcanzables.
3. Contrastar GC con gestión manual.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Recolector de basura | Libera lo inalcanzable |
| 2 | Alcanzabilidad | Si algo aún se puede usar |
| 3 | Pausas del GC | Coste del automatismo |

## 📖 Definiciones y características

- **Recolección de basura** — liberación automática de objetos ya inalcanzables. Clave: sin free manual.
- **Alcanzable** — objeto accesible desde una variable viva. Clave: lo inalcanzable es basura.
- **Pausa del GC** — momento en que el recolector trabaja. Clave: puede introducir latencia.

## 🧩 Situación

En Java, Python o Go creas objetos y los olvidas: el GC recupera su memoria cuando ya nadie los referencia. Cómodo, pero introduce pausas impredecibles.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de objetos temporales)
- **Salida** (stdout): `creados=<n> estado=recolectado`
- **Regla:** crear n objetos temporales; al perder la referencia, se recolectan

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `creados=5 estado=recolectado` |
| `0` | `creados=0 estado=recolectado` |
| `3` | `creados=3 estado=recolectado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
crear n objetos ; descartar referencias ; el GC recolecta
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
| Sintáctica | No hay free: se crean objetos y se olvidan. |
| Semántica | GC (Java/Python/Go) vs. ownership (Rust) vs. manual (C). |
| Paradigmática | SQL no expone memoria. |

## 🧬 El concepto en la familia

Java, C#, Go, Python, JS usan GC. Rust evita el GC con ownership; C es manual.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 131
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en el GC para recursos no-memoria** → causa: archivos/sockets sin cerrar → solución: cerrar explícitamente esos recursos
- **Retener referencias sin querer** → causa: fuga lógica: el GC no libera lo aún referenciado → solución: soltar las referencias que ya no usas

## ❓ Preguntas frecuentes

- **¿El GC elimina toda fuga?** Las de memoria en su mayoría; no las lógicas (referencias retenidas) ni otros recursos.
- **¿GC o sin GC?** GC da comodidad; sin GC (Rust/C) da control y latencia predecible.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 130](../../parte-8-como-funcionan-los-lenguajes/130-gestion-manual-de-memoria-c-malloc-free/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 132 ⏭️](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md)
