# Clase 130 — Gestión manual de memoria (C): malloc/free

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La memoria del heap no se administra sola: alguien tiene que decidir cuándo un bloque deja de estar en uso. En C ese alguien eres tú, y el contrato es explícito: cada `malloc` que tiene éxito genera una obligación de `free`. Esta clase hace visible ese contrato con un programa mínimo —reservar `n` enteros, llenarlos con `1..n`, sumarlos y liberar— porque el ejercicio expone en veinte líneas lo que en un sistema real se dispersa por miles. El *porqué* de estudiarlo es doble. Primero, porque **todos** los demás modelos de memoria del curso (el GC de la clase 131, el ownership de la 132) son respuestas de diseño a los problemas concretos que aparecen aquí: la fuga, el *use-after-free*, la doble liberación. No se entiende por qué Rust inventó el *borrow checker* si no se ha sentido antes qué se rompe sin él. Segundo, porque Bryant & O'Hallaron dedican en *Computer Systems: A Programmer's Perspective* un capítulo entero a la gestión dinámica de memoria precisamente porque el asignador es una pieza de software real, con políticas, fragmentación y coste medible, no una primitiva mágica del hardware.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué hace realmente `malloc` por dentro: dónde busca el bloque, qué metadatos guarda y qué devuelve.
2. Enunciar el contrato de propiedad implícito de C: quién reserva, quién libera y cuándo.
3. Describir los tres fallos clásicos —fuga, *use-after-free* y doble liberación— y por qué el compilador de C no puede detectarlos.
4. Contrastar la gestión manual con la automática en términos de coste, previsibilidad y superficie de error.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El asignador (`malloc`/`free`) | Es un programa: mantiene una lista de bloques libres y decide dónde cortar |
| 2 | Propiedad por convención | En C nadie más que la disciplina del autor garantiza que se libere |
| 3 | Fugas, *use-after-free* y doble liberación | Los tres fallos que motivaron el GC y el ownership |
| 4 | Fragmentación y coste | Por qué reservar en el heap no es gratis ni instantáneo |

## 📖 Definiciones y características

**`malloc(tamaño)`** no pide memoria al sistema operativo en cada llamada. El asignador de la biblioteca estándar mantiene un *pool* de memoria obtenido previamente del núcleo (mediante `brk`/`sbrk` para el heap clásico o `mmap` para bloques grandes) y, dentro de él, gestiona una estructura de bloques libres y ocupados. Cuando pides 40 bytes, el asignador recorre esa estructura buscando un hueco suficientemente grande —según la política, el *primer* hueco que sirva (*first fit*), el más ajustado (*best fit*) o el de una lista segregada por tamaños—, lo parte si sobra espacio, marca la parte reservada como ocupada y te devuelve un puntero a los datos. Justo *antes* de ese puntero, en memoria que no te pertenece, el asignador suele guardar una cabecera con el tamaño del bloque y bits de estado. Ese detalle explica dos cosas: por qué `free` puede liberar sin que le digas cuántos bytes eran, y por qué escribir un byte antes del puntero devuelto corrompe el asignador entero.

**`free(p)`** hace lo inverso: lee la cabecera, marca el bloque como libre y —esto es clave— intenta **fusionarlo (*coalescing*)** con los bloques libres adyacentes para no dejar el heap picado de huecos inútiles. La memoria casi nunca vuelve al sistema operativo; queda disponible para el siguiente `malloc` del mismo proceso. Por eso un programa con fugas puede ver crecer indefinidamente su RSS aunque el sistema tenga memoria de sobra: nadie devuelve nada.

La **fuga de memoria** es el bloque reservado cuyo último puntero se pierde: sigue marcado como ocupado, pero ya no existe forma de alcanzarlo ni, por tanto, de liberarlo. En un proceso de vida corta es inocuo (el SO recupera todo al terminar); en un servidor que corre meses es fatal. El **use-after-free** es el error inverso y mucho más grave: liberas y sigues usando el puntero. Como el asignador ya puede haber entregado ese mismo bloque a otra parte del programa, ahora dos piezas de código escriben sobre la misma memoria creyéndola suya —un fallo silencioso, no determinista, y una de las clases de vulnerabilidad más explotadas de la historia del software. La **doble liberación** corrompe directamente las estructuras internas del asignador, con consecuencias igual de arbitrarias.

Lo decisivo es que el compilador de C **no puede** detectar ninguno de los tres. El tipo `long *` no dice nada sobre quién es dueño del bloque ni durante cuánto tiempo es válido: la propiedad es una convención social escrita en comentarios y en la documentación, no en el sistema de tipos. Kernighan & Ritchie ya presentan `malloc`/`free` en *The C Programming Language* como una pareja indisociable; la disciplina la pone el programador.

