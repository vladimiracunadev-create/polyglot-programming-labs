# Clase 157 — ABI, enlace y convenciones de llamada

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **ABI, el enlace y las convenciones de llamada**: para que dos piezas binarias se comuniquen, deben compartir la misma ABI (cómo se pasan los datos y se llaman las funciones). Un desajuste (p. ej. 32 vs 64 bits) rompe la interoperabilidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la ABI.
2. Detectar una incompatibilidad de ABI.
3. Distinguir ABI de API.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | ABI | Contrato binario |
| 2 | Convención de llamada | Cómo se pasan los argumentos |
| 3 | Compatibilidad | Mismo ABI para enlazar |

## 📖 Definiciones y características

- **ABI** — Application Binary Interface: cómo se representan datos y se llaman funciones a nivel binario. Clave: debe coincidir para enlazar.
- **Convención de llamada** — reglas de paso de argumentos y retorno. Clave: parte de la ABI.
- **API vs. ABI** — API es el contrato en código fuente; ABI, el binario. Clave: distinto nivel.

## 🧩 Situación

Enlazar una librería de 32 bits con un programa de 64 bits falla: sus ABI no coinciden. La ABI es el contrato invisible que hace posible (o imposible) que dos binarios cooperen.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (ancho de bits de cada componente)
- **Salida** (stdout): `abi=<compatible|incompatible>`
- **Regla:** compatible si los anchos coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `64 64` | `abi=compatible` |
| `64 32` | `abi=incompatible` |
| `32 32` | `abi=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"abi={'compatible' if a == b else 'incompatible'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`abi=${a === b ? "compatible" : "incompatible"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`abi=${a === b ? "compatible" : "incompatible"}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]);
        System.out.println("abi=" + (a == b ? "compatible" : "incompatible"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]), b = int.Parse(p[1]);
Console.WriteLine($"abi={(a == b ? "compatible" : "incompatible")}");
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
	res := "incompatible"
	if a == b {
		res = "compatible"
	}
	fmt.Printf("abi=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] == v[1] { "compatible" } else { "incompatible" };
    println!("abi={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("abi=%s\n", a == b ? "compatible" : "incompatible");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL compara los anchos.
WITH t(a, b) AS (VALUES (64, 64))
SELECT printf('abi=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "abi=" . ($a === $b ? "compatible" : "incompatible") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Comparación de enteros en cada lenguaje. |
| Semántica | La ABI incluye tamaños, alineación y convención de llamada. |
| Paradigmática | SQL compara valores. |

## 🧬 El concepto en la familia

Cada plataforma (x86-64 System V, Windows x64) define su ABI; los binarios deben respetarla para enlazar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 157
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar binarios de distinta arquitectura** → causa: fallo de enlace o corrupción → solución: compilar todo para la misma ABI
- **Confundir API con ABI** → causa: esperar compatibilidad binaria del código fuente → solución: recordar que son contratos de distinto nivel

## ❓ Preguntas frecuentes

- **¿API o ABI?** API es el contrato fuente; ABI, el binario. Un cambio de ABI rompe binarios ya compilados.
- **¿Por qué importa la ABI?** Para enlazar librerías compiladas y usar la FFI sin corromper datos.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

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

> [⏮️ Clase 156](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 158 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md)
