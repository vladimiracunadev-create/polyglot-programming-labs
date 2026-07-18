# Clase 158 — Enlaces (bindings) y wrappers

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **enlaces (bindings) y wrappers**: una capa que adapta una librería nativa a un uso cómodo e idiomático en tu lenguaje. El wrapper traduce entre la frontera y tu código.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Envolver una función con un wrapper.
2. Explicar qué añade un binding.
3. Reconocer bindings comunes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Binding | Puente a una librería nativa |
| 2 | Wrapper | Adapta a un uso idiomático |
| 3 | Adaptación | Traducir entre fronteras |

## 📖 Definiciones y características

- **Binding** — capa que expone una librería de otro lenguaje en el tuyo. Clave: reutilizar sin reescribir.
- **Wrapper** — función que envuelve otra, adaptando su interfaz. Clave: uso más cómodo o seguro.
- **Adaptación** — traducir tipos y convenciones entre la librería nativa y tu código. Clave: ocultar la frontera.

## 🧩 Situación

Una librería de imágenes en C se expone en Python con un binding; el wrapper convierte tipos y hace la API pythónica. Aquí el wrapper duplica y presenta el resultado envuelto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `envuelto=wrap(<2n>)`
- **Regla:** wrapper que aplica doble y formatea

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `envuelto=wrap(10)` |
| `0` | `envuelto=wrap(0)` |
| `7` | `envuelto=wrap(14)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
r <- doble(n) ; ESCRIBIR 'wrap(' + r + ')'
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
| Sintáctica | Una función que envuelve a otra en cada lenguaje. |
| Semántica | El wrapper adapta tipos y convenciones de la frontera. |
| Paradigmática | SQL usa vistas para envolver consultas. |

## 🧬 El concepto en la familia

PyBind11, node-gyp, JNA, cbindgen generan bindings entre lenguajes y C/C++.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 158
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Wrapper que filtra detalles de la frontera** → causa: abstracción con fugas → solución: ocultar la complejidad de la interoperabilidad
- **No manejar errores de la librería nativa** → causa: caídas inesperadas → solución: traducir los errores al modelo de tu lenguaje

## ❓ Preguntas frecuentes

- **¿Binding o reescribir?** El binding reutiliza código probado; reescribir cuesta y arriesga.
- **¿Wrapper añade coste?** Un poco, pero la comodidad y seguridad suelen compensar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 157](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 159 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md)
