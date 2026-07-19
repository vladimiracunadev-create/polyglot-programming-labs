# Clase 095 — Mapas / diccionarios / tablas hash

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **mapa (diccionario)**: asociar claves con valores. Contar frecuencias es el uso más común: la clave es el número y el valor, cuántas veces aparece.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un mapa de frecuencias.
2. Consultar el valor de una clave.
3. Reconocer el acceso por clave en O(1).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mapa/diccionario | Clave → valor |
| 2 | Frecuencias | Contar apariciones |
| 3 | Acceso por clave | Búsqueda rápida |

## 📖 Definiciones y características

- **Mapa** — colección de pares clave→valor (dict, HashMap). Clave: búsqueda por clave en O(1).
- **Clave** — identificador único de una entrada. Clave: no se repite.
- **Frecuencia** — cuántas veces aparece un valor. Clave: uso típico del mapa.

## 🧩 Situación

Contar palabras, votos, visitas por página: el mapa asocia cada cosa con su cuenta y la actualiza al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<veces que aparece el primer elemento>`
- **Regla:** cuenta = frecuencia[lista[0]]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 3 3` | `cuenta=3` |
| `5 5` | `cuenta=2` |
| `7 1 2` | `cuenta=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; construir mapa de frecuencias ; ESCRIBIR frecuencia del primero
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
print(f"cuenta={freq[nums[0]]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map<number, number>();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<Integer, Integer> freq = new HashMap<>();
        for (String s : p) {
            int x = Integer.parseInt(s);
            freq.merge(x, 1, Integer::sum);
        }
        System.out.println("cuenta=" + freq.get(Integer.parseInt(p[0])));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var freq = new Dictionary<int, int>();
foreach (string s in p) {
    int x = int.Parse(s);
    freq[x] = freq.GetValueOrDefault(x, 0) + 1;
}
Console.WriteLine($"cuenta={freq[int.Parse(p[0])]}");
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
	fields := strings.Fields(line)
	freq := make(map[int]int)
	var nums []int
	for _, s := range fields {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
		freq[n]++
	}
	fmt.Printf("cuenta=%d\n", freq[nums[0]])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut freq: HashMap<i64, i64> = HashMap::new();
    for &x in &nums {
        *freq.entry(x).or_insert(0) += 1;
    }
    println!("cuenta={}", freq[&nums[0]]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int cuenta = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] == v[0]) cuenta++;
    }
    printf("cuenta=%d\n", cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: GROUP BY para frecuencias.
WITH nums(x) AS (VALUES (3), (1), (3), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado
FROM nums WHERE x = (SELECT x FROM nums LIMIT 1);
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$freq = array_count_values($nums);
echo "cuenta=" . $freq[$nums[0]] . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `dict` (Python), `{}`/Map (JS), `HashMap` (Java/Rust), `Dictionary` (C#). |
| Semántica | El mapa no garantiza orden de claves; C lo simula con arreglos. |
| Paradigmática | SQL agrupa con GROUP BY. |

## 🧬 El concepto en la familia

En Ruby `Hash.new(0)` para contar. En Go `map[int]int` es idiomático.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 095
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Leer una clave inexistente sin defecto** → causa: error o valor nulo → solución: inicializar con 0 o comprobar la existencia
- **Asumir orden de inserción** → causa: no siempre garantizado → solución: usar mapas ordenados si lo necesitas

## ❓ Preguntas frecuentes

- **¿Mapa o lista de pares?** Mapa para búsqueda rápida por clave; lista de pares si el orden importa.
- **¿Las claves pueden ser cualquier cosa?** Suelen requerir ser hashables/comparables; números y cadenas siempre valen.

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

> [⏮️ Clase 094](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 096 ⏭️](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md)
