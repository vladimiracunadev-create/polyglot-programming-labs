# Clase 079 — Paso por valor

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **paso por valor**: la función recibe una copia del argumento, así que modificar el parámetro dentro no afecta a la variable original de quien llama.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el paso por valor con un ejemplo.
2. Predecir que el original no cambia.
3. Reconocer que los primitivos se pasan por valor.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paso por valor | Se pasa una copia |
| 2 | Copia local | Modificarla no afecta fuera |
| 3 | Primitivos | Suelen pasarse por valor |
| 4 | Aislamiento | La función no toca al llamador |

## 📖 Definiciones y características

- **Paso por valor** — la función recibe una copia del argumento. Clave: el original no cambia.
- **Copia** — un duplicado independiente del valor. Clave: vive dentro de la función.
- **Parámetro local** — la variable de la función que contiene la copia. Clave: aislada del exterior.
- **Efecto en el llamador** — aquí, ninguno. Clave: la seguridad del paso por valor.

## 🧩 Situación

Pasas `n` a una función que lo duplica dentro; al volver, `n` sigue igual. La función trabajó con una copia. Entender esto evita esperar cambios que nunca ocurren.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `original=<n> local=<2n>`
- **Regla:** la función duplica una copia; el original permanece

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `original=5 local=10` |
| `3` | `original=3 local=6` |
| `0` | `original=0 local=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
local <- doblar(n)   // dentro trabaja una copia
ESCRIBIR "original=" n " local=" local
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doblar(x):
    x = x * 2  # modifica la copia local
    return x


n = int(sys.stdin.readline())
local = doblar(n)
print(f"original={n} local={local}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function doblar(x) {
  x = x * 2;
  return x;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const local = doblar(n);
console.log(`original=${n} local=${local}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function doblar(x: number): number {
  x = x * 2;
  return x;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const local: number = doblar(n);
console.log(`original=${n} local=${local}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int doblar(int x) {
        x = x * 2;
        return x;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int local = doblar(n);
        System.out.println("original=" + n + " local=" + local);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int Doblar(int x) {
    x = x * 2;
    return x;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int local = Doblar(n);
Console.WriteLine($"original={n} local={local}");
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

func doblar(x int) int {
	x = x * 2
	return x
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	local := doblar(n)
	fmt.Printf("original=%d local=%d\n", n, local)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(mut x: i64) -> i64 {
    x *= 2;
    x
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let local = doblar(n);
    println!("original={n} local={local}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doblar(long x) {
    x = x * 2; /* modifica la copia local */
    return x;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long local = doblar(n);
    printf("original=%ld local=%ld\n", n, local);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin variables del llamador; la expresión produce el valor.
WITH nums(n) AS (VALUES (5), (3), (0))
SELECT printf('original=%d local=%d', n, n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doblar($x) {
    $x = $x * 2;
    return $x;
}

$n = (int) trim(fgets(STDIN));
$local = doblar($n);
echo "original=$n local=$local\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Igual en todos: se llama y se recibe el retorno. |
| Semántica | Los primitivos se copian; el original nunca se altera. |
| Paradigmática | SQL no tiene variables mutables del llamador; todo es expresión. |

## 🧬 El concepto en la familia

En Ruby los enteros son inmutables: se comportan como paso por valor. En Java/Go/C, los primitivos siempre se pasan por valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 079
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que el original cambie** → causa: creer que se pasó por referencia → solución: recordar que los primitivos se copian
- **Modificar el parámetro creyendo que afecta fuera** → causa: no ver el aislamiento → solución: devolver el nuevo valor si quieres usarlo

## ❓ Preguntas frecuentes

- **¿Todo se pasa por valor?** Los primitivos sí; los objetos, la referencia se pasa por valor (siguiente clase).
- **¿Por qué es seguro?** La función no puede alterar por sorpresa las variables del llamador.

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

> [⏮️ Clase 078](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 080 ⏭️](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md)
