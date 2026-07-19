# Clase 098 — Grafos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer los **grafos**: nodos conectados por aristas. Representarlos como lista de aristas y contar nodos y aristas es el primer paso para modelar redes, mapas y dependencias.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar un grafo por sus aristas.
2. Contar aristas y nodos distintos.
3. Reconocer dónde aparecen los grafos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Grafo | Nodos y aristas |
| 2 | Arista | Conexión entre dos nodos |
| 3 | Nodos distintos | El conjunto de vértices |

## 📖 Definiciones y características

- **Grafo** — conjunto de nodos conectados por aristas. Clave: modela relaciones.
- **Arista** — conexión entre dos nodos. Clave: aquí, un par de números.
- **Nodo (vértice)** — una entidad del grafo. Clave: contar los distintos = tamaño del conjunto.

## 🧩 Situación

Redes sociales, mapas de carreteras, dependencias de paquetes: todo son grafos. Contar nodos y aristas es la medida básica de su tamaño.

## 🧮 Modelo

- **Entrada** (stdin): una línea con pares de enteros (cada par es una arista)
- **Salida** (stdout): `aristas=<número de pares> nodos=<nodos distintos>`
- **Regla:** aristas = tokens/2 ; nodos = |conjunto de todos los números|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3` | `aristas=2 nodos=3` |
| `1 2` | `aristas=1 nodos=2` |
| `1 2 2 3 3 1` | `aristas=3 nodos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER pares ; aristas <- pares ; nodos <- distintos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
aristas = len(nums) // 2
nodos = len(set(nums))
print(f"aristas={aristas} nodos={nodos}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> nodos = new HashSet<>();
        for (String s : p) nodos.add(Integer.parseInt(s));
        System.out.println("aristas=" + (p.length / 2) + " nodos=" + nodos.size());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int aristas = p.Length / 2;
int nodos = p.Select(int.Parse).Distinct().Count();
Console.WriteLine($"aristas={aristas} nodos={nodos}");
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
	set := make(map[int]struct{})
	for _, s := range f {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("aristas=%d nodos=%d\n", len(f)/2, len(set))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let aristas = nums.len() / 2;
    let nodos: HashSet<i64> = nums.iter().copied().collect();
    println!("aristas={} nodos={}", aristas, nodos.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[2048];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int nodos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) nodos++;
    }
    printf("aristas=%d nodos=%d\n", n / 2, nodos);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: aristas = filas de pares; nodos = valores distintos.
WITH nums(x) AS (VALUES (1), (2), (2), (3))
SELECT printf('aristas=%d nodos=%d', count(*) / 2, count(DISTINCT x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$aristas = intdiv(count($nums), 2);
$nodos = count(array_unique($nums));
echo "aristas=$aristas nodos=$nodos\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Conjunto de nodos + conteo de pares en cada lenguaje. |
| Semántica | El grafo puede guardarse como lista de aristas o de adyacencia. |
| Paradigmática | SQL modela grafos con tablas de nodos y aristas (relaciones). |

## 🧬 El concepto en la familia

En muchos lenguajes se usa un mapa de adyacencia `nodo → vecinos`. Aquí basta un conjunto para los nodos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 098
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar nodos con repetición** → causa: sobreestimar los vértices → solución: usar un conjunto de nodos distintos
- **Suponer número impar de tokens** → causa: arista incompleta → solución: asumir pares completos (grafo bien formado)

## ❓ Preguntas frecuentes

- **¿Lista de aristas o adyacencia?** Aristas es simple para contar; adyacencia es mejor para recorrer vecinos.
- **¿Dirigido o no?** Aquí solo contamos; la dirección importaría para recorridos.

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

> [⏮️ Clase 097](../../parte-6-datos-y-estructuras/097-arboles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 099 ⏭️](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md)
