# Clase 104 — Archivos: leer y escribir texto y binario

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la entrada/salida de archivos como lo que realmente es: un **flujo** (*stream*) de bytes que fluye entre tu programa y el mundo exterior —el disco, la red, el teclado, la pantalla—. Un archivo no se «lee de golpe» por arte de magia; se abre, se recorre de principio a fin transfiriendo trozos, y se cierra. En ese recorrido hay dos decisiones que gobiernan todo: si el flujo se trata como **texto** (una secuencia de caracteres con una codificación y saltos de línea que se normalizan) o como **binario** (bytes crudos, sin interpretar), y cómo el **buffering** amortigua el altísimo coste de hablar con el sistema operativo. Esta clase usa la operación textual más elemental —contar palabras y caracteres de una línea, el corazón del comando `wc`— para fijar el modelo mental de la lectura de archivos. El contenido llega por la entrada estándar, que no es más que un flujo como el de un archivo, para que el resultado se pueda verificar.

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

Un **flujo** (*stream*) es la abstracción central de la E/S: una fuente o destino de datos que se consume secuencialmente, sin necesidad de tener todo el contenido en memoria a la vez. Kernighan y Ritchie construyen sobre ella toda la biblioteca de C —`fopen` abre un flujo, `fgets`/`fread` lo leen, `fwrite` lo escribe, `fclose` lo cierra— y ese mismo trío abrir-usar-cerrar reaparece, con otros nombres, en los diez lenguajes. Cerrar importa por una razón concreta: cada archivo abierto ocupa un **descriptor** (*file descriptor*), un recurso finito que el sistema operativo administra; no cerrarlo lo deja retenido hasta que el proceso muera o se agote el límite.

El **modo texto** frente al **modo binario** es la distinción que más sorpresas causa. En modo texto, el flujo interpreta los bytes según una **codificación** (hoy casi siempre UTF-8) para producir caracteres, y **normaliza los saltos de línea** —en Windows, el par `\r\n` del disco se traduce a un solo `\n` al leer y viceversa al escribir. En modo binario no hay interpretación alguna: los bytes entran y salen tal cual, y por eso es el único modo correcto para imágenes, ejecutables o cualquier formato donde un byte `0x0D` no significa «fin de línea» sino un dato. Confundir los modos corrompe silenciosamente los binarios; tratar texto como bytes rompe los acentos y emojis, cuyos caracteres ocupan varios bytes en UTF-8 —de ahí que la *longitud en caracteres* y la *longitud en bytes* no siempre coincidan.

El **buffering** es la razón de que la E/S sea rápida. Cada llamada al sistema operativo (leer del disco, escribir en pantalla) es cara —cruza la frontera entre tu programa y el núcleo—, así que las bibliotecas acumulan los datos en un **búfer** en memoria y hablan con el sistema por grandes bloques en lugar de byte a byte. Por eso Java envuelve el flujo en un `BufferedReader` y Go en un `bufio.Reader`: amortizan miles de llamadas costosas en unas pocas. La contrapartida del buffering al escribir es que los datos pueden quedar «atrapados» en el búfer sin llegar al destino hasta que se **vacía** (*flush*) —lo que ocurre, entre otros momentos, al **cerrar** el flujo. Ahí se cierra el círculo: cerrar no es un trámite, es lo que garantiza que lo escrito realmente se persista y que el descriptor se libere.

## 🧩 Situación

Contar líneas, palabras y caracteres es el «hola mundo» del procesamiento de archivos: el venerable comando `wc` de Unix no hace más que eso, y sin embargo toca cada pieza del modelo —abrir un flujo, recorrerlo trozo a trozo, decidir qué cuenta como palabra, distinguir un carácter de un byte, cerrar. Es la tarea con la que se estrena todo el que aprende a leer archivos porque obliga a enfrentar las preguntas reales: ¿el salto de línea final cuenta como carácter?, ¿dos espacios seguidos son una palabra vacía?, ¿la longitud es en caracteres o en bytes? Aquí el contenido llega por la entrada estándar en lugar de por un archivo con nombre, pero es exactamente el mismo flujo: si mañana cambias `stdin` por el resultado de abrir «datos.txt», el resto del código no se entera. Esa es la potencia de la abstracción de flujo —la fuente cambia, el procesamiento no.

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

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

