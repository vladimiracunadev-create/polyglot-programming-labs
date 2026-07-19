# Clase 057 — Booleanos, condiciones y cortocircuito

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Producir booleanos con operadores de comparación y combinarlos con **AND cortocircuitado**. El cortocircuito evita evaluar la segunda condición si la primera ya decide el resultado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir booleanos a partir de comparaciones.
2. Combinar condiciones con AND/OR.
3. Explicar el cortocircuito y por qué importa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comparaciones | Producen valores de verdad |
| 2 | Operadores lógicos | AND, OR y su cortocircuito |
| 3 | Cortocircuito | No evalúa lo que no hace falta |
| 4 | Normalizar booleanos | true/false consistente entre lenguajes |

## 📖 Definiciones y características

- **Condición** — expresión que da verdadero o falso. Clave: gobierna las decisiones.
- **Cortocircuito** — en `a && b`, si `a` es falso no se evalúa `b`. Clave: evita trabajo y errores.
- **Operador relacional** — compara valores (>, <, ==). Clave: produce booleanos.
- **Predicado** — condición sobre un valor (es positivo, es par). Clave: bloque de la lógica.

## 🧩 Situación

Validar `if (usuario != null && usuario.activo)` depende del cortocircuito: sin él, se accedería a `usuario.activo` con `usuario` nulo y reventaría. El orden de las condiciones importa.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `positivo=<true|false> par=<true|false> ambos=<true|false>`
- **Regla:** positivo = n>0 ; par = n%2==0 ; ambos = positivo && par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `positivo=true par=true ambos=true` |
| `-3` | `positivo=false par=false ambos=false` |
| `7` | `positivo=true par=false ambos=false` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR positivo=(n>0), par=(n%2==0), ambos=((n>0) Y (n%2==0))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
tf = lambda x: "true" if x else "false"
pos = n > 0
par = n % 2 == 0
print(f"positivo={tf(pos)} par={tf(par)} ambos={tf(pos and par)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x) => (x ? "true" : "false");
const pos = n > 0;
const par = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x: boolean): string => (x ? "true" : "false");
const pos: boolean = n > 0;
const par: boolean = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        boolean pos = n > 0;
        boolean par = n % 2 == 0;
        System.out.printf("positivo=%s par=%s ambos=%s%n", tf(pos), tf(par), tf(pos && par));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string Tf(bool x) => x ? "true" : "false";
bool pos = n > 0;
bool par = n % 2 == 0;
Console.WriteLine($"positivo={Tf(pos)} par={Tf(par)} ambos={Tf(pos && par)}");
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

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	pos := n > 0
	par := n%2 == 0
	fmt.Printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pos = n > 0;
    let par = n % 2 == 0;
    println!("positivo={} par={} ambos={}", tf(pos), tf(par), tf(pos && par));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    int pos = n > 0;
    int par = n % 2 == 0;
    printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: condiciones con AND dentro de CASE WHEN.
WITH nums(n) AS (VALUES (4), (-3), (7))
SELECT printf('positivo=%s par=%s ambos=%s',
       CASE WHEN n > 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n > 0 AND n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$tf = fn($x) => $x ? "true" : "false";
$pos = $n > 0;
$par = $n % 2 === 0;
printf("positivo=%s par=%s ambos=%s\n", $tf($pos), $tf($par), $tf($pos && $par));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `and` (Python) vs. `&&` (C/Java/JS/Go/Rust/PHP). |
| Semántica | Todos cortocircuitan `&&`/`and`; C# imprime True/False (normalizar). |
| Paradigmática | SQL usa AND en la expresión y CASE WHEN para el texto. |

## 🧬 El concepto en la familia

En Ruby `n > 0 && n.even?`. En Haskell `n > 0 && even n`, con el mismo cortocircuito.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 057
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ordenar mal las condiciones** → causa: evaluar algo inválido antes de la guarda → solución: poner primero la condición que protege a la segunda
- **Imprimir True/False** → causa: formato por defecto de C# → solución: normalizar a minúsculas con un ayudante

## ❓ Preguntas frecuentes

- **¿`&` y `&&` son iguales?** No: `&` es bit a bit y evalúa ambos lados; `&&` cortocircuita.
- **¿El cortocircuito cambia el resultado?** No el valor lógico, pero sí si el segundo lado tiene efectos o puede fallar.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 056](../../parte-3-valores-tipos-y-variables/056-entrada-y-salida-basica-leer-y-escribir/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 058 ⏭️](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md)
