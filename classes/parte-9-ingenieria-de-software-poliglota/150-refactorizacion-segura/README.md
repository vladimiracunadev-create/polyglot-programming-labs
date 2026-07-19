# Clase 150 — Refactorización segura

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **refactorización segura**: mejorar la estructura interna del código sin cambiar su comportamiento observable, respaldado por pruebas. Cambiar `n*2` por `n+n` es una refactorización que las pruebas confirman equivalente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Refactorizar sin cambiar el resultado.
2. Verificar la equivalencia con una prueba.
3. Explicar por qué las pruebas habilitan refactorizar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Refactorización | Mejorar sin cambiar comportamiento |
| 2 | Comportamiento observable | Lo que se mantiene |
| 3 | Red de pruebas | Habilita el cambio seguro |

## 📖 Definiciones y características

- **Refactorización** — reestructurar el código sin alterar su comportamiento observable. Clave: mejora interna.
- **Comportamiento observable** — lo que el usuario/prueba percibe. Clave: no debe cambiar al refactorizar.
- **Red de seguridad** — las pruebas que confirman que la refactorización no rompió nada. Clave: sin ellas, refactorizar es arriesgado.

## 🧩 Situación

Quieres simplificar una función. Con pruebas que fijan su comportamiento, refactorizas con confianza: si las pruebas siguen verdes, el comportamiento se mantuvo. Aquí `n*2` y `n+n` son equivalentes.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `equivalente=<true|false> resultado=<2n>`
- **Regla:** viejo = n*2 ; nuevo = n+n ; equivalente si coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `equivalente=true resultado=10` |
| `0` | `equivalente=true resultado=0` |
| `7` | `equivalente=true resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
viejo <- n*2 ; nuevo <- n+n ; equivalente <- (viejo==nuevo) ; ESCRIBIR
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
viejo = n * 2
nuevo = n + n
eq = "true" if viejo == nuevo else "false"
print(f"equivalente={eq} resultado={nuevo}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        long viejo = n * 2, nuevo = n + n;
        System.out.println("equivalente=" + (viejo == nuevo ? "true" : "false") + " resultado=" + nuevo);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
long viejo = n * 2, nuevo = n + n;
Console.WriteLine($"equivalente={(viejo == nuevo ? "true" : "false")} resultado={nuevo}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	viejo, nuevo := n*2, n+n
	res := "false"
	if viejo == nuevo {
		res = "true"
	}
	fmt.Printf("equivalente=%s resultado=%d\n", res, nuevo)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let (viejo, nuevo) = (n * 2, n + n);
    let eq = if viejo == nuevo { "true" } else { "false" };
    println!("equivalente={eq} resultado={nuevo}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long viejo = n * 2, nuevo = n + n;
    printf("equivalente=%s resultado=%ld\n", viejo == nuevo ? "true" : "false", nuevo);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: dos expresiones equivalentes.
WITH nums(n) AS (VALUES (5))
SELECT printf('equivalente=%s resultado=%d', CASE WHEN n * 2 = n + n THEN 'true' ELSE 'false' END, n + n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$viejo = $n * 2;
$nuevo = $n + $n;
echo "equivalente=" . ($viejo === $nuevo ? "true" : "false") . " resultado=$nuevo\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Dos expresiones equivalentes en cada lenguaje. |
| Semántica | La refactorización preserva el resultado observable. |
| Paradigmática | SQL refactoriza consultas manteniendo el resultado. |

## 🧬 El concepto en la familia

Todos los IDE ofrecen refactorizaciones automáticas (renombrar, extraer) respaldadas por el análisis.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 150
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Refactorizar sin pruebas** → causa: romper comportamiento sin darte cuenta → solución: asegurar la red de pruebas primero
- **Cambiar comportamiento 'de paso'** → causa: no es refactorizar, es modificar → solución: separar refactorización de cambio funcional

## ❓ Preguntas frecuentes

- **¿Refactorizar cambia el comportamiento?** No: por definición lo preserva; solo mejora la estructura.
- **¿Cuándo refactorizar?** Continuamente, en pequeños pasos, con las pruebas en verde.

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

> [⏮️ Clase 149](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 151 ⏭️](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md)
