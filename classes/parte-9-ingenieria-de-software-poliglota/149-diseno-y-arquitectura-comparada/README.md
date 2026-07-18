# Clase 149 — Diseño y arquitectura comparada

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **diseño y la arquitectura**: un sistema se organiza en capas o componentes con responsabilidades claras. Contar las capas es la medida más básica de su estructura.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar las capas de una arquitectura.
2. Explicar la separación de responsabilidades.
3. Reconocer estilos arquitectónicos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arquitectura | Estructura de alto nivel |
| 2 | Capa/componente | Responsabilidad definida |
| 3 | Separación de responsabilidades | Cada parte hace una cosa |

## 📖 Definiciones y características

- **Arquitectura** — estructura de alto nivel de un sistema y sus componentes. Clave: guía las decisiones grandes.
- **Capa** — grupo de componentes con una responsabilidad (presentación, lógica, datos). Clave: separa preocupaciones.
- **Acoplamiento** — grado de dependencia entre componentes. Clave: bajo acoplamiento facilita el cambio.

## 🧩 Situación

Un sistema típico tiene capas: web (interfaz), api (lógica), datos (persistencia). Nombrar y contar las capas es el primer paso para razonar sobre su arquitectura.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de capas (palabras separadas por espacio)
- **Salida** (stdout): `capas=<cantidad>`
- **Regla:** contar los nombres de capa

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `web api datos` | `capas=3` |
| `cli` | `capas=1` |
| `web api datos cache` | `capas=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER capas ; ESCRIBIR cantidad
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
| Semántica | Cada capa aísla una responsabilidad. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Arquitecturas en capas, hexagonal, microservicios: todas organizan componentes con responsabilidades.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 149
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capas con responsabilidades mezcladas** → causa: difícil de mantener → solución: una responsabilidad por capa
- **Alto acoplamiento** → causa: un cambio propaga a todo → solución: definir contratos claros entre capas

## ❓ Preguntas frecuentes

- **¿Cuántas capas?** Las que el problema justifique; ni de más ni de menos.
- **¿Capas o microservicios?** Capas dentro de un proceso; microservicios los separan en servicios.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 148](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 150 ⏭️](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md)
