# Clase 084 — Funciones puras y efectos secundarios

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir una **función pura** —su resultado depende solo de sus argumentos y no cambia nada externo— de una con **efectos secundarios**. Las puras son predecibles, testeables y seguras de paralelizar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función pura.
2. Explicar qué es un efecto secundario.
3. Argumentar las ventajas de la pureza.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Función pura | Mismo entrada → mismo resultado |
| 2 | Efecto secundario | Cambiar algo externo |
| 3 | Transparencia referencial | Sustituir la llamada por su valor |
| 4 | Ventajas | Testeable, cacheable, paralelizable |

## 📖 Definiciones y características

- **Función pura** — su salida depende solo de sus entradas y no causa efectos externos. Clave: predecible.
- **Efecto secundario** — modificar estado externo, imprimir, leer archivos. Clave: rompe la pureza.
- **Transparencia referencial** — poder reemplazar la llamada por su resultado. Clave: propiedad de las puras.
- **Determinismo** — misma entrada, misma salida siempre. Clave: facilita las pruebas.

## 🧩 Situación

`cuadrado(n)` siempre da lo mismo para el mismo `n` y no toca nada más: es pura. Una función que además escribe en un log tiene un efecto secundario. Las puras son las más fáciles de probar y razonar.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `puro=<n²>`
- **Regla:** cuadrado(n) = n * n (sin efectos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `puro=16` |
| `-3` | `puro=9` |
| `0` | `puro=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION cuadrado(n): DEVOLVER n*n   // sin tocar nada externo
LEER n ; ESCRIBIR "puro=" cuadrado(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def cuadrado(n):
    return n * n  # pura: sin efectos secundarios


n = int(sys.stdin.readline())
print(f"puro={cuadrado(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function cuadrado(n) {
  return n * n;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function cuadrado(n: number): number {
  return n * n;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long cuadrado(long n) {
        return n * n;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("puro=" + cuadrado(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Cuadrado(long n) => n * n;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"puro={Cuadrado(n)}");
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

func cuadrado(n int64) int64 {
	return n * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("puro=%d\n", cuadrado(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn cuadrado(n: i64) -> i64 {
    n * n
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("puro={}", cuadrado(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long cuadrado(long n) {
    return n * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("puro=%ld\n", cuadrado(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL (declarativo) favorece expresiones puras.
WITH nums(n) AS (VALUES (4), (-3), (0))
SELECT printf('puro=%d', n * n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function cuadrado($n) {
    return $n * $n;
}

$n = (int) trim(fgets(STDIN));
echo "puro=" . cuadrado($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Idéntica en todos: una función que devuelve un cálculo. |
| Semántica | La pureza es una propiedad del diseño, no de la sintaxis. |
| Paradigmática | SQL (declarativo) y Haskell (puro) empujan hacia la pureza por defecto. |

## 🧬 El concepto en la familia

En Haskell casi todo es puro; los efectos se aíslan con el tipo IO. En Rust, la pureza es una convención, no forzada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 084
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar cálculo con impresión/estado** → causa: función difícil de testear → solución: separar el cálculo puro del efecto (I/O)
- **Depender de estado global** → causa: resultados no reproducibles → solución: pasar todo por parámetros

## ❓ Preguntas frecuentes

- **¿Todo debe ser puro?** No: los efectos son necesarios (I/O). La idea es aislarlos y mantener puro el núcleo.
- **¿Por qué importan las puras?** Se prueban fácil, se cachean (memoización) y se pueden paralelizar sin riesgo.

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

> [⏮️ Clase 083](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 085 ⏭️](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md)
