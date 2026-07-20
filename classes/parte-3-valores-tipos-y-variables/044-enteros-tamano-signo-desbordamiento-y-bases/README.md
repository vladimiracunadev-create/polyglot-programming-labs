# Clase 044 — Enteros: tamaño, signo, desbordamiento y bases

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La idea que vertebra esta clase es la distinción entre **valor** y **representación**. El número doscientos cincuenta y cinco es un solo valor; `255`, `0xff`, `0o377` y `0b11111111` son cuatro formas de *escribirlo* en bases 10, 16, 8 y 2. La base es un sistema posicional para nombrar el número, no una propiedad del número mismo: cambiar de base cambia el texto, nunca la cantidad. Esta separación, obvia una vez enunciada, es la que permite leer un color `#ff0000`, un permiso Unix `chmod 755` o una máscara de bits sin confundir la forma con el contenido.

Bajo esa superficie viven las otras tres palabras del título —**tamaño, signo y desbordamiento**— que son propiedades de cómo la *máquina* almacena el entero, y aquí K&R y CS:APP son la referencia. Un entero no vive en un espacio infinito: ocupa un número fijo de bits (8, 16, 32, 64) que define su rango. El **signo** decide si ese rango incluye negativos, y casi todos los lenguajes representan los negativos en **complemento a dos**, el esquema que hace que la resta sea una suma y que `-1` sea todos los bits a uno. Cuando una operación produce un valor fuera del rango, ocurre el **desbordamiento (overflow)**: en C sobre enteros sin signo el resultado "da la vuelta" módulo 2ⁿ de forma definida, mientras que sobre enteros con signo es comportamiento indefinido. Estos conceptos explican por qué el tamaño del tipo importa aunque el valor parezca pequeño.

El laboratorio se concentra en la representación en bases porque es donde las diferencias entre lenguajes se ven a simple vista: casi todos ofrecen formateo directo a hex, octal y binario, pero **C carece de especificador para binario** —hay que construirlo bit a bit— y SQL (sqlite) solo sabe formatear hexadecimal. Ese hueco de C, lejos de ser una molestia, es una ventana perfecta para entender qué hace en realidad una conversión de base.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar un mismo entero en decimal, hexadecimal, octal y binario.
2. Usar el formateo de bases de cada lenguaje.
3. Explicar por qué C no tiene `%b` y cómo se resuelve.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Valor vs. representación | El número es uno; las bases son formas de escribirlo |
| 2 | Hex, octal, binario | Bases 16, 8 y 2, comunes en programación |
| 3 | Formateo por lenguaje | Especificadores y funciones de conversión |
| 4 | El hueco de C | No hay `%b`: el binario se construye a mano |

## 📖 Definiciones y características

- **Base numérica** — sistema para escribir un número (10, 16, 8, 2). Clave: cambia la representación, no el valor.
- **Hexadecimal** — base 16 (0-9, a-f). Clave: compacta y común en memoria/colores.
- **Octal** — base 8. Clave: usada en permisos de archivos Unix.
- **Binario** — base 2 (0 y 1). Clave: la representación real en la máquina.

Conviene ver por qué la conversión de base es puramente mecánica. Para escribir un número en base *b* se le aplica repetidamente el resto y la división entera por *b*: los restos, leídos de abajo arriba, son los dígitos. Convertir `255` a binario es dividir por 2 una y otra vez recogiendo los restos (`1,1,1,1,1,1,1,1`), y a hex es dividir por 16 (`15,15` → `f,f`). Todo lenguaje con formateo de bases hace esto por dentro; cuando C nos obliga a programarlo a mano, simplemente expone el algoritmo que los demás ocultan.

El vínculo con el **tamaño y el signo** aparece en cuanto se mira el binario de un negativo. En complemento a dos, `-1` en 8 bits es `11111111` —el mismo patrón que `255` sin signo—, lo que ilustra que los bits no "saben" si son con o sin signo: es el *tipo* quien decide cómo interpretarlos. Por eso las implementaciones de esta clase usan tipos sin signo (`unsigned long` en C, `u64` en Rust) para el ejercicio de bases con enteros no negativos: así el binario se lee de forma directa sin la complicación del signo. El **hexadecimal** es popular precisamente porque cada dígito hex resume exactamente cuatro bits, de modo que `ff` = `1111 1111` de un vistazo; y el **octal**, con tres bits por dígito, sobrevive sobre todo en los permisos de archivos Unix (`chmod 644`).

## 🧩 Situación

El color `#ff0000` es rojo: `ff` es 255 en hexadecimal, es decir, el canal rojo al máximo. Convertir entre bases es cotidiano en programación de bajo nivel, gráficos, redes (máscaras y direcciones) y permisos de archivos. Elegimos mostrar `255`, `10` y `1` porque `255` es el máximo de un byte y da el binario completo `11111111`, un patrón que todo programador debe reconocer al instante; `10` distingue con claridad las cuatro bases (`a`, `12`, `1010`); y `1` verifica el caso mínimo. Cada lenguaje formatea a su manera, y C, al carecer de `%b`, nos obliga a construir el binario y con ello a entenderlo.

