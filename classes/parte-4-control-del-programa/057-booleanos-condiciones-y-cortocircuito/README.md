# Clase 057 — Booleanos, condiciones y cortocircuito

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Producir booleanos con operadores de comparación y combinarlos con **AND cortocircuitado**. El cortocircuito evita evaluar la segunda condición si la primera ya decide el resultado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir booleanos a partir de comparaciones.
2. Combinar condiciones con AND/OR.
3. Explicar el cortocircuito y por qué importa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comparaciones | Producen valores de verdad |
| 2 | Operadores lógicos | AND, OR y su cortocircuito |
| 3 | Cortocircuito | No evalúa lo que no hace falta |
| 4 | Normalizar booleanos | true/false consistente entre lenguajes |

## 📖 Definiciones y características

- **Condición** — expresión que da verdadero o falso. Clave: gobierna las decisiones.
- **Cortocircuito** — en `a && b`, si `a` es falso no se evalúa `b`. Clave: evita trabajo y errores.
- **Operador relacional** — compara valores (>, <, ==). Clave: produce booleanos.
- **Predicado** — condición sobre un valor (es positivo, es par). Clave: bloque de la lógica.

## 🧩 Situación

Validar `if (usuario != null && usuario.activo)` depende del cortocircuito: sin él, se accedería a `usuario.activo` con `usuario` nulo y reventaría. El orden de las condiciones importa.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `positivo=<true|false> par=<true|false> ambos=<true|false>`
- **Regla:** positivo = n>0 ; par = n%2==0 ; ambos = positivo && par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `positivo=true par=true ambos=true` |
| `-3` | `positivo=false par=false ambos=false` |
| `7` | `positivo=true par=false ambos=false` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR positivo=(n>0), par=(n%2==0), ambos=((n>0) Y (n%2==0))
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
| Sintáctica | `and` (Python) vs. `&&` (C/Java/JS/Go/Rust/PHP). |
| Semántica | Todos cortocircuitan `&&`/`and`; C# imprime True/False (normalizar). |
| Paradigmática | SQL usa AND en la expresión y CASE WHEN para el texto. |

## 🧬 El concepto en la familia

En Ruby `n > 0 && n.even?`. En Haskell `n > 0 && even n`, con el mismo cortocircuito.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 057
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ordenar mal las condiciones** → causa: evaluar algo inválido antes de la guarda → solución: poner primero la condición que protege a la segunda
- **Imprimir True/False** → causa: formato por defecto de C# → solución: normalizar a minúsculas con un ayudante

## ❓ Preguntas frecuentes

- **¿`&` y `&&` son iguales?** No: `&` es bit a bit y evalúa ambos lados; `&&` cortocircuita.
- **¿El cortocircuito cambia el resultado?** No el valor lógico, pero sí si el segundo lado tiene efectos o puede fallar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 056](../../parte-3-valores-tipos-y-variables/056-entrada-y-salida-basica-leer-y-escribir/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 058 ⏭️](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md)
