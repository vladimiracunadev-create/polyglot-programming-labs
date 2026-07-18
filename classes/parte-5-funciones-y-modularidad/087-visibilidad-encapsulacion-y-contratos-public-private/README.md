# Clase 087 — Visibilidad, encapsulación y contratos (public/private)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aplicar **encapsulación**: ocultar el estado interno (el saldo) y exponer solo operaciones controladas (depositar, consultar). El contrato público protege los datos de modificaciones inválidas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ocultar un campo con visibilidad privada.
2. Exponer métodos públicos como contrato.
3. Explicar por qué la encapsulación protege los datos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Encapsulación | Ocultar el estado interno |
| 2 | Visibilidad | public vs. private |
| 3 | Contrato público | Lo que se puede usar |
| 4 | Invariantes | Reglas que el objeto mantiene |

## 📖 Definiciones y características

- **Encapsulación** — agrupar datos y operaciones ocultando el estado interno. Clave: se accede solo por métodos.
- **Privado** — accesible solo desde dentro del tipo. Clave: protege el estado.
- **Público** — parte visible desde fuera (el contrato). Clave: lo que otros usan.
- **Invariante** — regla que el objeto siempre cumple (saldo >= 0). Clave: la encapsulación la protege.

## 🧩 Situación

Si el saldo fuera público, cualquiera podría ponerlo en negativo saltándose las reglas. Encapsulado, solo `depositar`/`retirar` lo tocan, garantizando que siempre sea válido.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (monto de cada depósito)
- **Salida** (stdout): `saldo=<2n>` (tras depositar n dos veces)
- **Regla:** cuenta.depositar(n) dos veces; saldo = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `50` | `saldo=100` |
| `0` | `saldo=0` |
| `30` | `saldo=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
cuenta <- nueva Cuenta()
cuenta.depositar(n) ; cuenta.depositar(n)
ESCRIBIR "saldo=" cuenta.saldo()
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
| Sintáctica | `private`/`public` (Java/C#), `_` por convención (Python), campos en minúscula (Go = privado del paquete). |
| Semántica | Java/C#/Rust hacen cumplir la privacidad; Python confía en la convención. |
| Paradigmática | SQL encapsula con vistas y permisos. |

## 🧬 El concepto en la familia

En Ruby los atributos son privados y se exponen con `attr_reader`/métodos. En Go, la mayúscula/minúscula del nombre define la visibilidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 087
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer el estado directamente** → causa: cualquiera lo corrompe → solución: hacerlo privado y ofrecer métodos
- **Getters/setters para todo sin criterio** → causa: encapsulación de fachada → solución: exponer operaciones con significado, no acceso crudo

## ❓ Preguntas frecuentes

- **¿Python encapsula de verdad?** Por convención (`_priv`); no lo impide, pero la comunidad lo respeta.
- **¿Encapsular es solo getters/setters?** No: es exponer operaciones con significado que mantienen los invariantes.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 086](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 088 ⏭️](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md)
