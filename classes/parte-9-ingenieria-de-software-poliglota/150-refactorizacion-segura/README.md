# Clase 150 — Refactorización segura

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **refactorización segura**: mejorar la estructura interna del código sin cambiar su comportamiento observable, respaldado por pruebas. Cambiar `n*2` por `n+n` es una refactorización que las pruebas confirman equivalente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Refactorizar sin cambiar el resultado.
2. Verificar la equivalencia con una prueba.
3. Explicar por qué las pruebas habilitan refactorizar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Refactorización | Mejorar sin cambiar comportamiento |
| 2 | Comportamiento observable | Lo que se mantiene |
| 3 | Red de pruebas | Habilita el cambio seguro |

## 📖 Definiciones y características

- **Refactorización** — reestructurar el código sin alterar su comportamiento observable. Clave: mejora interna.
- **Comportamiento observable** — lo que el usuario/prueba percibe. Clave: no debe cambiar al refactorizar.
- **Red de seguridad** — las pruebas que confirman que la refactorización no rompió nada. Clave: sin ellas, refactorizar es arriesgado.

## 🧩 Situación

Quieres simplificar una función. Con pruebas que fijan su comportamiento, refactorizas con confianza: si las pruebas siguen verdes, el comportamiento se mantuvo. Aquí `n*2` y `n+n` son equivalentes.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `equivalente=<true|false> resultado=<2n>`
- **Regla:** viejo = n*2 ; nuevo = n+n ; equivalente si coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `equivalente=true resultado=10` |
| `0` | `equivalente=true resultado=0` |
| `7` | `equivalente=true resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
viejo <- n*2 ; nuevo <- n+n ; equivalente <- (viejo==nuevo) ; ESCRIBIR
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
| Sintáctica | Dos expresiones equivalentes en cada lenguaje. |
| Semántica | La refactorización preserva el resultado observable. |
| Paradigmática | SQL refactoriza consultas manteniendo el resultado. |

## 🧬 El concepto en la familia

Todos los IDE ofrecen refactorizaciones automáticas (renombrar, extraer) respaldadas por el análisis.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 150
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Refactorizar sin pruebas** → causa: romper comportamiento sin darte cuenta → solución: asegurar la red de pruebas primero
- **Cambiar comportamiento 'de paso'** → causa: no es refactorizar, es modificar → solución: separar refactorización de cambio funcional

## ❓ Preguntas frecuentes

- **¿Refactorizar cambia el comportamiento?** No: por definición lo preserva; solo mejora la estructura.
- **¿Cuándo refactorizar?** Continuamente, en pequeños pasos, con las pruebas en verde.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 149](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 151 ⏭️](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md)
