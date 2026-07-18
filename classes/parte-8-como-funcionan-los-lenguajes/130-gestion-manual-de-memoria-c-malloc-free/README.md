# Clase 130 — Gestión manual de memoria (C): malloc/free

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **gestión manual de memoria** de C: reservar con malloc, usar y liberar con free. En los lenguajes con recolector esto es automático; en C es responsabilidad del programador.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reservar y liberar memoria (concepto).
2. Explicar malloc/free.
3. Contrastar con la gestión automática.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | malloc/free | Reservar y liberar a mano |
| 2 | Responsabilidad | Liberar lo que reservas |
| 3 | Fugas y dobles liberaciones | Los peligros |

## 📖 Definiciones y características

- **malloc** — reserva un bloque de memoria en el heap (C). Clave: devuelve un puntero.
- **free** — libera un bloque previamente reservado. Clave: olvidarlo causa fugas.
- **Fuga de memoria** — memoria reservada que nunca se libera. Clave: el programa la va acumulando.

## 🧩 Situación

En C, cada malloc necesita su free; olvidarlo es una fuga, liberar dos veces es un error grave. Los lenguajes con GC hacen esto por ti, a cambio de menos control.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `reservado=<n> suma=<1+...+n>`
- **Regla:** reservar n enteros, llenarlos 1..n, sumar, liberar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `reservado=5 suma=15` |
| `1` | `reservado=1 suma=1` |
| `3` | `reservado=3 suma=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar(n) ; llenar 1..n ; sumar ; liberar
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
| Sintáctica | malloc/free (C); las colecciones automáticas en los demás. |
| Semántica | C libera a mano; GC/ownership liberan por ti. |
| Paradigmática | SQL no expone gestión de memoria. |

## 🧬 El concepto en la familia

C y C++ (con new/delete) gestionan a mano; Rust automatiza vía ownership sin GC; el resto usa GC.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 130
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar free** → causa: fuga de memoria → solución: liberar todo lo reservado
- **Usar tras liberar** → causa: use-after-free → solución: no acceder a memoria ya liberada

## ❓ Preguntas frecuentes

- **¿Por qué gestionar a mano?** Control fino y rendimiento predecible, a cambio de responsabilidad.
- **¿El GC elimina las fugas?** Las de memoria en gran medida, pero no las de otros recursos (archivos, sockets).

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 129](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 131 ⏭️](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md)
