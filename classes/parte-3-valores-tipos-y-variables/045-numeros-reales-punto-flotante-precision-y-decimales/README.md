# Clase 045 — Números reales: punto flotante, precisión y decimales

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con números de punto flotante y su formateo. El foco: los reales son **aproximados** (`0.1 + 0.2` no es exactamente `0.3`), y por eso casi siempre se muestran con un número fijo de decimales usando un formato que fuerza la cultura (punto, no coma).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Operar con reales (suma y producto).
2. Formatear un real con un número fijo de decimales.
3. Explicar por qué el punto flotante es aproximado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Punto flotante | Representación aproximada de los reales |
| 2 | Formateo con decimales | Mostrar 2 decimales de forma consistente |
| 3 | Cultura/locale | Punto vs. coma decimal según el sistema |
| 4 | Redondeo | El formateo redondea; cuidado con los empates |

## 📖 Definiciones y características

- **Punto flotante** — representación binaria aproximada de números reales (IEEE 754). Clave: no todos los decimales son exactos.
- **Precisión** — cuántos dígitos significativos conserva un real. Clave: limitada; genera pequeños errores.
- **Formateo** — convertir el real a texto con N decimales. Clave: cómo se presenta el resultado.
- **Cultura invariante** — formato que usa el punto decimal sin importar el idioma del sistema. Clave: evita la coma decimal.

## 🧩 Situación

`0.1 + 0.2` da `0.30000000000000004` en casi todos los lenguajes. No es un bug: es cómo el hardware representa los reales. Por eso el dinero y los resultados se muestran con decimales fijos y formato controlado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos reales)
- **Salida** (stdout): `suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`
- **Regla:** suma = a + b ; producto = a * b (ambos a 2 decimales)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.5 2.5` | `suma=4.00 producto=3.75` |
| `0.1 0.2` | `suma=0.30 producto=0.02` |
| `10 3` | `suma=13.00 producto=30.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "suma=" FORMATEAR(a+b,2) " producto=" FORMATEAR(a*b,2)
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
| Sintáctica | `%.2f` (Python/C/Go), `toFixed(2)` (JS), `F2` (C#), `{:.2}` (Rust). |
| Semántica | El locale puede imprimir coma; se fuerza el punto (Locale.US, InvariantCulture). |
| Paradigmática | SQL formatea con `printf('%.2f', ...)` dentro de la consulta. |

## 🧬 El concepto en la familia

En Ruby: `format('%.2f', x)`. En Haskell: `printf "%.2f" x` (de Text.Printf). El problema del punto flotante es idéntico en toda la familia porque todos usan IEEE 754.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 045
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ver `4,00` en vez de `4.00`** → causa: el locale usa coma decimal → solución: forzar cultura invariante (Locale.US / InvariantCulture)
- **Comparar reales con `==`** → causa: esperar igualdad exacta → solución: comparar con una tolerancia, o formatear antes de comparar

## ❓ Preguntas frecuentes

- **¿Por qué 0.1+0.2 no es 0.3?** 0.1 y 0.2 no tienen representación binaria exacta; el error se arrastra a la suma.
- **¿Cómo manejo dinero entonces?** Con decimales fijos y formateo, o con tipos decimales exactos donde el lenguaje los ofrezca.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 044](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 046 ⏭️](../../parte-3-valores-tipos-y-variables/046-booleanos-y-valores-de-verdad/README.md)
