# Clase 159 — Serialización entre lenguajes: JSON, Protobuf, MessagePack

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **serialización entre lenguajes** (JSON, Protobuf, MessagePack): convertir datos a un formato común para que un componente en un lenguaje los envíe y otro en otro lenguaje los reciba. Aquí se serializa un par a texto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar un dato a un formato de intercambio.
2. Explicar por qué se necesita un formato común.
3. Reconocer JSON/Protobuf/MessagePack.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Serialización | De datos a formato de intercambio |
| 2 | Formato común | Entendido por todos |
| 3 | Esquema | Estructura acordada |

## 📖 Definiciones y características

- **Serialización** — convertir datos en un formato transmisible (texto o binario). Clave: cruzar la frontera de lenguaje.
- **Formato de intercambio** — representación común (JSON, Protobuf). Clave: independiente del lenguaje.
- **Esquema** — estructura acordada de los datos. Clave: emisor y receptor lo comparten.

## 🧩 Situación

Un servicio en Go envía datos a uno en Python: los serializa (a JSON o Protobuf), viajan como bytes y el otro los deserializa. El formato común es lo que permite el diálogo entre lenguajes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `serializado=<clave>:<valor>`
- **Regla:** unir clave y valor con ':'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `serializado=x:5` |
| `edad 30` | `serializado=edad:30` |
| `n 100` | `serializado=n:100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; ESCRIBIR clave:valor
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

clave, valor = sys.stdin.readline().split()
print(f"serializado={clave}:{valor}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`serializado=${clave}:${valor}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`serializado=${clave}:${valor}`);
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
        System.out.println("serializado=" + p[0] + ":" + p[1]);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"serializado={p[0]}:{p[1]}");
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
	fmt.Printf("serializado=%s:%s\n", p[0], p[1])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    println!("serializado={}:{}", p[0], p[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char clave[64], valor[64];
    if (scanf("%63s %63s", clave, valor) != 2) return 1;
    printf("serializado=%s:%s\n", clave, valor);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena clave y valor.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'serializado=' || clave || ':' || valor AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "serializado=$clave:$valor\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Concatenación (aquí); librerías JSON/Protobuf en la práctica. |
| Semántica | El formato debe interpretarse igual en ambos lados. |
| Paradigmática | SQL exporta a JSON con funciones del motor. |

## 🧬 El concepto en la familia

JSON (texto, universal), Protobuf/MessagePack (binarios, compactos y con esquema) son los formatos habituales.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 159
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Formato ambiguo sin esquema** → causa: el receptor no sabe interpretar → solución: acordar un esquema o formato estándar
- **Diferencias de codificación** → causa: acentos/emoji corruptos → solución: usar UTF-8 y formatos bien definidos

## ❓ Preguntas frecuentes

- **¿JSON o Protobuf?** JSON es legible y universal; Protobuf es compacto y tipado. Según el caso.
- **¿Serializar y deserializar son inversos?** Sí: uno convierte a formato, el otro reconstruye el dato.

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

> [⏮️ Clase 158](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 160 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md)
