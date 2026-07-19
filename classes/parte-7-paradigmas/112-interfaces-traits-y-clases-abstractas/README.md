# Clase 112 — Interfaces, traits y clases abstractas

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **interfaces / traits / clases abstractas**: un contrato que varios tipos implementan. Distintas figuras exponen `area()` y el programa las usa sin conocer el tipo concreto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un contrato (interfaz) y varias implementaciones.
2. Programar contra la interfaz, no la implementación.
3. Distinguir interfaz de clase abstracta.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interfaz/trait | Un contrato sin implementación |
| 2 | Implementar | Cumplir el contrato |
| 3 | Programar contra la interfaz | Desacoplar del tipo concreto |

## 📖 Definiciones y características

- **Interfaz** — conjunto de métodos que un tipo promete implementar. Clave: contrato sin código.
- **Trait** — el equivalente en Rust; puede llevar métodos por defecto. Clave: composición de comportamiento.
- **Clase abstracta** — clase incompleta que otras extienden. Clave: contrato + estado parcial.

## 🧩 Situación

`Forma` define `area()`; cuadrado y rectángulo lo implementan. El código que dibuja o mide no necesita saber qué figura es: confía en el contrato.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área>`
- **Regla:** cada figura implementa area() a su manera

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 6` | `area=36` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER figura ; f: Forma ; ESCRIBIR f.area()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Cuadrado:
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l * self.l


class Rectangulo:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def area(self):
        return self.a * self.b


t = sys.stdin.readline().split()
f = Cuadrado(int(t[1])) if t[0] == "cuadrado" else Rectangulo(int(t[1]), int(t[2]))
print(f"area={f.area()}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Cuadrado { constructor(l) { this.l = l; } area() { return this.l * this.l; } }
class Rectangulo { constructor(a, b) { this.a = a; this.b = b; } area() { return this.a * this.b; } }

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const f = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

interface Forma { area(): number; }
class Cuadrado implements Forma { constructor(private l: number) {} area() { return this.l * this.l; } }
class Rectangulo implements Forma { constructor(private a: number, private b: number) {} area() { return this.a * this.b; } }

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const f: Forma = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    interface Forma { long area(); }
    static class Cuadrado implements Forma {
        long l; Cuadrado(long l) { this.l = l; }
        public long area() { return l * l; }
    }
    static class Rectangulo implements Forma {
        long a, b; Rectangulo(long a, long b) { this.a = a; this.b = b; }
        public long area() { return a * b; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Forma f = t[0].equals("cuadrado")
                ? new Cuadrado(Long.parseLong(t[1]))
                : new Rectangulo(Long.parseLong(t[1]), Long.parseLong(t[2]));
        System.out.println("area=" + f.area());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
IForma f = t[0] == "cuadrado"
    ? new Cuadrado(long.Parse(t[1]))
    : new Rectangulo(long.Parse(t[1]), long.Parse(t[2]));
Console.WriteLine($"area={f.Area()}");

interface IForma { long Area(); }
class Cuadrado : IForma { long l; public Cuadrado(long l) { this.l = l; } public long Area() => l * l; }
class Rectangulo : IForma { long a, b; public Rectangulo(long a, long b) { this.a = a; this.b = b; } public long Area() => a * b; }
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

type Forma interface {
	area() int64
}

type Cuadrado struct{ l int64 }
type Rectangulo struct{ a, b int64 }

func (c Cuadrado) area() int64   { return c.l * c.l }
func (r Rectangulo) area() int64 { return r.a * r.b }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	var f Forma
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		f = Cuadrado{l}
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		f = Rectangulo{a, b}
	}
	fmt.Printf("area=%d\n", f.area())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

trait Forma {
    fn area(&self) -> i64;
}

struct Cuadrado(i64);
struct Rectangulo(i64, i64);

impl Forma for Cuadrado { fn area(&self) -> i64 { self.0 * self.0 } }
impl Forma for Rectangulo { fn area(&self) -> i64 { self.0 * self.1 } }

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let f: Box<dyn Forma> = if t[0] == "cuadrado" {
        Box::new(Cuadrado(t[1].parse().unwrap()))
    } else {
        Box::new(Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap()))
    };
    println!("area={}", f.area());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    long area;
    if (strcmp(tipo, "cuadrado") == 0) {
        long l; if (scanf("%ld", &l) != 1) return 1; area = l * l;
    } else {
        long a, b; if (scanf("%ld %ld", &a, &b) != 2) return 1; area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin interfaces; se usa CASE.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado FROM formas;
```

### PHP · `php main.php`

```php
<?php
interface Forma { public function area(): int; }
class Cuadrado implements Forma {
    public function __construct(private int $l) {}
    public function area(): int { return $this->l * $this->l; }
}
class Rectangulo implements Forma {
    public function __construct(private int $a, private int $b) {}
    public function area(): int { return $this->a * $this->b; }
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$f = $t[0] === "cuadrado" ? new Cuadrado((int) $t[1]) : new Rectangulo((int) $t[1], (int) $t[2]);
echo "area=" . $f->area() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `interface` (Java/C#/Go/TS/PHP), `trait` (Rust), duck typing (Python/JS). |
| Semántica | El contrato desacopla el uso del tipo concreto. |
| Paradigmática | SQL usa CASE; no hay interfaces. |

## 🧬 El concepto en la familia

En Kotlin, interfaces con métodos por defecto. En C++, clases abstractas con métodos virtuales puros.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 112
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depender de la implementación concreta** → causa: acoplamiento rígido → solución: programar contra la interfaz
- **Interfaz demasiado grande** → causa: difícil de implementar → solución: preferir interfaces pequeñas y enfocadas

## ❓ Preguntas frecuentes

- **¿Interfaz o clase abstracta?** Interfaz para un contrato puro; abstracta si compartes estado/código parcial.
- **¿Go tiene interfaces?** Sí, y se cumplen implícitamente (structural typing).

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

> [⏮️ Clase 111](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 113 ⏭️](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md)
