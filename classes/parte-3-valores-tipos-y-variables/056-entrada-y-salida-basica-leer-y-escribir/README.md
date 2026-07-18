# Clase 056 — Entrada y salida básica: leer y escribir

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la Parte 3 con lo más elemental: **leer de la entrada estándar y escribir en la salida estándar**. Todo el curso se apoya en este contrato (stdin → stdout), y aquí se ve desnudo en los 10 lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Leer una línea completa de stdin.
2. Escribir en stdout con un formato dado.
3. Reconocer el contrato stdin/stdout usado en todo el curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrada estándar (stdin) | El canal por defecto de entrada |
| 2 | Salida estándar (stdout) | El canal por defecto de salida |
| 3 | Leer una línea | Distinto de leer un token o un carácter |
| 4 | El contrato del curso | stdin → stdout, verificable |

## 📖 Definiciones y características

- **stdin** — canal de entrada estándar de un programa. Clave: de donde se leen los datos por defecto.
- **stdout** — canal de salida estándar. Clave: donde se escribe el resultado que se verifica.
- **Leer una línea** — obtener texto hasta el salto de línea. Clave: incluye espacios internos.
- **Eco** — devolver la entrada tal cual (con un prefijo). Clave: el ejemplo mínimo de E/S.

## 🧩 Situación

Todo programa de este curso lee de stdin y escribe en stdout; por eso el verificador puede comprobarlos a todos igual. El 'eco' es la forma más simple de ese contrato.

## 🧮 Modelo

- **Entrada** (stdin): una línea de texto
- **Salida** (stdout): `eco: <la línea leída>`
- **Regla:** salida = 'eco: ' + entrada

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `eco: hola` |
| `Polyglot` | `eco: Polyglot` |
| `123` | `eco: 123` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER linea
ESCRIBIR "eco: " linea
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
| Sintáctica | `input()`/`readline` (Python), `readFileSync(0)` (JS), `fgets` (C). |
| Semántica | Hay que quitar el salto de línea final para que el eco sea exacto. |
| Paradigmática | SQL no lee stdin: se muestra el eco sobre una tabla de textos. |

## 🧬 El concepto en la familia

En Ruby `gets.chomp`. En Haskell `getLine`. En C++ `std::getline(std::cin, s)`. Todos leen una línea y recortan el salto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 056
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar el salto de línea pegado** → causa: no recortar el `\n` final → solución: usar trim/chomp/TrimSpace antes de imprimir
- **Leer un token en vez de la línea** → causa: perder el texto tras el primer espacio → solución: leer la línea completa cuando el dato puede tener espacios

## ❓ Preguntas frecuentes

- **¿stdin y un archivo son distintos?** Conceptualmente no: stdin es un flujo; puede venir del teclado o redirigido de un archivo.
- **¿Por qué el curso usa stdin/stdout?** Es el contrato común que permite verificar los 10 lenguajes con los mismos casos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 055](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 057 ⏭️](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md)
