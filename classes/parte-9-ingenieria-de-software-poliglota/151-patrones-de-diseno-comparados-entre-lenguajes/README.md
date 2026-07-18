# Clase 151 — Patrones de diseño comparados entre lenguajes

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar los **patrones de diseño comparados**: el patrón **Estrategia** encapsula algoritmos intercambiables tras una interfaz común. Elegir la operación por su nombre selecciona la estrategia a aplicar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Aplicar el patrón Estrategia.
2. Seleccionar un algoritmo en ejecución.
3. Reconocer patrones en cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Patrón de diseño | Solución reutilizable a un problema común |
| 2 | Estrategia | Algoritmos intercambiables |
| 3 | Selección en ejecución | Elegir el comportamiento al vuelo |

## 📖 Definiciones y características

- **Patrón de diseño** — solución probada y reutilizable a un problema de diseño recurrente. Clave: vocabulario común.
- **Estrategia** — patrón que encapsula algoritmos intercambiables tras una interfaz. Clave: cambiar el comportamiento sin condicionales dispersos.
- **Despacho** — seleccionar qué código ejecutar según un valor. Clave: aquí, por el nombre de la operación.

## 🧩 Situación

Un sistema de cobro puede usar distintas estrategias (tarjeta, transferencia). El patrón Estrategia las hace intercambiables. Aquí, la operación se elige por su nombre y se aplica.

## 🧮 Modelo

- **Entrada** (stdin): una línea `estrategia a b` (estrategia ∈ {suma, resta, producto})
- **Salida** (stdout): `resultado=<a estrategia b>`
- **Regla:** aplicar la estrategia elegida a a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `suma 3 4` | `resultado=7` |
| `resta 10 3` | `resultado=7` |
| `producto 5 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER estrategia, a, b ; seleccionar operación ; aplicar
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
| Sintáctica | map de funciones, interfaz o switch en cada lenguaje. |
| Semántica | La estrategia se elige en ejecución. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

Estrategia, Observer, Factory, Singleton son patrones clásicos (GoF) presentes en todos los lenguajes OO.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 151
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Condicionales gigantes en vez de estrategias** → causa: código rígido → solución: encapsular cada algoritmo tras una interfaz común
- **Sobre-aplicar patrones** → causa: complejidad innecesaria → solución: usar el patrón solo cuando aporta

## ❓ Preguntas frecuentes

- **¿Estrategia o if/else?** Estrategia cuando los algoritmos cambian o crecen; if/else para casos simples y fijos.
- **¿Los patrones son obligatorios?** No: son herramientas; aplícalos cuando resuelven un problema real.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 150](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 152 ⏭️](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md)
