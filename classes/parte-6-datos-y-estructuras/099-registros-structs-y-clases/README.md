# Clase 099 — Registros, structs y clases

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Agrupar datos relacionados en un **registro/struct/clase** con campos nombrados. En vez de variables sueltas, un tipo compuesto con significado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un tipo con campos nombrados.
2. Crear una instancia y acceder a sus campos.
3. Distinguir struct de clase donde aplique.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Registro/struct | Campos nombrados juntos |
| 2 | Instancia | Un valor del tipo |
| 3 | Acceso a campos | `.nombre`, `.edad` |

## 📖 Definiciones y características

- **Registro/struct** — tipo con campos nombrados. Clave: agrupa datos relacionados.
- **Campo** — cada dato con nombre dentro del registro. Clave: `persona.edad`.
- **Instancia** — un valor concreto del tipo. Clave: `Persona("Ada", 36)`.

## 🧩 Situación

En vez de pasar `nombre` y `edad` sueltos por todas partes, un `Persona` los agrupa con significado y viaja como una sola cosa.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `Persona(nombre=<nombre>, edad=<edad>)`
- **Regla:** registro con campos nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `Persona(nombre=Ada, edad=36)` |
| `Bo 5` | `Persona(nombre=Bo, edad=5)` |
| `Cy 99` | `Persona(nombre=Cy, edad=99)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; crear Persona ; ESCRIBIR formateado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys
from dataclasses import dataclass


@dataclass
class Persona:
    nombre: str
    edad: int


t = sys.stdin.readline().split()
p = Persona(t[0], int(t[1]))
print(f"Persona(nombre={p.nombre}, edad={p.edad})")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${persona.nombre}, edad=${persona.edad})`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

interface Persona {
  nombre: string;
  edad: number;
}

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const p: Persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${p.nombre}, edad=${p.edad})`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Persona(String nombre, int edad) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Persona p = new Persona(t[0], Integer.parseInt(t[1]));
        System.out.println("Persona(nombre=" + p.nombre() + ", edad=" + p.edad() + ")");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var p = new Persona(t[0], int.Parse(t[1]));
Console.WriteLine($"Persona(nombre={p.Nombre}, edad={p.Edad})");

record Persona(string Nombre, int Edad);
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

type Persona struct {
	Nombre string
	Edad   int
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	edad, _ := strconv.Atoi(t[1])
	p := Persona{Nombre: t[0], Edad: edad}
	fmt.Printf("Persona(nombre=%s, edad=%d)\n", p.Nombre, p.Edad)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Persona {
    nombre: String,
    edad: i64,
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let p = Persona {
        nombre: t[0].to_string(),
        edad: t[1].parse().unwrap(),
    };
    println!("Persona(nombre={}, edad={})", p.nombre, p.edad);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Persona {
    char nombre[64];
    long edad;
};

int main(void) {
    struct Persona p;
    if (scanf("%63s %ld", p.nombre, &p.edad) != 2) return 1;
    printf("Persona(nombre=%s, edad=%ld)\n", p.nombre, p.edad);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una fila de una tabla es un registro.
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('Persona(nombre=%s, edad=%d)', nombre, edad) AS resultado FROM personas;
```

### PHP · `php main.php`

```php
<?php
class Persona {
    public function __construct(public string $nombre, public int $edad) {}
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$p = new Persona($t[0], (int) $t[1]);
echo "Persona(nombre={$p->nombre}, edad={$p->edad})\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `class`/`@dataclass` (Python), `record` (Java), `struct` (Go/Rust/C), objeto (JS). |
| Semántica | Struct suele ser por valor; clase por referencia (Java/C#). |
| Paradigmática | SQL: una fila de una tabla es un registro. |

## 🧬 El concepto en la familia

En Kotlin `data class Persona(val nombre: String, val edad: Int)`. En C++ `struct Persona`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 099
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar variables sueltas en vez de agrupar** → causa: datos que se desincronizan → solución: agruparlos en un registro con significado
- **Confundir struct (valor) con clase (referencia)** → causa: copias inesperadas → solución: conocer la semántica del lenguaje

## ❓ Preguntas frecuentes

- **¿Struct o clase?** Struct para datos por valor; clase para identidad y comportamiento (según el lenguaje).
- **¿Registro inmutable?** A menudo conviene: un record de Java o una data class con val.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 098](../../parte-6-datos-y-estructuras/098-grafos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 100 ⏭️](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md)
