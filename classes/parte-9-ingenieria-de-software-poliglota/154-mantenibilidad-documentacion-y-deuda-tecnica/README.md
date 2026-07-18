# Clase 154 — Mantenibilidad, documentación y deuda técnica

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la **mantenibilidad, la documentación y la deuda técnica**: medir la complejidad ayuda a mantener el código sano. Contar los módulos es una métrica básica; la deuda técnica crece cuando se ignora.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una métrica simple de estructura.
2. Explicar la deuda técnica.
3. Reconocer el valor de la documentación.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mantenibilidad | Facilidad de cambiar el código |
| 2 | Deuda técnica | El coste de los atajos |
| 3 | Métricas | Medir para gestionar |

## 📖 Definiciones y características

- **Mantenibilidad** — facilidad con que el código se entiende y modifica. Clave: reduce el coste futuro.
- **Deuda técnica** — coste acumulado de decisiones rápidas que habrá que pagar. Clave: crece si se ignora.
- **Documentación** — explicar el porqué del código. Clave: baja la barrera para mantenerlo.

## 🧩 Situación

Un sistema con muchos módulos poco documentados acumula deuda técnica: cada cambio cuesta más. Medir su estructura y documentar el porqué mantiene el proyecto sano a largo plazo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de módulos (palabras separadas por espacio)
- **Salida** (stdout): `complejidad=<número de módulos>`
- **Regla:** contar los módulos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `a b c` | `complejidad=3` |
| `x` | `complejidad=1` |
| `a b c d e` | `complejidad=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER módulos ; ESCRIBIR cantidad
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
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | La métrica estima la complejidad estructural. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

SonarQube y linters miden complejidad ciclomática, duplicación y deuda técnica automáticamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 154
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar la deuda técnica** → causa: el código se vuelve inmantenible → solución: pagarla en pequeñas dosis continuas
- **Documentar el qué en vez del porqué** → causa: comentarios redundantes → solución: explicar las decisiones, no repetir el código

## ❓ Preguntas frecuentes

- **¿Deuda técnica es siempre mala?** No: a veces es un préstamo consciente; el problema es no pagarla.
- **¿Qué documentar?** El porqué de las decisiones; el qué suele leerse en el código.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 153](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 155 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md)
