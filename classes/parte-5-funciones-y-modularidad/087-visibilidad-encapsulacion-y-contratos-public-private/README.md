# Clase 087 — Visibilidad, encapsulación y contratos (public/private)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aplicar **encapsulación**: ocultar el estado interno (el saldo) y exponer solo operaciones controladas (depositar, consultar). El contrato público protege los datos de modificaciones inválidas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ocultar un campo con visibilidad privada.
2. Exponer métodos públicos como contrato.
3. Explicar por qué la encapsulación protege los datos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Encapsulación | Ocultar el estado interno |
| 2 | Visibilidad | public vs. private |
| 3 | Contrato público | Lo que se puede usar |
| 4 | Invariantes | Reglas que el objeto mantiene |

## 📖 Definiciones y características

- **Encapsulación** — agrupar datos y operaciones ocultando el estado interno. Clave: se accede solo por métodos.
- **Privado** — accesible solo desde dentro del tipo. Clave: protege el estado.
- **Público** — parte visible desde fuera (el contrato). Clave: lo que otros usan.
- **Invariante** — regla que el objeto siempre cumple (saldo >= 0). Clave: la encapsulación la protege.

## 🧩 Situación

Si el saldo fuera público, cualquiera podría ponerlo en negativo saltándose las reglas. Encapsulado, solo `depositar`/`retirar` lo tocan, garantizando que siempre sea válido.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (monto de cada depósito)
- **Salida** (stdout): `saldo=<2n>` (tras depositar n dos veces)
- **Regla:** cuenta.depositar(n) dos veces; saldo = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `50` | `saldo=100` |
| `0` | `saldo=0` |
| `30` | `saldo=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
cuenta <- nueva Cuenta()
cuenta.depositar(n) ; cuenta.depositar(n)
ESCRIBIR "saldo=" cuenta.saldo()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Cuenta:
    def __init__(self):
        self._saldo = 0  # privado por convención

    def depositar(self, monto):
        self._saldo += monto

    def saldo(self):
        return self._saldo


n = int(sys.stdin.readline())
c = Cuenta()
c.depositar(n)
c.depositar(n)
print(f"saldo={c.saldo()}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Cuenta {
  #saldo = 0; // campo privado real
  depositar(monto) {
    this.#saldo += monto;
  }
  saldo() {
    return this.#saldo;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

class Cuenta {
  private saldoInterno = 0;
  depositar(monto: number): void {
    this.saldoInterno += monto;
  }
  saldo(): number {
    return this.saldoInterno;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Cuenta {
        private long saldo = 0;

        void depositar(long monto) {
            saldo += monto;
        }

        long saldo() {
            return saldo;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        Cuenta c = new Cuenta();
        c.depositar(n);
        c.depositar(n);
        System.out.println("saldo=" + c.saldo());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

// Las sentencias top-level van antes de la declaración del tipo.
long n = long.Parse(Console.In.ReadToEnd().Trim());
var c = new Cuenta();
c.Depositar(n);
c.Depositar(n);
Console.WriteLine($"saldo={c.Saldo()}");

class Cuenta {
    private long saldo = 0;
    public void Depositar(long monto) => saldo += monto;
    public long Saldo() => saldo;
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

// saldo en minúscula: privado del paquete.
type cuenta struct {
	saldo int64
}

func (c *cuenta) depositar(monto int64) {
	c.saldo += monto
}

func (c *cuenta) obtenerSaldo() int64 {
	return c.saldo
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	c := &cuenta{}
	c.depositar(n)
	c.depositar(n)
	fmt.Printf("saldo=%d\n", c.obtenerSaldo())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Cuenta {
    saldo: i64, // privado fuera del módulo
}

impl Cuenta {
    fn nueva() -> Self {
        Cuenta { saldo: 0 }
    }
    fn depositar(&mut self, monto: i64) {
        self.saldo += monto;
    }
    fn saldo(&self) -> i64 {
        self.saldo
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Cuenta::nueva();
    c.depositar(n);
    c.depositar(n);
    println!("saldo={}", c.saldo());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene 'private'; se usa una struct y funciones por convención. */
struct Cuenta {
    long saldo;
};

void depositar(struct Cuenta *c, long monto) {
    c->saldo += monto;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Cuenta c = {0};
    depositar(&c, n);
    depositar(&c, n);
    printf("saldo=%ld\n", c.saldo);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL encapsula con vistas/permisos; aquí el cálculo va en la consulta.
WITH montos(n) AS (VALUES (50), (0), (30))
SELECT printf('saldo=%d', n * 2) AS resultado FROM montos;
```

### PHP · `php main.php`

```php
<?php
class Cuenta {
    private $saldo = 0;

    public function depositar($monto) {
        $this->saldo += $monto;
    }

    public function saldo() {
        return $this->saldo;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Cuenta();
$c->depositar($n);
$c->depositar($n);
echo "saldo=" . $c->saldo() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `private`/`public` (Java/C#), `_` por convención (Python), campos en minúscula (Go = privado del paquete). |
| Semántica | Java/C#/Rust hacen cumplir la privacidad; Python confía en la convención. |
| Paradigmática | SQL encapsula con vistas y permisos. |

## 🧬 El concepto en la familia

En Ruby los atributos son privados y se exponen con `attr_reader`/métodos. En Go, la mayúscula/minúscula del nombre define la visibilidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 087
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer el estado directamente** → causa: cualquiera lo corrompe → solución: hacerlo privado y ofrecer métodos
- **Getters/setters para todo sin criterio** → causa: encapsulación de fachada → solución: exponer operaciones con significado, no acceso crudo

## ❓ Preguntas frecuentes

- **¿Python encapsula de verdad?** Por convención (`_priv`); no lo impide, pero la comunidad lo respeta.
- **¿Encapsular es solo getters/setters?** No: es exponer operaciones con significado que mantienen los invariantes.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 086](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 088 ⏭️](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md)
