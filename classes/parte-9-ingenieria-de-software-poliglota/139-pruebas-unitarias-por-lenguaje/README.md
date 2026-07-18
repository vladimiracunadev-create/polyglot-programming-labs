# Clase 139 — Pruebas unitarias por lenguaje

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una **prueba unitaria**: código que comprueba automáticamente que otro código produce el resultado esperado. Es la base de la calidad y el corazón del verificador de este curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una aserción.
2. Distinguir prueba que pasa de la que falla.
3. Reconocer el runner de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prueba unitaria | Verifica una unidad de código |
| 2 | Aserción | Comprobar el valor esperado |
| 3 | Pasa/falla | Verde o rojo |

## 📖 Definiciones y características

- **Prueba unitaria** — código que verifica una unidad (función) de forma automática. Clave: repetible.
- **Aserción** — comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo.
- **Runner** — herramienta que ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas.

## 🧩 Situación

Antes de confiar en una función, se escribe una prueba: 'sumar(3,4) debe dar 7'. Si un cambio la rompe, la prueba lo detecta al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `test=<pasa|falla>`
- **Regla:** pasa si a + b == esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `test=pasa` |
| `2 2 5` | `test=falla` |
| `10 5 15` | `test=pasa` |

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
| Sintáctica | assert (Python), expect (JS), assertEquals (Java). |
| Semántica | La aserción compara y decide el estado de la prueba. |
| Paradigmática | SQL prueba con consultas de comprobación. |

## 🧬 El concepto en la familia

pytest (Python), JUnit (Java), cargo test (Rust), phpunit (PHP): mismo concepto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 139
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No probar los casos límite** → causa: bugs en los extremos → solución: incluir 0, vacío y negativos
- **Pruebas frágiles** → causa: fallan por cambios irrelevantes → solución: probar el comportamiento, no la implementación

## ❓ Preguntas frecuentes

- **¿Cuántas pruebas?** Al menos una por comportamiento y por caso límite.
- **¿casos.json es una prueba?** Sí: compara la salida real con la esperada.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 138](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 140 ⏭️](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md)
