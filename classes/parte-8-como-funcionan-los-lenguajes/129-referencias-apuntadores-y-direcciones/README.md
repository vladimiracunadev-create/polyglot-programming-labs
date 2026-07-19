# Clase 129 — Referencias, apuntadores y direcciones

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **referencias, apuntadores y direcciones**: acceder a un dato a través de su posición o dirección, no directamente. Indexar una lista es aritmética de direcciones: base + índice.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Acceder a un elemento por su índice.
2. Explicar la indirección (referencia/puntero).
3. Relacionar el índice con la dirección.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Indirección | Acceder a través de una posición |
| 2 | Índice como dirección | base + desplazamiento |
| 3 | Referencia vs. puntero | Ambos apuntan a un dato |

## 📖 Definiciones y características

- **Referencia** — un valor que designa a otro dato. Clave: acceso indirecto.
- **Puntero** — referencia explícita que guarda una dirección (C). Clave: `arr + i` = dirección del elemento i.
- **Índice** — posición dentro de una secuencia. Clave: equivale a un desplazamiento desde la base.

## 🧩 Situación

`arr[i]` en el fondo es 've a la dirección base más i posiciones'. Los punteros de C hacen esa aritmética explícita; los índices la esconden. Ambos son indirección.

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
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

t = sys.stdin.read().split()
indice = int(t[0])
lista = [int(x) for x in t[1:]]
print(f"valor={lista[indice]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
```

### Java · `java Main.java`

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

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

int[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int indice = t[0];
Console.WriteLine($"valor={t[indice + 1]}");
```

### Go · `go run main.go`

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

### Rust · `rustc main.rs -o main && ./main`

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

### C · `cc main.c -o main && ./main`

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

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: acceso por posición con una subconsulta ordenada (ilustrativo).
WITH datos(pos, x) AS (VALUES (0, 10), (1, 20), (2, 30))
SELECT printf('valor=%d', x) AS resultado FROM datos WHERE pos = 1;
```

### PHP · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$indice = (int) $t[0];
$lista = array_slice($t, 1);
echo "valor={$lista[$indice]}\n";
```

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
