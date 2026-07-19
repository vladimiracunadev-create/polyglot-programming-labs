# Clase 173 — Pruebas end-to-end del sistema completo

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Realizar una **prueba end-to-end (e2e)**: ejercitar el sistema completo, de la entrada a la salida, como lo haría un usuario real. Aquí se comprueba que, dadas dos entradas, el sistema devuelve el total esperado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ejecutar una prueba end-to-end.
2. Distinguir e2e de unitaria e integración.
3. Reconocer su valor y su coste.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | End-to-end | El sistema completo |
| 2 | Flujo de usuario | De la entrada a la salida |
| 3 | Pirámide de pruebas | Muchas unitarias, pocas e2e |

## 📖 Definiciones y características

- **Prueba end-to-end** — verifica el sistema completo desde la perspectiva del usuario. Clave: cubre todos los componentes juntos.
- **Flujo** — el recorrido de una acción a través del sistema. Clave: lo que se ejercita en e2e.
- **Pirámide de pruebas** — muchas unitarias, algunas de integración, pocas e2e. Clave: equilibrio coste/valor.

## 🧩 Situación

Tras construir todos los componentes, una prueba e2e comprueba el flujo completo: el usuario introduce datos y obtiene el resultado correcto. Son valiosas pero costosas: se usan con moderación.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `e2e=<pasa|falla>`
- **Regla:** pasa si el sistema (a + b) da el esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `e2e=pasa` |
| `2 2 5` | `e2e=falla` |
| `10 5 15` | `e2e=pasa` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"e2e={'pasa' if a + b == esperado else 'falla'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`e2e=${a + b === esperado ? "pasa" : "falla"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`e2e=${a + b === esperado ? "pasa" : "falla"}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), e = Integer.parseInt(p[2]);
        System.out.println("e2e=" + (a + b == e ? "pasa" : "falla"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"e2e={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	e, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == e {
		res = "pasa"
	}
	fmt.Printf("e2e=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] + v[1] == v[2] { "pasa" } else { "falla" };
    println!("e2e={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b, e;
    if (scanf("%ld %ld %ld", &a, &b, &e) != 3) return 1;
    printf("e2e=%s\n", a + b == e ? "pasa" : "falla");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL prueba con una consulta de comprobacion.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('e2e=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$a, $b, $e] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "e2e=" . ($a + $b === $e ? "pasa" : "falla") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Comparación tras ejecutar el flujo. |
| Semántica | Se prueba el sistema completo, no una unidad. |
| Paradigmática | SQL prueba con consultas sobre datos de prueba. |

## 🧬 El concepto en la familia

Cypress, Playwright, Selenium ejecutan pruebas e2e sobre la aplicación real.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 173
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Solo pruebas e2e** → causa: lentas y frágiles → solución: seguir la pirámide: base de unitarias
- **e2e sin datos controlados** → causa: resultados no reproducibles → solución: usar datos de prueba fijos

## ❓ Preguntas frecuentes

- **¿e2e o unitaria?** Unitarias para la base rápida; e2e para verificar el flujo completo, con moderación.
- **¿Por qué son costosas?** Ejercitan todo el sistema: lentas y más frágiles ante cambios.

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

> [⏮️ Clase 172](../../parte-11-proyecto-integrador-poliglota/172-persistencia-y-almacenamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 174 ⏭️](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md)
