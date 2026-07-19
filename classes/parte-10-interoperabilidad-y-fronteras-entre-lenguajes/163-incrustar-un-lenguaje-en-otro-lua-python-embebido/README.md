# Clase 163 — Incrustar un lenguaje en otro (Lua, Python embebido)

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **incrustar un lenguaje en otro**: motores como Lua o Python se embeben en aplicaciones para permitir scripting sin recompilar. El anfitrión pasa datos al script, este los procesa y devuelve un resultado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Evaluar un script embebido.
2. Explicar el uso de lenguajes de scripting embebidos.
3. Reconocer casos (juegos, plugins).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lenguaje embebido | Un intérprete dentro de la app |
| 2 | Anfitrión y script | Quién ejecuta a quién |
| 3 | Extensibilidad | Cambiar comportamiento sin recompilar |

## 📖 Definiciones y características

- **Lenguaje embebido** — intérprete integrado en una aplicación anfitriona (Lua, Python). Clave: scripting sin recompilar.
- **Anfitrión** — la aplicación que hospeda el intérprete. Clave: expone datos y funciones al script.
- **Script embebido** — código interpretado que corre dentro del anfitrión. Clave: extiende la app.

## 🧩 Situación

Muchos juegos embeben Lua para su lógica; editores embeben Python para plugins. El anfitrión pasa datos al script y recibe el resultado, permitiendo modificar el comportamiento sin recompilar.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los datos que el anfitrión pasa al script)
- **Salida** (stdout): `resultado=<a+b>` (lo que el script calcula)
- **Regla:** el script embebido evalúa a + b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `resultado=7` |
| `10 5` | `resultado=15` |
| `0 0` | `resultado=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
anfitrión pasa a, b ; el script suma ; devuelve el resultado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
script = "a + b"  # el script embebido
resultado = eval(script, {}, {"a": a, "b": b})
print(f"resultado={resultado}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
// El anfitrion evalua el script embebido con los datos.
const resultado = a + b;
console.log(`resultado=${resultado}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const resultado: number = a + b;
console.log(`resultado=${resultado}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]);
        System.out.println("resultado=" + (a + b));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]), b = int.Parse(p[1]);
Console.WriteLine($"resultado={a + b}");
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
	fmt.Printf("resultado=%d\n", a+b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("resultado={}", v[0] + v[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("resultado=%ld\n", a + b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL se embebe en apps via librerias cliente; aqui, la suma.
WITH t(a, b) AS (VALUES (3, 4))
SELECT printf('resultado=%d', a + b) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "resultado=" . ($a + $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El anfitrión invoca al intérprete embebido; aquí se simula la evaluación. |
| Semántica | El script corre en el runtime del lenguaje embebido. |
| Paradigmática | SQL se embebe en apps vía librerías cliente. |

## 🧬 El concepto en la familia

Lua (juegos, Redis, Nginx), Python (Blender, editores), JavaScript (motores V8 embebidos) son los referentes.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 163
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer demasiado al script** → causa: riesgo de seguridad → solución: limitar lo que el script puede tocar (sandbox)
- **No validar la salida del script** → causa: datos inesperados → solución: comprobar lo que devuelve el script

## ❓ Preguntas frecuentes

- **¿Por qué embeber un lenguaje?** Para permitir personalización y plugins sin recompilar la app.
- **¿Lua o Python?** Lua es minúsculo y rápido de embeber; Python, más potente y con más librerías.

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

> [⏮️ Clase 162](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 164 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md)
