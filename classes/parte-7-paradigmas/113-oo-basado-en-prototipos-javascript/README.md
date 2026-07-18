# Clase 113 — OO basado en prototipos (JavaScript)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer la **OO basada en prototipos** de JavaScript: los objetos heredan directamente de otros objetos, no de clases. Aquí un objeto con un método `doble` calcula sobre su valor.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear un objeto con estado y método.
2. Explicar la herencia por prototipos.
3. Contrastar prototipos con clases.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prototipos | Objetos que heredan de objetos |
| 2 | Método en objeto | Comportamiento ligado al valor |
| 3 | Clases vs. prototipos | Dos modelos de OO |

## 📖 Definiciones y características

- **Prototipo** — objeto del que otro hereda propiedades y métodos. Clave: cadena de prototipos en JS.
- **Objeto literal** — objeto creado directamente con sus campos y métodos. Clave: `{ v: n, doble() {...} }`.
- **this** — referencia al objeto sobre el que se llama el método. Clave: accede a su estado.

## 🧩 Situación

JavaScript no tenía clases originalmente: los objetos heredaban de otros objetos (prototipos). Aunque hoy tiene `class`, por debajo sigue siendo prototipos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** objeto.doble() = valor·2

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
obj <- { valor: n, doble() { DEVOLVER valor*2 } } ; ESCRIBIR obj.doble()
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
| Sintáctica | Objeto literal con método (JS) vs. clase (otros). |
| Semántica | JS hereda por prototipos; los demás por clases. |
| Paradigmática | SQL no tiene objetos. |

## 🧬 El concepto en la familia

Self y Lua también usan prototipos. En los demás lenguajes del núcleo se modela con una clase o struct.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 113
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder el `this` en JS** → causa: el método pierde su contexto → solución: cuidar cómo se invoca el método
- **Creer que JS no es OO** → causa: lo es, por prototipos → solución: entender el modelo de prototipos

## ❓ Preguntas frecuentes

- **¿Prototipos o clases en JS?** Las clases de JS son azúcar sobre prototipos; por debajo es lo mismo.
- **¿Qué lenguajes usan prototipos?** JavaScript, Self, Lua; la mayoría usa clases.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 112](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 114 ⏭️](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md)
