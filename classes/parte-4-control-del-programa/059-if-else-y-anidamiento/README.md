# Clase 059 — if / else y anidamiento

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar `if` / `else if` encadenados para clasificar en varios rangos. Es la estructura de decisión más común y la base de toda ramificación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar if/else para varios rangos.
2. Ordenar los umbrales correctamente.
3. Cubrir el caso por defecto (else).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | if / else if / else | Elegir entre varias ramas |
| 2 | Rangos ordenados | De mayor a menor umbral |
| 3 | Caso por defecto | El else que recoge lo demás |
| 4 | Exclusividad | Solo una rama se ejecuta |

## 📖 Definiciones y características

- **if** — ejecuta un bloque si la condición es verdadera. Clave: la decisión básica.
- **else if** — condición alternativa si la anterior falló. Clave: encadena rangos.
- **else** — rama por defecto si ninguna condición se cumple. Clave: cubre el resto.
- **Umbral** — valor límite que separa dos categorías. Clave: su orden importa.

## 🧩 Situación

Asignar una nota por tramos aparece en todas partes: descuentos por volumen, niveles de riesgo, categorías. Si los umbrales se comprueban en mal orden, la clasificación falla.

## 🧮 Modelo

- **Entrada** (stdin): un entero `score` (0-100)
- **Salida** (stdout): `nota=<A|B|C|F>`
- **Regla:** score>=90→A; >=80→B; >=70→C; si no→F

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `95` | `nota=A` |
| `72` | `nota=C` |
| `40` | `nota=F` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER score
SI score>=90: A
SINO SI score>=80: B
SINO SI score>=70: C
SINO: F
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

score = int(sys.stdin.readline())
if score >= 90:
    nota = "A"
elif score >= 80:
    nota = "B"
elif score >= 70:
    nota = "C"
else:
    nota = "F"
print(f"nota={nota}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const score = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const score: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota: string;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int score = Integer.parseInt(br.readLine().trim());
        String nota;
        if (score >= 90) nota = "A";
        else if (score >= 80) nota = "B";
        else if (score >= 70) nota = "C";
        else nota = "F";
        System.out.println("nota=" + nota);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int score = int.Parse(Console.In.ReadToEnd().Trim());
string nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
Console.WriteLine($"nota={nota}");
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
	score, _ := strconv.Atoi(strings.TrimSpace(line))
	var nota string
	if score >= 90 {
		nota = "A"
	} else if score >= 80 {
		nota = "B"
	} else if score >= 70 {
		nota = "C"
	} else {
		nota = "F"
	}
	fmt.Printf("nota=%s\n", nota)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let score: i64 = s.trim().parse().unwrap();
    let nota = if score >= 90 {
        "A"
    } else if score >= 80 {
        "B"
    } else if score >= 70 {
        "C"
    } else {
        "F"
    };
    println!("nota={nota}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long score;
    if (scanf("%ld", &score) != 1) return 1;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    printf("nota=%c\n", nota);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: rangos con CASE WHEN en orden descendente.
WITH scores(score) AS (VALUES (95), (72), (40))
SELECT printf('nota=%s',
       CASE WHEN score >= 90 THEN 'A'
            WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C'
            ELSE 'F' END) AS resultado
FROM scores;
```

### PHP · `php main.php`

```php
<?php
$score = (int) trim(fgets(STDIN));
if ($score >= 90) {
    $nota = "A";
} elseif ($score >= 80) {
    $nota = "B";
} elseif ($score >= 70) {
    $nota = "C";
} else {
    $nota = "F";
}
echo "nota=$nota\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `elif` (Python) vs. `else if` (C/Java/JS) vs. `else if` con llaves. |
| Semántica | Solo se ejecuta la primera rama verdadera; el orden descendente es clave. |
| Paradigmática | SQL usa CASE WHEN con los umbrales en orden. |

## 🧬 El concepto en la familia

En Ruby se usa `if/elsif/else` o un `case` con rangos (`when 90..100`). En Kotlin, `when` con rangos es idiomático.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 059
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comprobar los umbrales de menor a mayor** → causa: todo cae en la primera rama → solución: ordenar de mayor a menor umbral
- **Olvidar el else** → causa: no clasificar algunos valores → solución: incluir siempre un caso por defecto

## ❓ Preguntas frecuentes

- **¿Puedo usar switch aquí?** Para rangos, if/else o `when`/`match` con rangos; el switch clásico es para valores exactos.
- **¿Importa el orden?** Mucho: la primera condición verdadera gana, así que van de más a menos exigente.

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

> [⏮️ Clase 058](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 060 ⏭️](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md)
