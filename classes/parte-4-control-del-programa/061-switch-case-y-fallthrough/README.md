# Clase 061 — switch, case y fallthrough

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar `switch` / `case` (o su equivalente) para elegir entre valores exactos, con un caso por defecto. Verás el `fallthrough` (caída) de C/Java y cómo otros lenguajes lo evitan.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Seleccionar por valor exacto con switch/case.
2. Usar el caso por defecto.
3. Explicar el fallthrough y cómo lo maneja cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | switch/case | Elegir por valor exacto |
| 2 | default | El caso por defecto |
| 3 | Fallthrough | Caída de un caso al siguiente (C/Java) |
| 4 | Alternativas | match/when sin caída |

## 📖 Definiciones y características

- **switch** — estructura que elige una rama según el valor exacto. Clave: para muchos valores concretos.
- **case** — una de las ramas del switch. Clave: coincide con un valor.
- **fallthrough** — en C/Java, un case sigue al siguiente si falta `break`. Clave: fuente de bugs.
- **default** — rama que se ejecuta si ningún case coincide. Clave: cubre lo inesperado.

## 🧩 Situación

Traducir un código a un nombre (día, mes, estado) es el caso típico de switch. Olvidar un `break` en C/Java hace 'caer' al siguiente case: un error clásico que otros lenguajes evitan por diseño.

## 🧮 Modelo

- **Entrada** (stdin): un entero `d` (día)
- **Salida** (stdout): `dia=<nombre>` o `dia=invalido`
- **Regla:** 1→lunes … 7→domingo; otro→invalido

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `dia=lunes` |
| `6` | `dia=sabado` |
| `8` | `dia=invalido` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER d
SEGUN d: 1..7 -> nombre ; otro -> invalido
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

d = int(sys.stdin.readline())
nombres = {1: "lunes", 2: "martes", 3: "miercoles", 4: "jueves",
           5: "viernes", 6: "sabado", 7: "domingo"}
print(f"dia={nombres.get(d, 'invalido')}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const d = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const d: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia: string;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int d = Integer.parseInt(br.readLine().trim());
        String dia;
        switch (d) {
            case 1: dia = "lunes"; break;
            case 2: dia = "martes"; break;
            case 3: dia = "miercoles"; break;
            case 4: dia = "jueves"; break;
            case 5: dia = "viernes"; break;
            case 6: dia = "sabado"; break;
            case 7: dia = "domingo"; break;
            default: dia = "invalido";
        }
        System.out.println("dia=" + dia);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int d = int.Parse(Console.In.ReadToEnd().Trim());
string dia = d switch {
    1 => "lunes",
    2 => "martes",
    3 => "miercoles",
    4 => "jueves",
    5 => "viernes",
    6 => "sabado",
    7 => "domingo",
    _ => "invalido",
};
Console.WriteLine($"dia={dia}");
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
	d, _ := strconv.Atoi(strings.TrimSpace(line))
	var dia string
	switch d {
	case 1:
		dia = "lunes"
	case 2:
		dia = "martes"
	case 3:
		dia = "miercoles"
	case 4:
		dia = "jueves"
	case 5:
		dia = "viernes"
	case 6:
		dia = "sabado"
	case 7:
		dia = "domingo"
	default:
		dia = "invalido"
	}
	fmt.Printf("dia=%s\n", dia)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let d: i64 = s.trim().parse().unwrap();
    let dia = match d {
        1 => "lunes",
        2 => "martes",
        3 => "miercoles",
        4 => "jueves",
        5 => "viernes",
        6 => "sabado",
        7 => "domingo",
        _ => "invalido",
    };
    println!("dia={dia}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long d;
    if (scanf("%ld", &d) != 1) return 1;
    const char *dia;
    switch (d) {
        case 1: dia = "lunes"; break;
        case 2: dia = "martes"; break;
        case 3: dia = "miercoles"; break;
        case 4: dia = "jueves"; break;
        case 5: dia = "viernes"; break;
        case 6: dia = "sabado"; break;
        case 7: dia = "domingo"; break;
        default: dia = "invalido";
    }
    printf("dia=%s\n", dia);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selección por valor con CASE WHEN.
WITH dias(d) AS (VALUES (1), (6), (8))
SELECT printf('dia=%s',
       CASE d WHEN 1 THEN 'lunes' WHEN 2 THEN 'martes' WHEN 3 THEN 'miercoles'
              WHEN 4 THEN 'jueves' WHEN 5 THEN 'viernes' WHEN 6 THEN 'sabado'
              WHEN 7 THEN 'domingo' ELSE 'invalido' END) AS resultado
FROM dias;
```

### PHP · `php main.php`

```php
<?php
$d = (int) trim(fgets(STDIN));
switch ($d) {
    case 1: $dia = "lunes"; break;
    case 2: $dia = "martes"; break;
    case 3: $dia = "miercoles"; break;
    case 4: $dia = "jueves"; break;
    case 5: $dia = "viernes"; break;
    case 6: $dia = "sabado"; break;
    case 7: $dia = "domingo"; break;
    default: $dia = "invalido";
}
echo "dia=$dia\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `switch` con `break` (C/Java/JS) vs. `match` (Rust) vs. `when` (Kotlin). |
| Semántica | C/Java caen sin `break`; Go, Rust y el switch de Python (match) no caen. |
| Paradigmática | SQL usa CASE WHEN valor. |

## 🧬 El concepto en la familia

En Ruby `case d; when 1 then 'lunes'`. En Kotlin `when (d) { 1 -> ... }`. Ninguno cae como C.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 061
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar `break` en C/Java** → causa: el flujo cae al siguiente case → solución: poner `break` en cada case o usar match/when
- **No manejar valores fuera de rango** → causa: salida vacía o error → solución: incluir siempre el caso por defecto

## ❓ Preguntas frecuentes

- **¿Por qué existe el fallthrough?** Herencia de C; a veces útil, pero suele ser un error olvidar el break.
- **¿Go tiene fallthrough?** No por defecto: hay que pedirlo con la palabra `fallthrough` explícita.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 060](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 062 ⏭️](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md)
