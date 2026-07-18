# Clase 167 — Componente CLI (lenguaje de sistemas)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente CLI** del sistema (idóneo para un lenguaje de sistemas): una interfaz de línea de comandos que recibe un comando y argumentos. Aquí se parsea el comando y se cuentan sus argumentos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Parsear una invocación de CLI.
2. Separar comando de argumentos.
3. Explicar el rol del componente CLI.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CLI | Interfaz de línea de comandos |
| 2 | Comando y argumentos | Qué hacer y con qué |
| 3 | Parseo | Interpretar la invocación |

## 📖 Definiciones y características

- **Componente CLI** — interfaz por terminal del sistema. Clave: automatizable y componible.
- **Comando** — la acción a ejecutar (el primer token). Clave: selecciona qué hacer.
- **Argumento** — dato que modifica la acción. Clave: se cuentan tras el comando.

## 🧩 Situación

La CLI del sistema recibe `run a b`: el comando es `run` y hay 2 argumentos. Parsear bien la invocación es la base de cualquier herramienta de línea de comandos, a menudo escrita en Go o Rust.

## 🧮 Modelo

- **Entrada** (stdin): una línea `comando arg1 arg2 ...` (al menos el comando)
- **Salida** (stdout): `comando=<comando> args=<número de argumentos>`
- **Regla:** primer token = comando; resto = argumentos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `run a b` | `comando=run args=2` |
| `build` | `comando=build args=0` |
| `deploy x y z` | `comando=deploy args=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens ; comando <- tokens[0] ; args <- tokens - 1
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
| Sintáctica | Separar el primer token del resto en cada lenguaje. |
| Semántica | El comando decide la acción; los argumentos, los datos. |
| Paradigmática | SQL no tiene CLI de argumentos; se consulta. |

## 🧬 El concepto en la familia

clap (Rust), cobra (Go), argparse (Python), commander (JS) construyen CLIs robustas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 167
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No validar los argumentos** → causa: errores al ejecutar → solución: comprobar cantidad y tipo de argumentos
- **Mensajes de ayuda ausentes** → causa: CLI difícil de usar → solución: ofrecer --help y errores claros

## ❓ Preguntas frecuentes

- **¿Qué lenguaje para una CLI?** Go y Rust por sus binarios únicos y rápidos; Python para scripts.
- **¿Argumentos posicionales o con nombre?** Nombrados (--flag) para claridad; posicionales para lo esencial.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 166](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 168 ⏭️](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md)
