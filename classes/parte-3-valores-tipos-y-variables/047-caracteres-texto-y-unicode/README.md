# Clase 047 — Caracteres, texto y Unicode

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Toda la escritura humana que una computadora manipula —este texto, tu nombre, un emoji— es, por dentro, una sucesión de números. Un **carácter** no se guarda como un dibujo: se guarda como un entero, su **punto de código** (*code point*), que un estándar de codificación asocia a un símbolo. La letra `A` es el número 65; la `a` minúscula es 97; el dígito `0` es 48. El objetivo de esta clase es que interiorices esa identidad entre carácter y número, porque de ella se derivan cosas que de otro modo parecen mágicas: por qué el orden alfabético "sabe" que la `A` va antes que la `B` (65 < 66), por qué `'a'` y `'A'` son distintos, y cómo convertir entre mayúsculas y minúsculas es en realidad restar 32.

Durante décadas ese diccionario carácter→número fue **ASCII**, que solo cubre 128 símbolos: suficiente para el inglés, insuficiente para la eñe, los acentos o el chino. La respuesta moderna es **Unicode**, un catálogo único que asigna un punto de código a cada carácter de cada sistema de escritura del mundo (y a los emoji), manteniendo los primeros 128 idénticos a ASCII para compatibilidad. En esta clase leemos un carácter de la entrada y mostramos su punto de código; los casos usan solo ASCII, pero la maquinaria conceptual —code point, `ord`, `unicode()`— es exactamente la misma que necesitarás para el texto multilingüe de la clase siguiente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Obtener el punto de código de un carácter.
2. Leer un único carácter de la entrada.
3. Explicar la relación entre carácter y número.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Carácter como número | Cada carácter tiene un código (ASCII/Unicode) |
| 2 | Leer un carácter | Distinto de leer una línea |
| 3 | ASCII y Unicode | Del código 0-127 a todo el texto humano |
| 4 | char vs. string | Un carácter no es una cadena de longitud 1 en todos |

## 📖 Definiciones y características

Conviene separar tres conceptos que el uso cotidiano confunde. Un **punto de código** (*code point*) es el número entero que Unicode asigna a un carácter abstracto; se escribe con la notación `U+` seguida de hexadecimal, así que `A` es `U+0041` (65 en decimal). Una **unidad de código** (*code unit*) es, en cambio, la pieza que usa una codificación concreta para almacenar ese punto: en UTF-8 mide un byte, en UTF-16 mide dos. Y un **grafema** es lo que un humano percibe como "un carácter" en pantalla, que a veces son varios puntos de código combinados (una letra con tilde, o un emoji con modificador de tono de piel). Para el texto ASCII de esta clase los tres coinciden —un carácter, un punto de código, un byte—, pero esa coincidencia es una feliz excepción, no la regla.

La codificación es el puente entre puntos de código y bytes. **ASCII** cubre 0-127 y cabe en 7 bits; fue diseñado para el inglés y quedó como subconjunto exacto de Unicode. **UTF-8** —hoy dominante en la web— es de ancho variable: usa 1 byte para los code points ASCII y hasta 4 para el resto, de modo que un archivo en inglés ocupa lo mismo que en ASCII puro pero puede representar cualquier símbolo. **UTF-16** usa 2 o 4 bytes y es el que emplean internamente Java, C# y JavaScript para sus cadenas. Unicode organiza su espacio en 17 *planos* de 65.536 posiciones; el primero, el *Basic Multilingual Plane*, contiene casi todo lo de uso común. Obtener el punto de código —`ord(c)` en Python, `unicode(c)` en SQL, `c as u32` en Rust— es preguntar "¿qué número identifica a este carácter?", con independencia de cómo se codifique en bytes.

Los términos en breve:

- **Carácter** — símbolo textual abstracto (letra, dígito, signo); internamente, un número.
- **Punto de código** — el entero que Unicode/ASCII asigna al carácter; `A` es `U+0041` = 65.
- **Unidad de código** — pieza de almacenamiento de una codificación (1 byte en UTF-8, 2 en UTF-16).
- **ASCII** — codificación de 0-127 para el inglés básico; subconjunto de Unicode.
- **Unicode** — catálogo universal que asigna un punto de código a cada carácter de todo idioma.

## 🧩 Situación

Cuando ordenas una lista de nombres, comparas contraseñas o validas que una entrada sea un dígito, no estás comparando "letras": estás comparando los números que hay debajo. La letra `A` y el entero 65 son, para la máquina, exactamente el mismo dato. Comprenderlo desmitifica media docena de comportamientos: el orden alfabético funciona porque `'A'` (65) < `'B'` (66); pasar de minúscula a mayúscula es restar 32 porque `'a'` (97) − 32 = 65; y `'a' == 'A'` es falso porque 97 ≠ 65, razón por la que las comparaciones distinguen mayúsculas salvo que las normalices.

