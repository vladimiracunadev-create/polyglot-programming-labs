# Clase 103 — Propiedad y ciclo de vida de los datos

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Responder la pregunta más callada y más consecuente de la programación de sistemas: **¿quién es responsable de liberar la memoria de un dato, y cuándo?** Todo dato ocupa un recurso —memoria, un descriptor de archivo, una conexión— que fue *adquirido* y que en algún momento debe ser *devuelto*. Entre esos dos instantes transcurre el **ciclo de vida**. Si nadie devuelve el recurso, se produce una *fuga* que va estrangulando al programa; si alguien lo devuelve dos veces o lo usa después de devolverlo, el comportamiento se vuelve indefinido y corrupto. La historia de los lenguajes es, en buena parte, la historia de tres respuestas distintas a esa pregunta: la gestión **manual** (tú lo liberas), la **recolección de basura** (el runtime lo libera cuando quiere) y la **propiedad con préstamos** (el compilador demuestra cuándo liberarlo). Esta clase te enseña a reconocer cuál de los tres modelos rige en cada lenguaje y qué precio paga cada uno: seguridad, determinismo o rendimiento —rara vez los tres a la vez.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el ciclo de vida de un recurso.
2. Liberar automáticamente al salir del ámbito.
3. Comparar RAII, defer y GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ciclo de vida | Crear → usar → liberar |
| 2 | RAII | La liberación va atada al ámbito |
| 3 | Liberación automática | defer, using, destructor |

## 📖 Definiciones y características

El **ciclo de vida** de un dato tiene tres actos —adquirir, usar, liberar— y la diferencia entre lenguajes está en quién dirige el tercero. En el modelo **manual**, encarnado por C, tú escribes `malloc` para pedir memoria del *heap* y tú escribes `free` para devolverla; Kernighan y Ritchie lo presentan en *The C Programming Language* como un par indisoluble, y toda la disciplina consiste en que cada `malloc` tenga exactamente un `free` en el momento correcto. El poder es total —controlas cada byte y cada instante— y por eso el peligro también: olvidar el `free` es una **fuga** (*memory leak*); llamarlo dos veces es un **doble free**; usar el puntero después de liberarlo es un **uso tras liberar** (*use-after-free*), la clase de error que alimenta la mitad de las vulnerabilidades de seguridad conocidas.

El modelo de **recolección de basura** (GC) —Java, Python, Go, JavaScript, C#— desplaza esa responsabilidad al *runtime*. Tú creas objetos y nunca los liberas: un recolector rastrea periódicamente qué datos siguen siendo *alcanzables* desde las variables vivas y reclama los que ya no lo son. Ganas seguridad casi total contra fugas y usos-tras-liberar, pero pagas dos precios: **pausas** impredecibles cuando el recolector se ejecuta y **no determinismo** sobre *cuándo* exactamente se libera un objeto —lo que importa poco para la memoria pero mucho para recursos como archivos, que no deben quedar abiertos «hasta que el GC se digne pasar».

El tercer modelo es la **propiedad con préstamos** (*ownership and borrowing*) de Rust, herencia directa del RAII de C++. Klabnik y Nichols dedican el corazón de *The Rust Programming Language* a sus reglas: cada valor tiene **un único dueño**; cuando el dueño sale de su ámbito, el valor se libera **determinísticamente** ejecutando `Drop`; y el préstamo (*borrow*) permite acceder al dato sin poseerlo bajo reglas que el **verificador de préstamos** comprueba en tiempo de **compilación**. Los **tiempos de vida** (*lifetimes*) anotan cuánto vive cada préstamo para que el compilador rechace toda referencia que sobreviva al dato que apunta. El resultado es la promesa que ningún otro modelo cumple: seguridad de memoria sin recolector y, por tanto, **sin coste en tiempo de ejecución** —lo que se paga es en tiempo de compilación y en la disciplina que el compilador exige.

## 🧩 Situación

Imagina un servicio que abre miles de archivos y conexiones por segundo. Cada recurso que abres es una promesa de cerrarlo, y las promesas rotas no fallan de inmediato: el programa funciona en las pruebas, pasa a producción y, horas después, se cae porque agotó el límite de descriptores de archivo del sistema operativo —una fuga lenta que ningún test corto detecta. Peor aún si el flujo tiene un `return` temprano o lanza una excepción entre el «abrir» y el «cerrar»: la liberación escrita al final nunca se ejecuta. La solución que los lenguajes maduros comparten es **atar la liberación al ámbito**, no a una línea que puede saltarse: `with` en Python, `defer` en Go, `try-with-resources` en Java, `using` en C#, `Drop` en Rust. Todos garantizan que el cierre ocurra al salir del bloque *pase lo que pase* —salida normal, `return` o error. El problema de hoy destila esa idea a su núcleo: crear un recurso con un valor, usarlo y liberarlo automáticamente al cerrar el ámbito, para que veas el mismo patrón encarnado en diez sintaxis.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (valor del recurso)
- **Salida** (stdout): `valor=<n> estado=liberado`
- **Regla:** crear recurso(n), usarlo, liberarlo al salir

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5 estado=liberado` |
| `0` | `valor=0 estado=liberado` |
| `9` | `valor=9 estado=liberado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; crear recurso ; usar ; liberar al salir del ámbito
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


