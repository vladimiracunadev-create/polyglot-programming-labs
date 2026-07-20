# Clase 129 — Referencias, apuntadores y direcciones

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Los datos del heap de la clase 128 no se manipulan directamente: se accede a ellos *a través* de algo que dice dónde están. Ese «algo» —una **dirección**, un **puntero** o una **referencia**— es la idea de **indirección**, una de las más poderosas y peligrosas de la programación. Esta clase la ilumina con una operación que parece inocente: acceder a `lista[indice]`. El *porqué* es que `arr[i]` no es una operación primitiva, sino azúcar sobre aritmética de direcciones: «toma la dirección base del arreglo, avanza `i` elementos, y lee lo que hay ahí». En C esa aritmética es visible (`*(arr + i)`); en Python, Java o Go está escondida bajo el corchete, pero el mecanismo subyacente es idéntico. Bryant & O'Hallaron muestran cómo el propio conjunto de instrucciones de la máquina ofrece *modos de direccionamiento* con base y desplazamiento escalado precisamente para que `arr[i]` sea una sola instrucción. Entender la indirección explica los punteros de C, las referencias de Java, el aliasing, el *segmentation fault* y por qué dos variables pueden apuntar al mismo objeto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Acceder a un elemento de una secuencia por su índice.
2. Explicar la indirección: acceder a un dato a través de una referencia a su posición.
3. Relacionar un índice con una dirección: base más desplazamiento.
4. Distinguir un puntero (dirección explícita, con aritmética) de una referencia gestionada.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Indirección | Acceder al dato a través de quien lo señala, no directamente |
| 2 | Índice como dirección | `arr[i]` equivale a base + i·tamaño del elemento |
| 3 | Referencia vs. puntero | Ambos designan un dato; difieren en control y seguridad |

## 📖 Definiciones y características

Una **referencia** es un valor que designa a otro dato en lugar de contenerlo. Cuando en Java escribes `List<Integer> a = b;`, `a` no copia la lista: ambas variables *referencian* el mismo objeto del heap. Modificar a través de una afecta a la otra —el fenómeno del *aliasing*—. La referencia es indirección con red de seguridad: no puedes hacer aritmética con ella ni apuntarla a una dirección arbitraria.

Un **puntero** es una referencia explícita que guarda literalmente una dirección de memoria, un número. En C, `arr` es la dirección del primer elemento, y `arr + i` calcula la dirección del elemento `i` sabiendo el tamaño de cada elemento —el compilador escala el desplazamiento por `sizeof`—. El operador `*` *desreferencia*: va a esa dirección y lee o escribe el valor. Con ese poder viene el peligro: un puntero puede apuntar a una dirección inválida, y desreferenciarlo produce el temido *segmentation fault*.

Un **índice** es una posición dentro de una secuencia, y aquí está la revelación de la clase: `lista[indice]` *es* aritmética de direcciones disfrazada. El índice es el desplazamiento desde la base. Por eso los arreglos empiezan en 0 —el primer elemento está a distancia cero de la base— y por eso el acceso indexado es O(1): no hay que recorrer nada, solo calcular una dirección y leerla.

## 🧩 Situación

Un programador que solo ha usado `arr[i]` en Python cree que indexar «busca» el elemento. Cuando pasa a C y ve `*(arr + i)`, o cuando en Java descubre que asignar una lista a otra variable no la copia sino que la comparte, se topa con que todo era indirección. Acceder a `lista[indice]` con los mismos casos en los diez lenguajes deja ver cómo cada uno expone —o esconde— que por debajo hay una dirección base y un desplazamiento.

## 🧮 Modelo

- **Entrada** (stdin): una línea `indice v0 v1 v2 ...` (el primero es el índice, base 0)
- **Salida** (stdout): `valor=<elemento en esa posición>`
- **Regla:** valor = lista[indice]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 10 20 30` | `valor=20` |
| `0 5 6 7` | `valor=5` |
| `2 100 200 300` | `valor=300` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER indice y lista ; ESCRIBIR lista[indice]
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

t = sys.stdin.read().split()
indice = int(t[0])
lista = [int(x) for x in t[1:]]
print(f"valor={lista[indice]}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
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
        String[] t = br.readLine().trim().split("\\s+");
        int indice = Integer.parseInt(t[0]);
        System.out.println("valor=" + Integer.parseInt(t[indice + 1]));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

int[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int indice = t[0];
Console.WriteLine($"valor={t[indice + 1]}");
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
	t := strings.Fields(line)
	indice, _ := strconv.Atoi(t[0])
	lista := t[1:]
	fmt.Printf("valor=%s\n", lista[indice])
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let indice: usize = t[0].parse().unwrap();
    let lista = &t[1..];
    println!("valor={}", lista[indice]);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long indice = v[0];
    long *lista = v + 1; /* aritmética de punteros */
    printf("valor=%ld\n", *(lista + indice));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: acceso por posición con una subconsulta ordenada (ilustrativo).
WITH datos(pos, x) AS (VALUES (0, 10), (1, 20), (2, 30))
SELECT printf('valor=%d', x) AS resultado FROM datos WHERE pos = 1;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$indice = (int) $t[0];
$lista = array_slice($t, 1);
echo "valor={$lista[$indice]}\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `arr[i]` en casi todos; en C, también `*(arr + i)`. |
| Semántica | El índice se traduce a una dirección de memoria. |
| Paradigmática | SQL accede por condición, no por índice. |

## 🧬 El concepto en la familia

En C `arr[i]` y `*(arr+i)` son equivalentes: puro puntero. En los demás, el índice abstrae la dirección.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 129
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Índice fuera de rango** → causa: acceso inválido → solución: verificar que 0 <= i < tamaño
- **Confundir el valor con su dirección** → causa: usar el puntero como valor → solución: desreferenciar para obtener el valor

## ❓ Preguntas frecuentes

- **¿Referencia o puntero?** El puntero es una referencia explícita con aritmética; la referencia suele ser más segura.
- **¿arr[i] es un puntero?** En C sí, por debajo; en otros lenguajes el índice abstrae la dirección.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 128](../../parte-8-como-funcionan-los-lenguajes/128-el-heap-y-la-asignacion-dinamica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 130 ⏭️](../../parte-8-como-funcionan-los-lenguajes/130-gestion-manual-de-memoria-c-malloc-free/README.md)
