# Clase 102 — Copia superficial vs. profunda; referencia vs. valor

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **copia** de **referencia compartida**, y **copia superficial** de **profunda**. Copiar una lista de valores y modificar la copia no altera el original; con referencias compartidas, sí.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Copiar una colección.
2. Comprobar que el original no cambia.
3. Distinguir copia superficial de profunda.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Copia vs. referencia | Duplicar o compartir |
| 2 | Copia superficial | Copia el primer nivel |
| 3 | Copia profunda | Copia todo recursivamente |

## 📖 Definiciones y características

- **Copia** — duplicado independiente. Clave: modificarlo no afecta al original.
- **Referencia compartida** — dos nombres para el mismo dato. Clave: cambiar uno cambia el otro.
- **Superficial vs. profunda** — copiar solo el nivel externo o todo el contenido. Clave: importa con datos anidados.

## 🧩 Situación

Asignar `b = a` en muchos lenguajes comparte la lista: cambiar `b` cambia `a`. Copiarla de verdad evita esa sorpresa. Con estructuras anidadas, la copia debe ser profunda.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `original=<lista> copia=<lista con el último cambiado a 99>` (unidos por -)
- **Regla:** copiar; copia[último] = 99; original intacto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `original=1-2-3 copia=1-2-99` |
| `5 5` | `original=5-5 copia=5-99` |
| `7` | `original=7 copia=99` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; copia <- COPIA(lista) ; copia[fin] <- 99 ; ESCRIBIR original y copia
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
| Sintáctica | `list(x)`/`x[:]` (Python), `[...x]` (JS), `clone()` (Rust/Java). |
| Semántica | Sin copiar, `b=a` comparte; hay que copiar explícitamente. |
| Paradigmática | SQL trabaja con conjuntos; no comparte referencias mutables. |

## 🧬 El concepto en la familia

En Ruby `dup` copia superficial; en muchos lenguajes la copia profunda requiere recorrer.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 102
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que asignar copia** → causa: `b=a` comparte la referencia → solución: copiar explícitamente si necesitas independencia
- **Copia superficial con datos anidados** → causa: los niveles internos siguen compartidos → solución: hacer copia profunda cuando haya anidamiento

## ❓ Preguntas frecuentes

- **¿Copia superficial o profunda?** Superficial si no hay anidamiento; profunda si hay estructuras dentro de estructuras.
- **¿Los primitivos se comparten?** No: los valores se copian; las colecciones/objetos se comparten por referencia.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 101](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 103 ⏭️](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md)
