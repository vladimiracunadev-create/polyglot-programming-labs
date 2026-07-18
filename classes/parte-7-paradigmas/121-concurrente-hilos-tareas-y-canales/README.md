# Clase 121 — Concurrente: hilos, tareas y canales

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Asomarse al paradigma **concurrente**: hacer varias cosas a la vez con hilos, tareas o canales. Sumar una lista puede repartirse entre trabajadores; el resultado combinado es la suma total.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la idea de dividir el trabajo.
2. Reconocer hilos, tareas y canales.
3. Combinar resultados parciales.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Concurrencia | Varias cosas a la vez |
| 2 | Dividir y combinar | Repartir el trabajo |
| 3 | Hilos, tareas, canales | Primitivas por lenguaje |

## 📖 Definiciones y características

- **Concurrencia** — estructurar el programa como tareas que progresan a la vez. Clave: aprovecha varios núcleos.
- **Hilo/goroutine** — unidad de ejecución concurrente. Clave: comparte o no memoria según el modelo.
- **Combinar** — reunir los resultados parciales en el final. Clave: la suma total.

## 🧩 Situación

Sumar millones de números, procesar imágenes o atender miles de conexiones: repartir el trabajo entre hilos o tareas aprovecha varios núcleos. El resultado combinado es el mismo, más rápido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma total>`
- **Regla:** repartir la lista, sumar por partes, combinar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma=10` |
| `5` | `suma=5` |
| `10 20 30` | `suma=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
dividir lista ; sumar cada parte (concurrente) ; combinar sumas
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
| Sintáctica | hilos (Java/C#), goroutines+canales (Go), async (Rust), workers (JS). |
| Semántica | El resultado es determinista; el orden de ejecución no. |
| Paradigmática | SQL delega el paralelismo al motor. |

## 🧬 El concepto en la familia

Go (CSP con goroutines/canales) y Erlang/Elixir (actores) son los referentes de la concurrencia segura.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 121
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin sincronizar** → causa: condiciones de carrera → solución: preferir mensajes o sumas parciales independientes
- **Sobre-paralelizar tareas pequeñas** → causa: el coste de coordinar supera la ganancia → solución: paralelizar solo cuando compensa

## ❓ Preguntas frecuentes

- **¿Concurrencia = paralelismo?** No exactamente: concurrencia es estructurar tareas; paralelismo es ejecutarlas a la vez.
- **¿El resultado cambia?** El valor no; el orden de ejecución sí puede variar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 120](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 122 ⏭️](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md)
