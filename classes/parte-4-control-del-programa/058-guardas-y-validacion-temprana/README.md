# Clase 058 — Guardas y validación temprana

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aplicar **guardas** (validación temprana): comprobar primero los casos inválidos o especiales y salir cuanto antes, dejando el camino principal limpio. Reduce el anidamiento y hace el código más legible.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir guardas que validan y salen temprano.
2. Evitar el anidamiento profundo de if.
3. Ordenar las comprobaciones de más restrictiva a menos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación temprana | Comprobar lo inválido primero |
| 2 | Guarda | Un if que corta el flujo pronto |
| 3 | Retorno temprano | Salir en cuanto se decide |
| 4 | Legibilidad | Menos anidamiento, más claridad |

## 📖 Definiciones y características

- **Guarda** — condición al inicio que corta el flujo si no se cumple. Clave: evita anidar.
- **Validación temprana** — rechazar entradas inválidas antes del cálculo. Clave: el camino feliz queda limpio.
- **Retorno temprano** — salir de la función en cuanto hay respuesta. Clave: menos ramas abiertas.
- **Camino feliz** — el flujo principal sin errores. Clave: se lee de corrido tras las guardas.

## 🧩 Situación

Con guardas, `if edad < 0: return invalido` al principio evita envolver todo el resto en un `else`. El código baja en escalera en vez de anidarse hacia la derecha.

## 🧮 Modelo

- **Entrada** (stdin): un entero `edad`
- **Salida** (stdout): `invalido` si edad<0, `menor` si edad<18, `adulto` en otro caso
- **Regla:** guardas: edad<0 → invalido; edad<18 → menor; si no → adulto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `invalido` |
| `10` | `menor` |
| `20` | `adulto` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER edad
SI edad < 0: ESCRIBIR "invalido" ; FIN
SI edad < 18: ESCRIBIR "menor" ; FIN
ESCRIBIR "adulto"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

edad = int(sys.stdin.readline())
if edad < 0:
    print("invalido")
elif edad < 18:
    print("menor")
else:
    print("adulto")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const edad = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const edad: number = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int edad = Integer.parseInt(br.readLine().trim());
        if (edad < 0) {
            System.out.println("invalido");
        } else if (edad < 18) {
            System.out.println("menor");
        } else {
            System.out.println("adulto");
        }
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int edad = int.Parse(Console.In.ReadToEnd().Trim());
if (edad < 0)
    Console.WriteLine("invalido");
else if (edad < 18)
    Console.WriteLine("menor");
else
    Console.WriteLine("adulto");
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
	edad, _ := strconv.Atoi(strings.TrimSpace(line))
	if edad < 0 {
		fmt.Println("invalido")
		return
	}
	if edad < 18 {
		fmt.Println("menor")
		return
	}
	fmt.Println("adulto")
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let edad: i64 = s.trim().parse().unwrap();
    if edad < 0 {
        println!("invalido");
    } else if edad < 18 {
        println!("menor");
    } else {
        println!("adulto");
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long edad;
    if (scanf("%ld", &edad) != 1) return 1;
    if (edad < 0) {
        printf("invalido\n");
    } else if (edad < 18) {
        printf("menor\n");
    } else {
        printf("adulto\n");
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: clasificación con CASE WHEN en orden.
WITH edades(edad) AS (VALUES (-5), (10), (20))
SELECT CASE WHEN edad < 0 THEN 'invalido'
            WHEN edad < 18 THEN 'menor'
            ELSE 'adulto' END AS resultado
FROM edades;
```

### PHP · `php main.php`

```php
<?php
$edad = (int) trim(fgets(STDIN));
if ($edad < 0) {
    echo "invalido\n";
} elseif ($edad < 18) {
    echo "menor\n";
} else {
    echo "adulto\n";
}
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `if ...: return` (Python) vs. `if (...) { return; }` (C/Java). |
| Semántica | El orden de las guardas define la clasificación; cambiarlo cambia el resultado. |
| Paradigmática | SQL encadena condiciones con CASE WHEN en orden. |

## 🧬 El concepto en la familia

En Ruby `return 'invalido' if edad < 0`. En Go es común la guarda con `if ...{ return }` al inicio de la función.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 058
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar en vez de usar guardas** → causa: escalera de if/else hacia la derecha → solución: sacar los casos especiales como guardas al inicio
- **Ordenar mal las guardas** → causa: clasificar mal por comprobar tarde → solución: ir de la condición más restrictiva a la más general

## ❓ Preguntas frecuentes

- **¿Guarda o if/else anidado?** La guarda suele ser más legible: aplana el código y deja claro el camino feliz.
- **¿Varios return son mala práctica?** No con guardas: hacen el flujo más claro, no más confuso.

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

> [⏮️ Clase 057](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 059 ⏭️](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md)
