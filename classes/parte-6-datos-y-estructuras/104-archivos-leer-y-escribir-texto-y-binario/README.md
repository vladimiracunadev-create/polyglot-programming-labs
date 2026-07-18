# Clase 104 — Archivos: leer y escribir texto y binario

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Procesar **contenido textual** como el de un archivo: leer una línea y extraer información (palabras, caracteres). Es el modelo de la lectura de archivos, aquí por la entrada estándar para poder verificarlo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Leer una línea completa con espacios.
2. Contar palabras y caracteres.
3. Relacionarlo con la lectura de archivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Leer contenido | Una línea con espacios |
| 2 | Contar palabras | Separar por espacios |
| 3 | Contar caracteres | Longitud del texto |

## 📖 Definiciones y características

- **Contenido de texto** — los caracteres de un archivo o entrada. Clave: se procesa línea a línea.
- **Palabra** — secuencia separada por espacios. Clave: se cuenta partiendo por espacios.
- **Carácter** — cada símbolo, incluidos los espacios. Clave: la longitud total.

## 🧩 Situación

Contar líneas, palabras o caracteres (como `wc`) es el 'hola mundo' del procesamiento de archivos. Aquí el contenido llega por stdin para poder verificar el resultado.

## 🧮 Modelo

- **Entrada** (stdin): una línea de texto (puede contener espacios)
- **Salida** (stdout): `palabras=<número de palabras> caracteres=<longitud incluyendo espacios>`
- **Regla:** palabras = partes por espacio; caracteres = longitud de la línea

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola mundo` | `palabras=2 caracteres=10` |
| `abc` | `palabras=1 caracteres=3` |
| `a b c d` | `palabras=4 caracteres=7` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER linea ; palabras <- partir por espacios ; caracteres <- longitud
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
| Sintáctica | `split()` y `len()` (Python) vs. equivalentes por lenguaje. |
| Semántica | La longitud incluye los espacios; las palabras no. |
| Paradigmática | SQL cuenta con funciones de texto y agregación. |

## 🧬 El concepto en la familia

En Ruby `linea.split.size` y `linea.length`. El comando Unix `wc` hace justo esto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 104
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar espacios como palabras** → causa: palabras vacías → solución: partir por uno o más espacios
- **Olvidar quitar el salto de línea** → causa: un carácter de más → solución: recortar el `\n` final antes de contar

## ❓ Preguntas frecuentes

- **¿Por qué stdin y no un archivo?** Para poder verificar el resultado con casos; un archivo se leería igual, línea a línea.
- **¿Los caracteres incluyen espacios?** Sí: son parte del contenido; las palabras no.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 103](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 105 ⏭️](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md)
