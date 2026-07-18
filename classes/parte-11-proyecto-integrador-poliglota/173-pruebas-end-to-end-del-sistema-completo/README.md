# Clase 173 — Pruebas end-to-end del sistema completo

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Realizar una **prueba end-to-end (e2e)**: ejercitar el sistema completo, de la entrada a la salida, como lo haría un usuario real. Aquí se comprueba que, dadas dos entradas, el sistema devuelve el total esperado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ejecutar una prueba end-to-end.
2. Distinguir e2e de unitaria e integración.
3. Reconocer su valor y su coste.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | End-to-end | El sistema completo |
| 2 | Flujo de usuario | De la entrada a la salida |
| 3 | Pirámide de pruebas | Muchas unitarias, pocas e2e |

## 📖 Definiciones y características

- **Prueba end-to-end** — verifica el sistema completo desde la perspectiva del usuario. Clave: cubre todos los componentes juntos.
- **Flujo** — el recorrido de una acción a través del sistema. Clave: lo que se ejercita en e2e.
- **Pirámide de pruebas** — muchas unitarias, algunas de integración, pocas e2e. Clave: equilibrio coste/valor.

## 🧩 Situación

Tras construir todos los componentes, una prueba e2e comprueba el flujo completo: el usuario introduce datos y obtiene el resultado correcto. Son valiosas pero costosas: se usan con moderación.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `e2e=<pasa|falla>`
- **Regla:** pasa si el sistema (a + b) da el esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `e2e=pasa` |
| `2 2 5` | `e2e=falla` |
| `10 5 15` | `e2e=pasa` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
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
| Sintáctica | Comparación tras ejecutar el flujo. |
| Semántica | Se prueba el sistema completo, no una unidad. |
| Paradigmática | SQL prueba con consultas sobre datos de prueba. |

## 🧬 El concepto en la familia

Cypress, Playwright, Selenium ejecutan pruebas e2e sobre la aplicación real.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 173
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Solo pruebas e2e** → causa: lentas y frágiles → solución: seguir la pirámide: base de unitarias
- **e2e sin datos controlados** → causa: resultados no reproducibles → solución: usar datos de prueba fijos

## ❓ Preguntas frecuentes

- **¿e2e o unitaria?** Unitarias para la base rápida; e2e para verificar el flujo completo, con moderación.
- **¿Por qué son costosas?** Ejercitan todo el sistema: lentas y más frágiles ante cambios.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 172](../../parte-11-proyecto-integrador-poliglota/172-persistencia-y-almacenamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 174 ⏭️](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md)
