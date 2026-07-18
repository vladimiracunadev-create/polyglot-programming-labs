# Clase 156 — La FFI (Foreign Function Interface): llamar a C desde todos

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **FFI (Foreign Function Interface)**: el mecanismo para llamar a código escrito en otro lenguaje, típicamente C. Casi todos los lenguajes pueden llamar a C, lo que hace de C el 'idioma común' entre lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la FFI.
2. Reconocer por qué C es el puente universal.
3. Llamar a una función 'externa'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | FFI | Llamar a otro lenguaje |
| 2 | C como puente | Casi todos llaman a C |
| 3 | Enlace | Unir con la librería externa |

## 📖 Definiciones y características

- **FFI** — interfaz para llamar a funciones de otro lenguaje. Clave: reutilizar librerías nativas.
- **Función externa** — definida en otro lenguaje (C) y llamada desde el tuyo. Clave: se declara su firma.
- **C como lingua franca** — casi todos los lenguajes exponen una FFI hacia C. Clave: puente universal.

## 🧩 Situación

Python usa librerías numéricas en C, Ruby extensiones en C, la JVM llama a C con JNI. La FFI hacia C conecta ecosistemas; por eso duplicar un número 'en C' se puede invocar desde cualquier lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** llamar a doble(n) 'externo'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
declarar doble (externa) ; ESCRIBIR doble(n)
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
| Sintáctica | ctypes/cffi (Python), extern (Rust/C), JNI (Java). |
| Semántica | La FFI cruza la frontera de lenguaje con una convención de llamada. |
| Paradigmática | SQL llama a funciones definidas por el usuario. |

## 🧬 El concepto en la familia

ctypes (Python), extern "C" (Rust/C++), JNI (Java), cgo (Go): todos hacia C.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 156
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Firmas incompatibles en la FFI** → causa: corrupción o caídas → solución: declarar exactamente los tipos que espera C
- **Ignorar la gestión de memoria a través de la frontera** → causa: fugas o dobles liberaciones → solución: acordar quién libera qué

## ❓ Preguntas frecuentes

- **¿Por qué C?** Su ABI simple y estable lo hace el mínimo común denominador.
- **¿Toda FFI es hacia C?** Mayormente; también hay puentes directos entre algunos lenguajes.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 155](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 157 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md)
