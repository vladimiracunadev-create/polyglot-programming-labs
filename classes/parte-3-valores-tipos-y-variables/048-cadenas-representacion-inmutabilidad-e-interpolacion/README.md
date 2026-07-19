# Clase 048 — Cadenas: representación, inmutabilidad e interpolación

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La cadena de texto es el tipo compuesto que más usarás en tu vida como programador —nombres, mensajes, rutas, respuestas de red— y, paradójicamente, uno de los que más decisiones de diseño esconde. Esta clase practica tres operaciones aparentemente triviales —leer una palabra, **interpolarla** en un saludo y medir su **longitud**— para sacar a la luz esas decisiones. La interpolación (`f"...{x}"` en Python, `` `${x}` `` en JavaScript, `%s` en `printf`) es azúcar sintáctica para construir texto insertando valores, y cada lenguaje la escribe distinto. La longitud, por su parte, plantea una pregunta engañosa: ¿longitud *en qué*? En bytes, en unidades de código, en caracteres? La respuesta varía de un lenguaje a otro, y solo coincide —como aquí— cuando el texto es ASCII puro.

Detrás de ambas operaciones vive un concepto central que esta clase quiere fijar: la **inmutabilidad**. En Python, Java, C#, Go, Rust y JavaScript una cadena no se modifica en el sitio; cada vez que "cambias" una, en realidad **creas una nueva**. Esa decisión —que Bloch y Ramalho justifican por seguridad, posibilidad de compartir y de usar cadenas como claves de tablas hash— tiene consecuencias de rendimiento (concatenar en un bucle puede ser costoso) y de corrección (una cadena que pasas a otra función no puede ser alterada a tus espaldas). Verás por qué medir la longitud es barato pero "modificar" no lo es, y cómo esa asimetría nace directamente de la inmutabilidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Interpolar una variable de texto en una cadena.
2. Obtener la longitud de una cadena.
3. Reconocer la inmutabilidad de las cadenas donde aplica.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interpolación | Insertar valores dentro de una cadena |
| 2 | Longitud | Cuántos caracteres tiene |
| 3 | Inmutabilidad | En muchos lenguajes la cadena no se modifica, se recrea |
| 4 | Bytes vs. caracteres | La longitud puede medir distinto |

## 📖 Definiciones y características

Una **cadena** es una secuencia ordenada de caracteres, pero cómo se representa esa secuencia en memoria distingue a las familias de lenguajes, y Scott dedica buena parte de su tratamiento de tipos a ello. Hay dos grandes modelos. El primero es el de C: una cadena es un array de bytes **terminado en un byte NUL** (`\0`), sin longitud almacenada; medirla obliga a recorrerla contando hasta el cero, que es justo lo que hace `strlen`. El segundo es el moderno: un objeto que guarda su longitud explícita junto a los datos, de modo que `len()` es una consulta instantánea. Python, Java, C#, Go y Rust siguen este segundo modelo, cada uno con su codificación interna (UTF-16 en Java/C#, UTF-8 en Go/Rust).

