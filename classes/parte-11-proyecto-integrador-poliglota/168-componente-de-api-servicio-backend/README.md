# Clase 168 — Componente de API/servicio (backend)

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construimos el corazón del sistema: el **componente de API o servicio backend**. Es donde vive la lógica de
negocio; recibe una petición y devuelve una **respuesta** compuesta por dos cosas inseparables: un **código
de estado** (¿fue bien?) y unos **datos** (el resultado). Hoy implementamos el caso feliz: responder `200`
(OK) con el dato recibido.

Que la respuesta lleve siempre un código de estado no es un detalle de HTTP: es un principio de diseño de
sistemas distribuidos. Nygard, en *Release It!*, dedica su libro a que un servicio no basta con que
funcione en la demo —tiene que **comportarse bien cuando algo falla**—, y el primer eslabón de ese buen
comportamiento es comunicar con honestidad el desenlace de cada petición. Un `200` que en realidad
encubre un error es, en sus palabras, una bomba de tiempo: el cliente cree que todo fue bien y sigue
adelante sobre datos rotos. Newman, en *Building Microservices*, complementa: la API es el contrato público
del servicio, y el código de estado es la parte del contrato que dice cómo interpretar el resto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir una respuesta de API que combine un **estado** y unos **datos**.
2. Explicar por qué el código de estado es la primera obligación de un servicio honesto.
3. Reconocer el papel del backend como sede de la lógica y contrato público del sistema.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Servicio/API | Atiende peticiones y contiene la lógica |
| 2 | Código de estado | 200 OK, 404, 500: comunica el desenlace |
| 3 | Respuesta | Estado + datos: lo que el cliente interpreta |

## 📖 Definiciones y características

El **componente de API** es el servicio que atiende peticiones y devuelve respuestas; concentra la lógica
del sistema y, por eso, es su cerebro. El **código de estado** es el número que resume el resultado: `200`
OK, `404` no encontrado, `500` error del servidor. La **respuesta** es la suma de ese estado y los datos;
es literalmente lo que el cliente va a consumir e interpretar.

La familia de códigos (2xx éxito, 4xx culpa del cliente, 5xx culpa del servidor) es un lenguaje común que
permite que un frontend en TypeScript, un cliente móvil en Kotlin y un `curl` en un script entiendan lo
mismo sin ponerse de acuerdo caso por caso. Ese es el poder de un contrato bien diseñado: reduce la
coordinación. Nygard insiste en que las respuestas de error son tan parte de la API como las de éxito —un
servicio que solo documenta el `200` es un servicio a medio diseñar—, porque los patrones de estabilidad
(timeouts, reintentos, *circuit breakers*) se apoyan justamente en distinguir un `503` transitorio de un
`400` definitivo.

## 🧩 Situación

