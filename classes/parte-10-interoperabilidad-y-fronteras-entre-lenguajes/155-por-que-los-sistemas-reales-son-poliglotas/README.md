# Clase 155 — Por qué los sistemas reales son políglotas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **por qué los sistemas reales son políglotas**: cada componente usa el lenguaje que mejor le sirve. Contar los componentes es la medida básica de un sistema hecho de piezas heterogéneas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar los componentes de un sistema.
2. Explicar por qué se combinan lenguajes.
3. Reconocer sistemas políglotas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema políglota | Varios lenguajes, un sistema |
| 2 | Componente | Una pieza con su lenguaje |
| 3 | Elegir por tarea | El mejor lenguaje para cada parte |

## 📖 Definiciones y características

- **Sistema políglota** — software compuesto por partes en distintos lenguajes. Clave: es lo normal en producción.
- **Componente** — pieza con una responsabilidad y su propio lenguaje. Clave: se integra con las demás.
- **Frontera** — el punto donde dos componentes se comunican. Clave: necesita un contrato claro.

## 🧩 Situación

Un producto real puede tener el frontend en TypeScript, el backend en Go, el núcleo numérico en Rust y los datos en SQL. Contar los componentes empieza a describir esa realidad políglota.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<cantidad>`
- **Regla:** contar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3` |
| `app` | `componentes=1` |
| `web api datos cache` | `componentes=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR cantidad
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
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | Cada componente puede estar en otro lenguaje. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Casi todo sistema grande es políglota: se elige el lenguaje por componente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 155
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Un solo lenguaje para todo por dogma** → causa: usar la herramienta equivocada → solución: elegir por la tarea de cada componente
- **Fronteras sin contrato** → causa: integraciones frágiles → solución: definir contratos claros entre componentes

## ❓ Preguntas frecuentes

- **¿Por qué no un solo lenguaje?** Cada uno destaca en cosas distintas; combinarlos aprovecha lo mejor de cada uno.
- **¿No complica el mantenimiento?** Algo, pero contratos claros lo controlan; la ventaja suele compensar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 154](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 156 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md)
