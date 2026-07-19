# Clase 126 — AOT vs. JIT: costos y beneficios

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comparar **AOT (compilación anticipada)** con **JIT (compilación en tiempo de ejecución)**. AOT compila todo antes de arrancar (rápido al iniciar); JIT compila sobre la marcha las partes calientes (arranque más lento, luego rápido).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una potencia de dos.
2. Explicar AOT vs. JIT.
3. Relacionar el modelo con arranque y rendimiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AOT | Compilar todo antes de ejecutar |
| 2 | JIT | Compilar las partes calientes al vuelo |
| 3 | Arranque vs. pico | Compromiso entre ambos |

## 📖 Definiciones y características

- **AOT** — compilación anticipada a código máquina (C, Rust, Go). Clave: arranque instantáneo.
- **JIT** — compilación durante la ejecución de lo más usado (JVM, V8). Clave: se calienta y acelera.
- **Código caliente** — el que se ejecuta muchas veces. Clave: el JIT lo optimiza.

## 🧩 Situación

Una herramienta de línea de comandos AOT arranca al instante; un servidor JIT tarda en calentar pero luego es muy rápido. El cálculo (2^n) es el mismo; cambia cuándo se compila.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 60)
- **Salida** (stdout): `resultado=<2^n>`
- **Regla:** 2 elevado a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=8` |
| `0` | `resultado=1` |
| `5` | `resultado=32` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
multiplicar 2 por sí mismo n veces (o desplazar bits)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"resultado={2 ** n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
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
        long r = 1;
        for (int i = 0; i < n; i++) r *= 2;
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long r = 1;
for (int i = 0; i < n; i++) r *= 2;
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var r int64 = 1
	for i := 0; i < n; i++ {
		r *= 2
	}
	fmt.Printf("resultado=%d\n", r)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u32 = s.trim().parse().unwrap();
    let r: i64 = 2i64.pow(n);
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    long r = 1;
    for (int i = 0; i < n; i++) r *= 2;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: potencia con un CTE recursivo (ilustrativo, n=3).
WITH RECURSIVE p(i, v) AS (VALUES (0, 1) UNION ALL SELECT i + 1, v * 2 FROM p WHERE i < 3)
SELECT printf('resultado=%d', v) AS resultado FROM p ORDER BY i DESC LIMIT 1;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$r = 1;
for ($i = 0; $i < $n; $i++) {
    $r *= 2;
}
echo "resultado=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle o desplazamiento de bits en cada lenguaje. |
| Semántica | El resultado no depende del modelo de compilación. |
| Paradigmática | SQL calcula con una expresión. |

## 🧬 El concepto en la familia

Go/Rust/C son AOT; la JVM y V8 son JIT; GraalVM ofrece AOT para la JVM.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 126
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desbordar con n grande** → causa: 2^64 no cabe → solución: aquí n <= 60
- **Empezar el acumulador en 0** → causa: siempre daría 0 → solución: iniciar el acumulador de producto en 1

## ❓ Preguntas frecuentes

- **¿AOT o JIT es mejor?** AOT para arranque rápido y binarios; JIT para procesos largos que se benefician del calentamiento.
- **¿Se pueden combinar?** Sí: GraalVM y otros ofrecen AOT sobre plataformas JIT.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 125](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 127 ⏭️](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md)
