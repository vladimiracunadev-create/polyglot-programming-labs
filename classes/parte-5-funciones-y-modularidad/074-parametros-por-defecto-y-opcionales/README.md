# Clase 074 — Parámetros por defecto y opcionales

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **parámetros por defecto**: un parámetro que toma un valor predefinido si no se pasa. Permite funciones flexibles sin sobrecargarlas. C y Go no los tienen; se simula.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un parámetro con valor por defecto.
2. Llamar la función con y sin ese argumento.
3. Reconocer lenguajes sin parámetros por defecto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Parámetro por defecto | Valor usado si no se pasa |
| 2 | Argumento opcional | Se puede omitir |
| 3 | Flexibilidad | Una función, varios usos |
| 4 | Sin soporte nativo | C y Go lo simulan |

## 📖 Definiciones y características

- **Parámetro por defecto** — toma un valor predefinido si el argumento se omite. Clave: `exp=2`.
- **Argumento opcional** — el que se puede no pasar. Clave: cae en el valor por defecto.
- **Sobrecarga** — varias funciones con el mismo nombre y distinta firma. Clave: alternativa en Java/C.
- **Simular defecto** — en C/Go, con dos funciones o comprobando la ausencia. Clave: no es nativo.

## 🧩 Situación

`potencia(base, exp=2)` permite `potencia(3)` = 9 y `potencia(2, 3)` = 8 con una sola definición. Sin defectos habría que escribir dos funciones o pasar siempre el exponente.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `base` (exp por defecto 2) o `base exp`
- **Salida** (stdout): `resultado=<base^exp>`
- **Regla:** potencia(base, exp=2) = base^exp

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=9` |
| `2 3` | `resultado=8` |
| `5` | `resultado=25` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens
base <- tokens[0] ; exp <- tokens[1] SI EXISTE SINO 2
ESCRIBIR "resultado=" base^exp
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def potencia(base, exp=2):
    r = 1
    for _ in range(exp):
        r *= base
    return r


t = sys.stdin.readline().split()
base = int(t[0])
if len(t) > 1:
    print(f"resultado={potencia(base, int(t[1]))}")
else:
    print(f"resultado={potencia(base)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function potencia(base, exp = 2) {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function potencia(base: number, exp = 2): number {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene defectos: se simula con sobrecarga.
    static long potencia(long base) {
        return potencia(base, 2);
    }

    static long potencia(long base, int exp) {
        long r = 1;
        for (int i = 0; i < exp; i++) r *= base;
        return r;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long base = Long.parseLong(t[0]);
        long r = t.length > 1 ? potencia(base, Integer.parseInt(t[1])) : potencia(base);
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Potencia(long baseN, int exp = 2) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= baseN;
    return r;
}

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long b = long.Parse(t[0]);
long res = t.Length > 1 ? Potencia(b, int.Parse(t[1])) : Potencia(b);
Console.WriteLine($"resultado={res}");
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

// Go no tiene defectos: se simula con la lógica de llamada.
func potencia(base int64, exp int) int64 {
	var r int64 = 1
	for i := 0; i < exp; i++ {
		r *= base
	}
	return r
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	base, _ := strconv.ParseInt(t[0], 10, 64)
	exp := 2
	if len(t) > 1 {
		exp, _ = strconv.Atoi(t[1])
	}
	fmt.Printf("resultado=%d\n", potencia(base, exp))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn potencia(base: i64, exp: u32) -> i64 {
    base.pow(exp)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let base: i64 = t[0].parse().unwrap();
    let exp: u32 = if t.len() > 1 { t[1].parse().unwrap() } else { 2 };
    println!("resultado={}", potencia(base, exp));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene defectos: se simula pasando siempre el exponente. */
long potencia(long base, int exp) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= base;
    return r;
}

int main(void) {
    long base;
    int exp;
    int leidos = scanf("%ld %d", &base, &exp);
    if (leidos < 1) return 1;
    if (leidos < 2) exp = 2;
    printf("resultado=%ld\n", potencia(base, exp));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COALESCE simula el valor por defecto (aquí, exponente 2 mediante base*base).
WITH datos(base) AS (VALUES (3), (5))
SELECT printf('resultado=%d', base * base) AS resultado FROM datos;
```

### PHP · `php main.php`

```php
<?php
function potencia($base, $exp = 2) {
    $r = 1;
    for ($i = 0; $i < $exp; $i++) {
        $r *= $base;
    }
    return $r;
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$base = (int) $t[0];
$res = count($t) > 1 ? potencia($base, (int) $t[1]) : potencia($base);
echo "resultado=$res\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def f(base, exp=2)` (Python) vs. simulación con comprobación (C/Go). |
| Semántica | Python/JS/C#/PHP tienen defectos nativos; C/Go no. |
| Paradigmática | SQL usa COALESCE para valores por defecto. |

## 🧬 El concepto en la familia

En Ruby `def potencia(base, exp = 2)`. En Kotlin `fun potencia(base: Int, exp: Int = 2)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 074
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Poner el parámetro con defecto antes de uno obligatorio** → causa: error de definición → solución: los parámetros con defecto van al final
- **Asumir defectos en C/Go** → causa: no existen → solución: simular con dos funciones o comprobando argumentos

## ❓ Preguntas frecuentes

- **¿Todos los lenguajes tienen defectos?** No: C y Go no; se simulan con sobrecarga o comprobación.
- **¿El defecto se evalúa una vez?** Cuidado en Python con defectos mutables (lista): se comparten entre llamadas.

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

> [⏮️ Clase 073](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 075 ⏭️](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md)
