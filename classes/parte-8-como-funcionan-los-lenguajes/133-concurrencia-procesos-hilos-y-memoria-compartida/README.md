# Clase 133 — Concurrencia: procesos, hilos y memoria compartida

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **concurrencia con memoria compartida**: varios hilos acceden a los mismos datos. Contar con un acumulador compartido ilustra el modelo; en concurrencia real, ese acceso debe protegerse.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar con un acumulador compartido.
2. Explicar procesos, hilos y memoria compartida.
3. Reconocer el riesgo de acceso concurrente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Proceso vs. hilo | Aislado vs. comparte memoria |
| 2 | Memoria compartida | Varios hilos, mismos datos |
| 3 | Protección | Evitar el acceso simultáneo inseguro |

## 📖 Definiciones y características

- **Proceso** — programa en ejecución con su propia memoria aislada. Clave: no comparte por defecto.
- **Hilo** — línea de ejecución dentro de un proceso; comparte su memoria. Clave: acceso concurrente a los datos.
- **Memoria compartida** — datos accesibles por varios hilos. Clave: requiere sincronización para ser segura.

## 🧩 Situación

Los hilos de un proceso comparten memoria: es rápido comunicar, pero peligroso si dos escriben a la vez el mismo dato. Contar con un acumulador es el ejemplo de un estado compartido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<número de elementos>`
- **Regla:** acumulador compartido que cuenta los elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `cuenta=3` |
| `5` | `cuenta=1` |
| `10 20 30 40` | `cuenta=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; PARA CADA elemento: cuenta <- cuenta + 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = sys.stdin.read().split()
cuenta = 0
for _ in nums:
    cuenta += 1  # acumulador compartido
print(f"cuenta={cuenta}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        int cuenta = 0;
        for (String s : nums) cuenta += 1;
        System.out.println("cuenta=" + cuenta);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int cuenta = 0;
foreach (var s in nums) cuenta += 1;
Console.WriteLine($"cuenta={cuenta}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	cuenta := 0
	for range strings.Fields(line) {
		cuenta++
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut cuenta = 0;
    for _ in s.split_whitespace() {
        cuenta += 1;
    }
    println!("cuenta={cuenta}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int cuenta = 0;
    while (scanf("%ld", &x) == 1) cuenta++;
    printf("cuenta=%d\n", cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COUNT sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$cuenta = 0;
foreach ($nums as $_) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Un contador compartido en cada lenguaje. |
| Semántica | Con hilos reales haría falta un mutex; aquí es secuencial. |
| Paradigmática | SQL delega el paralelismo al motor. |

## 🧬 El concepto en la familia

Java/C#/C++ comparten memoria entre hilos (con locks); Go y Erlang prefieren comunicar en vez de compartir.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 133
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Compartir sin sincronizar** → causa: condiciones de carrera → solución: proteger el acceso con mutex o preferir mensajes
- **Sobre-sincronizar** → causa: cuellos de botella → solución: minimizar la sección crítica

## ❓ Preguntas frecuentes

- **¿Compartir memoria o comunicar?** 'No comuniques compartiendo memoria; comparte comunicando' (lema de Go).
- **¿Proceso o hilo?** Hilo para compartir datos rápido; proceso para aislar y ser robusto.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 132](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 134 ⏭️](../../parte-8-como-funcionan-los-lenguajes/134-tareas-corrutinas-y-canales/README.md)