linea = sys.stdin.readline().rstrip("\n")
palabras = len(linea.split())
print(f"palabras={palabras} caracteres={len(linea)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        int palabras = linea.trim().isEmpty() ? 0 : linea.trim().split("\\s+").length;
        System.out.println("palabras=" + palabras + " caracteres=" + linea.length());
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
int palabras = linea.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
Console.WriteLine($"palabras={palabras} caracteres={linea.Length}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

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
	linea := strings.TrimRight(line, "\r\n")
	palabras := len(strings.Fields(linea))
	fmt.Printf("palabras=%d caracteres=%d\n", palabras, len(linea))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    let palabras = linea.split_whitespace().count();
    println!("palabras={} caracteres={}", palabras, linea.len());
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char buf[4096];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    int caracteres = (int) strlen(buf);
    int palabras = 0, dentro = 0;
    for (int i = 0; buf[i]; i++) {
        if (isspace((unsigned char) buf[i])) {
            dentro = 0;
        } else if (!dentro) {
            dentro = 1;
            palabras++;
        }
    }
    printf("palabras=%d caracteres=%d\n", palabras, caracteres);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: longitud con length(); palabras con funciones de texto (ilustrativo).
WITH t(linea) AS (VALUES ('hola mundo'))
SELECT printf('palabras=%d caracteres=%d',
       length(linea) - length(replace(linea, ' ', '')) + 1, length(linea)) AS resultado
FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$linea = rtrim(fgets(STDIN), "\r\n");
$palabras = $linea === "" ? 0 : count(preg_split('/\s+/', trim($linea)));
echo "palabras=$palabras caracteres=" . strlen($linea) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `hola mundo`, que debe producir `palabras=2 caracteres=10`. Las diez implementaciones leen la línea, la limpian, cuentan sus palabras y su longitud; miremos tres que muestran distintos niveles de abstracción sobre el flujo.

En **Python**, `sys.stdin.readline()` lee una línea del flujo de entrada —incluido el `\n` final— y `.rstrip("\n")` lo recorta, dejando `"hola mundo"` (10 caracteres). El `.split()` sin argumentos parte por cualquier tramo de espacios en blanco y descarta los vacíos, así que `["hola", "mundo"]` tiene `len` 2. `len(linea)` cuenta 10 caracteres. Nótese que `readline` ya trae el buffering de Python por debajo: no toca el sistema operativo carácter a carácter.

En **Java**, la abstracción del flujo es explícita y por capas. `new InputStreamReader(System.in)` envuelve el flujo de bytes crudo y lo decodifica a caracteres según la codificación; `new BufferedReader(...)` añade el búfer que amortiza las llamadas al sistema. `br.readLine()` devuelve la línea *sin* el salto de línea —Java ya lo normaliza—, de modo que `linea.length()` da 10 directamente. El `split("\\s+")` sobre la línea recortada produce dos elementos. Aquí se ve el ensamblaje manual de la tubería lector→decodificador→búfer que otros lenguajes ocultan.

En **C**, se trabaja al ras del metal. `fgets(buf, sizeof buf, stdin)` lee hasta un salto de línea o hasta llenar el búfer de 4096 bytes, dejando el `\n` dentro; `buf[strcspn(buf, "\r\n")] = '\0'` lo sustituye por el terminador de cadena. `strlen` cuenta 10 **bytes** —que aquí coinciden con caracteres porque el texto es ASCII, pero divergirían con acentos en UTF-8. Las palabras se cuentan con una máquina de estados: la bandera `dentro` distingue si vamos «dentro» de una palabra, e incrementa el contador solo en la transición de espacio a no-espacio. Ese bucle es, literalmente, lo que hacen por dentro los `split` de los demás lenguajes.

Los tres imprimen `palabras=2 caracteres=10`; el verificador comprueba que las diez coincidan carácter a carácter con `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `split()` y `len()` (Python) vs. equivalentes por lenguaje. |
| Semántica | La longitud incluye los espacios; las palabras no. |
| Paradigmática | SQL cuenta con funciones de texto y agregación. |

La diferencia más honda entre los diez es **cuánto de la tubería de E/S te obligan a construir a mano**. Python (`readline`), Go (`bufio.NewReader`) y C# (`Console.In`) te dan un lector de líneas casi listo; Java te hace ensamblar `InputStreamReader` + `BufferedReader`, exponiendo las capas de decodificación y buffering que los demás fusionan; C te da `fgets` sobre un búfer que tú declaras, con el tamaño y la gestión del salto de línea a tu cargo. Otra frontera real es **carácter frente a byte**: `linea.length()` en Java y `len(linea)` en Python cuentan *caracteres* (unidades de código), mientras `strlen` en C y `len(linea)` en Go cuentan *bytes* —una distinción invisible en ASCII pero decisiva en cuanto aparece un carácter multibyte de UTF-8, donde una `ñ` suma un carácter pero dos bytes. Por último, la **normalización de saltos de línea** difiere: en modo texto, un archivo con finales `\r\n` de Windows se ve con `\n` limpios en la mayoría de lenguajes, pero varias implementaciones recortan explícitamente `\r` y `\n` para no depender del modo —un recordatorio de que el mismo texto puede tener una longitud distinta según el sistema que lo escribió.

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

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 103](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 105 ⏭️](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md)
