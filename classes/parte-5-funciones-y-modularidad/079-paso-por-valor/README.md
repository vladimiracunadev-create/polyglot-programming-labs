# Clase 079 — Paso por valor

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **paso por valor**: la función recibe una copia del argumento, así que modificar el parámetro dentro no afecta a la variable original de quien llama.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el paso por valor con un ejemplo.
2. Predecir que el original no cambia.
3. Reconocer que los primitivos se pasan por valor.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paso por valor | Se pasa una copia |
| 2 | Copia local | Modificarla no afecta fuera |
| 3 | Primitivos | Suelen pasarse por valor |
| 4 | Aislamiento | La función no toca al llamador |

## 📖 Definiciones y características

- **Paso por valor** — la función recibe una copia del argumento. Clave: el original no cambia.
- **Copia** — un duplicado independiente del valor. Clave: vive dentro de la función.
- **Parámetro local** — la variable de la función que contiene la copia. Clave: aislada del exterior.
- **Efecto en el llamador** — aquí, ninguno. Clave: la seguridad del paso por valor.

## 🧩 Situación

Pasas `n` a una función que lo duplica dentro; al volver, `n` sigue igual. La función trabajó con una copia. Entender esto evita esperar cambios que nunca ocurren.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `original=<n> local=<2n>`
- **Regla:** la función duplica una copia; el original permanece

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `original=5 local=10` |
| `3` | `original=3 local=6` |
| `0` | `original=0 local=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
local <- doblar(n)   // dentro trabaja una copia
ESCRIBIR "original=" n " local=" local
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
| Sintáctica | Igual en todos: se llama y se recibe el retorno. |
| Semántica | Los primitivos se copian; el original nunca se altera. |
| Paradigmática | SQL no tiene variables mutables del llamador; todo es expresión. |

## 🧬 El concepto en la familia

En Ruby los enteros son inmutables: se comportan como paso por valor. En Java/Go/C, los primitivos siempre se pasan por valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 079
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que el original cambie** → causa: creer que se pasó por referencia → solución: recordar que los primitivos se copian
- **Modificar el parámetro creyendo que afecta fuera** → causa: no ver el aislamiento → solución: devolver el nuevo valor si quieres usarlo

## ❓ Preguntas frecuentes

- **¿Todo se pasa por valor?** Los primitivos sí; los objetos, la referencia se pasa por valor (siguiente clase).
- **¿Por qué es seguro?** La función no puede alterar por sorpresa las variables del llamador.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 078](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 080 ⏭️](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md)
