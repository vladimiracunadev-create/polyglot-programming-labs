# Clase 101 — Igualdad vs. identidad

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **igualdad** (mismo valor) de **identidad** (mismo objeto en memoria). Con valores primitivos coinciden; con objetos no siempre, y cada lenguaje ofrece operadores distintos (`==` vs. `is`/`===`).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comparar por valor.
2. Explicar la diferencia entre igualdad e identidad.
3. Reconocer los operadores de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Igualdad | Mismo valor |
| 2 | Identidad | Mismo objeto en memoria |
| 3 | Operadores | ==, is, ===, equals |

## 📖 Definiciones y características

- **Igualdad** — dos valores son iguales si representan lo mismo. Clave: `a == b`.
- **Identidad** — dos referencias apuntan al mismo objeto. Clave: `is` (Python), `===` no es exactamente eso en JS.
- **equals vs. ==** — en Java `==` compara referencias de objetos; `equals` compara valor. Clave: fuente de bugs.

## 🧩 Situación

En Java, dos cadenas con el mismo texto pueden ser `equals` pero no `==` (distintos objetos). Confundir igualdad con identidad es un error clásico.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `iguales=<true|false>`
- **Regla:** iguales = (a == b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `iguales=true` |
| `3 7` | `iguales=false` |
| `0 0` | `iguales=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; ESCRIBIR iguales=(a==b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"iguales={'true' if a == b else 'false'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        System.out.println("iguales=" + (a == b ? "true" : "false"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"iguales={(a == b ? "true" : "false")}");
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
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	res := "false"
	if a == b {
		res = "true"
	}
	fmt.Printf("iguales=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("iguales={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("iguales=%s\n", a == b ? "true" : "false");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara valores con =.
WITH pares(a, b) AS (VALUES (5, 5), (3, 7), (0, 0))
SELECT printf('iguales=%s', CASE WHEN a = b THEN 'true' ELSE 'false' END) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "iguales=" . ((int) $a === (int) $b ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `==` en todos para valor; identidad con `is` (Python), `===` (JS), `equals`/`==` (Java). |
| Semántica | Con primitivos, igualdad e identidad coinciden; con objetos no. |
| Paradigmática | SQL compara valores con `=`; NULL requiere `IS`. |

## 🧬 El concepto en la familia

En Ruby `==` es valor y `equal?` es identidad. En C#, `==` puede sobrecargarse; `ReferenceEquals` da identidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 101
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar `==` para objetos en Java** → causa: compara referencias, no valor → solución: usar `equals` para comparar contenido
- **Comparar reales con `==`** → causa: imprecisión → solución: aquí son enteros; con reales usar tolerancia

## ❓ Preguntas frecuentes

- **¿`==` compara valor o referencia?** Depende del lenguaje y del tipo; con primitivos, valor.
- **¿Qué es `is` en Python?** Compara identidad (mismo objeto), no valor.

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

> [⏮️ Clase 100](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 102 ⏭️](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md)
