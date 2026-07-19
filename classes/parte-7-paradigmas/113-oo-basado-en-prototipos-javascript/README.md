# Clase 113 — OO basado en prototipos (JavaScript)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer la **OO basada en prototipos** de JavaScript: los objetos heredan directamente de otros objetos, no de clases. Aquí un objeto con un método `doble` calcula sobre su valor.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear un objeto con estado y método.
2. Explicar la herencia por prototipos.
3. Contrastar prototipos con clases.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prototipos | Objetos que heredan de objetos |
| 2 | Método en objeto | Comportamiento ligado al valor |
| 3 | Clases vs. prototipos | Dos modelos de OO |

## 📖 Definiciones y características

- **Prototipo** — objeto del que otro hereda propiedades y métodos. Clave: cadena de prototipos en JS.
- **Objeto literal** — objeto creado directamente con sus campos y métodos. Clave: `{ v: n, doble() {...} }`.
- **this** — referencia al objeto sobre el que se llama el método. Clave: accede a su estado.

## 🧩 Situación

JavaScript no tenía clases originalmente: los objetos heredaban de otros objetos (prototipos). Aunque hoy tiene `class`, por debajo sigue siendo prototipos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** objeto.doble() = valor·2

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
obj <- { valor: n, doble() { DEVOLVER valor*2 } } ; ESCRIBIR obj.doble()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
obj = {"valor": n}
def doble(o):
    return o["valor"] * 2
print(f"resultado={doble(obj)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
// Objeto literal con método (modelo de prototipos).
const obj = {
  valor: n,
  doble() {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const obj = {
  valor: n,
  doble(): number {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Obj {
        int valor;
        Obj(int v) { valor = v; }
        int doble() { return valor * 2; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + new Obj(n).doble());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var obj = new Obj(n);
Console.WriteLine($"resultado={obj.Doble()}");

class Obj {
    int valor;
    public Obj(int v) { valor = v; }
    public int Doble() => valor * 2;
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

type Obj struct{ valor int }

func (o Obj) doble() int { return o.valor * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	o := Obj{valor: n}
	fmt.Printf("resultado=%d\n", o.doble())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Obj {
    valor: i64,
}

impl Obj {
    fn doble(&self) -> i64 {
        self.valor * 2
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let o = Obj { valor: n };
    println!("resultado={}", o.doble());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Obj {
    long valor;
};

long doble(struct Obj *o) {
    return o->valor * 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Obj o = {n};
    printf("resultado=%ld\n", doble(&o));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene objetos; el cálculo va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$obj = new class($n) {
    public function __construct(public int $valor) {}
    public function doble(): int { return $this->valor * 2; }
};
echo "resultado=" . $obj->doble() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Objeto literal con método (JS) vs. clase (otros). |
| Semántica | JS hereda por prototipos; los demás por clases. |
| Paradigmática | SQL no tiene objetos. |

## 🧬 El concepto en la familia

Self y Lua también usan prototipos. En los demás lenguajes del núcleo se modela con una clase o struct.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 113
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder el `this` en JS** → causa: el método pierde su contexto → solución: cuidar cómo se invoca el método
- **Creer que JS no es OO** → causa: lo es, por prototipos → solución: entender el modelo de prototipos

## ❓ Preguntas frecuentes

- **¿Prototipos o clases en JS?** Las clases de JS son azúcar sobre prototipos; por debajo es lo mismo.
- **¿Qué lenguajes usan prototipos?** JavaScript, Self, Lua; la mayoría usa clases.

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

> [⏮️ Clase 112](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 114 ⏭️](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md)
