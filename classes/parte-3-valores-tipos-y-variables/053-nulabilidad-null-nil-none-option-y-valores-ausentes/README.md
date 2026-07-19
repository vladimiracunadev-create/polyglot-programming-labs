# Clase 053 — Nulabilidad: null, nil, None, Option y valores ausentes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Modelar la **ausencia de valor**: null, nil, None, Option. Usando 0 como centinela de 'ausente', verás cómo cada lenguaje representa y maneja la falta de un dato, y por qué las opciones tipadas (Option/Result) evitan el temido puntero nulo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir un valor presente de uno ausente.
2. Nombrar cómo cada lenguaje representa la ausencia.
3. Explicar por qué Option/None es más seguro que null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ausencia de valor | No todo dato existe siempre |
| 2 | null / nil / None | Nombres del 'nada' por lenguaje |
| 3 | Option / Maybe | Ausencia tipada y segura |
| 4 | El error del billón de dólares | Los NullPointerException |

## 📖 Definiciones y características

- **Nulabilidad** — posibilidad de que un valor esté ausente. Clave: fuente clásica de errores.
- **null / nil / None** — representación de 'sin valor'. Clave: cada lenguaje lo llama distinto.
- **Option / Maybe** — tipo que envuelve 'hay valor' o 'no hay' (Rust, Haskell). Clave: obliga a manejar la ausencia.
- **Valor centinela** — un valor normal usado para significar 'ausente' (aquí, 0). Clave: sencillo pero frágil.

## 🧩 Situación

Buscar un usuario que no existe: ¿qué devuelves? null puede reventar el programa más tarde con un NullPointerException. Modelar la ausencia explícitamente (Option/None) obliga a tratarla.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 significa ausente)
- **Salida** (stdout): `valor=<n>` si hay valor, o `valor=ausente` si n es 0
- **Regla:** si n == 0 → 'ausente'; si no → n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5` |
| `0` | `valor=ausente` |
| `42` | `valor=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
SI n == 0: ESCRIBIR "valor=ausente"
SINO: ESCRIBIR "valor=" n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print("valor=ausente" if n == 0 else f"valor={n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(n === 0 ? "valor=ausente" : `valor=${n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(n === 0 ? "valor=ausente" : `valor=${n}`);
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
        System.out.println(n == 0 ? "valor=ausente" : "valor=" + n);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine(n == 0 ? "valor=ausente" : $"valor={n}");
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
	if n == 0 {
		fmt.Println("valor=ausente")
	} else {
		fmt.Printf("valor=%d\n", n)
	}
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor: Option<i64> = if n == 0 { None } else { Some(n) };
    match valor {
        None => println!("valor=ausente"),
        Some(v) => println!("valor={v}"),
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n == 0) {
        printf("valor=ausente\n");
    } else {
        printf("valor=%ld\n", n);
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL tiene NULL nativo; aquí 0 modela la ausencia con CASE WHEN.
WITH nums(n) AS (VALUES (5), (0), (42))
SELECT CASE WHEN n = 0 THEN 'valor=ausente' ELSE printf('valor=%d', n) END AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo $n === 0 ? "valor=ausente\n" : "valor=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Operador ternario o `if` para decidir presente/ausente. |
| Semántica | Rust modela la ausencia con `Option<T>`; Java/C con null o un centinela. |
| Paradigmática | SQL tiene `NULL` nativo y `CASE WHEN` para tratarlo. |

## 🧬 El concepto en la familia

En Rust idiomático sería `Option<i64>` y un `match`. En Haskell `Maybe Int`. En Kotlin el tipo `Int?` marca la nulabilidad en el propio tipo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 053
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor ausente como si existiera** → causa: el NullPointerException clásico → solución: comprobar la ausencia antes de usar el valor
- **Elegir un centinela que es un dato válido** → causa: 0 podría ser legítimo → solución: preferir un tipo Option explícito cuando el lenguaje lo ofrece

## ❓ Preguntas frecuentes

- **¿Por qué null es peligroso?** Se cuela sin avisar y estalla al usarlo. Los tipos Option obligan a manejarlo.
- **¿Qué lenguajes del núcleo tienen Option?** Rust (`Option`). Otros usan null/nil; Kotlin (primo JVM) marca nulabilidad en el tipo.

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

> [⏮️ Clase 052](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 054 ⏭️](../../parte-3-valores-tipos-y-variables/054-mutabilidad-e-inmutabilidad/README.md)
