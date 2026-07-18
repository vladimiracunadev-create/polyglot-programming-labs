# Clase 153 — Seguridad: entradas, memoria y dependencias

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **seguridad**: validar y sanear las entradas para evitar inyecciones y datos maliciosos. Comprobar que una entrada es alfanumérica es una validación básica que cierra muchos ataques.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Validar una entrada contra un conjunto permitido.
2. Explicar por qué no confiar en la entrada.
3. Reconocer riesgos de seguridad comunes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación de entrada | No confiar en lo externo |
| 2 | Saneamiento | Limpiar datos peligrosos |
| 3 | Inyección | Datos que se ejecutan como código |

## 📖 Definiciones y características

- **Validación de entrada** — comprobar que los datos cumplen lo esperado antes de usarlos. Clave: primera defensa.
- **Saneamiento** — eliminar o escapar caracteres peligrosos. Clave: evita inyecciones.
- **Inyección** — datos maliciosos que el programa interpreta como comando (SQL, shell). Clave: causa frecuente de brechas.

## 🧩 Situación

Un campo que debería ser un nombre recibe `'; DROP TABLE`. Validar que solo contiene caracteres alfanuméricos rechaza la entrada maliciosa antes de que cause daño.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (entrada a validar)
- **Salida** (stdout): `seguro=<true|false>` (true si es alfanumérica)
- **Regla:** seguro si todos los caracteres son letras o dígitos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `abc` | `seguro=true` |
| `a;b` | `seguro=false` |
| `hola123` | `seguro=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER entrada ; seguro <- todos los caracteres alfanuméricos
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
| Sintáctica | isalnum/regex en cada lenguaje. |
| Semántica | Se valida contra una lista blanca (más seguro que una negra). |
| Paradigmática | SQL usa consultas parametrizadas para evitar inyección. |

## 🧬 El concepto en la familia

Toda plataforma web valida entradas; las consultas parametrizadas evitan la inyección SQL.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 153
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en la entrada del usuario** → causa: inyecciones y corrupción → solución: validar y sanear siempre
- **Lista negra en vez de blanca** → causa: olvidar un caso peligroso → solución: permitir solo lo conocido (lista blanca)

## ❓ Preguntas frecuentes

- **¿Validar en cliente o servidor?** En ambos, pero la validación del servidor es la que cuenta.
- **¿Cómo evitar inyección SQL?** Con consultas parametrizadas, nunca concatenando la entrada.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 152](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 154 ⏭️](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md)
