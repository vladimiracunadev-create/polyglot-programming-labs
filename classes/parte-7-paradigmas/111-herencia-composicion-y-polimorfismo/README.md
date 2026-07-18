# Clase 111 — Herencia, composición y polimorfismo

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar **herencia, composición y polimorfismo**: distintos tipos que comparten una interfaz común (`sonido`) y responden cada uno a su manera. Llamar al mismo método da resultados distintos según el tipo real.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer el polimorfismo (mismo método, distinto comportamiento).
2. Distinguir herencia de composición.
3. Despachar según el tipo real.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Herencia | Un tipo deriva de otro |
| 2 | Polimorfismo | Mismo método, comportamiento distinto |
| 3 | Composición | Construir con partes, alternativa a heredar |

## 📖 Definiciones y características

- **Herencia** — un tipo hereda estado/comportamiento de otro. Clave: reutiliza y especializa.
- **Polimorfismo** — el mismo método se comporta distinto según el tipo real. Clave: `animal.sonido()`.
- **Composición** — construir un objeto a partir de otros (tiene-un) en vez de heredar (es-un). Clave: más flexible.

## 🧩 Situación

Perro, gato y vaca son animales, pero cada uno suena distinto. El polimorfismo permite tratarlos igual (`animal.sonido()`) y obtener la respuesta correcta según el tipo.

## 🧮 Modelo

- **Entrada** (stdin): una palabra: `perro`, `gato` o `vaca`
- **Salida** (stdout): `sonido=<guau|miau|muu>`
- **Regla:** cada tipo devuelve su propio sonido

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `perro` | `sonido=guau` |
| `gato` | `sonido=miau` |
| `vaca` | `sonido=muu` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo ; crear animal ; ESCRIBIR animal.sonido()
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
| Sintáctica | Herencia/interfaces (Java/C#), traits (Rust), interfaces (Go), duck typing (Python/JS). |
| Semántica | El despacho es dinámico: se decide en ejecución por el tipo real. |
| Paradigmática | SQL usa CASE; no hay despacho polimórfico. |

## 🧬 El concepto en la familia

En Ruby el polimorfismo es por duck typing. En Kotlin, interfaces y clases selladas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 111
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Abusar de la herencia profunda** → causa: jerarquías frágiles → solución: preferir composición cuando encaje
- **Olvidar un tipo** → causa: caso sin manejar → solución: cubrir todos o usar un default

## ❓ Preguntas frecuentes

- **¿Herencia o composición?** Composición por defecto; herencia cuando hay un 'es-un' real y estable.
- **¿Qué es duck typing?** Si suena como pato, es pato: importa el método, no el tipo declarado.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 110](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 112 ⏭️](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md)
