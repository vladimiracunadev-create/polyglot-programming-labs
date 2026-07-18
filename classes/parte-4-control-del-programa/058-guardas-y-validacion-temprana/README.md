# Clase 058 — Guardas y validación temprana

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aplicar **guardas** (validación temprana): comprobar primero los casos inválidos o especiales y salir cuanto antes, dejando el camino principal limpio. Reduce el anidamiento y hace el código más legible.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir guardas que validan y salen temprano.
2. Evitar el anidamiento profundo de if.
3. Ordenar las comprobaciones de más restrictiva a menos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación temprana | Comprobar lo inválido primero |
| 2 | Guarda | Un if que corta el flujo pronto |
| 3 | Retorno temprano | Salir en cuanto se decide |
| 4 | Legibilidad | Menos anidamiento, más claridad |

## 📖 Definiciones y características

- **Guarda** — condición al inicio que corta el flujo si no se cumple. Clave: evita anidar.
- **Validación temprana** — rechazar entradas inválidas antes del cálculo. Clave: el camino feliz queda limpio.
- **Retorno temprano** — salir de la función en cuanto hay respuesta. Clave: menos ramas abiertas.
- **Camino feliz** — el flujo principal sin errores. Clave: se lee de corrido tras las guardas.

## 🧩 Situación

Con guardas, `if edad < 0: return invalido` al principio evita envolver todo el resto en un `else`. El código baja en escalera en vez de anidarse hacia la derecha.

## 🧮 Modelo

- **Entrada** (stdin): un entero `edad`
- **Salida** (stdout): `invalido` si edad<0, `menor` si edad<18, `adulto` en otro caso
- **Regla:** guardas: edad<0 → invalido; edad<18 → menor; si no → adulto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `invalido` |
| `10` | `menor` |
| `20` | `adulto` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER edad
SI edad < 0: ESCRIBIR "invalido" ; FIN
SI edad < 18: ESCRIBIR "menor" ; FIN
ESCRIBIR "adulto"
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
| Sintáctica | `if ...: return` (Python) vs. `if (...) { return; }` (C/Java). |
| Semántica | El orden de las guardas define la clasificación; cambiarlo cambia el resultado. |
| Paradigmática | SQL encadena condiciones con CASE WHEN en orden. |

## 🧬 El concepto en la familia

En Ruby `return 'invalido' if edad < 0`. En Go es común la guarda con `if ...{ return }` al inicio de la función.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 058
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar en vez de usar guardas** → causa: escalera de if/else hacia la derecha → solución: sacar los casos especiales como guardas al inicio
- **Ordenar mal las guardas** → causa: clasificar mal por comprobar tarde → solución: ir de la condición más restrictiva a la más general

## ❓ Preguntas frecuentes

- **¿Guarda o if/else anidado?** La guarda suele ser más legible: aplana el código y deja claro el camino feliz.
- **¿Varios return son mala práctica?** No con guardas: hacen el flujo más claro, no más confuso.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 057](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 059 ⏭️](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md)