class Recurso:
    def __init__(self, valor):
        self.valor = valor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # aquí se liberaría


n = int(sys.stdin.readline())
with Recurso(n) as r:
    valor = r.valor
print(f"valor={valor} estado=liberado")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor;
{
  const recurso = { valor: n };
  valor = recurso.valor;
  // en JS el GC libera; aquí el ámbito marca el fin de uso
}
console.log(`valor=${valor} estado=liberado`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor: number;
{
  const recurso = { valor: n };
  valor = recurso.valor;
}
console.log(`valor=${valor} estado=liberado`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Recurso implements AutoCloseable {
        final int valor;
        Recurso(int v) { this.valor = v; }
        public void close() { /* se libera aquí */ }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int valor;
        try (Recurso r = new Recurso(n)) {
            valor = r.valor;
        }
        System.out.println("valor=" + valor + " estado=liberado");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int valor;
using (var r = new Recurso(n)) {
    valor = r.Valor;
}
Console.WriteLine($"valor={valor} estado=liberado");

class Recurso : IDisposable {
    public int Valor { get; }
    public Recurso(int v) { Valor = v; }
    public void Dispose() { /* se libera aquí */ }
}
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
	valor := 0
	func() {
		defer func() { /* se libera al salir */ }()
		valor = n
	}()
	fmt.Printf("valor=%d estado=liberado\n", valor)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Recurso {
    valor: i64,
}

impl Drop for Recurso {
    fn drop(&mut self) {
        // se libera automáticamente al salir del ámbito
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor;
    {
        let r = Recurso { valor: n };
        valor = r.valor;
    } // aquí se ejecuta Drop
    println!("valor={valor} estado=liberado");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *recurso = malloc(sizeof(long));
    *recurso = n;
    long valor = *recurso;
    free(recurso); /* liberación manual */
    printf("valor=%ld estado=liberado\n", valor);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el ciclo de vida se gestiona con transacciones; aquí se ilustra el valor.
WITH nums(n) AS (VALUES (5), (0), (9))
SELECT printf('valor=%d estado=liberado', n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
class Recurso {
    public function __construct(public int $valor) {}
    public function __destruct() { /* se libera aquí */ }
}

$n = (int) trim(fgets(STDIN));
$r = new Recurso($n);
$valor = $r->valor;
unset($r); // libera el recurso
echo "valor=$valor estado=liberado\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `5`, que debe producir `valor=5 estado=liberado`. Las diez implementaciones crean un recurso, guardan su valor y lo liberan al cerrar el ámbito; conviene mirar tres que representan los tres modelos de gestión de memoria.

En **C**, el modelo manual está a la vista. `malloc(sizeof(long))` pide al asignador un bloque del *heap* del tamaño de un `long` y devuelve un puntero, `recurso`. Se escribe `*recurso = n` (guardar 5 en ese bloque), se copia a `valor` la lectura `*recurso`, y entonces —línea crítica— `free(recurso)` devuelve el bloque al asignador. El orden importa: se lee *antes* de liberar, porque tras el `free` el puntero queda colgando y desreferenciarlo sería un uso-tras-liberar. Como `valor` ya es una copia en la pila, imprimir `valor=5 estado=liberado` es seguro aunque el recurso ya no exista.

En **Rust**, nadie escribe la liberación: la declara el tipo. `impl Drop for Recurso` define qué ocurre cuando un `Recurso` se destruye. Dentro del bloque `{ let r = Recurso { valor: n }; valor = r.valor; }`, `r` es el **único dueño** del recurso; en la llave de cierre `}`, `r` sale de ámbito y el compilador **inserta automáticamente** la llamada a `drop`. No hay recolector ni `free` manual: la liberación es determinista y está garantizada por la compilación. `valor` se copió antes de cerrar el bloque, así que la impresión final produce `valor=5 estado=liberado`.

En **Python**, el modelo es GC pero el `with` fuerza el determinismo del *cierre*. `with Recurso(n) as r:` invoca `__enter__` al entrar y, garantizado, `__exit__` al salir del bloque —ahí iría la liberación real. El objeto en sí lo reclamará el recolector más tarde, cuando nadie lo alcance; lo que el `with` asegura no es *cuándo se libera la memoria* sino *cuándo se ejecuta el cierre*. Se guarda `valor = r.valor` dentro del bloque y se imprime fuera: `valor=5 estado=liberado`.

Los tres producen la misma línea, pero por caminos filosóficamente distintos: C confía en el programador, Rust confía en el compilador, Python confía en el runtime. El verificador comprueba que las diez coincidan carácter a carácter con `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Drop` (Rust), `defer` (Go), `using`/`try-with-resources` (C#/Java). |
| Semántica | Rust/C++ liberan determinísticamente; Java/Python dependen del GC salvo cierre explícito. |
| Paradigmática | SQL gestiona transacciones (COMMIT/ROLLBACK) como ciclo de vida. |

La frontera más profunda entre estos diez lenguajes es **el momento de la liberación**. En C, ese momento lo fijas tú con `free`, y equivocarte es corromper la memoria; en Rust y C++ lo fija el fin del ámbito, verificado en compilación y sin coste en ejecución; en Java, Python, JavaScript, Go y C# lo fija el recolector, en un instante que tú no controlas. Esa diferencia se vuelve tangible con los recursos que *no* son memoria: un archivo abierto ocupa un descriptor del sistema operativo, un bien mucho más escaso que la RAM, y esperar al GC para cerrarlo es una receta para agotarlos. Por eso incluso los lenguajes con GC ofrecen un mecanismo determinista de cierre —`try-with-resources`, `using`, `defer`, `with`— que actúa sobre el ámbito y no sobre el recolector. Go ocupa una posición peculiar: tiene GC para la memoria, pero `defer` para el cierre ordenado, atando la liberación a la *función* en lugar de al *bloque* como hace RAII. Y hay un eje de **propiedad**: en Rust un valor tiene un dueño y moverlo transfiere esa propiedad; en los lenguajes con GC los objetos se comparten libremente por referencia y el recolector desenreda quién sigue vivo.

## 🧬 El concepto en la familia

La idea de atar la liberación al ámbito nació en C++ con el patrón RAII (*Resource Acquisition Is Initialization*): el destructor de un objeto se ejecuta al salir del ámbito, de modo que un objeto en la pila que envuelve un recurso lo devuelve automáticamente al destruirse —el `Drop` de Rust es su descendiente directo, elevado por el sistema de propiedad a garantía verificada en compilación. Python replica la idea sin destructores deterministas mediante el *context manager* (`with`, los métodos `__enter__`/`__exit__`), que Ramalho analiza en *Fluent Python* como la forma pitónica de garantizar el cierre. Go la reformula con `defer`, que difiere una llamada hasta el retorno de la función; Java y C# la ofrecen como `try-with-resources` y `using` sobre las interfaces `AutoCloseable`/`IDisposable`. Bajo tanta sintaxis distinta late un mismo principio: **la adquisición y la liberación deben ser simétricas y estar ligadas a una región del código**, no a la buena memoria del programador.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 103
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No liberar recursos** → causa: cada `malloc`/`open`/`connect` sin su liberación correspondiente acumula una fuga que estrangula el programa con el tiempo → solución: atar la liberación al ámbito con RAII/`defer`/`using`/`with`, para que ocurra aunque haya un `return` temprano o una excepción.
- **Confiar solo en el GC para recursos que no son memoria** → causa: el recolector libera cuando le conviene, y un archivo o conexión puede quedar abierto minutos, agotando los descriptores del sistema → solución: cerrar explícita y deterministamente archivos, sockets y conexiones; nunca dejarlos «para que los recoja el GC».
- **Uso tras liberar (use-after-free)** → causa: en C, leer `*recurso` después de `free(recurso)`, o guardar en Rust una referencia que sobreviva al dato → solución: en C, copiar el valor antes de liberar y no volver a usar el puntero; en Rust, el verificador de préstamos lo rechaza en compilación.
- **Doble liberación (double free)** → causa: llamar `free` dos veces sobre el mismo puntero, o liberar un recurso ya cerrado → solución: liberar una sola vez y anular el puntero (`recurso = NULL`); en Rust el modelo de propiedad lo hace imposible.

## ❓ Preguntas frecuentes

- **¿El recolector de basura libera todo automáticamente?** Libera la *memoria* inalcanzable, sí, pero con dos salvedades: no lo hace en un instante que puedas predecir, y no gestiona recursos que no son memoria —archivos, conexiones, bloqueos. Esos ciérralos tú de forma determinista con `with`/`using`/`defer`.
- **¿RAII o `defer`?** Ambos garantizan la liberación al salir del ámbito, pero atan a cosas distintas: RAII (Rust, C++) la ata al **tipo** del recurso —el propio objeto sabe destruirse—, mientras `defer` (Go) la ata a la **función** —difieres una llamada explícita hasta el retorno. RAII es automático dondequiera que use el tipo; `defer` hay que recordarlo en cada función.
- **¿Qué gana Rust frente a un lenguaje con GC?** Determinismo y rendimiento sin sacrificar seguridad: la memoria se libera en un punto exacto y conocido, sin recolector que introduzca pausas, y aun así el compilador demuestra que no hay fugas, dobles frees ni usos-tras-liberar. El coste se paga en tiempo de compilación y en aprender las reglas de propiedad.
- **¿Por qué C sigue usando gestión manual?** Porque el control total es a veces el requisito: sistemas embebidos, núcleos de sistema operativo y código de máxima latencia predecible no pueden permitirse ni un recolector ni la sobrecarga de verificación. El precio es que la corrección recae por completo en el programador.

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

> [⏮️ Clase 102](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 104 ⏭️](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md)