## 🧩 Situación

Un servicio escrito en C atiende peticiones sin problemas durante horas y, tras dos días en producción, el sistema lo mata por consumo de memoria. El código no tiene ningún bucle que crezca: simplemente hay una ruta de error, poco frecuente, que retorna antes de llegar al `free`. Cada petición fallida se lleva unos kilobytes que nunca vuelven. Ese patrón —el `free` que se salta un `return` temprano o un `goto`— es la fuga más común de C, y es exactamente el problema que RAII (clase 132) resuelve atando la liberación al final del ámbito en lugar de a una línea concreta. Reservar, llenar, sumar y liberar `n` enteros es el mismo ciclo en miniatura, con el `free` en su sitio.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `reservado=<n> suma=<1+...+n>`
- **Regla:** reservar n enteros, llenarlos 1..n, sumar, liberar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `reservado=5 suma=15` |
| `1` | `reservado=1 suma=1` |
| `3` | `reservado=3 suma=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar(n) ; llenar 1..n ; sumar ; liberar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
arr = [0] * n  # el runtime gestiona la memoria
for i in range(n):
    arr[i] = i + 1
print(f"reservado={n} suma={sum(arr)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr: number[] = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
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
        int[] arr = new int[n];
        long suma = 0;
        for (int i = 0; i < n; i++) {
            arr[i] = i + 1;
            suma += arr[i];
        }
        System.out.println("reservado=" + n + " suma=" + suma);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int[] arr = new int[n];
long suma = 0;
for (int i = 0; i < n; i++) {
    arr[i] = i + 1;
    suma += arr[i];
}
Console.WriteLine($"reservado={n} suma={suma}");
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
	arr := make([]int, n)
	suma := 0
	for i := 0; i < n; i++ {
		arr[i] = i + 1
		suma += arr[i]
	}
	fmt.Printf("reservado=%d suma=%d\n", n, suma)
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
    let arr: Vec<i64> = (1..=n).collect(); // Vec libera al salir del ámbito
    let suma: i64 = arr.iter().sum();
    println!("reservado={n} suma={suma}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *arr = malloc(n * sizeof(long));
    long suma = 0;
    for (long i = 0; i < n; i++) {
        arr[i] = i + 1;
        suma += arr[i];
    }
    printf("reservado=%ld suma=%ld\n", n, suma);
    free(arr);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone la gestión de memoria; se calcula la suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('reservado=%d suma=%d', max(i), sum(i)) AS resultado FROM r;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$arr = array_fill(0, $n, 0);
for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $i + 1;
}
echo "reservado=$n suma=" . array_sum($arr) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Las diez implementaciones hacen lo mismo, pero solo una nombra la memoria.

En **C**, `malloc(n * sizeof(long))` es la única línea del curso en la que pides memoria explícitamente. Fíjate en `sizeof(long)`: no reservas «n enteros», reservas *bytes*, y eres tú quien traduce elementos a bytes. Si te equivocas en esa multiplicación —o si `n * sizeof(long)` desborda— reservas de menos y el bucle escribe fuera del bloque, corrompiendo el heap sin que nada te avise. El código tampoco comprueba si `malloc` devolvió `NULL`, algo que ocurre cuando no hay memoria; en código de producción esa comprobación es obligatoria. El `free(arr)` al final cierra el contrato, y está colocado *después* del `printf` porque liberar antes y luego leer `arr` sería un *use-after-free* de manual.

En **Rust**, `(1..=n).collect()` construye un `Vec<i64>` que también vive en el heap: por dentro hay una reserva idéntica a la de C. La diferencia es que el `Vec` **posee** su bloque y el compilador sabe exactamente dónde muere —al cerrarse `main`—, momento en el que inserta la llamada de liberación. No hay `free` que escribir ni que olvidar; tampoco hay recolector observando en segundo plano. Ese es el modelo de la clase 132.

En **Python**, **Java**, **C#**, **Go**, **JavaScript** y **PHP** la reserva sigue existiendo (`[0] * n`, `new int[n]`, `make([]int, n)`) pero se vuelve invisible: el runtime la sirve desde su propio heap gestionado y un recolector decide cuándo devolverla. El precio es que dejas de controlar *cuándo* ocurre la liberación —tema de la clase 131— y que cada objeto carga metadatos que en C no pagarías. En **SQL** la pregunta ni siquiera se plantea: describes un resultado y el motor decide cómo materializarlo.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Quién libera | El programador (C); el compilador en el punto de destrucción (Rust); un recolector (Java, C#, Go, Python, JS, PHP); el motor (SQL). |
| Momento de la liberación | Determinista y elegido por ti (C, Rust); no determinista (Java, C#, Go, JS); casi inmediato por conteo de referencias (CPython, PHP). |
| Coste de reservar | Búsqueda en la lista de bloques libres (C, Rust); *bump allocation* en el vivero del GC (Java, C#, Go), mucho más barata por reserva. |
| Errores posibles | Fuga, *use-after-free*, doble liberación (C); solo fugas lógicas —referencias vivas de más— en los gestionados; nada de esto en Rust seguro. |
| Qué expresa el tipo | `long *` no dice quién es el dueño (C); `Vec<T>`, `Box<T>` y `&T` lo dicen explícitamente (Rust); irrelevante en los gestionados. |

## 🧬 El concepto en la familia

La familia C —C y C++ con `new`/`delete`— comparte el modelo manual, aunque C++ lo domestica con RAII y punteros inteligentes (`unique_ptr`, `shared_ptr`) que devuelven la liberación al compilador. Objective-C recorrió el camino intermedio: conteo manual de referencias (`retain`/`release`) y luego ARC, donde el compilador inserta esas llamadas por ti. Zig mantiene el control manual pero lo hace explícito pasando el asignador como parámetro, de modo que quién reserva es visible en la firma. Rust elimina la categoría de error entera moviendo la propiedad al sistema de tipos. Y la gran mayoría del resto —JVM, .NET, Go, los dinámicos— delega en un recolector. Conviene ver la secuencia como lo que es: cuarenta años de intentos de trasladar al compilador o al runtime una obligación que C dejó enteramente en manos humanas, con resultados históricamente malos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 130
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar `free` en una ruta de error** → causa: el `free` está al final de la función, pero un `return` temprano lo salta → solución: un único punto de salida con `goto cleanup`, o mejor, mover la liberación al fin de ámbito (RAII, clase 132).
- **Usar el puntero tras liberarlo** → causa: `free` no cambia el valor del puntero, solo marca el bloque; la variable sigue apuntando a memoria que ya es de otro → solución: asignar `NULL` inmediatamente después de `free`, y verificar con AddressSanitizer (`cc -fsanitize=address`).
- **No comprobar si `malloc` devolvió `NULL`** → causa: asumir que la reserva siempre funciona → solución: comprobar el retorno antes de escribir; en el ejemplo de esta clase se omite por brevedad, no porque sea correcto.
- **Calcular mal el tamaño** → causa: escribir `malloc(n)` en lugar de `malloc(n * sizeof(long))`, o usar el `sizeof` del puntero en vez del apuntado → solución: usar el patrón `malloc(n * sizeof(*arr))`, que se mantiene correcto aunque cambie el tipo de `arr`.
- **Liberar dos veces** → causa: dos rutas del código creen ambas ser dueñas del bloque → solución: documentar y respetar un único propietario por bloque; es exactamente la regla que Rust convierte en ley del compilador.

## ❓ Preguntas frecuentes

- **¿Por qué seguir gestionando a mano en 2020s?** Por previsibilidad. Un GC introduce pausas cuyo momento no controlas; en un kernel, un driver, un motor de audio o un sistema de control, una pausa de 5 ms en el instante equivocado es un fallo funcional. El coste de la gestión manual es conocido y ocurre exactamente donde tú lo pones.
- **¿`free` devuelve la memoria al sistema operativo?** Normalmente no. La devuelve al asignador de tu proceso, que la reutilizará. Solo bloques grandes servidos por `mmap` suelen devolverse al núcleo al liberarse. Por eso ver el consumo del proceso estable tras muchos `free` es lo esperado, no un síntoma de fuga.
- **¿El GC elimina las fugas?** Elimina las fugas *por olvido*, no las lógicas. Si mantienes una referencia viva a un objeto que ya no necesitas —una caché sin límite, un listener nunca dado de baja, una colección estática que solo crece—, el recolector la considera alcanzable y no la toca. Y no gestiona en absoluto otros recursos: descriptores de archivo, sockets y conexiones a base de datos siguen requiriendo cierre explícito.
- **¿Qué es la fragmentación y por qué importa?** Tras muchos ciclos de reserva y liberación de tamaños distintos, el heap queda salpicado de huecos pequeños. Puede haber megabytes libres en total y aun así fallar una reserva de 100 KB porque ningún hueco *contiguo* es suficiente. Bryant & O'Hallaron distinguen la fragmentación interna (espacio desperdiciado dentro de un bloque, por alineación) de la externa (huecos entre bloques); es la razón por la que muchos GC modernos compactan el heap, algo que `malloc` no puede hacer porque no sabe qué punteros tuyos habría que actualizar.

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

> [⏮️ Clase 129](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 131 ⏭️](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md)
