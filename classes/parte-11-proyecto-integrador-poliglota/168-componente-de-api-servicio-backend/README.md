# Clase 168 — Componente de API/servicio (backend)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de API/servicio** (backend): recibe una petición y devuelve una respuesta con un código de estado y datos. Aquí responde 200 (OK) con el dato recibido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir una respuesta de API con estado.
2. Explicar el rol del backend.
3. Reconocer los códigos de estado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Servicio/API | Responde peticiones |
| 2 | Código de estado | 200 OK, 404, 500 |
| 3 | Respuesta | Estado + datos |

## 📖 Definiciones y características

- **Componente de API** — servicio que atiende peticiones y devuelve respuestas. Clave: la lógica del sistema.
- **Código de estado** — número que indica el resultado (200 OK, 404 no encontrado). Clave: comunica el desenlace.
- **Respuesta** — estado más datos que el servicio devuelve. Clave: lo que consume el cliente.

## 🧩 Situación

El frontend pide un dato; el backend responde `200` con el dato o un error. El componente de API es el cerebro del sistema, a menudo en Go, Java o C# por su rendimiento y ecosistema.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (el dato solicitado)
- **Salida** (stdout): `respuesta=200 datos=<n>`
- **Regla:** responder 200 con el dato

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `respuesta=200 datos=5` |
| `0` | `respuesta=200 datos=0` |
| `42` | `respuesta=200 datos=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR estado 200 y datos=n
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
| Sintáctica | Formatear la respuesta en cada lenguaje. |
| Semántica | El código de estado comunica el resultado. |
| Paradigmática | SQL devuelve filas, no códigos HTTP. |

## 🧬 El concepto en la familia

Express (JS), Spring (Java), ASP.NET (C#), Gin (Go), FastAPI (Python) construyen APIs.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 168
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Devolver 200 en un error** → causa: el cliente no detecta el fallo → solución: usar el código correcto (4xx/5xx)
- **Respuestas sin formato acordado** → causa: el cliente no las interpreta → solución: seguir el contrato de la API

## ❓ Preguntas frecuentes

- **¿Qué código para 'no encontrado'?** 404; 200 es OK, 500 es error del servidor.
- **¿Qué lenguaje para el backend?** Depende: Go/Java/C# por rendimiento; Python por rapidez de desarrollo.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 167](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 169 ⏭️](../../parte-11-proyecto-integrador-poliglota/169-componente-web-frontend-js-ts/README.md)
