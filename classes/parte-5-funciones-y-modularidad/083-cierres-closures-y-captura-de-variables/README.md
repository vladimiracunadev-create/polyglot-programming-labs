# Clase 083 — Cierres (closures) y captura de variables

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **cierres (closures)**: funciones que capturan y recuerdan variables de su entorno. Un `sumador(base)` devuelve una función que suma `base` a lo que reciba, recordándolo entre llamadas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear un cierre que captura una variable.
2. Reusar el cierre en varias llamadas.
3. Explicar qué significa 'capturar el entorno'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Cierre (closure) | Función que recuerda su entorno |
| 2 | Captura | Recordar variables externas |
| 3 | Función que devuelve función | Fábricas de funciones |
| 4 | Estado encapsulado | El valor capturado persiste |

## 📖 Definiciones y características

- **Cierre** — función que captura variables de su entorno de definición. Clave: las recuerda al ejecutarse después.
- **Captura** — recordar una variable externa dentro del cierre. Clave: por valor o por referencia.
- **Función de orden superior** — la que devuelve o recibe funciones. Clave: fábrica de cierres.
- **Estado capturado** — el valor que el cierre conserva. Clave: como una variable privada.

## 🧩 Situación

`hacer_sumador(10)` devuelve una función que siempre suma 10. Llamarla con 1 da 11; con 2, 12. El cierre 'recuerda' el 10 sin que se lo vuelvas a pasar.

## 🧮 Modelo

- **Entrada** (stdin): un entero `base`
- **Salida** (stdout): `r1=<base+1> r2=<base+2>`
- **Regla:** sumar = λx. base + x ; r1 = sumar(1) ; r2 = sumar(2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `r1=11 r2=12` |
| `0` | `r1=1 r2=2` |
| `100` | `r1=101 r2=102` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER base
sumar <- hacer_sumador(base)   // captura base
ESCRIBIR "r1=" sumar(1) " r2=" sumar(2)
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
| Sintáctica | `lambda`/`=>`/`\|x\|` para el cierre; C usa un puntero a función + parámetro. |
| Semántica | La mayoría captura el entorno; C no tiene cierres (se pasa el dato aparte). |
| Paradigmática | SQL no tiene cierres; se parametriza con valores en la consulta. |

## 🧬 El concepto en la familia

En Ruby los bloques y `lambda` capturan el entorno. En Haskell, la aplicación parcial produce cierres de forma natural.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 083
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capturar por referencia sin querer** → causa: el cierre ve cambios posteriores de la variable → solución: capturar por valor si necesitas fijar el estado
- **Esperar cierres en C** → causa: no existen → solución: pasar el estado como parámetro explícito

## ❓ Preguntas frecuentes

- **¿Cierre o clase?** Un cierre es como un objeto con un solo método y estado privado; a veces más ligero.
- **¿Qué captura, el valor o la variable?** Depende del lenguaje: por valor (copia) o por referencia (enlace vivo).

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 082](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 084 ⏭️](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md)
