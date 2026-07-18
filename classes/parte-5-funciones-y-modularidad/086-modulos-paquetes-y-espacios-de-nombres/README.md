# Clase 086 — Módulos, paquetes y espacios de nombres

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Organizar el código en **módulos** (o paquetes/espacios de nombres): agrupar funciones relacionadas y usarlas con un prefijo o importándolas. Es lo que evita que un proyecto grande sea un solo archivo caótico.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Agrupar funciones en un módulo/espacio de nombres.
2. Invocar una función de otro módulo.
3. Reconocer import/require/use por lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Módulo | Agrupa código relacionado |
| 2 | Espacio de nombres | Evita choques de nombres |
| 3 | Importar | Traer lo que se necesita |
| 4 | Organización | Un proyecto no es un solo archivo |

## 📖 Definiciones y características

- **Módulo** — unidad que agrupa funciones/tipos relacionados. Clave: organización y reutilización.
- **Espacio de nombres** — prefijo que evita colisiones de nombres. Clave: `math.sqrt` vs. `otro.sqrt`.
- **Importar** — traer un módulo al alcance actual (import/require/use). Clave: acceder a su contenido.
- **Encapsulación de módulo** — exponer solo lo público. Clave: oculta detalles internos.

## 🧩 Situación

En un proyecto real, las utilidades matemáticas viven en un módulo, las de red en otro. Se importan donde hacen falta. Aquí, una función `doble` en un espacio propio se usa desde el principal.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** modulo.doble(n) = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `-4` | `resultado=-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR modulo
LEER n ; ESCRIBIR "resultado=" modulo.doble(n)
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
| Sintáctica | `import`/`from` (Python), `require`/`import` (JS), `use` (Rust), `package` (Go/Java). |
| Semántica | El módulo define un espacio de nombres; se accede con prefijo o importando nombres. |
| Paradigmática | SQL organiza en esquemas (schemas), análogos a espacios de nombres. |

## 🧬 El concepto en la familia

En Ruby, módulos con `module M; def self.doble`. En C, la 'modularidad' es por archivos .h/.c y enlace.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 086
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Meter todo en un archivo** → causa: proyecto inmantenible → solución: separar por módulos con responsabilidad clara
- **Importar de más (namespace pollution)** → causa: colisiones y confusión → solución: importar solo lo necesario o usar el prefijo del módulo

## ❓ Preguntas frecuentes

- **¿Módulo, paquete o namespace?** Términos cercanos: agrupar y nombrar código. Cada lenguaje usa su palabra.
- **¿Por qué prefijos?** Para que dos módulos puedan tener funciones con el mismo nombre sin chocar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 085](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 087 ⏭️](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md)
