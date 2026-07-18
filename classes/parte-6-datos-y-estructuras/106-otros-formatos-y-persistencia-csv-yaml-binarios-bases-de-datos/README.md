# Clase 106 — Otros formatos y persistencia: CSV, YAML, binarios, bases de datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con **persistencia y formatos tabulares**: CSV (valores separados por comas) es el formato más simple para guardar y compartir datos en tabla. Aquí se serializa una fila y se cuentan sus campos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar valores a una línea CSV.
2. Contar los campos.
3. Reconocer CSV frente a JSON.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CSV | Valores separados por comas |
| 2 | Campo | Cada valor de la fila |
| 3 | Persistencia | Guardar datos en formato de texto |

## 📖 Definiciones y características

- **CSV** — formato tabular: filas de valores separados por comas. Clave: simple y universal.
- **Campo** — cada valor de una fila CSV. Clave: separado por el delimitador.
- **Persistencia** — guardar datos para recuperarlos después. Clave: archivos, bases de datos.

## 🧩 Situación

Exportar a Excel, cargar datos en una base, intercambiar tablas: el CSV es el mínimo común denominador. Una fila `1,2,3` con 3 campos es su unidad.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `csv=<valores separados por coma> campos=<cantidad>`
- **Regla:** csv = unir con coma ; campos = cantidad de valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `csv=1,2,3 campos=3` |
| `5` | `csv=5 campos=1` |
| `10 20` | `csv=10,20 campos=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; csv <- unir con , ; campos <- longitud
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
| Sintáctica | `','.join(...)` (Python), `.join(',')` (JS), bucle (C). |
| Semántica | CSV real necesita escapar comas y comillas; aquí los datos son simples. |
| Paradigmática | SQL exporta/importa CSV con comandos del motor. |

## 🧬 El concepto en la familia

En Ruby `arr.join(',')`. Casi todos tienen una librería CSV que maneja comillas y saltos correctamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 106
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No escapar comas dentro de un campo** → causa: CSV corrupto → solución: usar una librería CSV para datos reales
- **Confundir campos con caracteres** → causa: contar mal → solución: los campos se separan por el delimitador

## ❓ Preguntas frecuentes

- **¿CSV o JSON?** CSV para tablas simples y planas; JSON para datos anidados y estructurados.
- **¿CSV siempre usa comas?** Casi siempre; algunos usan punto y coma o tabuladores según la configuración regional.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 105](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 107 ⏭️](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md)