El laboratorio lee un único carácter y muestra su punto de código. El caso `A` de `casos.json` espera `char=A codigo=65`; el caso `z` espera `char=z codigo=122`; el caso `0` espera `char=0 codigo=48` —y es instructivo, porque recuerda que el carácter `'0'` no vale 0 sino 48, un tropiezo clásico al convertir dígitos de texto a números—. Reproducir estas tres filas en diez lenguajes revela que "leer un carácter" y "obtener su código" se dicen de formas sorprendentemente distintas según el modelo de texto de cada lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): un único carácter (ASCII)
- **Salida** (stdout): `char=<c> codigo=<punto de código>`
- **Regla:** codigo = punto_de_codigo(c)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `A` | `char=A codigo=65` |
| `z` | `char=z codigo=122` |
| `0` | `char=0 codigo=48` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER c
ESCRIBIR "char=" c " codigo=" CODIGO(c)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

c = sys.stdin.readline().rstrip("\n")[0]
print(f"char={c} codigo={ord(c)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const data = readFileSync(0, "utf8");
const c = data[0];
console.log(`char=${c} codigo=${data.charCodeAt(0)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const data: string = readFileSync(0, "utf8");
const c: string = data[0];
console.log(`char=${c} codigo=${data.charCodeAt(0)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        int r = System.in.read();
        char c = (char) r;
        System.out.println("char=" + c + " codigo=" + r);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int r = Console.In.Read();
char c = (char) r;
Console.WriteLine($"char={c} codigo={r}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	b, _ := bufio.NewReader(os.Stdin).ReadByte()
	fmt.Printf("char=%c codigo=%d\n", b, b)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c = s.chars().next().unwrap();
    println!("char={} codigo={}", c, c as u32);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    int c = getchar();
    printf("char=%c codigo=%d\n", c, c);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: unicode(c) devuelve el punto de código de un carácter.
WITH chars(c) AS (VALUES ('A'), ('z'), ('0'))
SELECT printf('char=%s codigo=%d', c, unicode(c)) AS resultado
FROM chars;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$c = fgetc(STDIN);
printf("char=%s codigo=%d\n", $c, ord($c));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Tomemos el caso testigo `A`, cuya salida esperada en `casos.json` es `char=A codigo=65`, y veamos cómo cada modelo de texto llega hasta ese 65.

En **Python**, la línea `c = sys.stdin.readline().rstrip("\n")[0]` lee la línea, le quita el salto final con `rstrip("\n")` y toma el primer carácter con `[0]`. Aquí aflora una decisión de diseño de Python 3, que Ramalho subraya en *Fluent Python*: **un `str` es una secuencia de puntos de código, no de bytes**. Por eso `c` es directamente el carácter `'A'`, y `ord(c)` devuelve su punto de código, 65. La función `ord` (de *ordinal*) es la inversa de `chr`; juntas expresan la identidad carácter↔número que da nombre a la clase. La f-string produce exactamente `char=A codigo=65`.

El contraste más rico es **C**, donde `int c = getchar();` guarda el resultado en un `int`, no en un `char`. Esto no es un descuido: `getchar` devuelve `int` para poder señalar el fin de fichero con `EOF` (−1), un valor que no cabe en un `char`. Y como Kernighan y Ritchie explican, en C **un carácter ya es un entero pequeño**: no hay que "convertirlo" a su código porque nunca dejó de ser un número. Por eso `printf("char=%c codigo=%d\n", c, c)` pasa la *misma variable* `c` dos veces: `%c` la interpreta como carácter (imprime `A`) y `%d` como decimal (imprime 65). Un solo valor, dos lecturas.

**Java** ocupa un punto intermedio revelador. `int r = System.in.read();` lee un byte como `int`, y `char c = (char) r;` lo convierte con una conversión explícita. La distinción importa porque en Java el tipo `char` es una **unidad de código UTF-16 de 16 bits**, no un punto de código completo —Bloch advierte que para caracteres fuera del plano básico un solo `char` no basta—. Para el rango ASCII de esta clase la simplificación es inofensiva: `r` vale 65, `c` imprime `A`, y la salida es `char=A codigo=65`. C# hace exactamente lo mismo con `Console.In.Read()`.

**Rust** exhibe el modelo más estricto y explícito. Tras leer toda la entrada, `let c = s.chars().next().unwrap();` pide el iterador `chars()` —que, siguiendo a Klabnik y Nichols, recorre *escalares Unicode*, no bytes— y toma el primero. El tipo `char` de Rust ocupa **4 bytes** justamente para albergar cualquier punto de código. La conversión `c as u32` lo transforma en su número, 65, sin ambigüedad. Es el opuesto filosófico de C: donde C dice "un carácter siempre fue un número", Rust dice "un carácter es un escalar Unicode y su número lo pides con una conversión declarada".

Por último **Go** trabaja a nivel de byte: `bufio.NewReader(os.Stdin).ReadByte()` devuelve un `byte`, y `fmt.Printf("char=%c codigo=%d\n", b, b)` lo imprime como carácter y como número, igual que C. Funciona para ASCII porque cada carácter cabe en un byte; para texto Unicode habría que leer *runes*, el tipo de Go para puntos de código. **SQL**, declarativo, usa `unicode(c)` sobre la tabla `VALUES ('A'),('z'),('0')` para obtener el mismo 65, 122 y 48.

## 🔬 Comparación

Todos convierten un carácter en su punto de código, pero cada lenguaje revela ahí su **modelo de texto**: qué es exactamente un "carácter" y cuántos bits ocupa. Esa es la diferencia de fondo detrás de las sintaxis.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | La operación se nombra distinto: `ord(c)` (Python/PHP), `charCodeAt(0)` (JS/TS), `c as u32` (Rust), `unicode(c)` (SQL), o simplemente reusar la variable con `%d` (C/Go). |
| Semántica | Distintos modelos de "carácter": en C y Go el carácter es un byte/entero pequeño; en Java, C# y JS es una unidad de código UTF-16 de 16 bits; en Python 3 y Rust es un punto de código Unicode completo (`char` de Rust ocupa 4 bytes). Para ASCII todos coinciden en el número. |
| Paradigmática | SQL aplica la función `unicode(c)` fila a fila sobre una columna de texto, sin leer stdin; el verificador la marca como ilustrativa. |

La consecuencia práctica de estos modelos aparece más allá de ASCII. `charCodeAt` de JavaScript devuelve una *unidad UTF-16*, así que para un emoji fuera del plano básico entrega media pareja subrogada, no el punto de código real (para eso existe `codePointAt`). El `char` de 4 bytes de Rust y el `str` de puntos de código de Python evitan esa trampa por diseño. El laboratorio se mantiene en ASCII precisamente para que las diez implementaciones coincidan y el foco esté en la idea —carácter es número— antes de enfrentar la complejidad del texto multilingüe.

## 🧬 El concepto en la familia

En Ruby, `c.ord`. En Haskell, `Data.Char.ord c`, con su inverso `chr`. En C++, un `char` es directamente convertible a `int`, igual que en C. En Swift, el modelo va un paso más allá: su tipo `Character` representa un *grafema* completo (posiblemente varios puntos de código), lo que lo hace correcto pero distinto de todos los anteriores. El patrón general: cuanto más moderno el lenguaje, más se aleja "carácter" del byte crudo y más se acerca a la unidad que percibe un lector humano.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 047
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir carácter con cadena** → causa: tratar `'A'` como texto de longitud 1 en lenguajes que sí distinguen ambos tipos (Rust `char` vs. `String`, C `char` vs. `char[]`) → solución: usar el tipo carácter y su código donde corresponde.
- **Asumir solo ASCII** → causa: código que funciona con `A`-`z` pero rompe con acentos, eñes o emoji → solución: recordar que Unicode va mucho más allá de 0-127; aquí usamos ASCII para simplificar, pero el texto real es multibyte.
- **Creer que `'0'` vale 0** → causa: convertir un dígito de texto a número sin restar → solución: el carácter `'0'` es el punto de código 48; para su valor numérico se hace `c - '0'`.
- **Contar puntos de código como bytes (o viceversa)** → causa: mezclar el número de caracteres con el tamaño en la codificación → solución: distinguir code point de code unit; en UTF-8 un carácter puede ocupar de 1 a 4 bytes.

## ❓ Preguntas frecuentes

- **¿`'A'` y `'a'` tienen el mismo código?** No: 65 y 97, separados por 32. Por eso las comparaciones distinguen mayúsculas y por eso cambiar de caja es sumar o restar 32 en el rango ASCII.
- **¿Un emoji es un carácter?** Es al menos un punto de código Unicode (a veces varios combinados para formar un solo grafema), y al codificarse en UTF-8 ocupa varios bytes. "Un emoji, un carácter" es cierto a nivel de percepción, pero no siempre a nivel de code point.
- **¿Por qué `getchar` en C devuelve `int` y no `char`?** Para poder representar `EOF` (−1), un valor fuera del rango de los caracteres válidos; si devolviera `char` no habría forma de distinguir el fin de fichero de un byte legítimo.
- **¿ASCII y Unicode son incompatibles?** Al contrario: los primeros 128 puntos de código de Unicode son idénticos a ASCII por diseño, así que todo texto ASCII válido es también Unicode (y UTF-8) válido sin cambiar un solo byte.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos de datos (tipo carácter y cadenas).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), tipos base.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), representación de caracteres y cadenas en memoria.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), `str` como secuencia de puntos de código, `ord`/`chr` y Unicode.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — strings UTF-16, `charCodeAt`/`codePointAt` — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), tipo `string`.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), `char` como unidad UTF-16 vs. punto de código.
- J. Skeet — *C# in Depth* (4ª ed., Manning), `char` y `string` en UTF-16.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), `rune` = punto de código, cadenas como bytes UTF-8.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — `char` de 4 bytes = escalar Unicode — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), `char` como entero pequeño, `getchar` y `EOF`.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly), tipos de cadena.
- J. Lockhart — *Modern PHP* (O'Reilly), cadenas y funciones de carácter.

---

> [⏮️ Clase 046](../../parte-3-valores-tipos-y-variables/046-booleanos-y-valores-de-verdad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 048 ⏭️](../../parte-3-valores-tipos-y-variables/048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md)
