# Clase 169 — Componente web/frontend (JS/TS)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente web/frontend** (JS/TS): la interfaz que el usuario ve. Aquí se simula el renderizado de una lista de n elementos, confirmando que el render fue correcto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular el renderizado de una vista.
2. Explicar el rol del frontend.
3. Reconocer JS/TS como su lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Frontend | La interfaz de usuario |
| 2 | Renderizar | Mostrar datos como UI |
| 3 | Componentes de UI | Piezas visuales |

## 📖 Definiciones y características

- **Componente web** — la interfaz que interactúa con el usuario. Clave: consume la API y muestra datos.
- **Renderizar** — convertir datos en elementos visuales. Clave: lo que el usuario ve.
- **Estado de la UI** — los datos que la interfaz muestra en un momento. Clave: cambia con la interacción.

## 🧩 Situación

El frontend recibe n elementos de la API y los renderiza como una lista. Confirmar que el render fue correcto cierra el flujo. Este componente vive en el navegador, en JavaScript o TypeScript.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de elementos a renderizar)
- **Salida** (stdout): `items=<n> render=ok`
- **Regla:** renderizar n elementos y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `items=3 render=ok` |
| `0` | `items=0 render=ok` |
| `10` | `items=10 render=ok` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; renderizar n items ; confirmar render
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"items={n} render=ok")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`items=${n} render=ok`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`items=${n} render=ok`);
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
        System.out.println("items=" + n + " render=ok");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"items={n} render=ok");
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
	fmt.Printf("items=%d render=ok\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("items={n} render=ok");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("items=%ld render=ok\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL provee datos; aqui, el render simulado.
WITH t(n) AS (VALUES (3))
SELECT printf('items=%d render=ok', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "items=$n render=ok\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | El frontend transforma datos en UI. |
| Paradigmática | SQL no renderiza; provee datos. |

## 🧬 El concepto en la familia

React, Vue, Svelte (JS/TS) y Flutter (Dart) construyen interfaces; el frontend es su terreno.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 169
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquear la UI con cálculo pesado** → causa: interfaz congelada → solución: mover el cómputo a un worker o al backend
- **Renderizar sin manejar el estado vacío** → causa: vista rota con 0 elementos → solución: considerar el caso de lista vacía

## ❓ Preguntas frecuentes

- **¿Frontend en qué lenguaje?** JavaScript/TypeScript en el navegador; Dart con Flutter para móvil.
- **¿Lógica en el frontend o backend?** La presentación en el frontend; la de negocio, en el backend.

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

> [⏮️ Clase 168](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 170 ⏭️](../../parte-11-proyecto-integrador-poliglota/170-componente-de-datos-y-consultas-sql/README.md)
