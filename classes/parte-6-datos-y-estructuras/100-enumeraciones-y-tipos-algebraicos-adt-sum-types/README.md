# Clase 100 — Enumeraciones y tipos algebraicos (ADT / sum types)

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **tipos algebraicos (suma)**: un valor que es una de varias alternativas, cada una con sus datos. `Forma = Cuadrado | Rectangulo`. El `match` decide y calcula según la variante.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Modelar alternativas con un tipo suma.
2. Decidir por variante con match/switch.
3. Reconocer la exhaustividad del tipo algebraico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipo suma (ADT) | Una de varias alternativas |
| 2 | Variante | Cada caso con sus datos |
| 3 | Match por variante | Decidir según la forma |

## 📖 Definiciones y características

- **Tipo algebraico (suma)** — valor que es una de varias alternativas (Cuadrado o Rectangulo). Clave: modela 'o esto o lo otro'.
- **Variante** — cada alternativa del tipo suma, con sus propios datos. Clave: `Cuadrado(lado)`.
- **Exhaustividad** — cubrir todas las variantes. Clave: Rust lo exige al compilar.

## 🧩 Situación

Un pago es efectivo, tarjeta o transferencia; una figura es círculo, cuadrado o rectángulo. Los tipos suma modelan estas alternativas con seguridad, y el match obliga a considerarlas todas.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área calculada>`
- **Regla:** cuadrado→lado²; rectangulo→ancho·alto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 7` | `area=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo y datos ; COINCIDIR tipo: cuadrado->l*l ; rectangulo->a*b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

t = sys.stdin.readline().split()
if t[0] == "cuadrado":
    area = int(t[1]) ** 2
else:  # rectangulo
    area = int(t[1]) * int(t[2])
print(f"area={area}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
let area;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let area: number;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
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
        long area;
        if (t[0].equals("cuadrado")) {
            long l = Long.parseLong(t[1]);
            area = l * l;
        } else {
            area = Long.parseLong(t[1]) * Long.parseLong(t[2]);
        }
        System.out.println("area=" + area);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long area = t[0] switch {
    "cuadrado" => long.Parse(t[1]) * long.Parse(t[1]),
    _ => long.Parse(t[1]) * long.Parse(t[2]),
};
Console.WriteLine($"area={area}");
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
	var area int64
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		area = l * l
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		area = a * b
	}
	fmt.Printf("area=%d\n", area)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

enum Forma {
    Cuadrado(i64),
    Rectangulo(i64, i64),
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let forma = if t[0] == "cuadrado" {
        Forma::Cuadrado(t[1].parse().unwrap())
    } else {
        Forma::Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap())
    };
    let area = match forma {
        Forma::Cuadrado(l) => l * l,
        Forma::Rectangulo(a, b) => a * b,
    };
    println!("area={area}");
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
        long l;
        if (scanf("%ld", &l) != 1) return 1;
        area = l * l;
    } else {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una columna 'tipo' + CASE modela las variantes.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado
FROM formas;
```

### PHP · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
if ($t[0] === "cuadrado") {
    $area = (int) $t[1] * (int) $t[1];
} else {
    $area = (int) $t[1] * (int) $t[2];
}
echo "area=$area\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `enum` con datos (Rust), sealed/record (Java/C#), etiqueta + campos (Go/C). |
| Semántica | Rust/Haskell garantizan exhaustividad; C usa una etiqueta manual. |
| Paradigmática | SQL usa una columna 'tipo' + CASE. |

## 🧬 El concepto en la familia

En Haskell `data Forma = Cuadrado Int | Rectangulo Int Int`. En Kotlin, una `sealed class`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 100
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar una variante** → causa: caso sin manejar → solución: en Rust el compilador avisa; en otros, incluir el default
- **Leer los datos de la variante equivocada** → causa: usar campos que no existen → solución: extraer solo los datos de la variante correcta

## ❓ Preguntas frecuentes

- **¿Tipo suma o herencia?** El tipo suma es cerrado y exhaustivo; la herencia es abierta. Distintas garantías.
- **¿Por qué 'algebraico'?** Combina 'sumas' (alternativas) y 'productos' (campos) de tipos.

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

> [⏮️ Clase 099](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 101 ⏭️](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md)
