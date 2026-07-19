# Clase 168 — Componente de API/servicio (backend)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de API/servicio** (backend): recibe una petición y devuelve una respuesta con un código de estado y datos. Aquí responde 200 (OK) con el dato recibido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir una respuesta de API con estado.
2. Explicar el rol del backend.
3. Reconocer los códigos de estado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Servicio/API | Responde peticiones |
| 2 | Código de estado | 200 OK, 404, 500 |
| 3 | Respuesta | Estado + datos |

## 📖 Definiciones y características

- **Componente de API** — servicio que atiende peticiones y devuelve respuestas. Clave: la lógica del sistema.
- **Código de estado** — número que indica el resultado (200 OK, 404 no encontrado). Clave: comunica el desenlace.
- **Respuesta** — estado más datos que el servicio devuelve. Clave: lo que consume el cliente.

## 🧩 Situación

El frontend pide un dato; el backend responde `200` con el dato o un error. El componente de API es el cerebro del sistema, a menudo en Go, Java o C# por su rendimiento y ecosistema.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (el dato solicitado)
- **Salida** (stdout): `respuesta=200 datos=<n>`
- **Regla:** responder 200 con el dato

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `respuesta=200 datos=5` |
| `0` | `respuesta=200 datos=0` |
| `42` | `respuesta=200 datos=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR estado 200 y datos=n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"respuesta=200 datos={n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`respuesta=200 datos=${n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`respuesta=200 datos=${n}`);
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
        System.out.println("respuesta=200 datos=" + n);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"respuesta=200 datos={n}");
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
	fmt.Printf("respuesta=200 datos=%d\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("respuesta=200 datos={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("respuesta=200 datos=%ld\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL devuelve filas; aqui, la respuesta simulada.
WITH t(n) AS (VALUES (5))
SELECT printf('respuesta=200 datos=%d', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "respuesta=200 datos=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Formatear la respuesta en cada lenguaje. |
| Semántica | El código de estado comunica el resultado. |
| Paradigmática | SQL devuelve filas, no códigos HTTP. |

## 🧬 El concepto en la familia

Express (JS), Spring (Java), ASP.NET (C#), Gin (Go), FastAPI (Python) construyen APIs.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 168
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Devolver 200 en un error** → causa: el cliente no detecta el fallo → solución: usar el código correcto (4xx/5xx)
- **Respuestas sin formato acordado** → causa: el cliente no las interpreta → solución: seguir el contrato de la API

## ❓ Preguntas frecuentes

- **¿Qué código para 'no encontrado'?** 404; 200 es OK, 500 es error del servidor.
- **¿Qué lenguaje para el backend?** Depende: Go/Java/C# por rendimiento; Python por rapidez de desarrollo.

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

> [⏮️ Clase 167](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 169 ⏭️](../../parte-11-proyecto-integrador-poliglota/169-componente-web-frontend-js-ts/README.md)
