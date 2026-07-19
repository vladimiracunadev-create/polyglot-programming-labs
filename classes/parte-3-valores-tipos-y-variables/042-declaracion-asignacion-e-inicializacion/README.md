# Clase 042 — Declaración, asignación e inicialización

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir tres actos que a menudo se confunden: **declarar** (introducir un nombre), **inicializar** (darle su primer valor) y **asignar** (cambiarlo después). El intercambio de dos variables los ejercita todos y revela cómo cada lenguaje los expresa (variable temporal vs. asignación múltiple).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar declaración, inicialización y (re)asignación.
2. Intercambiar dos variables con y sin temporal según el lenguaje.
3. Reconocer la asignación múltiple (desestructuración) donde existe.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarar vs. inicializar | Introducir un nombre no es lo mismo que darle valor |
| 2 | Reasignación | Cambiar el valor de una variable ya inicializada |
| 3 | Variable temporal | El patrón clásico para intercambiar |
| 4 | Asignación múltiple | a, b = b, a donde el lenguaje lo permite |

## 📖 Definiciones y características

- **Declaración** — introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usarla sin inicializar es un error clásico.
- **Asignación** — cambiar el valor de una variable existente. Clave: solo posible si es mutable.
- **Asignación múltiple** — asignar varias variables a la vez (a, b = b, a). Clave: evita la temporal en Python, JS, Go, Rust.

## 🧩 Situación

Intercambiar dos valores parece trivial, pero es donde se ve si un lenguaje ofrece asignación múltiple (Python, Go, Rust, JS) o exige la variable temporal de toda la vida (C, Java).

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `a=<nuevo a> b=<nuevo b>` tras intercambiar
- **Regla:** intercambiar a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `a=7 b=3` |
| `0 5` | `a=5 b=0` |
| `-2 9` | `a=9 b=-2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
tmp <- a ; a <- b ; b <- tmp   (o bien: a, b <- b, a)
ESCRIBIR "a=" a " b=" b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

# Declaración e inicialización a partir de la entrada.
a, b = sys.stdin.readline().split()
a, b = int(a), int(b)

# Asignación múltiple: intercambio sin variable temporal.
a, b = b, a

print(f"a={a} b={b}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

let [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

// Desestructuración: intercambio en una sola línea.
[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

let [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
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

        // Java no tiene asignación múltiple: variable temporal.
        int tmp = a;
        a = b;
        b = tmp;

        System.out.println("a=" + a + " b=" + b);
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

// C# sí ofrece asignación por tuplas.
(a, b) = (b, a);

Console.WriteLine($"a={a} b={b}");
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

	// Go permite intercambio con asignación múltiple.
	a, b = b, a

	fmt.Printf("a=%d b=%d\n", a, b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();

    // Intercambio por desestructuración de tupla.
    let (a, b) = (v[1], v[0]);

    println!("a={a} b={b}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;

    /* C exige una variable temporal para intercambiar. */
    long tmp = a;
    a = b;
    b = tmp;

    printf("a=%ld b=%ld\n", a, b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no reasigna variables: se describe la salida intercambiando columnas.
WITH pares(a, b) AS (VALUES (3, 7), (0, 5), (-2, 9))
SELECT printf('a=%d b=%d', b, a) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;

// PHP admite intercambio por lista.
[$a, $b] = [$b, $a];

printf("a=%d b=%d\n", $a, $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a, b = b, a` (Python/JS/Go/Rust) vs. `tmp=a;a=b;b=tmp;` (C/Java). |
| Semántica | La asignación múltiple evalúa el lado derecho antes de asignar; la temporal es manual. |
| Paradigmática | SQL no reasigna variables: se describe la salida intercambiando columnas. |

## 🧬 El concepto en la familia

En Ruby (scripting dinámico) es `a, b = b, a`, igual que Python. En Kotlin (JVM) se usa `also` o una temporal; en Haskell no hay reasignación: se define un nuevo valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 042
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder un valor al intercambiar sin temporal** → causa: asignar a=b antes de guardar a → solución: usar una temporal o la asignación múltiple del lenguaje
- **Usar una variable sin inicializar** → causa: declararla y no darle valor (C) → solución: inicializar siempre en la declaración

## ❓ Preguntas frecuentes

- **¿La asignación múltiple es más lenta?** No de forma apreciable; es más legible y evita el error de la temporal.
- **¿Por qué C no la tiene?** Es un lenguaje minimalista; el patrón con temporal es explícito y suficiente.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

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

> [⏮️ Clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 043 ⏭️](../../parte-3-valores-tipos-y-variables/043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md)
