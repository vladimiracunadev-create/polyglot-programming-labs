# Clase 167 — Componente CLI (lenguaje de sistemas)

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construimos el primer componente concreto del sistema: la **CLI**, la interfaz de línea de comandos. Es el
territorio natural de los lenguajes de sistemas (Go, Rust, C), que compilan a un binario único, arrancan al
instante y no arrastran un runtime. La tarea de hoy es la base de toda herramienta de terminal: **parsear
la invocación**, es decir, separar el **comando** (qué hacer) de sus **argumentos** (con qué datos), y
contar estos últimos.

Detrás de este ejercicio hay una idea vieja y poderosa. La filosofía Unix —que Hunt y Thomas reivindican en
*The Pragmatic Programmer* bajo la máxima "usa el poder de los shells" y "el texto plano es universal"—
dice que las herramientas pequeñas, componibles por línea de comandos, envejecen mejor que las grandes
aplicaciones cerradas. Una CLI bien parseada es automatizable: encaja en un script, en un `cron`, en un
pipeline de CI. Por eso la CLI no es un juguete de programadores nostálgicos, sino a menudo la puerta de
entrada más estable a un sistema.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Parsear una invocación de CLI separando el comando de sus argumentos.
2. Explicar por qué la línea de comandos hace un componente **automatizable y componible**.
3. Reconocer por qué los lenguajes de sistemas dominan este componente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CLI | La interfaz de terminal, componible en scripts |
| 2 | Comando y argumentos | El primer token decide; el resto son datos |
| 3 | Parseo | Interpretar la invocación es el paso cero |

## 📖 Definiciones y características

El **componente CLI** es la interfaz del sistema por terminal; su virtud es que se automatiza y se compone
con otras herramientas a través de texto plano. El **comando** es la acción a ejecutar —el primer token,
como `run`, `build` o `deploy`— y selecciona qué se hace. Un **argumento** es un dato que modifica esa
acción; en esta clase simplemente los contamos, pero en una CLI real serían rutas, banderas o valores.

La distinción comando/argumentos es la misma que estructura `git commit -m "..."`, `docker run imagen` o
`kubectl apply -f`. Reconocerla es reconocer un patrón universal: `argv[0]` es el programa, el siguiente
token suele ser el subcomando, y el resto son parámetros. Los lenguajes de sistemas brillan aquí porque un
binario compilado es lo que un administrador quiere desplegar: sin dependencias, rápido, predecible.
Donovan y Kernighan muestran en *The Go Programming Language* cómo Go se pensó justamente para esto —
herramientas de infraestructura que se distribuyen como un solo archivo—.

## 🧩 Situación

La CLI recibe `run a b`: el comando es `run` y hay 2 argumentos. Suena obvio hasta que piensas en todo lo
que un parser real debe decidir: ¿qué pasa si no hay comando? ¿los argumentos van posicionales o con
nombre (`--flag`)? ¿cómo se reporta un error para que un script que invoca la herramienta pueda detectarlo?
Empezar por el caso mínimo —primer token es el comando, el resto se cuenta— fija la estructura mental sobre
la que después se apoyan librerías como `clap` (Rust), `cobra` (Go) o `argparse` (Python). Parsear bien la
invocación es, literalmente, lo primero que hace cualquier programa de terminal antes de trabajar.

## 🧮 Modelo

