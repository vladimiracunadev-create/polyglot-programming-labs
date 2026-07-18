# Clase 143 — Dependencias, versiones y lockfiles

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **dependencias, versiones y lockfiles**: el versionado semántico (SemVer) 'mayor.menor.parche' comunica compatibilidad. Descomponerlo es el primer paso para gestionar dependencias con criterio.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Parsear una versión semántica.
2. Explicar qué significa cada componente.
3. Reconocer el papel del lockfile.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | SemVer | mayor.menor.parche |
| 2 | Compatibilidad | Qué implica cada número |
| 3 | Lockfile | Versiones exactas fijadas |

## 📖 Definiciones y características

- **Versionado semántico** — esquema mayor.menor.parche donde cada número señala el tipo de cambio. Clave: comunica compatibilidad.
- **Mayor/menor/parche** — cambios incompatibles / nuevas features / correcciones. Clave: guían las actualizaciones.
- **Lockfile** — archivo con las versiones exactas resueltas. Clave: builds reproducibles.

## 🧩 Situación

Al depender de una librería '^1.4.2', importa si sube a 1.5.0 (compatible) o a 2.0.0 (posible ruptura). El lockfile fija la versión exacta para que todos obtengan lo mismo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `mayor=<M> menor=<m> parche=<p>`
- **Regla:** separar la versión por puntos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `mayor=1 menor=2 parche=3` |
| `0.5.10` | `mayor=0 menor=5 parche=10` |
| `2.0.0` | `mayor=2 menor=0 parche=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; separar por '.' ; ESCRIBIR componentes
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
| Sintáctica | split por '.' en cada lenguaje. |
| Semántica | Cada número tiene un significado de compatibilidad. |
| Paradigmática | SQL separa con funciones de texto. |

## 🧬 El concepto en la familia

npm, cargo, pip, composer usan SemVer y lockfiles (package-lock.json, Cargo.lock).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 143
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No commitear el lockfile** → causa: builds distintos por máquina → solución: versionar el lockfile
- **Fijar a 'latest'** → causa: roturas por actualizaciones → solución: acotar rangos y confiar en el lock

## ❓ Preguntas frecuentes

- **¿Qué sube en un parche?** Solo correcciones compatibles; no rompe nada.
- **¿Por qué el lockfile?** Garantiza que todos instalen exactamente las mismas versiones.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 142](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 144 ⏭️](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md)
