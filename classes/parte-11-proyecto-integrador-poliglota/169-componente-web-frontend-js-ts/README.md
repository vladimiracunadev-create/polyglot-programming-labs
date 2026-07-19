# Clase 169 — Componente web/frontend (JS/TS)

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construimos la cara visible del sistema: el **componente web/frontend**. Es lo único que el usuario toca, y
vive casi por definición en JavaScript o TypeScript, porque son los lenguajes que el navegador ejecuta. Su
trabajo esencial es **renderizar**: convertir los datos que llegan de la API en elementos que una persona
ve y con los que interactúa. Hoy simulamos ese acto en su forma mínima —recibir `n` elementos y confirmar
que se renderizaron— para aislar la idea sin el ruido del DOM.

Por qué importa el frontend como componente separado tiene una respuesta de arquitectura. Newman describe
el patrón *Backend for Frontend*: la interfaz no debería contener la lógica de negocio (esa vive en el
backend, clase 168), sino solo la **presentación**. Esta separación es una aplicación directa de lo que
Hunt y Thomas llaman ortogonalidad: si mezclas cálculo de precios con el código que pinta la tabla, un
cambio de diseño te obliga a tocar la lógica y viceversa. Mantener el frontend como consumidor puro de la
API —recibe datos, los muestra— es lo que permite rediseñar la pantalla sin miedo y sustituir el cliente
web por uno móvil reutilizando el mismo backend.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular el renderizado de una vista a partir de datos.
2. Explicar por qué el frontend debe ser presentación pura y consumir la lógica del backend.
3. Reconocer por qué JS/TS es el lenguaje natural de este componente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Frontend | La interfaz que el usuario ve y toca |
| 2 | Renderizar | Convertir datos en UI |
| 3 | Estado de la UI | Lo que se muestra cambia con la interacción |

## 📖 Definiciones y características

El **componente web** es la interfaz que interactúa con el usuario; consume la API y muestra sus datos.
**Renderizar** es convertir esos datos en elementos visuales —es, literalmente, lo que el usuario ve—. El
**estado de la UI** son los datos que la interfaz muestra en un instante dado; cambia con cada interacción,
y gestionarlo bien es el problema central de los frameworks modernos.

La clave conceptual es la dirección del flujo: datos del backend → estado del frontend → render. Frameworks
como React, Vue o Svelte formalizan esta cadena con la idea de que la UI es una **función del estado**: dado
el mismo estado, el mismo render. Esa es una idea profundamente declarativa que Haverbeke desarrolla en
*Eloquent JavaScript* —describes qué debe verse, no los pasos para pintarlo—, y contrasta con la vieja
manipulación imperativa del DOM nodo por nodo. Confirmar "renderizado ok" es la versión atómica de cerrar
ese ciclo: los datos llegaron y la vista los reflejó.

## 🧩 Situación

