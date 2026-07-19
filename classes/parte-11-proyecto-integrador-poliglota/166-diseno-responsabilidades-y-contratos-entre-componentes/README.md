# Clase 166 — Diseño: responsabilidades y contratos entre componentes

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Diseñar el sistema definiendo **responsabilidades y contratos entre componentes**. Dos componentes encajan si respetan el mismo contrato en su frontera; aquí se comprueba comparando sus valores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comprobar la compatibilidad de un contrato.
2. Explicar el papel de los contratos.
3. Reconocer fronteras entre componentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato | El acuerdo en la frontera |
| 2 | Compatibilidad | Ambos lados coinciden |
| 3 | Responsabilidad | Qué hace cada componente |

## 📖 Definiciones y características

- **Contrato de frontera** — acuerdo de datos y formato entre dos componentes. Clave: permite evolucionar por separado.
- **Compatibilidad** — que emisor y receptor esperan lo mismo. Clave: sin ella, la integración falla.
- **Responsabilidad** — la tarea única de un componente. Clave: define qué expone en el contrato.

## 🧩 Situación

El backend produce un formato que el frontend consume. Si ambos respetan el contrato, encajan; si uno cambia sin avisar, se rompen. Comprobar la compatibilidad evita sorpresas en la integración.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los valores de contrato de cada componente)
- **Salida** (stdout): `contrato=<compatible|incompatible>`
- **Regla:** compatible si a == b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `contrato=compatible` |
| `5 6` | `contrato=incompatible` |
| `0 0` | `contrato=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = sys.stdin.readline().split()
print(f"contrato={'compatible' if a == b else 'incompatible'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${a === b ? "compatible" : "incompatible"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${a === b ? "compatible" : "incompatible"}`);
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
        System.out.println("contrato=" + (p[0].equals(p[1]) ? "compatible" : "incompatible"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"contrato={(p[0] == p[1] ? "compatible" : "incompatible")}");
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
	f := strings.Fields(line)
	res := "incompatible"
	if f[0] == f[1] {
		res = "compatible"
	}
	fmt.Printf("contrato=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let res = if v[0] == v[1] { "compatible" } else { "incompatible" };
    println!("contrato={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[64], b[64];
    if (scanf("%63s %63s", a, b) != 2) return 1;
    printf("contrato=%s\n", strcmp(a, b) == 0 ? "compatible" : "incompatible");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL compara los valores de contrato.
WITH t(a, b) AS (VALUES (5, 5))
SELECT printf('contrato=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=" . ($a === $b ? "compatible" : "incompatible") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Comparación en cada lenguaje. |
| Semántica | El contrato desacopla los componentes. |
| Paradigmática | SQL compara valores. |

## 🧬 El concepto en la familia

Los tests de contrato (Pact) verifican que servicios independientes respetan su frontera.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 166
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: romper al otro lado → solución: versionar y evolucionar con compatibilidad
- **Fronteras implícitas** → causa: malentendidos → solución: documentar el contrato explícitamente

## ❓ Preguntas frecuentes

- **¿Cómo verificar contratos?** Con tests de contrato entre el consumidor y el proveedor.
- **¿Contrato o integración total?** El contrato permite probar cada lado por separado, más barato.

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

> [⏮️ Clase 165](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 167 ⏭️](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md)
