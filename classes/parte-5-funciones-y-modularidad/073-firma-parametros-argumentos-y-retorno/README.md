# Clase 073 — Firma, parámetros, argumentos y retorno

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la anatomía de una función: **firma** (nombre + parámetros + tipo de retorno), **argumentos** (los valores que se pasan) y **retorno** (el valor que devuelve). Es la unidad de reutilización de todo programa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función con parámetros y retorno.
2. Distinguir parámetro de argumento.
3. Invocar la función y usar su valor.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Firma | Nombre, parámetros y tipo de retorno |
| 2 | Parámetro vs. argumento | El hueco vs. el valor real |
| 3 | Retorno | El valor que produce |
| 4 | Reutilización | Llamar en vez de repetir |

## 📖 Definiciones y características

- **Función** — bloque con nombre que recibe parámetros y devuelve un valor. Clave: la unidad de reutilización.
- **Firma** — nombre + parámetros + tipo de retorno. Clave: define cómo se usa.
- **Parámetro** — variable del hueco en la definición. Clave: recibe el argumento.
- **Argumento** — valor concreto que se pasa al llamar. Clave: llena el parámetro.

## 🧩 Situación

En vez de repetir `a + b` por todas partes, se define `suma(a, b)` una vez y se llama. La firma es el contrato: qué recibe y qué devuelve.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b>`
- **Regla:** suma(a, b) = a + b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7` |
| `10 20` | `suma=30` |
| `-5 5` | `suma=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(a, b): DEVOLVER a+b
LEER a, b ; ESCRIBIR "suma=" suma(a,b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def suma(a, b):
    return a + b


a, b = map(int, sys.stdin.readline().split())
print(f"suma={suma(a, b)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function suma(a, b) {
  return a + b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function suma(a: number, b: number): number {
  return a + b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int suma(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("suma=" + suma(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int Suma(int a, int b) => a + b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(int.Parse(p[0]), int.Parse(p[1]))}");
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

func suma(a, b int) int {
	return a + b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("suma=%d\n", suma(a, b))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(v[0], v[1]));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long suma(long a, long b) {
    return a + b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld\n", suma(a, b));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la operación se expresa en la propia consulta.
WITH pares(a, b) AS (VALUES (3, 4), (10, 20), (-5, 5))
SELECT printf('suma=%d', a + b) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
function suma($a, $b) {
    return $a + $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "suma=" . suma((int) $a, (int) $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def` (Python), `func` (Go), `fn` (Rust), tipo de retorno explícito (Java/C). |
| Semántica | Estáticos declaran los tipos de parámetros y retorno; dinámicos no. |
| Paradigmática | SQL define la operación en la propia consulta. |

## 🧬 El concepto en la familia

En Ruby `def suma(a, b)`. En Haskell `suma a b = a + b`, con la firma inferida.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 073
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir parámetro con argumento** → causa: usar mal los términos y el orden → solución: recordar: parámetro en la definición, argumento en la llamada
- **Olvidar el return** → causa: la función no devuelve nada → solución: asegurar que la función retorna el valor

## ❓ Preguntas frecuentes

- **¿Función o procedimiento?** Una función devuelve valor; un procedimiento solo actúa. Aquí devolvemos.
- **¿Por qué reutilizar?** Menos repetición, menos errores, un solo lugar que cambiar.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 072](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 074 ⏭️](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md)
