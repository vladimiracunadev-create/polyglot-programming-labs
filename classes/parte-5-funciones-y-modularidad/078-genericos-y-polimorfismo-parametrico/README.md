# Clase 078 — Genéricos y polimorfismo paramétrico

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una función **genérica**: la misma lógica para varios tipos, sin duplicar código. `max<T>` funciona con enteros, reales o texto porque solo exige que el tipo sea comparable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función genérica con un parámetro de tipo.
2. Explicar el polimorfismo paramétrico.
3. Reconocer las restricciones (comparable) de los genéricos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Genérico | Un tipo como parámetro |
| 2 | Polimorfismo paramétrico | Misma lógica, varios tipos |
| 3 | Restricciones | El tipo debe cumplir algo (comparable) |
| 4 | Sin duplicar | Una función en vez de N |

## 📖 Definiciones y características

- **Genérico** — función/tipo parametrizado por otro tipo (`max<T>`). Clave: reutilización con seguridad de tipos.
- **Polimorfismo paramétrico** — un código que funciona para muchos tipos. Clave: distinto del de herencia.
- **Restricción de tipo** — condición sobre el parámetro de tipo (comparable). Clave: habilita las operaciones.
- **Inferencia de tipo genérico** — el compilador deduce T al llamar. Clave: no hay que anotarlo.

## 🧩 Situación

Sin genéricos habría un `maxInt`, un `maxDouble`, un `maxString`... Con `max<T: Comparable>` se escribe una vez y sirve para todos, sin perder la comprobación de tipos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max<T>(a, b) = a si a>b, si no b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION max<T comparable>(a,b): DEVOLVER a SI a>b SINO b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def mayor(a, b):
    return a if a > b else b


a, b = map(int, sys.stdin.readline().split())
print(f"max={mayor(a, b)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// JS es dinámico: la función ya sirve para cualquier tipo comparable.
function mayor(a, b) {
  return a > b ? a : b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function mayor<T>(a: T, b: T): T {
  return a > b ? a : b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static <T extends Comparable<T>> T mayor(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        System.out.println("max=" + mayor(a, b));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

T Mayor<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"max={Mayor(a, b)}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"cmp"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func mayor[T cmp.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("max=%d\n", mayor(a, b))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn mayor<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("max={}", mayor(v[0], v[1]));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene genéricos: se escribe una función por tipo (o macros). */
long mayor(long a, long b) {
    return a > b ? a : b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("max=%ld\n", mayor(a, b));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: max() es polimórfico incorporado.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
// PHP es dinámico: la función sirve para cualquier tipo comparable.
function mayor($a, $b) {
    return $a > $b ? $a : $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "max=" . mayor((int) $a, (int) $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `<T>` (Java/C#/Rust), `[T any]` (Go), sin anotación (Python dinámico). |
| Semántica | Estáticos comprueban T al compilar; Python confía en pato (duck typing). |
| Paradigmática | SQL usa `max()` polimórfico incorporado. |

## 🧬 El concepto en la familia

En Kotlin `fun <T: Comparable<T>> maxOf`. En Haskell la firma `Ord a => a -> a -> a` expresa la restricción.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 078
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar Object en vez de genéricos (Java viejo)** → causa: perder la seguridad de tipos → solución: usar genéricos con restricción Comparable
- **Olvidar la restricción comparable** → causa: el tipo no soporta `>` → solución: acotar T a un tipo comparable

## ❓ Preguntas frecuentes

- **¿Genéricos o sobrecarga?** Genéricos evitan duplicar; sobrecarga es para comportamientos distintos por tipo.
- **¿Python tiene genéricos?** Su tipado dinámico ya es 'genérico'; con anotaciones existen `TypeVar` para herramientas.

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

> [⏮️ Clase 077](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 079 ⏭️](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md)
