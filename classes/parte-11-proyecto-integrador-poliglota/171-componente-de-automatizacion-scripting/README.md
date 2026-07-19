# Clase 171 — Componente de automatización/scripting

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de automatización/scripting**: tareas repetitivas que se ejecutan sin intervención (limpieza, despliegue, informes). Aquí se procesan n tareas y se confirma su finalización.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Procesar un lote de tareas.
2. Confirmar la finalización.
3. Reconocer el rol de la automatización.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Automatización | Tareas sin intervención |
| 2 | Scripting | Pegamento entre componentes |
| 3 | Lote de tareas | Procesar en serie |

## 📖 Definiciones y características

- **Automatización** — ejecutar tareas repetitivas sin intervención humana. Clave: fiabilidad y ahorro de tiempo.
- **Script** — programa que orquesta o automatiza pasos. Clave: pegamento del sistema.
- **Lote** — conjunto de tareas procesadas juntas. Clave: eficiencia.

## 🧩 Situación

Un script nocturno procesa las tareas pendientes (limpiar, respaldar, notificar) y confirma su finalización. La automatización, a menudo en Python o Bash, mantiene el sistema funcionando solo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de tareas)
- **Salida** (stdout): `tareas=<n> estado=completado`
- **Regla:** procesar n tareas y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `tareas=5 estado=completado` |
| `0` | `tareas=0 estado=completado` |
| `3` | `tareas=3 estado=completado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; procesar n tareas ; ESCRIBIR completado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"tareas={n} estado=completado")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`tareas=${n} estado=completado`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`tareas=${n} estado=completado`);
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
        System.out.println("tareas=" + n + " estado=completado");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"tareas={n} estado=completado");
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
	fmt.Printf("tareas=%d estado=completado\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("tareas={n} estado=completado");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("tareas=%ld estado=completado\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL automatiza con procedimientos/trabajos; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('tareas=%d estado=completado', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "tareas=$n estado=completado\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | La automatización procesa y confirma. |
| Paradigmática | SQL automatiza con procedimientos/trabajos. |

## 🧬 El concepto en la familia

Python y Bash dominan el scripting; herramientas como cron y Airflow orquestan tareas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 171
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Automatizar sin registrar** → causa: no saber si falló → solución: loggear el resultado de cada tarea
- **Sin manejo de errores** → causa: una tarea rota detiene todo → solución: aislar fallos y reintentar

## ❓ Preguntas frecuentes

- **¿Qué lenguaje para automatizar?** Python y Bash por su rapidez de escritura y ubicuidad.
- **¿Automatizar todo?** Lo repetitivo y propenso a error; lo puntual, a mano.

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

> [⏮️ Clase 170](../../parte-11-proyecto-integrador-poliglota/170-componente-de-datos-y-consultas-sql/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 172 ⏭️](../../parte-11-proyecto-integrador-poliglota/172-persistencia-y-almacenamiento/README.md)
