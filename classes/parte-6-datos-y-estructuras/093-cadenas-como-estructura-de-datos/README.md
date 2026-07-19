# Clase 093 — Cadenas como estructura de datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Dejar de ver la **cadena** como un tipo escalar «que guarda texto» y verla como lo que realmente es: una **estructura de datos**, una secuencia indexable de caracteres o bytes que por dentro casi siempre es un arreglo. De ahí heredan las cadenas su acceso por posición y su recorrido lineal O(n), exactamente como el arreglo de la clase 089. Pero hay una decisión de diseño que separa a las cadenas de los arreglos ordinarios en la mayoría de lenguajes: la **inmutabilidad**. En Java, C#, Python, JavaScript y Go una cadena no se modifica en sitio; cualquier «cambio» —concatenar, invertir, reemplazar— produce un objeto nuevo. Esa garantía tiene un precio: concatenar dos cadenas de longitud *n* copia los *n* caracteres, y hacerlo dentro de un bucle degenera en O(n²) si no se usa un constructor especializado (`StringBuilder`, `join`, `strings.Builder`). El objetivo de hoy es sentir esa doble naturaleza —secuencia que se recorre, valor que no se muta— invirtiendo una palabra, la operación mínima que obliga a construir una cadena nueva.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una cadena carácter a carácter.
2. Construir una cadena invertida.
3. Reconocer la inmutabilidad de las cadenas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Cadena como secuencia | Caracteres indexados |
| 2 | Inversión | Del último al primero |
| 3 | Inmutabilidad | Se crea una nueva cadena |

## 📖 Definiciones y características

Una **cadena (string)** es una secuencia finita de caracteres. Su representación en memoria es casi universalmente un arreglo: un bloque contiguo de unidades de código, más una longitud (o un terminador). Por eso comparte la física del arreglo de la clase 089 —acceso a la posición *i* en O(1) cuando el ancho de cada unidad es fijo, recorrido completo en O(n)— pero le añade una capa semántica: esas celdas *significan* texto, y el texto se codifica. Ahí aparece la distinción que Ramalho desgrana en *Fluent Python* entre **bytes** y **code points**: en UTF-8 un carácter puede ocupar de uno a cuatro bytes, de modo que «indexar por byte» y «indexar por carácter» dejan de coincidir en cuanto el texto sale del ASCII. C trabaja al nivel más bajo —bytes crudos— mientras Python 3 o Rust razonan en code points.

El segundo rasgo definitorio es la **inmutabilidad**. En Java (Bloch, *Effective Java*, la trata como ejemplo canónico de clase inmutable), C#, Python, JavaScript y Go la cadena, una vez creada, no cambia: es un valor, no un contenedor mutable. Invertirla, concatenarla o reemplazar una letra construye siempre una cadena nueva y deja la original intacta. La ventaja es que una cadena inmutable se puede compartir, cachear e *internar* sin miedo a que otro la altere. El coste asoma al concatenar: unir dos cadenas es O(n) porque hay que copiar; concatenar en un bucle de *k* pasos, ingenuamente, es O(n²) —cada paso recopia todo lo acumulado—, y por eso existen los constructores incrementales. C es la excepción: un `char[]` terminado en `'\0'` es un buffer **mutable**, y Rust distingue explícitamente `String` (propietaria, mutable, en el heap) de `&str` (un préstamo de solo lectura), garantizando en ambos que el contenido es UTF-8 válido.

