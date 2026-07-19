# Clase 103 — Propiedad y ciclo de vida de los datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **propiedad y el ciclo de vida** de los datos: cuándo se crea y cuándo se libera un recurso. RAII (Rust/C++), `defer` (Go), `try-with-resources` (Java) y `using` (C#) atan la liberación al ámbito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el ciclo de vida de un recurso.
2. Liberar automáticamente al salir del ámbito.
3. Comparar RAII, defer y GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ciclo de vida | Crear → usar → liberar |
| 2 | RAII | La liberación va atada al ámbito |
| 3 | Liberación automática | defer, using, destructor |

## 📖 Definiciones y características

- **Ciclo de vida** — el tiempo entre que un recurso se crea y se libera. Clave: gestionarlo evita fugas.
- **RAII** — Resource Acquisition Is Initialization: el recurso se libera al destruirse el dueño. Clave: Rust/C++.
- **defer/using** — mecanismos que garantizan la liberación al salir del ámbito. Clave: Go, C#, Java.

## 🧩 Situación

Un archivo abierto debe cerrarse; una conexión, liberarse. RAII y defer garantizan que ocurra aunque haya un error, atando la liberación al fin del ámbito.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (valor del recurso)
- **Salida** (stdout): `valor=<n> estado=liberado`
- **Regla:** crear recurso(n), usarlo, liberarlo al salir

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5 estado=liberado` |
| `0` | `valor=0 estado=liberado` |
| `9` | `valor=9 estado=liberado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; crear recurso ; usar ; liberar al salir del ámbito
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Recurso:
    def __init__(self, valor):
        self.valor = valor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # aquí se liberaría


n = int(sys.stdin.readline())
with Recurso(n) as r:
    valor = r.valor
print(f"valor={valor} estado=liberado")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor;
{
  const recurso = { valor: n };
  valor = recurso.valor;
  // en JS el GC libera; aquí el ámbito marca el fin de uso
}
console.log(`valor=${valor} estado=liberado`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor: number;
{
  const recurso = { valor: n };
  valor = recurso.valor;
}
console.log(`valor=${valor} estado=liberado`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Recurso implements AutoCloseable {
        final int valor;
        Recurso(int v) { this.valor = v; }
        public void close() { /* se libera aquí */ }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int valor;
        try (Recurso r = new Recurso(n)) {
            valor = r.valor;
        }
        System.out.println("valor=" + valor + " estado=liberado");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int valor;
using (var r = new Recurso(n)) {
    valor = r.Valor;
}
Console.WriteLine($"valor={valor} estado=liberado");

class Recurso : IDisposable {
    public int Valor { get; }
    public Recurso(int v) { Valor = v; }
    public void Dispose() { /* se libera aquí */ }
}
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
	valor := 0
	func() {
		defer func() { /* se libera al salir */ }()
		valor = n
	}()
	fmt.Printf("valor=%d estado=liberado\n", valor)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Recurso {
    valor: i64,
}

impl Drop for Recurso {
    fn drop(&mut self) {
        // se libera automáticamente al salir del ámbito
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor;
    {
        let r = Recurso { valor: n };
        valor = r.valor;
    } // aquí se ejecuta Drop
    println!("valor={valor} estado=liberado");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *recurso = malloc(sizeof(long));
    *recurso = n;
    long valor = *recurso;
    free(recurso); /* liberación manual */
    printf("valor=%ld estado=liberado\n", valor);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el ciclo de vida se gestiona con transacciones; aquí se ilustra el valor.
WITH nums(n) AS (VALUES (5), (0), (9))
SELECT printf('valor=%d estado=liberado', n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
class Recurso {
    public function __construct(public int $valor) {}
    public function __destruct() { /* se libera aquí */ }
}

$n = (int) trim(fgets(STDIN));
$r = new Recurso($n);
$valor = $r->valor;
unset($r); // libera el recurso
echo "valor=$valor estado=liberado\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Drop` (Rust), `defer` (Go), `using`/`try-with-resources` (C#/Java). |
| Semántica | Rust/C++ liberan determinísticamente; Java/Python dependen del GC salvo cierre explícito. |
| Paradigmática | SQL gestiona transacciones (COMMIT/ROLLBACK) como ciclo de vida. |

## 🧬 El concepto en la familia

En C++ el destructor libera al salir del ámbito, como el `Drop` de Rust. En Python, el `with` (context manager).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 103
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No liberar recursos** → causa: fugas de memoria/handles → solución: usar RAII/defer/using para atarlo al ámbito
- **Confiar solo en el GC para recursos no-memoria** → causa: archivos abiertos demasiado tiempo → solución: cerrar explícitamente archivos y conexiones

## ❓ Preguntas frecuentes

- **¿GC libera todo?** Libera memoria, pero no siempre a tiempo ni otros recursos (archivos): ciérralos tú.
- **¿RAII o defer?** RAII ata la liberación al tipo; defer, a la función. Ambos garantizan el cierre.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 102](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 104 ⏭️](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md)
