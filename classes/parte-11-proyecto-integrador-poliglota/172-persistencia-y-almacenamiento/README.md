# Clase 172 — Persistencia y almacenamiento

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir la **persistencia y el almacenamiento**: guardar datos para recuperarlos después. Aquí se almacena un par clave/valor y se confirma lo guardado, como haría un almacén clave-valor.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Guardar un par clave/valor.
2. Confirmar el almacenamiento.
3. Reconocer tipos de almacenamiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Persistencia | Sobrevivir al reinicio |
| 2 | Clave/valor | Almacén simple |
| 3 | Almacenamiento | Dónde viven los datos |

## 📖 Definiciones y características

- **Persistencia** — guardar datos de forma duradera (disco, base de datos). Clave: sobreviven al reinicio.
- **Almacén clave-valor** — guarda valores indexados por una clave (Redis, mapas persistentes). Clave: acceso rápido por clave.
- **Durabilidad** — garantía de que lo guardado no se pierde. Clave: propiedad clave del almacenamiento.

## 🧩 Situación

El sistema guarda la configuración y el estado: un almacén clave-valor mapea `usuario → sesión`. Persistir bien es lo que permite apagar y volver a encender sin perder datos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `guardado=<clave>=<valor>`
- **Regla:** almacenar el par y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `guardado=x=5` |
| `nombre ada` | `guardado=nombre=ada` |
| `n 100` | `guardado=n=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; guardar ; confirmar clave=valor
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

clave, valor = sys.stdin.readline().split()
almacen = {}
almacen[clave] = valor
print(f"guardado={clave}={almacen[clave]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
const almacen = new Map();
almacen.set(clave, valor);
console.log(`guardado=${clave}=${almacen.get(clave)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
const almacen = new Map<string, string>();
almacen.set(clave, valor);
console.log(`guardado=${clave}=${almacen.get(clave)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<String, String> almacen = new HashMap<>();
        almacen.put(p[0], p[1]);
        System.out.println("guardado=" + p[0] + "=" + almacen.get(p[0]));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var almacen = new Dictionary<string, string>();
almacen[p[0]] = p[1];
Console.WriteLine($"guardado={p[0]}={almacen[p[0]]}");
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
	p := strings.Fields(line)
	almacen := map[string]string{}
	almacen[p[0]] = p[1]
	fmt.Printf("guardado=%s=%s\n", p[0], almacen[p[0]])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    let mut almacen: HashMap<&str, &str> = HashMap::new();
    almacen.insert(p[0], p[1]);
    println!("guardado={}={}", p[0], almacen[p[0]]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char clave[64], valor[64];
    if (scanf("%63s %63s", clave, valor) != 2) return 1;
    printf("guardado=%s=%s\n", clave, valor);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL persiste en tablas; aqui, el par guardado.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'guardado=' || clave || '=' || valor AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
$almacen = [];
$almacen[$clave] = $valor;
echo "guardado=$clave={$almacen[$clave]}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Un mapa/diccionario en cada lenguaje; una tabla en SQL. |
| Semántica | La persistencia hace duraderos los datos. |
| Paradigmática | SQL persiste en tablas con INSERT. |

## 🧬 El concepto en la familia

Redis (clave-valor), PostgreSQL (relacional), sistemas de archivos: opciones de persistencia según el caso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 172
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Guardar sin durabilidad garantizada** → causa: pérdida ante caídas → solución: usar almacenamiento que confirme la escritura
- **Claves sin convención** → causa: colisiones y confusión → solución: definir un esquema de claves claro

## ❓ Preguntas frecuentes

- **¿Clave-valor o relacional?** Clave-valor para acceso simple y rápido; relacional para datos estructurados y consultas.
- **¿Persistir en disco o memoria?** Memoria para caché rápida; disco para durabilidad.

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

> [⏮️ Clase 171](../../parte-11-proyecto-integrador-poliglota/171-componente-de-automatizacion-scripting/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 173 ⏭️](../../parte-11-proyecto-integrador-poliglota/173-pruebas-end-to-end-del-sistema-completo/README.md)
