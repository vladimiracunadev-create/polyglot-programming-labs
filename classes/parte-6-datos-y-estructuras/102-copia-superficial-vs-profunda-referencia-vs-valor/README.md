# Clase 102 — Copia superficial vs. profunda; referencia vs. valor

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **copia** de **referencia compartida**, y **copia superficial** de **profunda**. Copiar una lista de valores y modificar la copia no altera el original; con referencias compartidas, sí.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Copiar una colección.
2. Comprobar que el original no cambia.
3. Distinguir copia superficial de profunda.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Copia vs. referencia | Duplicar o compartir |
| 2 | Copia superficial | Copia el primer nivel |
| 3 | Copia profunda | Copia todo recursivamente |

## 📖 Definiciones y características

- **Copia** — duplicado independiente. Clave: modificarlo no afecta al original.
- **Referencia compartida** — dos nombres para el mismo dato. Clave: cambiar uno cambia el otro.
- **Superficial vs. profunda** — copiar solo el nivel externo o todo el contenido. Clave: importa con datos anidados.

## 🧩 Situación

Asignar `b = a` en muchos lenguajes comparte la lista: cambiar `b` cambia `a`. Copiarla de verdad evita esa sorpresa. Con estructuras anidadas, la copia debe ser profunda.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `original=<lista> copia=<lista con el último cambiado a 99>` (unidos por -)
- **Regla:** copiar; copia[último] = 99; original intacto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `original=1-2-3 copia=1-2-99` |
| `5 5` | `original=5-5 copia=5-99` |
| `7` | `original=7 copia=99` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; copia <- COPIA(lista) ; copia[fin] <- 99 ; ESCRIBIR original y copia
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
copia = list(nums)  # copia superficial (aquí basta, son enteros)
copia[-1] = 99
print(f"original={'-'.join(map(str, nums))} copia={'-'.join(map(str, copia))}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia: number[] = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int[] copia = Arrays.copyOf(nums, nums.length);
        copia[copia.length - 1] = 99;
        System.out.println("original=" + join(nums) + " copia=" + join(copia));
    }

    static String join(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append("-");
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] nums = p.Select(int.Parse).ToArray();
int[] copia = (int[]) nums.Clone();
copia[copia.Length - 1] = 99;
Console.WriteLine($"original={string.Join("-", nums)} copia={string.Join("-", copia)}");
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
	f := strings.Fields(line)
	nums := make([]int, len(f))
	for i, s := range f {
		nums[i], _ = strconv.Atoi(s)
	}
	copia := make([]int, len(nums))
	copy(copia, nums)
	copia[len(copia)-1] = 99
	fmt.Printf("original=%s copia=%s\n", join(nums), join(copia))
}

func join(a []int) string {
	parts := make([]string, len(a))
	for i, n := range a {
		parts[i] = strconv.Itoa(n)
	}
	return strings.Join(parts, "-")
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn join(a: &[i64]) -> String {
    a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut copia = nums.clone();
    let n = copia.len();
    copia[n - 1] = 99;
    println!("original={} copia={}", join(&nums), join(&copia));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long copia[1024];
    for (int i = 0; i < n; i++) copia[i] = v[i];
    copia[n - 1] = 99;
    printf("original=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", v[i]); }
    printf(" copia=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", copia[i]); }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: los conjuntos no comparten referencias mutables; se ilustra el cambio.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'original=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos))
     || ' copia=' || (SELECT group_concat(CASE WHEN pos = (SELECT max(pos) FROM nums) THEN 99 ELSE x END, '-')
                       FROM (SELECT pos, x FROM nums ORDER BY pos)) AS resultado;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$copia = $nums; // PHP copia los arreglos por valor
$copia[count($copia) - 1] = 99;
echo "original=" . implode("-", $nums) . " copia=" . implode("-", $copia) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list(x)`/`x[:]` (Python), `[...x]` (JS), `clone()` (Rust/Java). |
| Semántica | Sin copiar, `b=a` comparte; hay que copiar explícitamente. |
| Paradigmática | SQL trabaja con conjuntos; no comparte referencias mutables. |

## 🧬 El concepto en la familia

En Ruby `dup` copia superficial; en muchos lenguajes la copia profunda requiere recorrer.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 102
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que asignar copia** → causa: `b=a` comparte la referencia → solución: copiar explícitamente si necesitas independencia
- **Copia superficial con datos anidados** → causa: los niveles internos siguen compartidos → solución: hacer copia profunda cuando haya anidamiento

## ❓ Preguntas frecuentes

- **¿Copia superficial o profunda?** Superficial si no hay anidamiento; profunda si hay estructuras dentro de estructuras.
- **¿Los primitivos se comparten?** No: los valores se copian; las colecciones/objetos se comparten por referencia.

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

> [⏮️ Clase 101](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 103 ⏭️](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md)
