# Clase 157 — ABI, enlace y convenciones de llamada

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **ABI, el enlace y las convenciones de llamada**: para que dos piezas binarias se comuniquen, deben compartir la misma ABI (cómo se pasan los datos y se llaman las funciones). Un desajuste (p. ej. 32 vs 64 bits) rompe la interoperabilidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la ABI.
2. Detectar una incompatibilidad de ABI.
3. Distinguir ABI de API.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | ABI | Contrato binario |
| 2 | Convención de llamada | Cómo se pasan los argumentos |
| 3 | Compatibilidad | Mismo ABI para enlazar |

## 📖 Definiciones y características

- **ABI** — Application Binary Interface: cómo se representan datos y se llaman funciones a nivel binario. Clave: debe coincidir para enlazar.
- **Convención de llamada** — reglas de paso de argumentos y retorno. Clave: parte de la ABI.
- **API vs. ABI** — API es el contrato en código fuente; ABI, el binario. Clave: distinto nivel.

## 🧩 Situación

Enlazar una librería de 32 bits con un programa de 64 bits falla: sus ABI no coinciden. La ABI es el contrato invisible que hace posible (o imposible) que dos binarios cooperen.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (ancho de bits de cada componente)
- **Salida** (stdout): `abi=<compatible|incompatible>`
- **Regla:** compatible si los anchos coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `64 64` | `abi=compatible` |
| `64 32` | `abi=incompatible` |
| `32 32` | `abi=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
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
| Sintáctica | Comparación de enteros en cada lenguaje. |
| Semántica | La ABI incluye tamaños, alineación y convención de llamada. |
| Paradigmática | SQL compara valores. |

## 🧬 El concepto en la familia

Cada plataforma (x86-64 System V, Windows x64) define su ABI; los binarios deben respetarla para enlazar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 157
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar binarios de distinta arquitectura** → causa: fallo de enlace o corrupción → solución: compilar todo para la misma ABI
- **Confundir API con ABI** → causa: esperar compatibilidad binaria del código fuente → solución: recordar que son contratos de distinto nivel

## ❓ Preguntas frecuentes

- **¿API o ABI?** API es el contrato fuente; ABI, el binario. Un cambio de ABI rompe binarios ya compilados.
- **¿Por qué importa la ABI?** Para enlazar librerías compiladas y usar la FFI sin corromper datos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 156](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 158 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md)
