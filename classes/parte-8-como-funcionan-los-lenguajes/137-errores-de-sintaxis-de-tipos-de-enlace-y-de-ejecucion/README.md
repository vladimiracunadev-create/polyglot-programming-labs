# Clase 137 — Errores: de sintaxis, de tipos, de enlace y de ejecución

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Clasificar los **tipos de error** por el momento en que aparecen: de sintaxis (al parsear), de tipos (al comprobar tipos), de enlace (al unir con librerías) y de ejecución (al correr). Saber cuándo ocurre cada uno acelera el diagnóstico.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Nombrar las cuatro clases de error.
2. Asociar cada error a su fase.
3. Diagnosticar según cuándo aparece.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Error de sintaxis | El código no se puede parsear |
| 2 | Error de tipos | Operación inválida para los tipos |
| 3 | Error de enlace y de ejecución | Al unir librerías o al correr |

## 📖 Definiciones y características

- **Error de sintaxis** — el código viola las reglas gramaticales. Clave: se detecta al parsear.
- **Error de tipos** — operación no válida para los tipos implicados. Clave: en compilación (estáticos) o ejecución (dinámicos).
- **Error de enlace** — no se encuentra una función/símbolo al unir con librerías. Clave: entre compilar y ejecutar.
- **Error de ejecución** — ocurre al correr (división por cero, índice fuera de rango). Clave: en tiempo de ejecución.

## 🧩 Situación

Un `;` olvidado es de sintaxis; sumar texto y número, de tipos; una librería ausente, de enlace; dividir por cero, de ejecución. Saber la fase reduce el tiempo de búsqueda del fallo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `codigo` (1 a 4)
- **Salida** (stdout): `error=<sintaxis|tipos|enlace|ejecucion>`
- **Regla:** 1→sintaxis, 2→tipos, 3→enlace, 4→ejecucion

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `error=sintaxis` |
| `3` | `error=enlace` |
| `4` | `error=ejecucion` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER codigo ; SEGUN codigo: 1..4 -> nombre del error
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

codigo = int(sys.stdin.readline())
nombres = {1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion"}
print(f"error={nombres.get(codigo, 'desconocido')}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const codigo = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const codigo: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres: Record<number, string> = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int codigo = Integer.parseInt(br.readLine().trim());
        String e;
        switch (codigo) {
            case 1: e = "sintaxis"; break;
            case 2: e = "tipos"; break;
            case 3: e = "enlace"; break;
            case 4: e = "ejecucion"; break;
            default: e = "desconocido";
        }
        System.out.println("error=" + e);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int codigo = int.Parse(Console.In.ReadToEnd().Trim());
string e = codigo switch {
    1 => "sintaxis",
    2 => "tipos",
    3 => "enlace",
    4 => "ejecucion",
    _ => "desconocido",
};
Console.WriteLine($"error={e}");
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
	codigo, _ := strconv.Atoi(strings.TrimSpace(line))
	var e string
	switch codigo {
	case 1:
		e = "sintaxis"
	case 2:
		e = "tipos"
	case 3:
		e = "enlace"
	case 4:
		e = "ejecucion"
	default:
		e = "desconocido"
	}
	fmt.Printf("error=%s\n", e)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let codigo: i64 = s.trim().parse().unwrap();
    let e = match codigo {
        1 => "sintaxis",
        2 => "tipos",
        3 => "enlace",
        4 => "ejecucion",
        _ => "desconocido",
    };
    println!("error={e}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    int codigo;
    if (scanf("%d", &codigo) != 1) return 1;
    const char *e;
    switch (codigo) {
        case 1: e = "sintaxis"; break;
        case 2: e = "tipos"; break;
        case 3: e = "enlace"; break;
        case 4: e = "ejecucion"; break;
        default: e = "desconocido";
    }
    printf("error=%s\n", e);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selección por código con CASE.
WITH c(codigo) AS (VALUES (1))
SELECT printf('error=%s', CASE codigo WHEN 1 THEN 'sintaxis' WHEN 2 THEN 'tipos' WHEN 3 THEN 'enlace' WHEN 4 THEN 'ejecucion' ELSE 'desconocido' END) AS resultado
FROM c;
```

### PHP · `php main.php`

```php
<?php
$codigo = (int) trim(fgets(STDIN));
$nombres = [1 => "sintaxis", 2 => "tipos", 3 => "enlace", 4 => "ejecucion"];
echo "error=" . ($nombres[$codigo] ?? "desconocido") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | switch/match sobre el código en cada lenguaje. |
| Semántica | En estáticos, los de tipos salen al compilar; en dinámicos, al ejecutar. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

Los compilados detectan sintaxis, tipos y enlace antes de ejecutar; los interpretados, muchos al correr.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 137
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir error de tipos con de ejecución** → causa: buscar en la fase equivocada → solución: recordar cuándo comprueba tipos tu lenguaje
- **Ignorar el error de enlace** → causa: 'símbolo no encontrado' → solución: verificar librerías y su enlazado

## ❓ Preguntas frecuentes

- **¿Cuándo salen los errores de tipos?** En compilación (estáticos) o en ejecución (dinámicos).
- **¿Qué es un error de enlace?** Cuando el enlazador no encuentra una función/símbolo referenciado.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 136](../../parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 138 ⏭️](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md)
