# Clase 161 — Procesos y comunicación: stdin/stdout, sockets, colas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **comunicación entre procesos**: procesos separados intercambian datos por tuberías (stdin/stdout), sockets o colas. Una cola FIFO entrega los datos en orden a un consumidor que los suma.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recibir datos por una cola.
2. Explicar los mecanismos de comunicación entre procesos.
3. Reconocer stdin/stdout como tubería.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tubería (pipe) | stdout de uno a stdin de otro |
| 2 | Cola/socket | Comunicación asíncrona o en red |
| 3 | Productor/consumidor | Uno envía, otro recibe |

## 📖 Definiciones y características

- **Comunicación entre procesos (IPC)** — mecanismos para que procesos separados intercambien datos. Clave: tuberías, sockets, colas.
- **Tubería** — conecta la salida de un proceso con la entrada de otro. Clave: base de los comandos Unix encadenados.
- **Cola** — buffer FIFO que desacopla productor y consumidor. Clave: comunicación asíncrona.

## 🧩 Situación

En Unix, `productor | consumidor` conecta procesos por una tubería. Este curso usa justo eso: stdin/stdout como frontera común entre implementaciones. Aquí una cola entrega los números y se suman.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (mensajes en la cola)
- **Salida** (stdout): `recibido=<suma de los mensajes>`
- **Regla:** sumar los mensajes recibidos en orden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `recibido=6` |
| `5` | `recibido=5` |
| `10 20 30 40` | `recibido=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA CADA mensaje de la cola: acumular ; ESCRIBIR suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
recibido = 0
for m in nums:  # consumidor de la cola
    recibido += m
print(f"recibido={recibido}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let recibido = 0;
for (const m of nums) recibido += m;
console.log(`recibido=${recibido}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let recibido = 0;
for (const m of nums) recibido += m;
console.log(`recibido=${recibido}`);
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
        long recibido = 0;
        for (String s : p) recibido += Integer.parseInt(s);
        System.out.println("recibido=" + recibido);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

long recibido = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"recibido={recibido}");
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
	recibido := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		recibido += n
	}
	fmt.Printf("recibido=%d\n", recibido)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let recibido: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("recibido={recibido}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long recibido = 0, m;
    while (scanf("%ld", &m) == 1) recibido += m;
    printf("recibido=%ld\n", recibido);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL agrega los mensajes con SUM.
WITH cola(x) AS (VALUES (1), (2), (3))
SELECT printf('recibido=%d', sum(x)) AS resultado FROM cola;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "recibido=" . array_sum($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Recorrer la entrada (cola) en cada lenguaje. |
| Semántica | La cola desacopla al productor del consumidor. |
| Paradigmática | SQL no maneja procesos; agrega datos. |

## 🧬 El concepto en la familia

Tuberías Unix, sockets, y colas (RabbitMQ, Kafka) conectan procesos y servicios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 161
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden con múltiples productores** → causa: mensajes entremezclados → solución: una cola por flujo o marcar el orden
- **No cerrar la tubería** → causa: el consumidor espera para siempre → solución: cerrar/EOF al terminar de enviar

## ❓ Preguntas frecuentes

- **¿Tubería o socket?** Tubería para procesos en la misma máquina; socket para red.
- **¿Por qué stdin/stdout?** Es la tubería universal; por eso el curso verifica con ella.

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

> [⏮️ Clase 160](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 162 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md)
