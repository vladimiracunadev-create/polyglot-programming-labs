# Clase 160 — Contratos de API: REST, gRPC y esquemas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **contratos de API (REST, gRPC)**: la frontera entre servicios se define con un contrato (qué operaciones, qué datos). Un endpoint REST combina un método (GET, POST) con un recurso (/users).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un endpoint a partir de método y recurso.
2. Explicar qué es un contrato de API.
3. Distinguir REST de gRPC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato de API | El acuerdo entre servicios |
| 2 | REST | Recursos y métodos HTTP |
| 3 | gRPC | Contratos con esquema (Protobuf) |

## 📖 Definiciones y características

- **Contrato de API** — acuerdo de qué operaciones y datos expone un servicio. Clave: frontera estable entre componentes.
- **REST** — estilo basado en recursos y métodos HTTP (GET, POST, PUT). Clave: simple y universal.
- **gRPC** — framework de RPC con contratos definidos en Protobuf. Clave: eficiente y tipado.

## 🧩 Situación

El frontend habla con el backend a través de una API: `GET /users` pide los usuarios. El contrato define esos endpoints; mientras se respete, cada lado puede evolucionar por separado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `metodo recurso`
- **Salida** (stdout): `contrato=<METODO> /<recurso>`
- **Regla:** combinar método y recurso en un endpoint

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `GET users` | `contrato=GET /users` |
| `POST items` | `contrato=POST /items` |
| `PUT data` | `contrato=PUT /data` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER metodo, recurso ; ESCRIBIR metodo + ' /' + recurso
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

metodo, recurso = sys.stdin.readline().split()
print(f"contrato={metodo} /{recurso}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [metodo, recurso] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${metodo} /${recurso}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [metodo, recurso] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${metodo} /${recurso}`);
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
        System.out.println("contrato=" + p[0] + " /" + p[1]);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"contrato={p[0]} /{p[1]}");
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
	fmt.Printf("contrato=%s /%s\n", p[0], p[1])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    println!("contrato={} /{}", p[0], p[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char metodo[16], recurso[64];
    if (scanf("%15s %63s", metodo, recurso) != 2) return 1;
    printf("contrato=%s /%s\n", metodo, recurso);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL construye el endpoint por concatenacion.
WITH t(metodo, recurso) AS (VALUES ('GET', 'users'))
SELECT 'contrato=' || metodo || ' /' || recurso AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$metodo, $recurso] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=$metodo /$recurso\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Concatenación en cada lenguaje. |
| Semántica | El contrato desacopla cliente y servidor. |
| Paradigmática | SQL expone datos vía vistas/procedimientos. |

## 🧬 El concepto en la familia

REST (HTTP), gRPC (Protobuf), GraphQL son estilos de contrato entre servicios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 160
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: romper a los clientes → solución: versionar la API y evolucionar con compatibilidad
- **Endpoints ambiguos** → causa: confusión y errores → solución: seguir convenciones REST claras

## ❓ Preguntas frecuentes

- **¿REST o gRPC?** REST para APIs públicas y simples; gRPC para comunicación interna eficiente y tipada.
- **¿Qué es un endpoint?** Un punto de acceso: método + ruta que ofrece una operación.

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

> [⏮️ Clase 159](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 161 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md)
