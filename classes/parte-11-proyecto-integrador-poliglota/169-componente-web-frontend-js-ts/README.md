# Clase 169 — Componente web/frontend (JS/TS)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente web/frontend** (JS/TS): la interfaz que el usuario ve. Aquí se simula el renderizado de una lista de n elementos, confirmando que el render fue correcto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular el renderizado de una vista.
2. Explicar el rol del frontend.
3. Reconocer JS/TS como su lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Frontend | La interfaz de usuario |
| 2 | Renderizar | Mostrar datos como UI |
| 3 | Componentes de UI | Piezas visuales |

## 📖 Definiciones y características

- **Componente web** — la interfaz que interactúa con el usuario. Clave: consume la API y muestra datos.
- **Renderizar** — convertir datos en elementos visuales. Clave: lo que el usuario ve.
- **Estado de la UI** — los datos que la interfaz muestra en un momento. Clave: cambia con la interacción.

## 🧩 Situación

El frontend recibe n elementos de la API y los renderiza como una lista. Confirmar que el render fue correcto cierra el flujo. Este componente vive en el navegador, en JavaScript o TypeScript.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de elementos a renderizar)
- **Salida** (stdout): `items=<n> render=ok`
- **Regla:** renderizar n elementos y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `items=3 render=ok` |
| `0` | `items=0 render=ok` |
| `10` | `items=10 render=ok` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; renderizar n items ; confirmar render
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
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | El frontend transforma datos en UI. |
| Paradigmática | SQL no renderiza; provee datos. |

## 🧬 El concepto en la familia

React, Vue, Svelte (JS/TS) y Flutter (Dart) construyen interfaces; el frontend es su terreno.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 169
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquear la UI con cálculo pesado** → causa: interfaz congelada → solución: mover el cómputo a un worker o al backend
- **Renderizar sin manejar el estado vacío** → causa: vista rota con 0 elementos → solución: considerar el caso de lista vacía

## ❓ Preguntas frecuentes

- **¿Frontend en qué lenguaje?** JavaScript/TypeScript en el navegador; Dart con Flutter para móvil.
- **¿Lógica en el frontend o backend?** La presentación en el frontend; la de negocio, en el backend.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 168](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 170 ⏭️](../../parte-11-proyecto-integrador-poliglota/170-componente-de-datos-y-consultas-sql/README.md)
