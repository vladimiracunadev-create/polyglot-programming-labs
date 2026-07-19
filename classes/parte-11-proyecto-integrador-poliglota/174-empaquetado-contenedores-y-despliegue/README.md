# Clase 174 — Empaquetado, contenedores y despliegue

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Realizar el **empaquetado, los contenedores y el despliegue**: meter el sistema y su entorno en una imagen de contenedor reproducible. Aquí se construye el nombre de la imagen a partir de la versión.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Etiquetar una imagen de contenedor.
2. Explicar qué resuelve un contenedor.
3. Relacionar imagen con despliegue.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contenedor | Programa + su entorno |
| 2 | Imagen etiquetada | app:version |
| 3 | Despliegue | Correr la imagen |

## 📖 Definiciones y características

- **Contenedor** — empaqueta el programa con su entorno mínimo. Clave: elimina el 'funciona en mi máquina'.
- **Imagen** — plantilla de la que se crean contenedores, etiquetada con una versión. Clave: `app:1.2.3`.
- **Despliegue** — poner en marcha la imagen en un entorno. Clave: reproducible y versionado.

## 🧩 Situación

El sistema políglota (frontend, backend, datos) se empaqueta en imágenes de contenedor etiquetadas por versión y se despliega. La imagen lleva el entorno consigo, así corre igual en cualquier lado.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `imagen=app:<versión>`
- **Regla:** construir el nombre de imagen app:version

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `imagen=app:1.2.3` |
| `0.9.0` | `imagen=app:0.9.0` |
| `2.1.5` | `imagen=app:2.1.5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; ESCRIBIR 'imagen=app:' + version
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

version = sys.stdin.readline().strip()
print(f"imagen=app:{version}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String version = br.readLine().trim();
        System.out.println("imagen=app:" + version);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string version = Console.In.ReadToEnd().Trim();
Console.WriteLine($"imagen=app:{version}");
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
	version := strings.TrimSpace(line)
	fmt.Printf("imagen=app:%s\n", version)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let version = s.trim();
    println!("imagen=app:{version}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("imagen=app:%s\n", version);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena el nombre de la imagen.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'imagen=app:' || v AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$version = trim(fgets(STDIN));
echo "imagen=app:$version\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Concatenación en cada lenguaje. |
| Semántica | La etiqueta identifica la versión de la imagen. |
| Paradigmática | SQL concatena con \|\|. |

## 🧬 El concepto en la familia

Docker y OCI empaquetan en imágenes; Kubernetes las despliega y orquesta.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 174
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imágenes sin versión (:latest)** → causa: no saber qué corre → solución: etiquetar con la versión concreta
- **Imágenes enormes** → causa: despliegues lentos → solución: usar imágenes base mínimas y multi-stage

## ❓ Preguntas frecuentes

- **¿Contenedor o máquina virtual?** El contenedor comparte el kernel y es más ligero; empaqueta el entorno, no un SO completo.
- **¿Por qué etiquetar?** Para saber exactamente qué versión está desplegada y poder revertir.

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

> [⏮️ Clase 173](../../parte-11-proyecto-integrador-poliglota/173-pruebas-end-to-end-del-sistema-completo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 175 ⏭️](../../parte-11-proyecto-integrador-poliglota/175-documentacion-y-defensa-de-las-decisiones-de-lenguaje/README.md)
