# Clase 141 — Depuradores: gdb, lldb, pdb y los de IDE

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar la idea de un **depurador**: avanzar paso a paso viendo cómo evoluciona el estado. La traza de sumas acumuladas (1, 3, 6, …) muestra el valor del acumulador en cada paso, como haría un depurador.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir una traza de estados.
2. Explicar el avance paso a paso.
3. Nombrar los depuradores por runtime.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Traza | Estado en cada paso |
| 2 | Paso a paso | Avanzar controladamente |
| 3 | Punto de ruptura | Pausar para inspeccionar |

## 📖 Definiciones y características

- **Depurador** — herramienta para pausar y avanzar viendo el estado (gdb, pdb). Clave: diagnóstico.
- **Traza** — secuencia de estados por los que pasa el programa. Clave: revela dónde se desvía.
- **Paso a paso (step)** — avanzar una instrucción a la vez. Clave: inspeccionar cada cambio.

## 🧩 Situación

Cuando un resultado sorprende, se avanza paso a paso viendo el acumulador. La traza 1-3-6 muestra la suma acumulada tras cada elemento, como el panel de variables de un depurador.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `traza=<sumas acumuladas 1..n unidas por ->`
- **Regla:** traza[i] = 1 + 2 + ... + i

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `traza=1-3-6` |
| `1` | `traza=1` |
| `4` | `traza=1-3-6-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
acc <- 0 ; PARA i de 1 a n: acc <- acc+i ; emitir acc
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
| Sintáctica | Bucle con acumulador en cada lenguaje. |
| Semántica | La traza expone el estado intermedio. |
| Paradigmática | SQL usa sumas acumuladas con funciones de ventana. |

## 🧬 El concepto en la familia

gdb/lldb, pdb, y los depuradores de la JVM/.NET y los IDE ofrecen este avance paso a paso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 141
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depurar sin observar el estado** → causa: cambios al azar → solución: trazar el acumulador en cada paso
- **Olvidar reiniciar el acumulador** → causa: traza incorrecta → solución: empezar el acumulador en 0

## ❓ Preguntas frecuentes

- **¿print o depurador?** El depurador evita recompilar y permite avanzar paso a paso.
- **¿Qué es un watch?** Una expresión que el depurador reevalúa en cada pausa.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 140](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 142 ⏭️](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md)