## 🧮 Modelo

- **Entrada** (stdin): una línea `n` (entero no negativo)
- **Salida** (stdout): `dec=<n> hex=<hex minúscula> oct=<octal> bin=<binario>`
- **Regla:** misma n en base 10, 16, 8 y 2 (sin prefijos ni ceros a la izquierda)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `255` | `dec=255 hex=ff oct=377 bin=11111111` |
| `10` | `dec=10 hex=a oct=12 bin=1010` |
| `1` | `dec=1 hex=1 oct=1 bin=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR "dec=" n " hex=" BASE(n,16) " oct=" BASE(n,8) " bin=" BASE(n,2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"dec={n} hex={n:x} oct={n:o} bin={n:b}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`dec=${n} hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`dec=${n} hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}`);
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
        int n = Integer.parseInt(br.readLine().trim());
        System.out.printf("dec=%d hex=%s oct=%s bin=%s%n", n,
                Integer.toHexString(n), Integer.toOctalString(n), Integer.toBinaryString(n));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Globalization;

int n = int.Parse(Console.In.ReadToEnd().Trim(), CultureInfo.InvariantCulture);
Console.WriteLine($"dec={n} hex={Convert.ToString(n, 16)} oct={Convert.ToString(n, 8)} bin={Convert.ToString(n, 2)}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("dec=%d hex=%x oct=%o bin=%b\n", n, n, n, n)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u64 = s.trim().parse().unwrap();
    println!("dec={n} hex={:x} oct={:o} bin={:b}", n, n, n);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    unsigned long n;
    if (scanf("%lu", &n) != 1) return 1;

    /* C no tiene especificador para binario: se construye a mano. */
    char bin[65];
    int i = 0;
    if (n == 0) {
        bin[i++] = '0';
    } else {
        char tmp[65];
        int j = 0;
        unsigned long t = n;
        while (t > 0) {
            tmp[j++] = (char) ('0' + (t & 1UL));
            t >>= 1;
        }
        while (j > 0) {
            bin[i++] = tmp[--j];
        }
    }
    bin[i] = '\0';

    printf("dec=%lu hex=%lx oct=%lo bin=%s\n", n, n, n, bin);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL (sqlite) solo formatea hexadecimal con %x; octal y binario no son nativos.
WITH nums(n) AS (VALUES (255), (10), (1))
SELECT printf('dec=%d hex=%x', n, n) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
printf("dec=%d hex=%s oct=%s bin=%s\n", $n, dechex($n), decoct($n), decbin($n));
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el caso `255` de [`casos.json`](casos.json), cuya salida exacta es `dec=255 hex=ff oct=377 bin=11111111`. Es el caso más revelador porque `255` es el byte lleno.

En **Python**, todo el trabajo cabe en una f-string: `f"dec={n} hex={n:x} oct={n:o} bin={n:b}"`. Cada sufijo tras los dos puntos es un *especificador de formato* que le pide al lenguaje representar el mismo entero `n` en otra base: `:x` da hexadecimal en minúscula (`ff`), `:o` octal (`377`) y `:b` binario (`11111111`). No hay cuatro números: hay uno, `255`, mirado por cuatro ventanas. El valor nunca cambia; solo cambia el texto que produce cada especificador.

En **C** se hace visible el algoritmo que Python esconde. El hex y el octal sí tienen especificador (`%lx`, `%lo`), pero el binario no existe en `printf`, así que el autor lo fabrica. El bloque construye la cadena de bits: mientras `t > 0`, la expresión `(char) ('0' + (t & 1UL))` calcula el bit menos significativo —`t & 1UL` aísla el último bit y sumarlo a `'0'` lo convierte en el carácter `'0'` o `'1'`— y `t >>= 1` desplaza `t` un bit a la derecha, descartando el bit ya procesado. Para `255` esto genera ocho unos, pero *en orden inverso* (del bit menos al más significativo), por eso se guardan en `tmp` y luego el segundo bucle los copia de atrás hacia adelante a `bin`, dejando `11111111`. El `if (n == 0)` cubre el caso especial en que el bucle no correría ni una vez. Finalmente `printf("dec=%lu hex=%lx oct=%lo bin=%s\n", n, n, n, bin)` imprime las tres primeras bases con especificadores y la cuarta como la cadena que construimos: `dec=255 hex=ff oct=377 bin=11111111`. Este bucle *es*, literalmente, el método de restos y divisiones por 2 descrito arriba, con `& 1` haciendo de resto y `>> 1` de división.

En **Go** y **Rust** vuelve la comodidad: Go usa `fmt.Printf("dec=%d hex=%x oct=%o bin=%b\n", n, n, n, n)` con el verbo `%b` que C no tiene, y Rust `println!("dec={n} hex={:x} oct={:o} bin={:b}", n, n, n)` con la misma familia de especificadores. Un detalle de tipos: Rust declara `let n: u64` (sin signo) precisamente para que `{:b}` de un negativo no aparezca nunca en este ejercicio de enteros no negativos, mientras que C usa `unsigned long` por la misma razón. Comparar C con Go/Rust deja la moraleja: el `%b` no es magia del lenguaje, es ese bucle de desplazamientos empaquetado en la biblioteca.

## 🔬 Comparación

La conversión de base separa a los lenguajes en dos grupos: los que traen formateo directo a las cuatro bases y los que dejan huecos. Ese hueco no es un defecto arbitrario, sino el rastro de qué consideró indispensable cada diseño: hex y octal han sido históricamente universales; el binario, más reciente como formato de salida, faltó en el `printf` de C y en muchos SQL.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `f"{n:x}"` (Python), `n.toString(16)` (JS/TS), `%x/%o/%b` (Go/Rust), `Convert.ToString(n, 2)` (C#), `Integer.toBinaryString` (Java). |
| Semántica | C **no** tiene `%b`: el binario se genera con un bucle de `& 1` y `>> 1` sobre los bits. |
| Valor vs. representación | Ningún lenguaje cambia el número: `255`, `ff`, `377` y `11111111` son el mismo valor en cuatro bases. |
| Tamaño y signo | Rust (`u64`) y C (`unsigned long`) usan tipos sin signo para que el binario de un no negativo se lea directo, sin complemento a dos. |
| Paradigmática | SQL (sqlite) solo formatea hex con `%x`; octal y binario no son nativos y se omiten. |

## 🧬 El concepto en la familia

- **Scripting dinámico** (Ruby): un solo método `to_s(base)` cubre todas las bases: `n.to_s(16)`, `n.to_s(8)`, `n.to_s(2)`. Perl y Python resuelven lo mismo con `sprintf`/f-strings.
- **C/llaves** (C++): los manipuladores de stream `std::hex` y `std::oct` cambian la base de salida de `cout`, pero —igual que en C— no hay uno para binario; se recurre a `std::bitset<8>(n)` para obtener la cadena de bits.
- **JVM** (Kotlin/Java): Java ofrece `Integer.toHexString/toOctalString/toBinaryString` y Kotlin añade `n.toString(radix)` genérico, más cercano al estilo de Ruby.
- **Ensamblador / bajo nivel**: en este nivel no hay "bases"; se trabaja con los bits crudos y la base es solo la notación que el ensamblador o el depurador elige para mostrarlos, lo que refuerza que la base es representación, no valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 044
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Buscar `%b` en C** → causa: asumir que existe como en Go/Rust → solución: construir el binario con un bucle de desplazamientos (`& 1` y `>> 1`).
- **Obtener hex en mayúscula** → causa: usar `%X`/`X` en vez de `%x`/`x` → solución: elegir el especificador de minúsculas que pide el contrato.
- **Añadir prefijos no pedidos** → causa: algunas funciones devuelven `0xff` u `0o377` → solución: usar el formateo crudo sin prefijo, tal como fija el contrato.
- **Dejar ceros a la izquierda** → causa: formatear con ancho fijo (`%08b`) rellena con ceros → solución: no fijar ancho, para que `1` salga `1` y no `00000001`.
- **Confundir el binario de un negativo con el de su magnitud** → causa: en complemento a dos `-1` es `11111111`, no `-1` → solución: en este ejercicio se usan tipos sin signo y enteros no negativos, evitando la ambigüedad.

## ❓ Preguntas frecuentes

- **¿Por qué C no tiene binario en printf?** El estándar del `printf` heredó hex y octal por su uso histórico en direcciones y permisos, pero nunca incorporó `%b`; se implementa a mano con unas pocas líneas.
- **¿El valor cambia entre bases?** No: `255`, `ff`, `377` y `11111111` son el mismo número escrito de forma distinta. La base es notación, no cantidad.
- **¿Qué relación hay entre hex y binario?** Cada dígito hexadecimal codifica exactamente cuatro bits, así que `ff` = `1111 1111`. Por eso el hex es la forma compacta preferida para leer patrones de bits.
- **¿Qué tiene que ver el tamaño del entero con esto?** El tamaño (8, 32, 64 bits) fija cuántos dígitos binarios como máximo tendrá el número y cuándo se produce desbordamiento; con `unsigned` el resultado da la vuelta módulo 2ⁿ, con signo el estándar de C lo deja indefinido.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. de tipos primitivos y representación.
- B. C. Pierce — *Types and Programming Languages* (MIT Press), sobre tipos y seguridad.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. de representación de datos en memoria.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), cap. de tipos y operadores de bits (`&`, `>>`) y complemento a dos.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 043](../../parte-3-valores-tipos-y-variables/043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 045 ⏭️](../../parte-3-valores-tipos-y-variables/045-numeros-reales-punto-flotante-precision-y-decimales/README.md)
