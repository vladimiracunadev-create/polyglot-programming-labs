# Clase 110 — Orientado a objetos: clases, objetos y estado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **orientado a objetos**: agrupar estado (datos) y comportamiento (métodos) en objetos. Un contador con su método `incrementar` es el ejemplo mínimo de estado encapsulado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una clase con estado y métodos.
2. Crear un objeto y cambiar su estado.
3. Reconocer la unión de datos y comportamiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Clase y objeto | Molde e instancia |
| 2 | Estado | Datos del objeto |
| 3 | Método | Comportamiento que actúa sobre el estado |

## 📖 Definiciones y características

- **Objeto** — instancia que agrupa estado y comportamiento. Clave: datos + métodos juntos.
- **Clase** — molde que define objetos. Clave: describe estado y métodos.
- **Método** — función asociada a un objeto que opera sobre su estado. Clave: `contador.incrementar()`.

## 🧩 Situación

Un carrito de compra, una cuenta, un contador: la OO modela entidades con estado que evoluciona mediante métodos. El objeto recuerda su estado entre llamadas.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** contador incrementado n veces desde 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
c <- Contador() ; REPETIR n veces: c.incrementar() ; ESCRIBIR c.cuenta
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Contador:
    def __init__(self):
        self.cuenta = 0

    def incrementar(self):
        self.cuenta += 1


n = int(sys.stdin.readline())
c = Contador()
for _ in range(n):
    c.incrementar()
print(f"cuenta={c.cuenta}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Contador {
  constructor() {
    this.cuenta = 0;
  }
  incrementar() {
    this.cuenta++;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Contador();
for (let i = 0; i < n; i++) c.incrementar();
console.log(`cuenta=${c.cuenta}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

class Contador {
  cuenta = 0;
  incrementar(): void {
    this.cuenta++;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Contador();
for (let i = 0; i < n; i++) c.incrementar();
console.log(`cuenta=${c.cuenta}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Contador {
        int cuenta = 0;
        void incrementar() { cuenta++; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Contador c = new Contador();
        for (int i = 0; i < n; i++) c.incrementar();
        System.out.println("cuenta=" + c.cuenta);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var c = new Contador();
for (int i = 0; i < n; i++) c.Incrementar();
Console.WriteLine($"cuenta={c.Cuenta}");

class Contador {
    public int Cuenta { get; private set; }
    public void Incrementar() => Cuenta++;
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

type Contador struct {
	cuenta int
}

func (c *Contador) incrementar() {
	c.cuenta++
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	c := &Contador{}
	for i := 0; i < n; i++ {
		c.incrementar()
	}
	fmt.Printf("cuenta=%d\n", c.cuenta)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Contador {
    cuenta: i64,
}

impl Contador {
    fn nuevo() -> Self {
        Contador { cuenta: 0 }
    }
    fn incrementar(&mut self) {
        self.cuenta += 1;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Contador::nuevo();
    for _ in 0..n {
        c.incrementar();
    }
    println!("cuenta={}", c.cuenta);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Contador {
    long cuenta;
};

void incrementar(struct Contador *c) {
    c->cuenta++;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Contador c = {0};
    for (long i = 0; i < n; i++) incrementar(&c);
    printf("cuenta=%ld\n", c.cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene objetos con estado; el contador es el propio valor.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
class Contador {
    public int $cuenta = 0;
    public function incrementar() {
        $this->cuenta++;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Contador();
for ($i = 0; $i < $n; $i++) {
    $c->incrementar();
}
echo "cuenta={$c->cuenta}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `class` (Python/Java/C#/PHP), `struct`+métodos (Go/Rust), objeto (JS). |
| Semántica | El objeto conserva su estado entre llamadas a métodos. |
| Paradigmática | SQL no tiene objetos con estado; opera sobre datos. |

## 🧬 El concepto en la familia

En Ruby todo es un objeto. En Go/Rust no hay clases, pero structs con métodos cumplen el rol.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 110
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin control** → causa: objetos que se pisan → solución: encapsular el estado en cada objeto
- **Confundir clase con objeto** → causa: molde vs. instancia → solución: la clase define; el objeto existe

## ❓ Preguntas frecuentes

- **¿Todo debe ser objeto?** No: la OO es una herramienta; a veces una función basta.
- **¿Go tiene clases?** No, pero structs con métodos ofrecen lo esencial de la OO.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 109](../../parte-7-paradigmas/109-procedimental-y-modular/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 111 ⏭️](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md)
