# Clase 044 — Enteros: tamaño, signo, desbordamiento y bases

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender que un entero es un valor único que puede **representarse** en varias bases. La conversión revela diferencias reales: casi todos tienen formateo de hex/octal/binario, pero **C carece de especificador para binario** (hay que construirlo) y SQL solo formatea hex.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar un mismo entero en decimal, hexadecimal, octal y binario.
2. Usar el formateo de bases de cada lenguaje.
3. Explicar por qué C no tiene `%b` y cómo se resuelve.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Valor vs. representación | El número es uno; las bases son formas de escribirlo |
| 2 | Hex, octal, binario | Bases 16, 8 y 2, comunes en programación |
| 3 | Formateo por lenguaje | Especificadores y funciones de conversión |
| 4 | El hueco de C | No hay `%b`: el binario se construye a mano |

## 📖 Definiciones y características

- **Base numérica** — sistema para escribir un número (10, 16, 8, 2). Clave: cambia la representación, no el valor.
- **Hexadecimal** — base 16 (0-9, a-f). Clave: compacta y común en memoria/colores.
- **Octal** — base 8. Clave: usada en permisos de archivos Unix.
- **Binario** — base 2 (0 y 1). Clave: la representación real en la máquina.

## 🧩 Situación

El color `#ff0000` es rojo: `ff` es 255 en hexadecimal. Convertir entre bases es cotidiano en programación de bajo nivel, gráficos y permisos. Cada lenguaje lo formatea a su manera, y C obliga a construir el binario.

## 🧮 Modelo

- **Entrada** (stdin): una línea `n` (entero no negativo)
- **Salida** (stdout): `dec=<n> hex=<hex minúscula> oct=<octal> bin=<binario>`
- **Regla:** misma n en base 10, 16, 8 y 2 (sin prefijos ni ceros a la izquierda)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `255` | `dec=255 hex=ff oct=377 bin=11111111` |
| `10` | `dec=10 hex=a oct=12 bin=1010` |
| `1` | `dec=1 hex=1 oct=1 bin=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR "dec=" n " hex=" BASE(n,16) " oct=" BASE(n,8) " bin=" BASE(n,2)
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
| Sintáctica | `f"{n:x}"` (Python), `n.toString(16)` (JS), `%x/%o/%b` (Go/Rust). |
| Semántica | C **no** tiene `%b`: el binario se genera con un bucle sobre los bits. |
| Paradigmática | SQL (sqlite) solo formatea hex con `%x`; octal y binario no son nativos. |

## 🧬 El concepto en la familia

En Ruby: `n.to_s(16)`, `to_s(8)`, `to_s(2)`. En C++ se usa `std::hex`/`std::oct` con streams, pero el binario también requiere ayuda (`std::bitset`).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 044
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Buscar `%b` en C** → causa: asumir que existe como en Go/Rust → solución: construir el binario con un bucle de desplazamientos
- **Obtener hex en mayúscula** → causa: usar `%X` en vez de `%x` → solución: elegir el especificador de minúsculas que pide el contrato

## ❓ Preguntas frecuentes

- **¿Por qué C no tiene binario en printf?** El estándar nunca lo incluyó; hex y octal sí. Se implementa a mano fácilmente.
- **¿El valor cambia entre bases?** No: `255`, `ff`, `377` y `11111111` son el mismo número escrito distinto.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 043](../../parte-3-valores-tipos-y-variables/043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 045 ⏭️](../../parte-3-valores-tipos-y-variables/045-numeros-reales-punto-flotante-precision-y-decimales/README.md)
