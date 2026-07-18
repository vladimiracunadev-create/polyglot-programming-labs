# Clase 163 — Incrustar un lenguaje en otro (Lua, Python embebido)

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **incrustar un lenguaje en otro**: motores como Lua o Python se embeben en aplicaciones para permitir scripting sin recompilar. El anfitrión pasa datos al script, este los procesa y devuelve un resultado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Evaluar un script embebido.
2. Explicar el uso de lenguajes de scripting embebidos.
3. Reconocer casos (juegos, plugins).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lenguaje embebido | Un intérprete dentro de la app |
| 2 | Anfitrión y script | Quién ejecuta a quién |
| 3 | Extensibilidad | Cambiar comportamiento sin recompilar |

## 📖 Definiciones y características

- **Lenguaje embebido** — intérprete integrado en una aplicación anfitriona (Lua, Python). Clave: scripting sin recompilar.
- **Anfitrión** — la aplicación que hospeda el intérprete. Clave: expone datos y funciones al script.
- **Script embebido** — código interpretado que corre dentro del anfitrión. Clave: extiende la app.

## 🧩 Situación

Muchos juegos embeben Lua para su lógica; editores embeben Python para plugins. El anfitrión pasa datos al script y recibe el resultado, permitiendo modificar el comportamiento sin recompilar.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los datos que el anfitrión pasa al script)
- **Salida** (stdout): `resultado=<a+b>` (lo que el script calcula)
- **Regla:** el script embebido evalúa a + b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `resultado=7` |
| `10 5` | `resultado=15` |
| `0 0` | `resultado=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
anfitrión pasa a, b ; el script suma ; devuelve el resultado
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
| Sintáctica | El anfitrión invoca al intérprete embebido; aquí se simula la evaluación. |
| Semántica | El script corre en el runtime del lenguaje embebido. |
| Paradigmática | SQL se embebe en apps vía librerías cliente. |

## 🧬 El concepto en la familia

Lua (juegos, Redis, Nginx), Python (Blender, editores), JavaScript (motores V8 embebidos) son los referentes.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 163
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer demasiado al script** → causa: riesgo de seguridad → solución: limitar lo que el script puede tocar (sandbox)
- **No validar la salida del script** → causa: datos inesperados → solución: comprobar lo que devuelve el script

## ❓ Preguntas frecuentes

- **¿Por qué embeber un lenguaje?** Para permitir personalización y plugins sin recompilar la app.
- **¿Lua o Python?** Lua es minúsculo y rápido de embeber; Python, más potente y con más librerías.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 162](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 164 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md)
