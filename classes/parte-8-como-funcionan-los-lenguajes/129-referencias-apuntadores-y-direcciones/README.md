# Clase 129 — Referencias, apuntadores y direcciones

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **referencias, apuntadores y direcciones**: acceder a un dato a través de su posición o dirección, no directamente. Indexar una lista es aritmética de direcciones: base + índice.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Acceder a un elemento por su índice.
2. Explicar la indirección (referencia/puntero).
3. Relacionar el índice con la dirección.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Indirección | Acceder a través de una posición |
| 2 | Índice como dirección | base + desplazamiento |
| 3 | Referencia vs. puntero | Ambos apuntan a un dato |

## 📖 Definiciones y características

- **Referencia** — un valor que designa a otro dato. Clave: acceso indirecto.
- **Puntero** — referencia explícita que guarda una dirección (C). Clave: `arr + i` = dirección del elemento i.
- **Índice** — posición dentro de una secuencia. Clave: equivale a un desplazamiento desde la base.

## 🧩 Situación

`arr[i]` en el fondo es 've a la dirección base más i posiciones'. Los punteros de C hacen esa aritmética explícita; los índices la esconden. Ambos son indirección.

## 🧮 Modelo

- **Entrada** (stdin): una línea `indice v0 v1 v2 ...` (el primero es el índice, base 0)
- **Salida** (stdout): `valor=<elemento en esa posición>`
- **Regla:** valor = lista[indice]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 10 20 30` | `valor=20` |
| `0 5 6 7` | `valor=5` |
| `2 100 200 300` | `valor=300` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER indice y lista ; ESCRIBIR lista[indice]
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
| Sintáctica | `arr[i]` en casi todos; en C, también `*(arr + i)`. |
| Semántica | El índice se traduce a una dirección de memoria. |
| Paradigmática | SQL accede por condición, no por índice. |

## 🧬 El concepto en la familia

En C `arr[i]` y `*(arr+i)` son equivalentes: puro puntero. En los demás, el índice abstrae la dirección.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 129
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Índice fuera de rango** → causa: acceso inválido → solución: verificar que 0 <= i < tamaño
- **Confundir el valor con su dirección** → causa: usar el puntero como valor → solución: desreferenciar para obtener el valor

## ❓ Preguntas frecuentes

- **¿Referencia o puntero?** El puntero es una referencia explícita con aritmética; la referencia suele ser más segura.
- **¿arr[i] es un puntero?** En C sí, por debajo; en otros lenguajes el índice abstrae la dirección.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 128](../../parte-8-como-funcionan-los-lenguajes/128-el-heap-y-la-asignacion-dinamica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 130 ⏭️](../../parte-8-como-funcionan-los-lenguajes/130-gestion-manual-de-memoria-c-malloc-free/README.md)
