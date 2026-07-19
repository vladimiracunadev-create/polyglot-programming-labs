# Clase 119 — Orientado a eventos y callbacks

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **orientado a eventos y callbacks**: en vez de un flujo lineal, se registran manejadores que reaccionan cuando ocurre un evento. Aquí un callback recolecta cada evento emitido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Registrar un callback.
2. Emitir eventos que lo invocan.
3. Reconocer la inversión de control.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Evento | Algo que ocurre |
| 2 | Callback/manejador | Función que reacciona |
| 3 | Inversión de control | El sistema llama a tu código |

## 📖 Definiciones y características

- **Evento** — suceso al que el programa reacciona (clic, mensaje, dato). Clave: dispara callbacks.
- **Callback** — función registrada para ejecutarse cuando ocurre el evento. Clave: no la llamas tú.
- **Inversión de control** — el sistema invoca tu código, no al revés. Clave: base de la GUI y del servidor.

## 🧩 Situación

Interfaces, servidores, sensores: no siguen un guion lineal, reaccionan a eventos. Registras un callback ('cuando llegue X, haz Y') y el sistema lo invoca.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de eventos, n >= 1)
- **Salida** (stdout): `eventos=<1-2-...-n>` (orden en que llegaron)
- **Regla:** por cada i en 1..n, emitir evento i; el callback lo recolecta

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `eventos=1-2-3` |
| `1` | `eventos=1` |
| `4` | `eventos=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
registrar callback ; PARA i de 1 a n: emitir(i) ; ESCRIBIR recolectados
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

recolectados = []


def al_evento(i):
    recolectados.append(i)


n = int(sys.stdin.readline())
for i in range(1, n + 1):
    al_evento(i)
print("eventos=" + "-".join(str(x) for x in recolectados))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const recolectados = [];
const alEvento = (i) => recolectados.push(i);

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const recolectados: number[] = [];
const alEvento = (i: number): void => {
  recolectados.push(i);
};

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.function.IntConsumer;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> recolectados = new ArrayList<>();
        IntConsumer alEvento = recolectados::add;
        for (int i = 1; i <= n; i++) alEvento.accept(i);
        System.out.println("eventos=" + recolectados.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var recolectados = new List<int>();
Action<int> alEvento = i => recolectados.Add(i);
for (int i = 1; i <= n; i++) alEvento(i);
Console.WriteLine($"eventos={string.Join("-", recolectados)}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var recolectados []string
	alEvento := func(i int) {
		recolectados = append(recolectados, strconv.Itoa(i))
	}
	for i := 1; i <= n; i++ {
		alEvento(i)
	}
	fmt.Printf("eventos=%s\n", strings.Join(recolectados, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn al_evento(recolectados: &mut Vec<String>, i: i64) {
    recolectados.push(i.to_string());
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut recolectados: Vec<String> = Vec::new();
    for i in 1..=n {
        al_evento(&mut recolectados, i);
    }
    println!("eventos={}", recolectados.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("eventos=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", i);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene eventos; se genera la secuencia con un CTE (ilustrativo, n=3).
WITH RECURSIVE e(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM e WHERE i < 3)
SELECT 'eventos=' || group_concat(i, '-') AS resultado FROM e;
```

### PHP · `php main.php`

```php
<?php
$recolectados = [];
$alEvento = function ($i) use (&$recolectados) {
    $recolectados[] = $i;
};

$n = (int) trim(fgets(STDIN));
for ($i = 1; $i <= $n; $i++) {
    $alEvento($i);
}
echo "eventos=" . implode("-", $recolectados) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Callback como función pasada (Python/JS/Go), delegate (C#), interfaz (Java). |
| Semántica | El emisor invoca el callback; el flujo no es lineal. |
| Paradigmática | SQL no tiene eventos; procesa datos. |

## 🧬 El concepto en la familia

En JS los EventEmitter y los `addEventListener` del navegador son puro estilo de eventos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 119
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Callback con efectos secundarios ocultos** → causa: estado difícil de seguir → solución: mantener el callback claro y enfocado
- **Olvidar registrar el manejador** → causa: el evento no hace nada → solución: registrar antes de emitir

## ❓ Preguntas frecuentes

- **¿Callback o async/await?** async/await suele leer mejor; ambos manejan lo asíncrono/eventos.
- **¿Qué es inversión de control?** Que el framework/sistema llame a tu código cuando toca, no tú a él.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 118](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 120 ⏭️](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md)
