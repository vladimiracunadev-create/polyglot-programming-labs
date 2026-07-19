# Clase 162 — WebAssembly como objetivo común

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **WebAssembly (Wasm)** como objetivo común: un formato binario portable al que compilan muchos lenguajes (Rust, C, Go) y que corre en el navegador o en runtimes. Es un 'punto de encuentro' entre lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es WebAssembly.
2. Reconocer qué lenguajes compilan a Wasm.
3. Ver Wasm como objetivo común.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | WebAssembly | Binario portable y rápido |
| 2 | Objetivo de compilación | Muchos lenguajes compilan a Wasm |
| 3 | Runtime | Navegador o fuera de él (WASI) |

## 📖 Definiciones y características

- **WebAssembly** — formato binario portable y eficiente, objetivo de compilación de varios lenguajes. Clave: corre en el navegador y en runtimes.
- **Objetivo (target)** — el formato al que compila un lenguaje. Clave: Rust, C, Go pueden apuntar a Wasm.
- **WASI** — interfaz de sistema para Wasm fuera del navegador. Clave: Wasm del lado servidor.

## 🧩 Situación

Un módulo de cálculo escrito en Rust se compila a Wasm y corre en el navegador junto a JavaScript, o en un runtime del servidor. Wasm es el objetivo común que deja a varios lenguajes convivir.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<n²>`
- **Regla:** calcular n al cuadrado (como en un módulo Wasm)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=25` |
| `0` | `resultado=0` |
| `7` | `resultado=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n*n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"resultado={n * n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${n * n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${n * n}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + (n * n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={n * n}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", n*n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", n * n);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", n * n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL calcula el cuadrado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "resultado=" . ($n * $n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El cálculo es idéntico; lo distinto es el objetivo de compilación. |
| Semántica | Wasm ejecuta el mismo cálculo de forma portable y rápida. |
| Paradigmática | SQL corre en su propio motor, no en Wasm. |

## 🧬 El concepto en la familia

Rust, C/C++, Go, C# (Blazor) compilan a WebAssembly; runtimes como Wasmtime lo ejecutan.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 162
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar acceso directo al sistema en Wasm del navegador** → causa: el sandbox lo limita → solución: usar las APIs disponibles (o WASI en servidor)
- **Módulos Wasm enormes** → causa: carga lenta → solución: optimizar el tamaño del binario

## ❓ Preguntas frecuentes

- **¿Wasm reemplaza a JavaScript?** No: lo complementa para cargas de cómputo intensivo.
- **¿Wasm solo en el navegador?** No: con WASI también en el servidor y en la nube.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

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

> [⏮️ Clase 161](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 163 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)
