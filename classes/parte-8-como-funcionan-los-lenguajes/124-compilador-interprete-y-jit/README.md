# Clase 124 — Compilador, intérprete y JIT

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Diferenciar **compilador, intérprete y JIT** por su forma de ejecutar. El programa (contar dígitos) es el mismo; lo que cambia entre modelos es cuándo y cómo se traduce a instrucciones de la máquina.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar dígitos recorriendo el número.
2. Explicar compilado, interpretado y JIT.
3. Relacionar el modelo con el rendimiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Compilador | Traduce antes de ejecutar |
| 2 | Intérprete | Ejecuta la fuente al vuelo |
| 3 | JIT | Compila durante la ejecución |

## 📖 Definiciones y características

- **Compilador** — traduce todo el programa a código máquina antes de ejecutar. Clave: rápido, errores antes.
- **Intérprete** — ejecuta la fuente instrucción a instrucción. Clave: flexible, más lento.
- **JIT** — compila a máquina las partes calientes durante la ejecución. Clave: combina ambos (V8, JVM).

## 🧩 Situación

Contar dígitos corre igual en C (compilado), Python (interpretado) y JavaScript (JIT); lo que cambia es el rendimiento y cuándo aparecen los errores, no el resultado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 0)
- **Salida** (stdout): `digitos=<cantidad de dígitos>`
- **Regla:** contar los dígitos de n (0 tiene 1)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `12345` | `digitos=5` |
| `7` | `digitos=1` |
| `100` | `digitos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
contar dígitos dividiendo por 10 hasta 0 (o longitud del texto)
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
| Sintáctica | Igual en todos: recorrer o medir el número. |
| Semántica | El modelo de ejecución no cambia el resultado. |
| Paradigmática | SQL usa length sobre el texto del número. |

## 🧬 El concepto en la familia

C compila; CPython interpreta bytecode; V8 y la JVM usan JIT. El programa es idéntico.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 124
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar 0 como 0 dígitos** → causa: el 0 tiene un dígito → solución: tratar el caso n=0
- **Dividir sin parar** → causa: bucle infinito → solución: parar cuando el número llega a 0

## ❓ Preguntas frecuentes

- **¿Cuál es más rápido?** Compilado suele ganar en ejecución; interpretado gana en iteración; JIT busca ambos.
- **¿Python compila?** A bytecode internamente; luego lo interpreta.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 123](../../parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 125 ⏭️](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md)
