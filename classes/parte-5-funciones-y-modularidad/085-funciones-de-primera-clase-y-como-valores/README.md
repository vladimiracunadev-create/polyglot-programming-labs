# Clase 085 — Funciones de primera clase y como valores

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Tratar las funciones como **valores de primera clase**: guardarlas en variables y pasarlas como argumentos. `aplicar(suma, a, b)` ejecuta la función recibida; es la base de map/filter/reduce y de los callbacks.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Pasar una función como argumento.
2. Guardar una función en una variable.
3. Explicar 'valor de primera clase'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Primera clase | Las funciones son valores |
| 2 | Pasar funciones | Como cualquier argumento |
| 3 | Función de orden superior | Recibe otra función |
| 4 | Callbacks | El patrón detrás de eventos |

## 📖 Definiciones y características

- **Valor de primera clase** — algo que se puede guardar, pasar y devolver. Clave: las funciones lo son en casi todos los lenguajes.
- **Función de orden superior** — recibe o devuelve funciones. Clave: `aplicar(f, a, b)`.
- **Callback** — función pasada para ejecutarse después. Clave: base de eventos y asincronía.
- **Puntero a función** — en C, un valor que apunta a una función. Clave: su forma de primera clase.

## 🧩 Situación

`aplicar(suma, 3, 4)` da 7 y `aplicar(producto, 3, 4)` da 12, usando la misma función `aplicar`. Poder pasar la operación como dato es lo que hace posibles map, filter y los callbacks.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b> producto=<a*b>`
- **Regla:** aplicar(f, a, b) = f(a, b); con f = suma y f = producto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7 producto=12` |
| `5 5` | `suma=10 producto=25` |
| `0 9` | `suma=9 producto=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION aplicar(f, a, b): DEVOLVER f(a, b)
ESCRIBIR "suma=" aplicar(suma,a,b) " producto=" aplicar(producto,a,b)
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
| Sintáctica | Pasar `suma` directamente (Python/JS/Go/Rust) vs. puntero a función (C) o interfaz funcional (Java). |
| Semántica | La función es un valor; se invoca con `f(a, b)`. |
| Paradigmática | SQL no pasa funciones; usa operadores/funciones incorporadas. |

## 🧬 El concepto en la familia

En Ruby se pasan `Proc`/bloques o `method(:suma)`. En Haskell pasar funciones es lo más natural del lenguaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 085
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Llamar la función en vez de pasarla** → causa: pasar `suma(a,b)` en lugar de `suma` → solución: pasar el nombre sin paréntesis
- **Firmas incompatibles** → causa: la de orden superior espera otra forma → solución: asegurar que la función pasada encaja con lo esperado

## ❓ Preguntas frecuentes

- **¿Callbacks son esto?** Sí: un callback es una función que pasas para que se ejecute más tarde.
- **¿C tiene funciones de primera clase?** Parcialmente: con punteros a función, aunque sin cierres.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 084](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 086 ⏭️](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md)
