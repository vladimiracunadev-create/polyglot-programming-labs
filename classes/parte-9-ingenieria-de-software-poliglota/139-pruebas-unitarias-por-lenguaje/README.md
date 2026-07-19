# Clase 139 — Pruebas unitarias por lenguaje

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una **prueba unitaria**: código que comprueba automáticamente que otro código produce el resultado esperado. Es la base de la calidad y el corazón del verificador de este curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una aserción.
2. Distinguir prueba que pasa de la que falla.
3. Reconocer el runner de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prueba unitaria | Verifica una unidad de código |
| 2 | Aserción | Comprobar el valor esperado |
| 3 | Pasa/falla | Verde o rojo |

## 📖 Definiciones y características

- **Prueba unitaria** — código que verifica una unidad (función) de forma automática. Clave: repetible.
- **Aserción** — comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo.
- **Runner** — herramienta que ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas.

## 🧩 Situación

Antes de confiar en una función, se escribe una prueba: 'sumar(3,4) debe dar 7'. Si un cambio la rompe, la prueba lo detecta al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `test=<pasa|falla>`
- **Regla:** pasa si a + b == esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `test=pasa` |
| `2 2 5` | `test=falla` |
| `10 5 15` | `test=pasa` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"test={'pasa' if a + b == esperado else 'falla'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), esperado = Integer.parseInt(p[2]);
        System.out.println("test=" + (a + b == esperado ? "pasa" : "falla"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"test={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
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
	esperado, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == esperado {
		res = "pasa"
	}
	fmt.Printf("test=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] + v[1] == v[2] { "pasa" } else { "falla" };
    println!("test={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b, esperado;
    if (scanf("%ld %ld %ld", &a, &b, &esperado) != 3) return 1;
    printf("test=%s\n", a + b == esperado ? "pasa" : "falla");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una consulta de comprobación.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('test=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$a, $b, $esperado] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "test=" . ($a + $b === $esperado ? "pasa" : "falla") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | assert (Python), expect (JS), assertEquals (Java). |
| Semántica | La aserción compara y decide el estado de la prueba. |
| Paradigmática | SQL prueba con consultas de comprobación. |

## 🧬 El concepto en la familia

pytest (Python), JUnit (Java), cargo test (Rust), phpunit (PHP): mismo concepto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 139
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No probar los casos límite** → causa: bugs en los extremos → solución: incluir 0, vacío y negativos
- **Pruebas frágiles** → causa: fallan por cambios irrelevantes → solución: probar el comportamiento, no la implementación

## ❓ Preguntas frecuentes

- **¿Cuántas pruebas?** Al menos una por comportamiento y por caso límite.
- **¿casos.json es una prueba?** Sí: compara la salida real con la esperada.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 138](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 140 ⏭️](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md)
