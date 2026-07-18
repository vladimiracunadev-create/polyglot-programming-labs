# Clase 112 — Interfaces, traits y clases abstractas

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **interfaces / traits / clases abstractas**: un contrato que varios tipos implementan. Distintas figuras exponen `area()` y el programa las usa sin conocer el tipo concreto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un contrato (interfaz) y varias implementaciones.
2. Programar contra la interfaz, no la implementación.
3. Distinguir interfaz de clase abstracta.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interfaz/trait | Un contrato sin implementación |
| 2 | Implementar | Cumplir el contrato |
| 3 | Programar contra la interfaz | Desacoplar del tipo concreto |

## 📖 Definiciones y características

- **Interfaz** — conjunto de métodos que un tipo promete implementar. Clave: contrato sin código.
- **Trait** — el equivalente en Rust; puede llevar métodos por defecto. Clave: composición de comportamiento.
- **Clase abstracta** — clase incompleta que otras extienden. Clave: contrato + estado parcial.

## 🧩 Situación

`Forma` define `area()`; cuadrado y rectángulo lo implementan. El código que dibuja o mide no necesita saber qué figura es: confía en el contrato.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área>`
- **Regla:** cada figura implementa area() a su manera

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 6` | `area=36` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER figura ; f: Forma ; ESCRIBIR f.area()
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
| Sintáctica | `interface` (Java/C#/Go/TS/PHP), `trait` (Rust), duck typing (Python/JS). |
| Semántica | El contrato desacopla el uso del tipo concreto. |
| Paradigmática | SQL usa CASE; no hay interfaces. |

## 🧬 El concepto en la familia

En Kotlin, interfaces con métodos por defecto. En C++, clases abstractas con métodos virtuales puros.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 112
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depender de la implementación concreta** → causa: acoplamiento rígido → solución: programar contra la interfaz
- **Interfaz demasiado grande** → causa: difícil de implementar → solución: preferir interfaces pequeñas y enfocadas

## ❓ Preguntas frecuentes

- **¿Interfaz o clase abstracta?** Interfaz para un contrato puro; abstracta si compartes estado/código parcial.
- **¿Go tiene interfaces?** Sí, y se cumplen implícitamente (structural typing).

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 111](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 113 ⏭️](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md)
