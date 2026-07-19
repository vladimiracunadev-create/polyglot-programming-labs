# Clase 080 — Paso por referencia

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **paso por referencia**: la función recibe un enlace a la variable original, así que modificar el parámetro **sí** cambia la variable de quien llama. C usa punteros, Go `*`, Rust `&mut`, C# `ref`.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Modificar una variable del llamador desde una función.
2. Distinguir referencia de copia.
3. Reconocer cómo cada lenguaje pasa referencias.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paso por referencia | Se pasa un enlace, no una copia |
| 2 | Punteros/referencias | &, *, ref, &mut |
| 3 | Efecto en el llamador | El original cambia |
| 4 | Riesgo | Modificaciones a distancia |

## 📖 Definiciones y características

- **Paso por referencia** — la función accede a la variable original. Clave: puede modificarla.
- **Puntero** — valor que guarda la dirección de otra variable (C). Clave: permite modificarla.
- **Referencia mutable** — enlace que permite cambiar el valor (`&mut` en Rust, `ref` en C#). Clave: modificación explícita.
- **Efecto secundario** — cambiar algo fuera de la función. Clave: potente pero peligroso.

## 🧩 Situación

Una función `doblar(&n)` cambia `n` para siempre. Es útil (evita copiar datos grandes) pero peligroso: modificaciones 'a distancia' que sorprenden si no se esperan.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `antes=<n> despues=<2n>`
- **Regla:** la función duplica la variable original vía referencia

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `antes=5 despues=10` |
| `3` | `antes=3 despues=6` |
| `7` | `antes=7 despues=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; antes <- n
doblar(referencia a n)   // modifica el original
ESCRIBIR "antes=" antes " despues=" n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doblar(caja):
    caja[0] *= 2  # modifica el contenido compartido


n = int(sys.stdin.readline())
antes = n
caja = [n]
doblar(caja)
print(f"antes={antes} despues={caja[0]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function doblar(caja) {
  caja.v *= 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function doblar(caja: { v: number }): void {
  caja.v *= 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes: number = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java pasa la referencia del arreglo: se puede mutar su contenido.
    static void doblar(int[] caja) {
        caja[0] *= 2;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int antes = n;
        int[] caja = { n };
        doblar(caja);
        System.out.println("antes=" + antes + " despues=" + caja[0]);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

void Doblar(ref int x) {
    x *= 2;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int antes = n;
int v = n;
Doblar(ref v);
Console.WriteLine($"antes={antes} despues={v}");
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

func doblar(p *int) {
	*p *= 2
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	antes := n
	doblar(&n)
	fmt.Printf("antes=%d despues=%d\n", antes, n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(x: &mut i64) {
    *x *= 2;
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut n: i64 = s.trim().parse().unwrap();
    let antes = n;
    doblar(&mut n);
    println!("antes={antes} despues={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

void doblar(long *p) {
    *p *= 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long antes = n;
    doblar(&n);
    printf("antes=%ld despues=%ld\n", antes, n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no modifica variables; el 'despues' se calcula en la expresión.
WITH nums(n) AS (VALUES (5), (3), (7))
SELECT printf('antes=%d despues=%d', n, n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doblar(&$x) {
    $x *= 2;
}

$n = (int) trim(fgets(STDIN));
$antes = $n;
doblar($n);
echo "antes=$antes despues=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `*p` (C/Go), `&mut` (Rust), `ref` (C#), objeto/lista (Java/JS/Python). |
| Semántica | Referencia mutable cambia el original; los primitivos por valor no. |
| Paradigmática | SQL no modifica variables: usa UPDATE sobre datos. |

## 🧬 El concepto en la familia

En Ruby los objetos se pasan por referencia (de valor); los enteros no se mutan. En C++ hay referencias `&` explícitas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 080
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar sin querer el original** → causa: efecto secundario inesperado → solución: pasar por valor si no debes cambiar el original
- **Confundir puntero con valor** → causa: modificar la copia del puntero → solución: desreferenciar (`*p`) para tocar el valor apuntado

## ❓ Preguntas frecuentes

- **¿Referencia o valor?** Referencia para modificar o evitar copiar datos grandes; valor para aislar.
- **¿Java pasa por referencia?** Pasa la referencia por valor: puedes mutar el objeto, no reasignar la variable del llamador.

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

> [⏮️ Clase 079](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 081 ⏭️](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md)
