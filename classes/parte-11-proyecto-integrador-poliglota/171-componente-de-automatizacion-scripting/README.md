# Clase 171 — Componente de automatización/scripting

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construimos el **componente de automatización**: los scripts que ejecutan tareas repetitivas sin que nadie
las mire —limpiar temporales, respaldar, desplegar, mandar informes—. Es el pegamento del sistema, el que
hace que las piezas trabajen juntas de noche y en fin de semana. Hoy modelamos su forma esencial: procesar
un **lote** de `n` tareas y **confirmar** su finalización.

La automatización es uno de los pilares de *The Pragmatic Programmer*, donde Hunt y Thomas dedican un
capítulo entero a "la ubicuidad de la automatización" con una tesis contundente: **todo lo que haces a mano
más de una vez es un candidato a script**, porque las manos se cansan, se distraen y se equivocan, mientras
un script hace lo mismo la vez mil que la primera. Esa fiabilidad no es solo comodidad: es la base de la
reproducibilidad. Un despliegue automatizado se puede auditar, versionar y repetir idéntico; un despliegue
manual es una anécdota irrepetible. Por eso este componente, aunque humilde, sostiene la salud del sistema
entero.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Procesar un lote de tareas y confirmar su finalización.
2. Explicar por qué automatizar da fiabilidad y reproducibilidad, no solo ahorro de tiempo.
3. Reconocer el papel del scripting como pegamento entre componentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Automatización | Tareas repetitivas sin intervención humana |
| 2 | Scripting | El pegamento que compone los componentes |
| 3 | Lote de tareas | Procesar en serie y confirmar |

## 📖 Definiciones y características

La **automatización** es ejecutar tareas repetitivas sin intervención humana; su valor es la fiabilidad y
la reproducibilidad, no solo el tiempo ahorrado. Un **script** es un programa que orquesta o automatiza
pasos —el pegamento que une componentes que no fueron diseñados para hablarse directamente—. Un **lote** es
un conjunto de tareas procesadas juntas, la unidad típica de un trabajo nocturno.

Hay una propiedad silenciosa pero crucial en este mundo: la **idempotencia**. Un buen script de
automatización se puede volver a lanzar tras un fallo sin causar estragos —respaldar dos veces no rompe
nada, pero cobrar dos veces sí—. Nygard, en *Release It!*, advierte que los trabajos automáticos son
justamente donde los fallos se acumulan en silencio: si nadie mira y nadie registra, un lote roto puede
llevar semanas pasando desapercibido. De ahí que confirmar la finalización —el `estado=completado` de esta
clase— no sea decorativo: es la señal que un sistema de monitoreo necesita para saber que la noche fue bien.

## 🧩 Situación

Un script nocturno procesa las tareas pendientes: limpia archivos temporales, respalda la base de datos,
notifica por correo, y al terminar confirma. Si una de esas tareas falla y el script se detiene sin avisar,
el respaldo no se hizo y nadie se entera hasta que hace falta restaurarlo —el peor momento posible—. Por eso
la automatización real se apoya en tres cosas que este ejercicio mínimo prefigura: procesar el lote,
**registrar** el resultado y **confirmar** el desenlace. Python y Bash dominan aquí por su rapidez de
escritura y su ubicuidad: están en todas partes y expresan "haz esto, luego esto" con un mínimo de
ceremonia.

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
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"tareas={n} estado=completado")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`tareas=${n} estado=completado`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`tareas=${n} estado=completado`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

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

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"tareas={n} estado=completado");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

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

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("tareas={n} estado=completado");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("tareas=%ld estado=completado\n", n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL automatiza con procedimientos/trabajos; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('tareas=%d estado=completado', n) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

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