El frontend recibe `n` elementos de la API y los renderiza como una lista; confirmar que el render fue
correcto cierra el flujo de extremo a extremo. Piensa en el caso `n = 0`: una lista vacía. Un frontend
descuidado se rompe o muestra una pantalla en blanco desconcertante; uno bien pensado renderiza igual y
avisa "no hay elementos". Ese detalle —el estado vacío— es la diferencia entre una UI robusta y una frágil,
y por eso el modelo incluye el caso `0`. Este componente vive en el navegador, y su lenguaje es JavaScript
o TypeScript porque son los que el navegador entiende de forma nativa.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de elementos a renderizar)
- **Salida** (stdout): `items=<n> render=ok`
- **Regla:** renderizar n elementos y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `items=3 render=ok` |
| `0` | `items=0 render=ok` |
| `10` | `items=10 render=ok` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; renderizar n items ; confirmar render
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"items={n} render=ok")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`items=${n} render=ok`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`items=${n} render=ok`);
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
        System.out.println("items=" + n + " render=ok");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"items={n} render=ok");
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
	fmt.Printf("items=%d render=ok\n", n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("items={n} render=ok");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("items=%ld render=ok\n", n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL provee datos; aqui, el render simulado.
WITH t(n) AS (VALUES (3))
SELECT printf('items=%d render=ok', n) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "items=$n render=ok\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) es: de `3` sale `items=3 render=ok`; de `0`, `items=0 render=ok`.
El `render=ok` fijo modela "la vista reflejó los datos"; el número modela cuántos elementos. Que el caso
`0` esté en los casos es intencional: fuerza a que el estado vacío no sea una excepción sino un valor más.

Como este componente es JS/TS por naturaleza, empecemos por su lenguaje. **JavaScript**:

```javascript
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`items=${n} render=ok`);
```

`readFileSync(0, ...)` lee el descriptor 0 (stdin) —el equivalente de "recibir los datos de la API"—,
`parseInt(..., 10)` los convierte a entero en base 10 (el `10` explícito evita sorpresas históricas de JS
con octales), y el *template literal* compone la línea. Es exactamente el gesto que un componente hace:
tomar datos crudos y producir una salida presentable.

**TypeScript** es el mismo código con una promesa añadida: la anotación `const n: number`. No cambia lo que
se ejecuta —TS se borra al compilar—, pero convierte en error de compilación tratar `n` como si fuera texto
más adelante. Cherny, en *Programming TypeScript*, defiende justo esto: el tipo es documentación que el
compilador verifica, valiosísima en una UI donde el estado se pasa por muchas manos.

Ahora el contraste. **Python** hace lo mismo (`n = int(sys.stdin.readline())`) pero nunca correría en un
navegador; aquí demuestra que el *algoritmo* es universal aunque el *lenguaje del componente* no lo sea.
**SQL** no renderiza —no es su trabajo—; solo provee los datos que el frontend mostraría, y por eso ilustra
la salida y el verificador la marca como *ilustrativa*. La lección políglota es nítida: el mismo `items=n
render=ok` sale de diez lenguajes, pero **solo dos de ellos pertenecen de verdad a este componente**. Elegir
el lenguaje por componente (clase 164) es precisamente esto.

## 🔬 Comparación

Formatear una salida es idéntico en todos; lo revelador es que este componente tiene un lenguaje "correcto".

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | *Template literals* (JS/TS), *f-strings* (Python), `printf` (Go/C), interpolación (PHP): la misma composición. |
| Semántica | TypeScript añade tipos verificados sobre JS sin cambiar la ejecución; el resto infiere o convierte en tiempo de ejecución. |
| Paradigmática | El frontend transforma datos en UI (imperativo o declarativo por framework); SQL no renderiza, solo aporta los datos. |

La diferencia más real no es de sintaxis sino de **pertenencia**: JS/TS corren en el navegador; los demás
no. Un frontend en C sería una curiosidad; uno en TypeScript es el estándar de la industria. Esa es la
diferencia que un sistema políglota respeta al asignar lenguajes por componente.

## 🧬 El concepto en la familia

React, Vue y Svelte (JS/TS) y Flutter (Dart) construyen interfaces sobre la idea de "UI como función del
estado". Todos parten del mismo ciclo datos → estado → render que aquí reducimos a una línea; conocer el
ciclo crudo es lo que hace legible cualquiera de esos frameworks, porque debajo de su magia hay este mismo
flujo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 169
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquear la UI con cálculo pesado** → causa: JS es de un solo hilo y un cómputo largo congela la interfaz → solución: mover el trabajo a un *web worker* o al backend.
- **Renderizar sin manejar el estado vacío** → causa: la vista se rompe o queda en blanco con `0` elementos → solución: tratar la lista vacía como un estado de primera clase, no como un error.
- **Meter lógica de negocio en el frontend** → causa: el precio o las reglas quedan atrapados en el cliente y no se pueden reutilizar → solución: dejar la presentación en el frontend y la lógica en el backend.

## ❓ Preguntas frecuentes

- **¿Frontend en qué lenguaje?** JavaScript/TypeScript en el navegador; Dart con Flutter para móvil. Es el componente donde el lenguaje viene casi impuesto por la plataforma.
- **¿Lógica en el frontend o backend?** La presentación en el frontend; la de negocio en el backend. Así rediseñas la UI sin tocar reglas y reutilizas el backend con varios clientes.
- **¿Por qué TypeScript sobre JavaScript?** Porque los tipos atrapan en compilación errores de estado que en JS solo aparecerían en tiempo de ejecución, y en una UI el estado pasa por muchas manos.

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

> [⏮️ Clase 168](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 170 ⏭️](../../parte-11-proyecto-integrador-poliglota/170-componente-de-datos-y-consultas-sql/README.md)
