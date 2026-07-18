# Clase 132 — RAII, propiedad y préstamos (Rust/C++)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **RAII, propiedad y préstamos** como alternativa al GC. En Rust, un valor tiene un dueño y puede prestarse para leerlo sin copiarlo ni transferir la propiedad; se libera determinísticamente al salir del ámbito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar propiedad y préstamo.
2. Leer un valor prestado sin poseerlo.
3. Contrastar RAII con el GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Propiedad | Un dueño por valor |
| 2 | Préstamo | Usar sin poseer |
| 3 | RAII | Liberar al salir del ámbito |

## 📖 Definiciones y características

- **RAII** — la vida del recurso se ata a la del objeto dueño. Clave: liberación determinista, sin GC.
- **Propiedad** — cada valor tiene un dueño responsable de liberarlo. Clave: base de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.

## 🧩 Situación

Rust libera memoria sin recolector: el dueño la libera al salir del ámbito (RAII) y los préstamos permiten leer sin copiar. El resultado es memoria segura sin pausas de GC.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** prestar n a una función que devuelve 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
prestar n (referencia) a doble(&n) ; ESCRIBIR resultado
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
| Sintáctica | `&valor` (Rust/C++) vs. paso normal en los demás. |
| Semántica | Rust libera determinísticamente sin GC; el préstamo no copia. |
| Paradigmática | SQL no expone propiedad de memoria. |

## 🧬 El concepto en la familia

C++ tiene RAII y referencias; Rust lo lleva más lejos comprobando los préstamos en compilación.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 132
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Prestar y mover a la vez (Rust)** → causa: conflicto de préstamos → solución: elegir prestar o mover, no ambos a la vez
- **Depender del GC donde hay RAII** → causa: esperar pausas donde no las hay → solución: aprovechar la liberación determinista

## ❓ Preguntas frecuentes

- **¿RAII o GC?** RAII da liberación predecible sin pausas; el GC da comodidad. Distintos compromisos.
- **¿Prestar copia el dato?** No: un préstamo es una referencia; no duplica.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 131](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 133 ⏭️](../../parte-8-como-funcionan-los-lenguajes/133-concurrencia-procesos-hilos-y-memoria-compartida/README.md)
