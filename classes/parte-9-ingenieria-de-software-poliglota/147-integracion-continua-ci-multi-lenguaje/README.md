# Clase 147 — Integración continua (CI) multi-lenguaje

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **integración continua (CI)**: cada cambio dispara un pipeline de pasos (compilar, probar, lint); si todos pasan, el resultado es 'verde'. Si uno falla, es 'rojo' y el cambio se bloquea.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Combinar el resultado de varios pasos.
2. Explicar el pipeline de CI.
3. Reconocer el valor de bloquear en rojo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CI | Verificar cada cambio |
| 2 | Pipeline | Pasos encadenados |
| 3 | Verde/rojo | Todo pasa o algo falla |

## 📖 Definiciones y características

- **Integración continua** — ejecutar automáticamente pruebas y checks en cada cambio. Clave: detecta errores pronto.
- **Pipeline** — secuencia de pasos (build, test, lint). Clave: todos deben pasar.
- **Verde/rojo** — estado del pipeline: todo pasa (verde) o algo falla (rojo). Clave: bloquea lo roto.

## 🧩 Situación

Al subir un cambio, el CI compila, prueba y revisa el estilo. Si algún paso falla, el pipeline se pone rojo y el cambio no se integra. Es lo que mantiene verde este repositorio.

## 🧮 Modelo

- **Entrada** (stdin): una línea con 0 y 1 (resultado de cada paso; 1 = pasó)
- **Salida** (stdout): `ci=<verde|rojo>`
- **Regla:** verde si todos los pasos son 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 1 1` | `ci=verde` |
| `1 0 1` | `ci=rojo` |
| `1 1` | `ci=verde` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER pasos ; verde <- todos == 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

pasos = [int(x) for x in sys.stdin.read().split()]
print(f"ci={'verde' if all(p == 1 for p in pasos) else 'rojo'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const pasos = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const pasos: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean verde = true;
        for (String s : p) if (Integer.parseInt(s) != 1) verde = false;
        System.out.println("ci=" + (verde ? "verde" : "rojo"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

bool verde = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .All(x => int.Parse(x) == 1);
Console.WriteLine($"ci={(verde ? "verde" : "rojo")}");
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
	verde := true
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n != 1 {
			verde = false
		}
	}
	res := "rojo"
	if verde {
		res = "verde"
	}
	fmt.Printf("ci=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let verde = s.split_whitespace().all(|x| x.parse::<i64>().unwrap() == 1);
    println!("ci={}", if verde { "verde" } else { "rojo" });
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int verde = 1;
    while (scanf("%ld", &x) == 1) {
        if (x != 1) verde = 0;
    }
    printf("ci=%s\n", verde ? "verde" : "rojo");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: verde si el mínimo de los pasos es 1.
WITH pasos(x) AS (VALUES (1), (1), (1))
SELECT printf('ci=%s', CASE WHEN min(x) = 1 THEN 'verde' ELSE 'rojo' END) AS resultado FROM pasos;
```

### PHP · `php main.php`

```php
<?php
$pasos = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$verde = !in_array(0, $pasos, true);
echo "ci=" . ($verde ? "verde" : "rojo") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | all/every/reduce en cada lenguaje. |
| Semántica | Basta un paso en rojo para que el pipeline falle. |
| Paradigmática | SQL usa MIN sobre los pasos. |

## 🧬 El concepto en la familia

GitHub Actions, GitLab CI, Jenkins ejecutan pipelines que bloquean en rojo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 147
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el rojo del CI** → causa: integrar código roto → solución: no fusionar hasta que esté verde
- **Pipelines lentísimos** → causa: el equipo los evita → solución: optimizar con caché y paralelismo

## ❓ Preguntas frecuentes

- **¿Qué pasos debe tener?** Al menos compilar, probar y lint; según el proyecto, más.
- **¿CI y CD?** CI verifica; CD (entrega/despliegue continuos) automatiza la publicación.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 146](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 148 ⏭️](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md)
