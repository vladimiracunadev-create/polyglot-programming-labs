# Clase 146 — Revisión de código y estándares

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **revisión de código y los estándares**: un linter comprueba automáticamente convenciones (nombres, formato). Aquí se valida que un identificador esté en minúsculas, como haría una regla de estilo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Validar una convención de nombres.
2. Explicar el papel del linter.
3. Reconocer el valor de los estándares.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estándar de estilo | Reglas compartidas |
| 2 | Linter | Verifica automáticamente |
| 3 | Revisión de código | Segundo par de ojos |

## 📖 Definiciones y características

- **Estándar de código** — convenciones acordadas (nombres, formato). Clave: consistencia en el equipo.
- **Linter** — herramienta que detecta violaciones de estilo y errores probables. Clave: automatiza la revisión.
- **Revisión de código** — otra persona revisa el cambio antes de integrarlo. Clave: calidad y difusión de conocimiento.

## 🧩 Situación

En muchos proyectos, los identificadores van en minúsculas. Un linter marca 'Total' como violación. Automatizar estas reglas evita discusiones y mantiene el código uniforme.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (identificador, solo letras)
- **Salida** (stdout): `valido=<true|false>` (true si está todo en minúsculas)
- **Regla:** valido si todos los caracteres son minúsculas

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `total` | `valido=true` |
| `Total` | `valido=false` |
| `abc` | `valido=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER palabra ; valido <- todos los caracteres en minúscula
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
| Sintáctica | islower/comparación de caracteres en cada lenguaje. |
| Semántica | La regla se comprueba carácter a carácter. |
| Paradigmática | SQL compara con lower(). |

## 🧬 El concepto en la familia

ESLint, Ruff, Clippy, gofmt/govet aplican reglas de estilo automáticamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 146
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Reglas de estilo manuales** → causa: inconsistencia → solución: delegar en el linter
- **Ignorar los avisos del linter** → causa: bugs latentes → solución: resolverlos o justificarlos

## ❓ Preguntas frecuentes

- **¿Linter o revisión humana?** Ambos: el linter automatiza lo mecánico; la revisión, el criterio.
- **¿Por qué estándares?** Un código uniforme se lee y mantiene mejor.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 145](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 147 ⏭️](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md)
