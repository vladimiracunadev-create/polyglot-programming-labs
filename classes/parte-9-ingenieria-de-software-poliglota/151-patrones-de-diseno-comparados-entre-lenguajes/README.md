# Clase 151 — Patrones de diseño comparados entre lenguajes

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar los **patrones de diseño comparados**: el patrón **Estrategia** encapsula algoritmos intercambiables tras una interfaz común. Elegir la operación por su nombre selecciona la estrategia a aplicar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Aplicar el patrón Estrategia.
2. Seleccionar un algoritmo en ejecución.
3. Reconocer patrones en cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Patrón de diseño | Solución reutilizable a un problema común |
| 2 | Estrategia | Algoritmos intercambiables |
| 3 | Selección en ejecución | Elegir el comportamiento al vuelo |

## 📖 Definiciones y características

- **Patrón de diseño** — solución probada y reutilizable a un problema de diseño recurrente. Clave: vocabulario común.
- **Estrategia** — patrón que encapsula algoritmos intercambiables tras una interfaz. Clave: cambiar el comportamiento sin condicionales dispersos.
- **Despacho** — seleccionar qué código ejecutar según un valor. Clave: aquí, por el nombre de la operación.

## 🧩 Situación

Un sistema de cobro puede usar distintas estrategias (tarjeta, transferencia). El patrón Estrategia las hace intercambiables. Aquí, la operación se elige por su nombre y se aplica.

## 🧮 Modelo

- **Entrada** (stdin): una línea `estrategia a b` (estrategia ∈ {suma, resta, producto})
- **Salida** (stdout): `resultado=<a estrategia b>`
- **Regla:** aplicar la estrategia elegida a a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `suma 3 4` | `resultado=7` |
| `resta 10 3` | `resultado=7` |
| `producto 5 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER estrategia, a, b ; seleccionar operación ; aplicar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

estrategia, a, b = sys.stdin.readline().split()
a, b = int(a), int(b)
ops = {"suma": a + b, "resta": a - b, "producto": a * b}
print(f"resultado={ops[estrategia]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops: Record<string, number> = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[1]), b = Long.parseLong(t[2]);
        long r;
        switch (t[0]) {
            case "suma": r = a + b; break;
            case "resta": r = a - b; break;
            default: r = a * b;
        }
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[1]), b = long.Parse(t[2]);
long r = t[0] switch { "suma" => a + b, "resta" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[1])
	b, _ := strconv.Atoi(t[2])
	ops := map[string]int{"suma": a + b, "resta": a - b, "producto": a * b}
	fmt.Printf("resultado=%d\n", ops[t[0]])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[1].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[0] {
        "suma" => a + b,
        "resta" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char e[32];
    long a, b;
    if (scanf("%31s %ld %ld", e, &a, &b) != 3) return 1;
    long r;
    if (strcmp(e, "suma") == 0) r = a + b;
    else if (strcmp(e, "resta") == 0) r = a - b;
    else r = a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selecciona la estrategia con CASE.
WITH t(e, a, b) AS (VALUES ('suma', 3, 4))
SELECT printf('resultado=%d', CASE e WHEN 'suma' THEN a + b WHEN 'resta' THEN a - b ELSE a * b END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$e, $a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$ops = ["suma" => $a + $b, "resta" => $a - $b, "producto" => $a * $b];
echo "resultado=" . $ops[$e] . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | map de funciones, interfaz o switch en cada lenguaje. |
| Semántica | La estrategia se elige en ejecución. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

Estrategia, Observer, Factory, Singleton son patrones clásicos (GoF) presentes en todos los lenguajes OO.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 151
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Condicionales gigantes en vez de estrategias** → causa: código rígido → solución: encapsular cada algoritmo tras una interfaz común
- **Sobre-aplicar patrones** → causa: complejidad innecesaria → solución: usar el patrón solo cuando aporta

## ❓ Preguntas frecuentes

- **¿Estrategia o if/else?** Estrategia cuando los algoritmos cambian o crecen; if/else para casos simples y fijos.
- **¿Los patrones son obligatorios?** No: son herramientas; aplícalos cuando resuelven un problema real.

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

> [⏮️ Clase 150](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 152 ⏭️](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md)