- **Cadena** — secuencia de caracteres respaldada por un arreglo de unidades de código; acceso O(1) por posición, recorrido O(n).
- **Inmutable** — no se modifica en sitio (Java, C#, Python, JavaScript, Go): invertir o concatenar crea otra cadena. C y el `String` de Rust son mutables.
- **Índice de carácter** — posición desde el inicio, base 0; coincide con el índice de byte solo mientras el texto sea ASCII/de ancho fijo.

## 🧩 Situación

Invertir texto, comprobar si una palabra es palíndromo, normalizar identificadores, procesar entradas del usuario: tratar la cadena como una secuencia recorrible es una constante en cualquier programa. El caso de hoy —invertir una palabra— es deliberadamente pequeño para que la atención caiga sobre la estructura y no sobre el algoritmo. Al recorrer del último carácter al primero verás que necesitas *acumular* el resultado en algún sitio, y ese sitio no puede ser la cadena original: en la mayoría de lenguajes es inmutable. Esa fricción —«¿dónde escribo el resultado si no puedo tocar la entrada?»— es justo la lección. En ASCII cada carácter es un byte, así que aquí índice de byte e índice de carácter coinciden y podemos ignorar la codificación; pero el mismo código con acentos o emoji rompería si invirtiéramos por bytes, y eso lo retomamos en los errores comunes.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `invertido=<la palabra al revés>`
- **Regla:** invertir la secuencia de caracteres

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `invertido=aloh` |
| `Ada` | `invertido=adA` |
| `abc` | `invertido=cba` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; recorrer del final al inicio ; ESCRIBIR invertido
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
print(f"invertido={w[::-1]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
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
        System.out.println("invertido=" + new StringBuilder(w).reverse());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"invertido={new string(w.Reverse().ToArray())}");
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
	r := []rune(w)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	fmt.Printf("invertido=%s\n", string(r))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let inv: String = w.chars().rev().collect();
    println!("invertido={inv}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int n = (int) strlen(w);
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) putchar(w[i]);
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sqlite no trae reverse; se invierte con un CTE recursivo (ilustrativo).
WITH RECURSIVE r(i, acc, s) AS (
    SELECT length('hola'), '', 'hola'
    UNION ALL SELECT i - 1, acc || substr(s, i, 1), s FROM r WHERE i > 0
)
SELECT 'invertido=' || acc AS resultado FROM r WHERE i = 0;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
echo "invertido=" . strrev($w) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `hola`, que debe producir `invertido=aloh`. Las diez implementaciones invierten la misma secuencia de cuatro caracteres, pero cada una revela una manera distinta de sortear la inmutabilidad.

En **Python**, todo el trabajo lo hace `w[::-1]`. Es una *rebanada extendida* con paso `-1`: Python recorre `hola` desde el final (`a`, `l`, `o`, `h`) y construye una **cadena nueva** con esos caracteres. La original nunca se toca —no podría, es inmutable— y el f-string la incrusta tras `invertido=`. Una sola expresión esconde una copia O(n): recorrer los cuatro caracteres y reservar una cadena de longitud 4.

En **Java**, la cadena `w = "hola"` es inmutable por diseño, así que invertirla en sitio es imposible. La solución idiomática es envolver la cadena en un `new StringBuilder(w)` —un buffer **mutable** que copia los caracteres una vez— y llamar a `.reverse()`, que intercambia los caracteres dentro de ese buffer sin crear objetos intermedios. Este es el patrón que Bloch recomienda para toda construcción incremental de texto: usar el buffer mutable y materializar la cadena una única vez al final. El `StringBuilder`, al concatenarse con `"invertido=" + ...`, se convierte a `String` mediante su `toString()`.

En **C**, no hay ni inmutabilidad ni función incorporada: `char w[256]` es un buffer mutable, `scanf("%255s", w)` lo llena y `strlen` cuenta 4. En lugar de construir una cadena nueva, el bucle `for (int i = n - 1; i >= 0; i--)` emite carácter a carácter con `putchar`, desde `w[3]='a'` hasta `w[0]='h'`. No hay copia: se imprime directamente en orden inverso. Es la aritmética de índices al desnudo, sin ninguna capa entre el código y el arreglo de bytes.

Los tres imprimen `invertido=aloh`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`, incluido el caso `Ada` → `adA`, que exige respetar mayúsculas.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `w[::-1]` (Python), `.reverse()` sobre arreglo de chars (JS/Rust). |
| Semántica | En Rust hay que iterar por `chars()` (UTF-8); en C es por bytes. |
| Paradigmática | SQL tiene la función `reverse` en algunos motores; sqlite no de serie. |

La diferencia semántica más honda es **qué unidad recorre cada lenguaje**. C itera sobre `char`, es decir, sobre **bytes**: con texto ASCII funciona, pero invertir «árbol» por bytes partiría la `á` en dos y produciría basura. Rust obliga a elegir explícitamente —`w.chars().rev()` recorre code points UTF-8, mientras `w.bytes()` recorriría bytes— y no deja que ese error pase inadvertido. Go convierte a `[]rune` justo para no invertir bytes sueltos. Python y JavaScript operan sobre code points de serie. El segundo eje es **mutable vs. inmutable**: Java necesita el rodeo del `StringBuilder`, C# construye un `new string(...)` a partir del arreglo invertido y PHP tiene `strrev` como función de biblioteca, pero ninguno modifica la cadena de entrada. Solo C y el `String` de Rust admiten mutación real del contenido. Y hay un eje de **valor vs. referencia** implícito: como las cadenas inmutables son valores, dos variables pueden compartir la misma memoria sin peligro, algo que ningún arreglo mutable permite.

## 🧬 El concepto en la familia

Casi todos los lenguajes ofrecen dos caras de la cadena: la inmutable de uso diario y un constructor mutable para armarla por partes. Java tiene `String` frente a `StringBuilder`/`StringBuffer`; C# tiene `string` frente a `StringBuilder`; Go tiene `string` frente a `strings.Builder` y `[]byte`; Rust separa `&str` (préstamo inmutable) de `String` (dueña, mutable). Python y JavaScript no exponen un builder explícito, pero la práctica idiomática —acumular trozos en una lista y unirlos con `"".join(...)` o `arr.join("")`— cumple la misma función de evitar el O(n²) de concatenar en bucle. C queda aparte: su cadena *es* el buffer mutable (`char[]` con `'\0'`), sin distinción entre las dos caras, a cambio de que el programador cargue con la memoria y los límites. Reconocer este par inmutable/constructor en cada lenguaje evita el error de rendimiento más común con texto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 093
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir por bytes con Unicode** → causa: en UTF-8 un carácter ocupa varios bytes, e invertir la secuencia de bytes parte esos caracteres y produce texto corrupto → solución: iterar por caracteres/code points (`chars()` en Rust, `[]rune` en Go); aquí, al ser ASCII, byte y carácter coinciden y no hay problema.
- **Intentar mutar la cadena** → causa: en Java, C#, Python, JavaScript y Go la cadena es inmutable, así que `w[0] = 'X'` o un método «in-place» no existen o no cambian el original → solución: construir una cadena nueva con la operación (rebanada, `StringBuilder`, `join`).
- **Concatenar dentro de un bucle** → causa: `s = s + trozo` en cada vuelta recopia todo lo acumulado, degenerando en O(n²) → solución: acumular los trozos y unirlos una sola vez (`"".join(lista)`, `StringBuilder`, `strings.Builder`).
- **Confundir longitud en bytes con longitud en caracteres** → causa: `strlen`/`len` de bytes no cuenta caracteres cuando hay multibyte → solución: usar la longitud en code points cuando lo que importa son caracteres.

## ❓ Preguntas frecuentes

- **¿Por qué invertir crea otra cadena?** Porque en Java, C#, Python, JavaScript y Go las cadenas son inmutables: no existe una operación que reescriba sus celdas en sitio. Invertir, concatenar o reemplazar siempre devuelve un objeto nuevo y deja intacto el original. En C, en cambio, el `char[]` sí se puede invertir intercambiando posiciones.
- **¿Por qué concatenar en bucle puede ser O(n²)?** Porque cada concatenación de una cadena inmutable copia todo el contenido acumulado hasta ese momento; si repites *k* veces, la copia total crece cuadráticamente. Un constructor mutable (`StringBuilder`, `strings.Builder`) amortiza las copias y baja el coste a O(n).
- **¿ASCII o Unicode?** Aquí trabajamos en ASCII, donde cada carácter es exactamente un byte y podemos ignorar la codificación. Con Unicode hay que respetar los límites de carácter: iterar por code points, no por bytes, o arriesgarse a partir caracteres multibyte.
- **¿La cadena y el arreglo son lo mismo?** Por dentro, casi: una cadena suele ser un arreglo de unidades de código con una longitud. La diferencia es la capa semántica (codificación de texto) y, sobre todo, la inmutabilidad que la mayoría de lenguajes imponen sobre las cadenas pero no sobre los arreglos.

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

> [⏮️ Clase 092](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 094 ⏭️](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md)
