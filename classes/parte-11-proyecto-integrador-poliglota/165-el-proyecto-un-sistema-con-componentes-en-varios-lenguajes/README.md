# Clase 165 — El proyecto: un sistema con componentes en varios lenguajes

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Arrancar el **proyecto integrador**: un sistema real hecho de componentes en varios lenguajes. El primer paso es inventariar los componentes que lo forman.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Inventariar los componentes de un sistema.
2. Nombrar cada pieza.
3. Entender el proyecto como suma de componentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema | El todo integrado |
| 2 | Componente | Cada pieza con su lenguaje |
| 3 | Inventario | Qué partes lo forman |

## 📖 Definiciones y características

- **Sistema integrador** — producto compuesto por varios componentes que colaboran. Clave: cada uno en su lenguaje idóneo.
- **Componente** — pieza con una responsabilidad. Clave: se integra con las demás.
- **Inventario** — lista de las partes del sistema. Clave: primer paso del diseño.

## 🧩 Situación

Antes de construir, se enumeran los componentes: CLI, API, web, datos. Ese inventario define el alcance del proyecto integrador y qué lenguaje usará cada pieza.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<N> nombres=<unidos por ->`
- **Regla:** contar y listar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3 nombres=cli-api-web` |
| `app` | `componentes=1 nombres=app` |
| `web api datos cache` | `componentes=4 nombres=web-api-datos-cache` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR conteo y nombres unidos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

c = sys.stdin.read().split()
print(f"componentes={len(c)} nombres={'-'.join(c)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const c = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const c: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] c = br.readLine().trim().split("\\s+");
        System.out.println("componentes=" + c.length + " nombres=" + String.join("-", c));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"componentes={c.Length} nombres={string.Join("-", c)}");
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
	c := strings.Fields(line)
	fmt.Printf("componentes=%d nombres=%s\n", len(c), strings.Join(c, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: Vec<&str> = s.split_whitespace().collect();
    println!("componentes={} nombres={}", c.len(), c.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char t[64];
    char buf[4096];
    buf[0] = '\0';
    int n = 0;
    while (scanf("%63s", t) == 1) {
        if (n > 0) strcat(buf, "-");
        strcat(buf, t);
        n++;
    }
    printf("componentes=%d nombres=%s\n", n, buf);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL cuenta y une los componentes.
WITH c(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d nombres=%s', count(*), group_concat(nombre, '-')) AS resultado FROM c;
```

### PHP · `php main.php`

```php
<?php
$c = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($c) . " nombres=" . implode("-", $c) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contar y unir en cada lenguaje. |
| Semántica | Cada componente puede estar en otro lenguaje. |
| Paradigmática | SQL agrega con group_concat. |

## 🧬 El concepto en la familia

Todo sistema real es un inventario de componentes con responsabilidades y lenguajes propios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 165
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Componentes sin responsabilidad clara** → causa: solapamientos → solución: una responsabilidad por componente
- **Olvidar un componente** → causa: integración incompleta → solución: inventariar todas las piezas

## ❓ Preguntas frecuentes

- **¿Cuántos componentes?** Los que el problema justifique; ni de más ni de menos.
- **¿Por dónde empezar?** Por el inventario y los contratos entre componentes.

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

> [⏮️ Clase 164](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 166 ⏭️](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md)
