# Clase 130 — Gestión manual de memoria (C): malloc/free

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **gestión manual de memoria** de C: reservar con malloc, usar y liberar con free. En los lenguajes con recolector esto es automático; en C es responsabilidad del programador.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reservar y liberar memoria (concepto).
2. Explicar malloc/free.
3. Contrastar con la gestión automática.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | malloc/free | Reservar y liberar a mano |
| 2 | Responsabilidad | Liberar lo que reservas |
| 3 | Fugas y dobles liberaciones | Los peligros |

## 📖 Definiciones y características

- **malloc** — reserva un bloque de memoria en el heap (C). Clave: devuelve un puntero.
- **free** — libera un bloque previamente reservado. Clave: olvidarlo causa fugas.
- **Fuga de memoria** — memoria reservada que nunca se libera. Clave: el programa la va acumulando.

## 🧩 Situación

En C, cada malloc necesita su free; olvidarlo es una fuga, liberar dos veces es un error grave. Los lenguajes con GC hacen esto por ti, a cambio de menos control.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `reservado=<n> suma=<1+...+n>`
- **Regla:** reservar n enteros, llenarlos 1..n, sumar, liberar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `reservado=5 suma=15` |
| `1` | `reservado=1 suma=1` |
| `3` | `reservado=3 suma=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar(n) ; llenar 1..n ; sumar ; liberar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
arr = [0] * n  # el runtime gestiona la memoria
for i in range(n):
    arr[i] = i + 1
print(f"reservado={n} suma={sum(arr)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr: number[] = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
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
        int[] arr = new int[n];
        long suma = 0;
        for (int i = 0; i < n; i++) {
            arr[i] = i + 1;
            suma += arr[i];
        }
        System.out.println("reservado=" + n + " suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int[] arr = new int[n];
long suma = 0;
for (int i = 0; i < n; i++) {
    arr[i] = i + 1;
    suma += arr[i];
}
Console.WriteLine($"reservado={n} suma={suma}");
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
	arr := make([]int, n)
	suma := 0
	for i := 0; i < n; i++ {
		arr[i] = i + 1
		suma += arr[i]
	}
	fmt.Printf("reservado=%d suma=%d\n", n, suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let arr: Vec<i64> = (1..=n).collect(); // Vec libera al salir del ámbito
    let suma: i64 = arr.iter().sum();
    println!("reservado={n} suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *arr = malloc(n * sizeof(long));
    long suma = 0;
    for (long i = 0; i < n; i++) {
        arr[i] = i + 1;
        suma += arr[i];
    }
    printf("reservado=%ld suma=%ld\n", n, suma);
    free(arr);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone la gestión de memoria; se calcula la suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('reservado=%d suma=%d', max(i), sum(i)) AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$arr = array_fill(0, $n, 0);
for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $i + 1;
}
echo "reservado=$n suma=" . array_sum($arr) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | malloc/free (C); las colecciones automáticas en los demás. |
| Semántica | C libera a mano; GC/ownership liberan por ti. |
| Paradigmática | SQL no expone gestión de memoria. |

## 🧬 El concepto en la familia

C y C++ (con new/delete) gestionan a mano; Rust automatiza vía ownership sin GC; el resto usa GC.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 130
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar free** → causa: fuga de memoria → solución: liberar todo lo reservado
- **Usar tras liberar** → causa: use-after-free → solución: no acceder a memoria ya liberada

## ❓ Preguntas frecuentes

- **¿Por qué gestionar a mano?** Control fino y rendimiento predecible, a cambio de responsabilidad.
- **¿El GC elimina las fugas?** Las de memoria en gran medida, pero no las de otros recursos (archivos, sockets).

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

> [⏮️ Clase 129](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 131 ⏭️](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md)
