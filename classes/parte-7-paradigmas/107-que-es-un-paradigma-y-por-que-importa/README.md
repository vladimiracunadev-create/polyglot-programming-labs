# Clase 107 — Qué es un paradigma y por qué importa

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender qué es un **paradigma**: una forma de estructurar la solución (imperativa, funcional, declarativa…). El mismo problema —sumar 1 a n— puede resolverse de varias maneras según el paradigma.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir qué es un paradigma.
2. Reconocer que un problema admite varios enfoques.
3. Situar los paradigmas del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paradigma | Forma de estructurar la solución |
| 2 | Multiparadigma | Un lenguaje puede ofrecer varios |
| 3 | Mismo problema, varios enfoques | Imperativo, funcional, declarativo |

## 📖 Definiciones y características

- **Paradigma** — estilo de estructurar programas (imperativo, OO, funcional, declarativo). Clave: cambia cómo se piensa.
- **Multiparadigma** — lenguaje que soporta varios estilos (Python, C#, Rust). Clave: eliges por problema.
- **Enfoque** — la estrategia elegida para resolver. Clave: distintos paradigmas, distinta forma.

## 🧩 Situación

Sumar 1..n se puede hacer con un bucle (imperativo), con reduce (funcional) o con una fórmula/consulta (declarativo). El paradigma decide la forma, no el resultado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `3` | `suma=6` |
| `1` | `suma=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; sumar 1..n ; ESCRIBIR suma
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
| Sintáctica | Bucle, `reduce` o fórmula según el estilo. |
| Semántica | Todos dan el mismo resultado; cambia la estructura. |
| Paradigmática | Imperativo describe pasos; declarativo describe el resultado. |

## 🧬 El concepto en la familia

Casi todos los lenguajes del núcleo son multiparadigma: permiten el mismo problema de varias formas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 107
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que hay un solo modo correcto** → causa: encasillarse en un paradigma → solución: elegir el que mejor exprese el problema
- **Confundir paradigma con lenguaje** → causa: un lenguaje ofrece varios → solución: distinguir el estilo del lenguaje

## ❓ Preguntas frecuentes

- **¿Cuál es mejor?** Depende del problema: cada paradigma brilla en distintos casos.
- **¿Un lenguaje = un paradigma?** No: la mayoría son multiparadigma.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 106](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 108 ⏭️](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md)
