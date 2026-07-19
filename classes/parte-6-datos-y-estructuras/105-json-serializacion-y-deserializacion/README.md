# Clase 105 — JSON: serialización y deserialización

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con **JSON**: el formato universal de intercambio de datos. Aquí se **serializa** (construye) un objeto JSON con un formato fijo; en la práctica también se deserializa (parsea).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar datos a JSON.
2. Respetar el formato (comillas, dos puntos).
3. Reconocer JSON como formato de intercambio.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | JSON | Formato de intercambio de datos |
| 2 | Serializar | De datos a texto JSON |
| 3 | Deserializar | De texto JSON a datos |

## 📖 Definiciones y características

- **JSON** — formato de texto para datos estructurados (objetos, arreglos). Clave: universal entre lenguajes.
- **Serializar** — convertir datos en su representación de texto (JSON). Clave: para enviarlos o guardarlos.
- **Deserializar** — reconstruir datos desde el texto JSON. Clave: la operación inversa.

## 🧩 Situación

Las APIs web hablan JSON. Un objeto `{"nombre": "Ada", "edad": 36}` viaja entre un servidor en Go y un cliente en JavaScript sin problema: JSON es el idioma común.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `{"nombre": "<nombre>", "edad": <edad>}`
- **Regla:** objeto JSON con las claves nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `{"nombre": "Ada", "edad": 36}` |
| `Bo 5` | `{"nombre": "Bo", "edad": 5}` |
| `Cy 99` | `{"nombre": "Cy", "edad": 99}` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; construir objeto ; serializar a JSON
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

t = sys.stdin.readline().split()
nombre, edad = t[0], int(t[1])
print(f'{{"nombre": "{nombre}", "edad": {edad}}}')
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre = t[0];
const edad = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre: string = t[0];
const edad: number = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        String nombre = t[0];
        int edad = Integer.parseInt(t[1]);
        System.out.println("{\"nombre\": \"" + nombre + "\", \"edad\": " + edad + "}");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string nombre = t[0];
int edad = int.Parse(t[1]);
Console.WriteLine($"{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
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
	t := strings.Fields(line)
	nombre := t[0]
	edad, _ := strconv.Atoi(t[1])
	fmt.Printf("{\"nombre\": \"%s\", \"edad\": %d}\n", nombre, edad)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let nombre = t[0];
    let edad: i64 = t[1].parse().unwrap();
    println!("{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char nombre[64];
    long edad;
    if (scanf("%63s %ld", nombre, &edad) != 2) return 1;
    printf("{\"nombre\": \"%s\", \"edad\": %ld}\n", nombre, edad);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: construye JSON con printf (o json_object en motores con la extensión).
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('{"nombre": "%s", "edad": %d}', nombre, edad) AS resultado FROM personas;
```

### PHP · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$nombre = $t[0];
$edad = (int) $t[1];
echo "{\"nombre\": \"$nombre\", \"edad\": $edad}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Librerías `json` (Python), `JSON.stringify` (JS), pero el formato es idéntico. |
| Semántica | Las cadenas van entre comillas dobles; los números sin comillas. |
| Paradigmática | SQL genera JSON con funciones `json_object` (aquí, con printf). |

## 🧬 El concepto en la familia

En Ruby `to_json`. En casi todos hay una librería estándar o popular para JSON; el formato no cambia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 105
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comillas simples en JSON** → causa: JSON exige comillas dobles → solución: usar comillas dobles siempre
- **Poner comillas a los números** → causa: tipo incorrecto → solución: los números van sin comillas

## ❓ Preguntas frecuentes

- **¿Construir JSON a mano o con librería?** En la práctica, librería (escapa bien); aquí a mano para fijar el formato exacto.
- **¿JSON solo para web?** No: también para configuración, logs y almacenamiento.

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

> [⏮️ Clase 104](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 106 ⏭️](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md)
