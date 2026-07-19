# Clase 136 — El modelo de memoria y las condiciones de carrera

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **modelo de memoria y las condiciones de carrera**: cuando dos hilos actualizan el mismo dato sin coordinación, el resultado puede corromperse. Incrementar de forma segura garantiza el valor correcto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una condición de carrera.
2. Reconocer la necesidad de sincronización.
3. Producir un conteo correcto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Condición de carrera | Dos hilos, un dato, sin orden |
| 2 | Sección crítica | Código que solo un hilo debe ejecutar a la vez |
| 3 | Atomicidad | Operación indivisible |

## 📖 Definiciones y características

- **Condición de carrera** — el resultado depende del orden imprevisible de dos accesos concurrentes. Clave: corrompe datos.
- **Sección crítica** — código que accede a un recurso compartido y debe ejecutarse en exclusión. Clave: se protege con un lock.
- **Operación atómica** — indivisible: ocurre entera o nada. Clave: evita la carrera en incrementos.

## 🧩 Situación

Si dos hilos hacen `contador++` a la vez sin protección, pueden leer el mismo valor y perder un incremento. Un lock o una operación atómica garantiza el conteo correcto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** incrementar un contador n veces, con exclusión

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; REPETIR n veces (protegido): cuenta <- cuenta + 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
cuenta = 0
for _ in range(n):  # sección crítica protegida (aquí, secuencial)
    cuenta += 1
print(f"cuenta={cuenta}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        AtomicInteger cuenta = new AtomicInteger(0);
        for (int i = 0; i < n; i++) cuenta.incrementAndGet();
        System.out.println("cuenta=" + cuenta.get());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Threading;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int cuenta = 0;
for (int i = 0; i < n; i++) Interlocked.Increment(ref cuenta);
Console.WriteLine($"cuenta={cuenta}");
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
	"sync"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var mu sync.Mutex
	cuenta := 0
	for i := 0; i < n; i++ {
		mu.Lock()
		cuenta++
		mu.Unlock()
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;
use std::sync::Mutex;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let cuenta = Mutex::new(0i64);
    for _ in 0..n {
        *cuenta.lock().unwrap() += 1;
    }
    println!("cuenta={}", *cuenta.lock().unwrap());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long cuenta = 0;
    for (long i = 0; i < n; i++) cuenta++;
    printf("cuenta=%ld\n", cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa transacciones para la consistencia; aquí, el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$cuenta = 0;
for ($i = 0; $i < $n; $i++) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | lock/mutex (Java/C#/Go), atómicos, o secuencial (aquí). |
| Semántica | Sin protección el resultado sería imprevisible con hilos reales. |
| Paradigmática | SQL usa transacciones para la consistencia. |

## 🧬 El concepto en la familia

Java (synchronized/AtomicInteger), Go (sync.Mutex/atomic), Rust (Mutex/Atomic) protegen la sección crítica.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 136
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Incrementar sin proteger** → causa: condición de carrera, conteo incorrecto → solución: usar lock o atómicos
- **Bloquear de más** → causa: cuello de botella → solución: minimizar la sección crítica

## ❓ Preguntas frecuentes

- **¿Toda variable compartida necesita lock?** Si más de un hilo la modifica, sí (o un tipo atómico).
- **¿Atómico o lock?** Atómico para operaciones simples; lock para secciones más complejas.

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

> [⏮️ Clase 135](../../parte-8-como-funcionan-los-lenguajes/135-actores-y-paso-de-mensajes-modelo-beam/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 137 ⏭️](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md)
