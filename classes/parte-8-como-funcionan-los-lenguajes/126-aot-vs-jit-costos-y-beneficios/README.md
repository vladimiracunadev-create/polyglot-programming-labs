# Clase 126 — AOT vs. JIT: costos y beneficios

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comparar **AOT (compilación anticipada)** con **JIT (compilación en tiempo de ejecución)**. AOT compila todo antes de arrancar (rápido al iniciar); JIT compila sobre la marcha las partes calientes (arranque más lento, luego rápido).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una potencia de dos.
2. Explicar AOT vs. JIT.
3. Relacionar el modelo con arranque y rendimiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AOT | Compilar todo antes de ejecutar |
| 2 | JIT | Compilar las partes calientes al vuelo |
| 3 | Arranque vs. pico | Compromiso entre ambos |

## 📖 Definiciones y características

- **AOT** — compilación anticipada a código máquina (C, Rust, Go). Clave: arranque instantáneo.
- **JIT** — compilación durante la ejecución de lo más usado (JVM, V8). Clave: se calienta y acelera.
- **Código caliente** — el que se ejecuta muchas veces. Clave: el JIT lo optimiza.

## 🧩 Situación

Una herramienta de línea de comandos AOT arranca al instante; un servidor JIT tarda en calentar pero luego es muy rápido. El cálculo (2^n) es el mismo; cambia cuándo se compila.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 60)
- **Salida** (stdout): `resultado=<2^n>`
- **Regla:** 2 elevado a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=8` |
| `0` | `resultado=1` |
| `5` | `resultado=32` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
multiplicar 2 por sí mismo n veces (o desplazar bits)
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
| Sintáctica | Bucle o desplazamiento de bits en cada lenguaje. |
| Semántica | El resultado no depende del modelo de compilación. |
| Paradigmática | SQL calcula con una expresión. |

## 🧬 El concepto en la familia

Go/Rust/C son AOT; la JVM y V8 son JIT; GraalVM ofrece AOT para la JVM.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 126
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desbordar con n grande** → causa: 2^64 no cabe → solución: aquí n <= 60
- **Empezar el acumulador en 0** → causa: siempre daría 0 → solución: iniciar el acumulador de producto en 1

## ❓ Preguntas frecuentes

- **¿AOT o JIT es mejor?** AOT para arranque rápido y binarios; JIT para procesos largos que se benefician del calentamiento.
- **¿Se pueden combinar?** Sí: GraalVM y otros ofrecen AOT sobre plataformas JIT.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 125](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 127 ⏭️](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md)