La **inmutabilidad** es la característica que más consecuencias tiene. Una cadena inmutable no puede alterarse tras crearse: toda operación que "cambie" texto (concatenar, reemplazar, poner en mayúsculas) devuelve una cadena nueva y deja la original intacta. Esto habilita optimizaciones importantes —el *interning*, por el que el runtime comparte una única copia de cadenas idénticas (los literales de Java van a un *string pool*), y el cacheo del hash para usarlas como claves— y aporta seguridad: si le pasas una cadena a otra función, tienes la garantía de que no la modificará. La contrapartida es que concatenar en un bucle crea objetos intermedios; de ahí que existan `StringBuilder` (Java/C#), `str.join` (Python) o `strings.Builder` (Go). C es la excepción notable: sus arrays de `char` **sí son mutables**, con la responsabilidad —y el riesgo de desbordamiento— que eso conlleva.

Sobre la **longitud**, la sutileza es qué se cuenta. Java, C# y JavaScript devuelven el número de *unidades de código UTF-16*; Go y Rust, el número de *bytes* de la codificación UTF-8; Python 3, el número de *puntos de código*. Para el texto ASCII de esta clase los tres criterios coinciden, pero con un carácter multibyte divergen: `len("é")` es 1 en Python y 2 en Go.

Los términos en breve:

- **Cadena** — secuencia de caracteres; el tipo para todo texto.
- **Interpolación** — insertar el valor de una variable dentro de una cadena (`f"...{x}"`, `${x}`, `%s`).
- **Longitud** — número de unidades de la cadena; su unidad (byte, code unit, code point) depende del lenguaje.
- **Inmutabilidad** — en Python, Java, C#, JS, Go y Rust la cadena no se modifica in situ: se crea una nueva.
- **Interning** — compartir una sola copia de cadenas idénticas para ahorrar memoria y acelerar comparaciones.

## 🧩 Situación

"Hola, Ada. Tu nombre tiene 3 letras." Un saludo personalizado y un contador de caracteres están en el corazón de casi cualquier interfaz: formularios que validan longitud mínima, mensajes que insertan el nombre del usuario, límites de caracteres en un campo. Son operaciones tan cotidianas que parecen no tener misterio, y precisamente por eso son un excelente banco de pruebas: al hacerlas en diez lenguajes, las diferencias que emergen no son accidentales, sino ventanas a cómo cada uno modela el texto.

El laboratorio recibe una palabra ASCII y produce `hola=<palabra> longitud=<n>`. El caso `Ada` de `casos.json` espera `hola=Ada longitud=3`; el caso `polyglot` espera `hola=polyglot longitud=8`. Como el texto es ASCII, todas las nociones de longitud coinciden y las diez implementaciones dan el mismo número —pero la interpolación se escribe de seis formas distintas y la longitud se calcula sobre bytes en unos lenguajes y sobre code units en otros. Ver ese contraste con un caso trivial prepara el terreno para cuando la palabra traiga acentos y los números dejen de coincidir.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `hola=<palabra> longitud=<número de caracteres>`
- **Regla:** longitud = |palabra|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `hola=Ada longitud=3` |
| `Bo` | `hola=Bo longitud=2` |
| `polyglot` | `hola=polyglot longitud=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w
ESCRIBIR "hola=" w " longitud=" LONGITUD(w)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
print(f"hola={w} longitud={len(w)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
console.log(`hola=${w} longitud=${w.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`hola=${w} longitud=${w.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        System.out.println("hola=" + w + " longitud=" + w.length());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"hola={w} longitud={w.Length}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	fmt.Printf("hola=%s longitud=%d\n", w, len(w))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    println!("hola={} longitud={}", w, w.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[256];
    if (scanf("%255s", buf) != 1) return 1;
    printf("hola=%s longitud=%d\n", buf, (int) strlen(buf));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: length(w) cuenta los caracteres de una cadena.
WITH palabras(w) AS (VALUES ('Ada'), ('Bo'), ('polyglot'))
SELECT printf('hola=%s longitud=%d', w, length(w)) AS resultado
FROM palabras;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
printf("hola=%s longitud=%d\n", $w, strlen($w));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el caso testigo `Ada`, cuya salida esperada en `casos.json` es `hola=Ada longitud=3`, y veamos qué modelo de cadena aplica cada lenguaje.

En **Python**, `w = sys.stdin.readline().strip()` lee la línea y `strip()` elimina espacios y el salto final, dejando `w = "Ada"`. La línea siguiente concentra las dos operaciones: dentro de la f-string, `` {w} `` interpola el texto —Python evalúa la expresión y la inserta— y `` {len(w)} `` mide la longitud. Aquí `len` cuenta **puntos de código**: como `w` es un `str` (secuencia de code points), devuelve 3. La salida es exactamente `hola=Ada longitud=3`. Nota que `w` es inmutable: `strip()` no modificó la línea original, sino que devolvió una cadena nueva ya recortada.

El contraste esencial es **C**, que expone el modelo más antiguo. `char buf[256];` reserva un array mutable, y `scanf("%255s", buf)` lee una palabra (deteniéndose en el espacio) copiando sus bytes y **añadiendo automáticamente el terminador NUL** `\0`. Por eso `strlen(buf)` funciona: recorre el array byte a byte contando hasta encontrar ese cero, y devuelve 3. La diferencia de fondo con Python es doble: la longitud no está guardada (se calcula recorriendo), y la cadena es mutable (podrías escribir `buf[0] = 'X'`). El `printf("hola=%s longitud=%d\n", buf, (int) strlen(buf))` usa `%s` para interpolar el texto y `%d` para el número; el `(int)` convierte el `size_t` que devuelve `strlen` al tipo que espera `%d`.

**Go** ilumina la cuestión de "longitud en qué unidad". `w := strings.TrimSpace(line)` recorta, y `fmt.Printf("hola=%s longitud=%d\n", w, len(w))` interpola con `%s`. Pero aquí `len(w)` cuenta **bytes**, no caracteres: como Donovan y Kernighan explican, en Go una cadena es una secuencia inmutable de bytes UTF-8. Para `"Ada"` (ASCII, un byte por letra) el resultado es 3 y coincide con Python; para `"café"` daría 5, no 4, porque la `é` ocupa dos bytes. Si quisiéramos contar caracteres usaríamos `utf8.RuneCountInString`. Rust comparte este modelo: su `w.len()` también devuelve bytes de la codificación UTF-8.

**Java** representa el tercer modelo. `br.readLine().trim()` produce un `String` inmutable, y `w.length()` devuelve el número de **unidades de código UTF-16**. La concatenación `"hola=" + w + " longitud=" + w.length()` es interpolación por el operador `+`; cada `+` sobre cadenas inmutables crea, en teoría, un objeto nuevo (el compilador lo optimiza con un builder). Para `Ada` da 3, igual que todos. **SQL**, declarativo, aplica `length(w)` sobre la tabla `VALUES ('Ada'),('Bo'),('polyglot')` y el verificador lo marca como ilustrativo.

## 🔬 Comparación

Las tres operaciones dan el mismo resultado en ASCII, pero cada lenguaje las apoya en un modelo de cadena distinto: dónde vive la longitud, qué unidad cuenta, y si el texto es o no mutable. La tabla resume esas divergencias.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | La longitud y la interpolación se escriben distinto: `len(w)` (Python/Go), `w.length` (Java) / `.length` (JS/TS), `w.len()` (Rust), `strlen(w)` (C), `length(w)` (SQL); interpolación con f-string, plantilla `${}`, `+` o `%s`. |
| Semántica | La unidad de `len` cambia: puntos de código en Python 3, unidades UTF-16 en Java/C#/JS, bytes UTF-8 en Go/Rust. En C no hay longitud guardada: `strlen` la calcula recorriendo hasta el NUL. Para ASCII todas dan el mismo número. |
| Paradigmática | SQL usa `length(w)` fila a fila sobre una columna declarada con `VALUES`, sin leer stdin; el verificador lo marca como ilustrativo. |

Una diferencia que la tabla no captura del todo es la **mutabilidad**. En Python, Java, C#, JS, Go y Rust la cadena es inmutable —"modificarla" crea otra—, con las ventajas de compartición e *interning* ya vistas. C rompe el molde: sus arrays de `char` son mutables y no llevan longitud, lo que da máximo control a costa de máxima responsabilidad (un `strcpy` sin cuidar el tamaño desborda el buffer). Esta es, en el fondo, la misma tensión entre seguridad y control que atraviesa toda la comparación entre lenguajes de alto y bajo nivel.

## 🧬 El concepto en la familia

En Ruby, `w.length`, con cadenas *mutables* (una rareza entre los lenguajes de alto nivel). En Haskell, `length w` sobre una lista de caracteres inmutable. En C++, `w.size()` sobre un `std::string` mutable que sí guarda su longitud. Todos coinciden en ASCII y divergen con Unicode multibyte, y todos, salvo los de la familia C, ocultan la gestión de memoria del texto tras un tipo de cadena de primera clase. El eje que ordena a la familia es cuánto abstrae cada lenguaje entre "la secuencia de caracteres que el programador ve" y "los bytes que hay en memoria".

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 048
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir que longitud = caracteres siempre** → causa: olvidar que la unidad de `len` depende del lenguaje y de la codificación → solución: recordar que en Go/Rust `len` cuenta bytes UTF-8; usa `utf8.RuneCountInString` (Go) o `w.chars().count()` (Rust) para contar caracteres.
- **Modificar una cadena in situ** → causa: esperar mutación en Java/Python/JS donde la cadena es inmutable → solución: asignar el resultado (`s = s.replace(...)`); toda operación devuelve una cadena nueva.
- **Concatenar en un bucle con `+`** → causa: crear una cadena intermedia por cada iteración sobre texto inmutable, con coste cuadrático → solución: usar `StringBuilder` (Java/C#), `str.join` (Python) o `strings.Builder` (Go).
- **Olvidar el terminador NUL en C** → causa: reservar un buffer justo del tamaño del texto sin espacio para el `\0` → solución: dimensionar siempre un byte más y usar límites como `%255s` en `scanf`.

## ❓ Preguntas frecuentes

- **¿Por qué las cadenas son inmutables?** Por seguridad (nadie puede alterar tu cadena a tus espaldas) y por optimización: permite compartir una copia entre referencias, cachear su hash para usarlas como claves de diccionario, e *internar* literales idénticos. Modificar crea una copia nueva.
- **¿`len` en Go da caracteres?** No, da bytes de la codificación UTF-8; para contar caracteres Unicode se usa `utf8.RuneCountInString`. En ASCII coinciden porque cada carácter ocupa un byte.
- **¿Qué es el interning de cadenas?** Un mecanismo por el que el runtime mantiene una única copia de cada cadena literal distinta (el *string pool* de Java, por ejemplo), de modo que dos literales idénticos comparten memoria y su comparación por identidad es inmediata.
- **¿La interpolación es más que estética?** Sí: además de legible, muchas implementaciones la compilan a construcción eficiente de texto. Pero cuidado en SQL: interpolar entradas de usuario directamente en una consulta abre la puerta a inyección; ahí se usan parámetros, no interpolación.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos de datos (tipo cadena, longitud y diseño).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), tipos base y su semántica.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), representación de cadenas en memoria (longitud explícita vs. terminada en NUL).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), inmutabilidad de `str`, `bytes` vs. `str` e interpolación.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — strings inmutables UTF-16 y plantillas — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), tipo `string` y literales de plantilla.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), `String` inmutable y `StringBuilder` para concatenación.
- J. Skeet — *C# in Depth* (4ª ed., Manning), `string` inmutable e interpolación con `$""`.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), cadenas como bytes UTF-8 inmutables, `len` vs. runes.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — `String` vs. `&str`, UTF-8, `len` en bytes — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), cadenas terminadas en NUL, `strlen`, arrays de `char` mutables.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly), tipos de cadena y `length`.
- J. Lockhart — *Modern PHP* (O'Reilly), cadenas, interpolación y funciones de longitud.

---

> [⏮️ Clase 047](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 049 ⏭️](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md)
