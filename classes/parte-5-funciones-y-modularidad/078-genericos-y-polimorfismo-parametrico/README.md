# Clase 078 — Genéricos y polimorfismo paramétrico

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una función **genérica**: la misma lógica para varios tipos, sin duplicar código. `max<T>` funciona con enteros, reales o texto porque solo exige que el tipo sea comparable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función genérica con un parámetro de tipo.
2. Explicar el polimorfismo paramétrico.
3. Reconocer las restricciones (comparable) de los genéricos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Genérico | Un tipo como parámetro |
| 2 | Polimorfismo paramétrico | Misma lógica, varios tipos |
| 3 | Restricciones | El tipo debe cumplir algo (comparable) |
| 4 | Sin duplicar | Una función en vez de N |

## 📖 Definiciones y características

- **Genérico** — función/tipo parametrizado por otro tipo (`max<T>`). Clave: reutilización con seguridad de tipos.
- **Polimorfismo paramétrico** — un código que funciona para muchos tipos. Clave: distinto del de herencia.
- **Restricción de tipo** — condición sobre el parámetro de tipo (comparable). Clave: habilita las operaciones.
- **Inferencia de tipo genérico** — el compilador deduce T al llamar. Clave: no hay que anotarlo.

## 🧩 Situación

Sin genéricos habría un `maxInt`, un `maxDouble`, un `maxString`... Con `max<T: Comparable>` se escribe una vez y sirve para todos, sin perder la comprobación de tipos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max<T>(a, b) = a si a>b, si no b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION max<T comparable>(a,b): DEVOLVER a SI a>b SINO b
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
| Sintáctica | `<T>` (Java/C#/Rust), `[T any]` (Go), sin anotación (Python dinámico). |
| Semántica | Estáticos comprueban T al compilar; Python confía en pato (duck typing). |
| Paradigmática | SQL usa `max()` polimórfico incorporado. |

## 🧬 El concepto en la familia

En Kotlin `fun <T: Comparable<T>> maxOf`. En Haskell la firma `Ord a => a -> a -> a` expresa la restricción.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 078
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar Object en vez de genéricos (Java viejo)** → causa: perder la seguridad de tipos → solución: usar genéricos con restricción Comparable
- **Olvidar la restricción comparable** → causa: el tipo no soporta `>` → solución: acotar T a un tipo comparable

## ❓ Preguntas frecuentes

- **¿Genéricos o sobrecarga?** Genéricos evitan duplicar; sobrecarga es para comportamientos distintos por tipo.
- **¿Python tiene genéricos?** Su tipado dinámico ya es 'genérico'; con anotaciones existen `TypeVar` para herramientas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 077](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 079 ⏭️](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md)