El frontend pide un dato; el backend responde `200` con el dato, o `404` si no existe, o `500` si algo se
rompió por dentro. Ese pequeño número gobierna lo que el cliente hará después: mostrar el resultado,
enseñar "no encontrado" o reintentar más tarde. El componente de API es el lugar donde a menudo se elige
Go, Java o C# por su rendimiento y su ecosistema de servidores (Spring, ASP.NET, Gin), o Python con FastAPI
por la velocidad de desarrollo. Empezar por el caso `200` fija la forma de la respuesta —estado más datos—
que los casos de error rellenarán después.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (el dato solicitado)
- **Salida** (stdout): `respuesta=200 datos=<n>`
- **Regla:** responder 200 con el dato

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `respuesta=200 datos=5` |
| `0` | `respuesta=200 datos=0` |
| `42` | `respuesta=200 datos=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR estado 200 y datos=n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"respuesta=200 datos={n}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`respuesta=200 datos=${n}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`respuesta=200 datos=${n}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("respuesta=200 datos=" + n);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"respuesta=200 datos={n}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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
	fmt.Printf("respuesta=200 datos=%d\n", n)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("respuesta=200 datos={n}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("respuesta=200 datos=%ld\n", n);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL devuelve filas; aqui, la respuesta simulada.
WITH t(n) AS (VALUES (5))
SELECT printf('respuesta=200 datos=%d', n) AS resultado FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "respuesta=200 datos=$n\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) es deliberadamente simple para que el foco esté en la **forma** de
la respuesta: de `5` sale `respuesta=200 datos=5`; de `0`, `respuesta=200 datos=0`. Un backend real leería
JSON de una petición HTTP; aquí el "cuerpo de la petición" es el entero por stdin, y la respuesta es la
línea de salida. La abstracción se sostiene: leer una entrada, devolver estado + datos.

**Python** convierte y responde en dos gestos: `n = int(sys.stdin.readline())` parsea el dato pedido, y la
*f-string* `f"respuesta=200 datos={n}"` arma la respuesta con su código fijo. La conversión a `int` importa:
un backend valida y tipa lo que entra antes de confiar en ello.

**Rust** hace explícito ese contrato de tipos donde Python lo deja implícito:

```rust
let n: i64 = s.trim().parse().unwrap();
println!("respuesta=200 datos={n}");
```

La anotación `: i64` y el `parse()` dicen "espero un entero de 64 bits, y si no lo es, esto no continúa".
El `unwrap()` es la versión abrupta de manejar el error —en producción sería un `match` que devolvería un
`400`—, pero el mensaje de Klabnik y Nichols en *The Rust Programming Language* ya está: los errores son
valores que el tipo te obliga a mirar. Un backend en Rust no puede "olvidar" que el parseo puede fallar.

**Go** parsea con `strconv.Atoi` devolviendo `(valor, error)` —el segundo, aquí ignorado con `_`, sería en
un servidor real la señal para responder `400`—. **C** usa `scanf("%ld", &n)` y comprueba que leyó
exactamente un valor (`!= 1`) antes de responder, saliendo con `return 1` si no. **SQL** ilustra la
respuesta como una fila calculada, recordándonos que su modelo es "devolver conjuntos", no "devolver
códigos HTTP". En los cinco, el patrón es el mismo: **validar la entrada, componer estado + datos**. La
diferencia está en cuánto te obliga el lenguaje a tomar en serio el fallo del parseo, que es exactamente el
fallo que un backend descuidado convierte en un `500`.

## 🔬 Comparación

La respuesta de una API es "estado + datos", y la parte interesante es qué pasa cuando la entrada no es lo
esperado.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `int(...)` (Python), `parse()` (Rust), `Atoi` (Go), `int.Parse` (C#), `scanf` (C): la misma validación de tipo. |
| Semántica | Rust y Go hacen del error de parseo un valor explícito; Python lanza excepción; C devuelve un código. Ese error es, en un backend real, la diferencia entre un `400` y un `500`. |
| Paradigmática | Los servicios imperativos componen y emiten una respuesta; SQL devuelve filas de un conjunto, no códigos de estado. |

La lección de Nygard aplica letra por letra: el caso feliz es el 20 % del diseño; el 80 % es qué respondes
cuando la entrada es basura, el vecino no contesta o la base de datos tarda. El código de estado es la
herramienta con la que ese 80 % se hace comunicable.

## 🧬 El concepto en la familia

Express (JS), Spring (Java), ASP.NET (C#), Gin (Go) y FastAPI (Python) construyen APIs sobre este mismo
esqueleto: recibir una petición, ejecutar la lógica, devolver estado + datos. Cambian el rendimiento, el
sistema de tipos y la ergonomía, pero el contrato —código de estado más cuerpo— es idéntico, y por eso
saltar de un framework a otro es aprender la forma, no el fondo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 168
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Devolver 200 en un error** → causa: el cliente cree que todo fue bien y sigue sobre datos rotos → solución: usar el código correcto (4xx para culpa del cliente, 5xx para fallo del servidor).
- **Respuestas sin formato acordado** → causa: cada endpoint responde a su manera y el cliente no las interpreta → solución: seguir un contrato de API consistente y versionado.
- **No validar la entrada** → causa: un dato mal formado se cuela y revienta dentro, generando un `500` → solución: parsear y validar en la frontera y responder `400` cuando la petición sea inválida.

## ❓ Preguntas frecuentes

- **¿Qué código para 'no encontrado'?** `404`. `200` es OK, `400` es petición inválida del cliente, `500` es error interno del servidor y `503` es "no disponible ahora, reintenta".
- **¿Qué lenguaje para el backend?** Depende del contexto: Go, Java o C# por rendimiento y ecosistema de servidores; Python (FastAPI) por rapidez de desarrollo. La API es el mismo contrato en todos.
- **¿Dónde manejo los fallos del vecino?** En el backend, con los patrones de *Release It!*: timeouts, reintentos con límite y *circuit breakers*, para que un servicio lento no arrastre a todo el sistema.

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

> [⏮️ Clase 167](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 169 ⏭️](../../parte-11-proyecto-integrador-poliglota/169-componente-web-frontend-js-ts/README.md)
