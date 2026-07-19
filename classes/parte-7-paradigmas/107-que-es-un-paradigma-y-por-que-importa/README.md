# Clase 107 — Qué es un paradigma y por qué importa

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender qué es un **paradigma**: una forma de estructurar la solución (imperativa, funcional, declarativa…). El mismo problema —sumar 1 a n— puede resolverse de varias maneras según el paradigma.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir qué es un paradigma.
2. Reconocer que un problema admite varios enfoques.
3. Situar los paradigmas del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paradigma | Forma de estructurar la solución |
| 2 | Multiparadigma | Un lenguaje puede ofrecer varios |
| 3 | Mismo problema, varios enfoques | Imperativo, funcional, declarativo |

## 📖 Definiciones y características

- **Paradigma** — estilo de estructurar programas (imperativo, OO, funcional, declarativo). Clave: cambia cómo se piensa.
- **Multiparadigma** — lenguaje que soporta varios estilos (Python, C#, Rust). Clave: eliges por problema.
- **Enfoque** — la estrategia elegida para resolver. Clave: distintos paradigmas, distinta forma.

## 🧩 Situación

Sumar 1..n se puede hacer con un bucle (imperativo), con reduce (funcional) o con una fórmula/consulta (declarativo). El paradigma decide la forma, no el resultado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `3` | `suma=6` |
| `1` | `suma=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; sumar 1..n ; ESCRIBIR suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
suma = sum(range(1, n + 1))
print(f"suma={suma}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
for (let i = 1; i <= n; i++) suma += i;
console.log(`suma=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
for (let i = 1; i <= n; i++) suma += i;
console.log(`suma=${suma}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long suma = 0;
        for (int i = 1; i <= n; i++) suma += i;
        System.out.println("suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
for (int i = 1; i <= n; i++) suma += i;
Console.WriteLine($"suma={suma}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	suma := 0
	for i := 1; i <= n; i++ {
		suma += i
	}
	fmt.Printf("suma=%d\n", suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let suma: i64 = (1..=n).sum();
    println!("suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    for (long i = 1; i <= n; i++) suma += i;
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL (declarativo): suma con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d', sum(i)) AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
}
echo "suma=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle, `reduce` o fórmula según el estilo. |
| Semántica | Todos dan el mismo resultado; cambia la estructura. |
| Paradigmática | Imperativo describe pasos; declarativo describe el resultado. |

## 🧬 El concepto en la familia

Casi todos los lenguajes del núcleo son multiparadigma: permiten el mismo problema de varias formas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 107
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que hay un solo modo correcto** → causa: encasillarse en un paradigma → solución: elegir el que mejor exprese el problema
- **Confundir paradigma con lenguaje** → causa: un lenguaje ofrece varios → solución: distinguir el estilo del lenguaje

## ❓ Preguntas frecuentes

- **¿Cuál es mejor?** Depende del problema: cada paradigma brilla en distintos casos.
- **¿Un lenguaje = un paradigma?** No: la mayoría son multiparadigma.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 106](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 108 ⏭️](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md)
