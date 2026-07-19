# Clase 077 — Múltiples retornos y desestructuración

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Devolver **más de un valor** de una función y **desestructurarlos** al recibirlos. Go y Python lo hacen nativamente; otros usan tuplas, arreglos u objetos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Devolver varios valores de una función.
2. Desestructurar el resultado en variables.
3. Comparar tuplas, arreglos y objetos como vehículo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Múltiples retornos | Más de un valor de salida |
| 2 | Tupla | Agrupar valores sin nombre |
| 3 | Desestructuración | Repartir en variables |
| 4 | Vehículos | Tupla, arreglo, struct u objeto |

## 📖 Definiciones y características

- **Múltiple retorno** — una función devuelve varios valores. Clave: nativo en Go, Python, Rust.
- **Tupla** — grupo ordenado de valores. Clave: el vehículo habitual del multi-retorno.
- **Desestructuración** — repartir una tupla/objeto en variables. Clave: `q, r = divmod(a, b)`.
- **Struct/objeto de salida** — en Java/C se devuelve un objeto con campos. Clave: alternativa al multi-retorno.

## 🧩 Situación

`divmod(17, 5)` devuelve cociente 3 y resto 2 de una vez. Sin multi-retorno habría que llamar dos veces o crear un objeto solo para eso.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros positivos, b != 0)
- **Salida** (stdout): `cociente=<a/b> resto=<a%b>`
- **Regla:** (cociente, resto) = (a/b, a%b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `17 5` | `cociente=3 resto=2` |
| `10 2` | `cociente=5 resto=0` |
| `7 3` | `cociente=2 resto=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION divmod(a,b): DEVOLVER (a/b, a%b)
LEER a,b ; (q,r) <- divmod(a,b) ; ESCRIBIR q, r
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def divmod2(a, b):
    return a // b, a % b


a, b = map(int, sys.stdin.readline().split())
q, r = divmod2(a, b)
print(f"cociente={q} resto={r}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function divmod(a, b) {
  return [Math.trunc(a / b), a % b];
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function divmod(a: number, b: number): [number, number] {
  return [Math.trunc(a / b), a % b];
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r]: [number, number] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java devuelve un objeto (record) para varios valores.
    record DivRes(int cociente, int resto) {}

    static DivRes divmod(int a, int b) {
        return new DivRes(a / b, a % b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        DivRes d = divmod(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        System.out.println("cociente=" + d.cociente() + " resto=" + d.resto());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

(int, int) Divmod(int a, int b) => (a / b, a % b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var (q, r) = Divmod(int.Parse(p[0]), int.Parse(p[1]));
Console.WriteLine($"cociente={q} resto={r}");
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

func divmod(a, b int) (int, int) {
	return a / b, a % b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	q, r := divmod(a, b)
	fmt.Printf("cociente=%d resto=%d\n", q, r)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn divmod(a: i64, b: i64) -> (i64, i64) {
    (a / b, a % b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (q, r) = divmod(v[0], v[1]);
    println!("cociente={q} resto={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C devuelve un valor; el segundo va por puntero. */
long divmod(long a, long b, long *resto) {
    *resto = a % b;
    return a / b;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long q = divmod(a, b, &r);
    printf("cociente=%ld resto=%ld\n", q, r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: varias columnas por fila son un multi-retorno natural.
WITH pares(a, b) AS (VALUES (17, 5), (10, 2), (7, 3))
SELECT printf('cociente=%d resto=%d', a / b, a % b) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
function divmod($a, $b) {
    return [intdiv($a, $b), $a % $b];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
[$q, $r] = divmod((int) $a, (int) $b);
echo "cociente=$q resto=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `q, r = ...` (Python/Go/Rust) vs. objeto/arreglo (Java/JS). |
| Semántica | Go/Python devuelven varios valores; Java devuelve un objeto contenedor. |
| Paradigmática | SQL devuelve varias columnas por fila, un multi-retorno natural. |

## 🧬 El concepto en la familia

En Ruby `return q, r` (una tupla). En Kotlin, un `Pair` o un `data class`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 077
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Devolver un objeto solo para dos valores** → causa: sobre-ingeniería en lenguajes con tuplas → solución: usar el multi-retorno nativo si existe
- **Orden de la desestructuración** → causa: asignar cociente al resto → solución: respetar el orden de los valores devueltos

## ❓ Preguntas frecuentes

- **¿Tupla o struct?** Tupla para pocos valores anónimos; struct/clase si quieren nombres y significado.
- **¿Java tiene multi-retorno?** No nativo: se devuelve un objeto (record) con los campos.

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

> [⏮️ Clase 076](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 078 ⏭️](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md)