- **Entrada** (stdin): una línea `comando arg1 arg2 ...` (al menos el comando)
- **Salida** (stdout): `comando=<comando> args=<número de argumentos>`
- **Regla:** primer token = comando; resto = argumentos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `run a b` | `comando=run args=2` |
| `build` | `comando=build args=0` |
| `deploy x y z` | `comando=deploy args=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens ; comando <- tokens[0] ; args <- tokens - 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

t = sys.stdin.read().split()
print(f"comando={t[0]} args={len(t) - 1}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
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
        System.out.println("comando=" + t[0] + " args=" + (t.length - 1));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"comando={t[0]} args={t.Length - 1}");
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
	t := strings.Fields(line)
	fmt.Printf("comando=%s args=%d\n", t[0], len(t)-1)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    println!("comando={} args={}", t[0], t.len() - 1);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char comando[64], t[64];
    if (scanf("%63s", comando) != 1) return 1;
    int args = 0;
    while (scanf("%63s", t) == 1) args++;
    printf("comando=%s args=%d\n", comando, args);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene CLI; se ilustra con valores.
WITH t(comando, args) AS (VALUES ('run', 2))
SELECT printf('comando=%s args=%d', comando, args) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
echo "comando={$t[0]} args=" . (count($t) - 1) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) pide: de `run a b` sale `comando=run args=2`; de `build` solo,
`comando=build args=0`. La lógica es "primer token = comando; resto = argumentos". Veamos cómo cada familia
la expresa, porque el manejo del "primero contra el resto" distingue las abstracciones.

**Python** lo hace en dos líneas de una elegancia casi tramposa:

```python
t = sys.stdin.read().split()
print(f"comando={t[0]} args={len(t) - 1}")
```

`split()` produce la lista completa de tokens; `t[0]` es el comando y `len(t) - 1` cuenta el resto. No hay
bucle: la lista ya lo sabe todo. Es el estilo que Ramalho llama "dejar que la secuencia trabaje".

**C** revela lo que Python oculta. No hay lista que preguntar por su longitud, así que hay que **leer**
token a token y contar a mano:

```c
if (scanf("%63s", comando) != 1) return 1;
int args = 0;
while (scanf("%63s", t) == 1) args++;
```

El primer `scanf` captura el comando; el `while` consume los argumentos incrementando `args`. Fíjate en dos
detalles de sistemas: el `%63s` limita la lectura a 63 caracteres para no desbordar el buffer de 64 (una
defensa contra el clásico *buffer overflow*), y el `return 1` ante la falta de comando comunica el error
por el **código de salida**, exactamente como un script espera. Kernighan y Ritchie enseñan esta disciplina
de "leer, contar, comprobar" como el pan de cada día en C.

**Go** se sitúa en medio: `strings.Fields(line)` da la lista como Python, y `t[0]` / `len(t)-1` la
recorren, pero conserva el gesto explícito de leer la línea con un `bufio.Reader`. **SQL** no tiene CLI de
argumentos —su "invocación" es la consulta misma—, así que ilustra el resultado con una tabla de valores y
el verificador la marca como *ilustrativa*. El mismo `comando=... args=...` sale de tres modelos: la lista
de alto nivel, el conteo byte a byte y la consulta declarativa.

## 🔬 Comparación

Separar "el primero del resto" parece idéntico, pero exhibe cuánto te acerca cada lenguaje al hardware.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `t[0]` + `len(t)-1` (Python/Go/JS), `scanf` en bucle (C), `preg_split` (PHP): el mismo "cabeza y cola". |
| Semántica | Los de alto nivel obtienen una colección con longitud conocida; C lee del flujo y cuenta, y debe acotar el buffer (`%63s`) para ser seguro. |
| Paradigmática | Los imperativos parsean una invocación; SQL no tiene invocación con argumentos, se consulta un conjunto. |

La diferencia real aquí es la **seguridad de memoria**: en Python o Go un token de más solo agranda una
lista; en C un token de más sin el límite `%63s` corrompe la pila. Esa es una de las razones por las que
las CLIs modernas se escriben cada vez más en Rust o Go —seguridad de memoria sin renunciar al binario
único—.

## 🧬 El concepto en la familia

`clap` (Rust), `cobra` (Go), `argparse` (Python) y `commander` (JS) construyen CLIs robustas sobre esta
misma base: descomponer `argv` en comando, subcomandos, banderas y argumentos. Todas heredan el modelo Unix
de `argv[0]` + resto que aquí implementamos a mano; conocer el patrón crudo es lo que permite leer y usar
cualquiera de esas librerías sin memorizarla.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 167
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No validar los argumentos** → causa: el programa asume que están y peta al usarlos → solución: comprobar cantidad y tipo antes de trabajar, y salir con código distinto de cero si faltan.
- **Mensajes de ayuda ausentes** → causa: una CLI sin `--help` es una caja negra → solución: ofrecer ayuda y mensajes de error claros en `stderr`.
- **Buffers sin acotar en C** → causa: leer un token más largo que el buffer corrompe memoria → solución: limitar la lectura (`%63s` para un buffer de 64) o usar lenguajes con seguridad de memoria.

## ❓ Preguntas frecuentes

- **¿Qué lenguaje para una CLI?** Go y Rust por su binario único, arranque instantáneo y seguridad de memoria; Python o Bash para scripts rápidos donde el runtime ya está.
- **¿Argumentos posicionales o con nombre?** Los nombrados (`--flag`) ganan en claridad y estabilidad; deja los posicionales para lo esencial e inequívoco (como la ruta principal).
- **¿Por dónde reporto los errores?** Los datos van a `stdout`, los errores a `stderr`, y el desenlace al **código de salida**: así un script que te invoca puede componerte con `&&` y `||`.

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

> [⏮️ Clase 166](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 168 ⏭️](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md)
