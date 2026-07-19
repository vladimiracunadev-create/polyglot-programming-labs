# Clase 176 — Cierre: retrospectiva y transferencia a nuevos lenguajes

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar el programa con una **retrospectiva y la transferencia a nuevos lenguajes**. Tras 176 clases, la lección central es que el conocimiento de la programación es transferible: lo aprendido se aplica a cualquier lenguaje, incluso a los que aún no conoces.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Cerrar el proyecto con una retrospectiva.
2. Afirmar la transferibilidad del conocimiento.
3. Mirar hacia el siguiente lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Retrospectiva | Qué aprendimos |
| 2 | Transferencia | Aplicar a lo nuevo |
| 3 | Siguiente lenguaje | Aprender por familia |

## 📖 Definiciones y características

- **Retrospectiva** — reflexión sobre lo hecho para mejorar. Clave: cierra el ciclo de aprendizaje.
- **Transferencia** — aplicar lo aprendido a un contexto nuevo. Clave: la tesis del programa.
- **Aprendizaje por familia** — usar el Atlas para leer un lenguaje nuevo por su parentesco. Clave: amplía sin empezar de cero.

## 🧩 Situación

Has recorrido pensamiento computacional, el Atlas de familias, toolchains, valores, control, funciones, datos, paradigmas, runtime, ingeniería, interoperabilidad y un proyecto integrador. La lección final: el próximo lenguaje ya no te asusta, porque reconoces sus conceptos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de lecciones que te llevas)
- **Salida** (stdout): `lecciones=<n> transferible=si`
- **Regla:** informar las lecciones y confirmar la transferibilidad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `lecciones=5 transferible=si` |
| `12` | `lecciones=12 transferible=si` |
| `1` | `lecciones=1 transferible=si` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR lecciones=n transferible=si
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"lecciones={n} transferible=si")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`lecciones=${n} transferible=si`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`lecciones=${n} transferible=si`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("lecciones=" + n + " transferible=si");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"lecciones={n} transferible=si");
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
	fmt.Printf("lecciones=%d transferible=si\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("lecciones={n} transferible=si");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("lecciones=%ld transferible=si\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL, la ultima vez: la misma idea, otra forma.
WITH t(n) AS (VALUES (5))
SELECT printf('lecciones=%d transferible=si', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "lecciones=$n transferible=si\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Una última vez, la misma idea en diez formas. |
| Semántica | El concepto permanece; la forma cambia. |
| Paradigmática | Del imperativo al declarativo, todo cabe en la misma tesis. |

## 🧬 El concepto en la familia

Con el Atlas y estas 176 clases, cualquier lenguaje nuevo se aprende reconociendo su familia y sus deltas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 176
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que hay que empezar de cero con cada lenguaje** → causa: desaprovechar lo transferible → solución: reconocer los conceptos y aprender solo las diferencias
- **Detener el aprendizaje aquí** → causa: el campo evoluciona → solución: seguir aplicando el método a lenguajes nuevos

## ❓ Preguntas frecuentes

- **¿Y ahora qué?** Elige un lenguaje del Atlas que no conozcas y léelo por su familia: comprobarás la transferencia.
- **¿Se acabó el aprendizaje?** Nunca: el método políglota es una forma de seguir aprendiendo cualquier lenguaje.

## 🔗 Referencias

**Libros de la parte:**

- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

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

> [⏮️ Clase 175](../../parte-11-proyecto-integrador-poliglota/175-documentacion-y-defensa-de-las-decisiones-de-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md)
