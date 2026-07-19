# Clase 115 — Funcional II: composición, currying y aplicación parcial

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (II)**: composición de funciones. Combinar funciones pequeñas (`doblar`, `incrementar`) en una mayor, aplicando primero una y luego la otra.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Componer dos funciones.
2. Aplicar la composición a un valor.
3. Reconocer la aplicación parcial/currying.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Composición | f(g(x)): encadenar funciones |
| 2 | Funciones pequeñas | Construir a partir de piezas |
| 3 | Currying | Funciones que devuelven funciones |

## 📖 Definiciones y características

- **Composición de funciones** — combinar funciones: `(f ∘ g)(x) = f(g(x))`. Clave: construir con piezas.
- **Currying** — transformar una función de varios argumentos en una cadena de funciones de uno. Clave: aplicación parcial.
- **Aplicación parcial** — fijar algunos argumentos y obtener una función nueva. Clave: reutilización.

## 🧩 Situación

En vez de escribir `x*2+1` a mano, se componen `doblar` e `incrementar`. Las funciones pequeñas y componibles son el corazón del estilo funcional.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n+1>` (doblar y luego incrementar)
- **Regla:** resultado = incrementar(doblar(n)) = 2n + 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=11` |
| `0` | `resultado=1` |
| `3` | `resultado=7` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblar(x)=2x ; inc(x)=x+1 ; compuesta = inc ∘ doblar ; ESCRIBIR compuesta(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doblar(x):
    return x * 2


def incrementar(x):
    return x + 1


n = int(sys.stdin.readline())
print(f"resultado={incrementar(doblar(n))}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doblar = (x) => x * 2;
const incrementar = (x) => x + 1;
const compuesta = (x) => incrementar(doblar(x));

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doblar = (x: number): number => x * 2;
const incrementar = (x: number): number => x + 1;
const compuesta = (x: number): number => incrementar(doblar(x));

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator doblar = x -> x * 2;
        IntUnaryOperator incrementar = x -> x + 1;
        IntUnaryOperator compuesta = doblar.andThen(incrementar);
        System.out.println("resultado=" + compuesta.applyAsInt(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Func<int, int> doblar = x => x * 2;
Func<int, int> incrementar = x => x + 1;
Func<int, int> compuesta = x => incrementar(doblar(x));
Console.WriteLine($"resultado={compuesta(n)}");
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

func doblar(x int) int      { return x * 2 }
func incrementar(x int) int { return x + 1 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", incrementar(doblar(n)))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(x: i64) -> i64 {
    x * 2
}

fn incrementar(x: i64) -> i64 {
    x + 1
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", incrementar(doblar(n)));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doblar(long x) { return x * 2; }
long incrementar(long x) { return x + 1; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", incrementar(doblar(n)));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se anidan las expresiones/funciones.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('resultado=%d', (n * 2) + 1) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$doblar = fn($x) => $x * 2;
$incrementar = fn($x) => $x + 1;
$compuesta = fn($x) => $incrementar($doblar($x));

$n = (int) trim(fgets(STDIN));
echo "resultado=" . $compuesta($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Composición explícita `inc(doblar(n))` o con operador de composición. |
| Semántica | El orden importa: doblar primero, luego incrementar. |
| Paradigmática | SQL anida funciones/expresiones. |

## 🧬 El concepto en la familia

En Haskell `(inc . doblar) n` con el operador `.`. En muchos lenguajes se anidan las llamadas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 115
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir el orden de composición** → causa: resultado distinto → solución: aplicar en el orden correcto
- **Componer funciones incompatibles** → causa: tipos que no encajan → solución: asegurar que la salida de una es la entrada de la otra

## ❓ Preguntas frecuentes

- **¿Composición o anidar llamadas?** Anidar es composición explícita; algunos lenguajes tienen un operador dedicado.
- **¿Currying para qué sirve?** Fijar argumentos y crear funciones especializadas reutilizables.

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

> [⏮️ Clase 114](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 116 ⏭️](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md)
