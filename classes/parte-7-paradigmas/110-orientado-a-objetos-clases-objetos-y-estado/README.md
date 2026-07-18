# Clase 110 — Orientado a objetos: clases, objetos y estado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **orientado a objetos**: agrupar estado (datos) y comportamiento (métodos) en objetos. Un contador con su método `incrementar` es el ejemplo mínimo de estado encapsulado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una clase con estado y métodos.
2. Crear un objeto y cambiar su estado.
3. Reconocer la unión de datos y comportamiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Clase y objeto | Molde e instancia |
| 2 | Estado | Datos del objeto |
| 3 | Método | Comportamiento que actúa sobre el estado |

## 📖 Definiciones y características

- **Objeto** — instancia que agrupa estado y comportamiento. Clave: datos + métodos juntos.
- **Clase** — molde que define objetos. Clave: describe estado y métodos.
- **Método** — función asociada a un objeto que opera sobre su estado. Clave: `contador.incrementar()`.

## 🧩 Situación

Un carrito de compra, una cuenta, un contador: la OO modela entidades con estado que evoluciona mediante métodos. El objeto recuerda su estado entre llamadas.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** contador incrementado n veces desde 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
c <- Contador() ; REPETIR n veces: c.incrementar() ; ESCRIBIR c.cuenta
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
| Sintáctica | `class` (Python/Java/C#/PHP), `struct`+métodos (Go/Rust), objeto (JS). |
| Semántica | El objeto conserva su estado entre llamadas a métodos. |
| Paradigmática | SQL no tiene objetos con estado; opera sobre datos. |

## 🧬 El concepto en la familia

En Ruby todo es un objeto. En Go/Rust no hay clases, pero structs con métodos cumplen el rol.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 110
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin control** → causa: objetos que se pisan → solución: encapsular el estado en cada objeto
- **Confundir clase con objeto** → causa: molde vs. instancia → solución: la clase define; el objeto existe

## ❓ Preguntas frecuentes

- **¿Todo debe ser objeto?** No: la OO es una herramienta; a veces una función basta.
- **¿Go tiene clases?** No, pero structs con métodos ofrecen lo esencial de la OO.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 109](../../parte-7-paradigmas/109-procedimental-y-modular/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 111 ⏭️](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md)
