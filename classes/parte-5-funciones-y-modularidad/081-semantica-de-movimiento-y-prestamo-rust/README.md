# Clase 081 — Semántica de movimiento y préstamo (Rust)

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el modelo con el que Rust gestiona la memoria sin recolector de basura y sin la gestión manual de C: la **propiedad** (*ownership*), el **movimiento** (*move*) y el **préstamo** (*borrow*). La idea central es tan simple de enunciar como profunda en sus consecuencias: en Rust, cada valor tiene en todo momento un único **dueño**, y cuando el dueño sale de ámbito, el valor se libera automáticamente. Pasar un valor a una función puede **moverlo** —transferir la propiedad, tras lo cual la variable original deja de ser válida— o **prestarlo** con `&` —dar acceso temporal para leerlo sin ceder la propiedad—. Es la tercera vía entre los dos mundos que ya viste: ni la copia defensiva del paso por valor, ni la mutación libre del paso por referencia, sino un sistema donde el compilador *demuestra* que cada acceso es seguro.

Steve Klabnik y Carol Nichols dedican el capítulo 4 de *The Rust Programming Language* —disponible gratis en línea— a este modelo, y lo presentan como el rasgo que distingue a Rust de todo lo demás. Su tesis: los lenguajes tradicionales te obligan a elegir entre control (C, con memoria manual y el riesgo de *use-after-free* o doble liberación) y comodidad (Java, Python, Go, con recolector de basura que cuesta rendimiento y latencia impredecible). Rust rechaza el dilema: mueve la comprobación al *compilador*. El **verificador de préstamos** (*borrow checker*) analiza estáticamente que nunca uses un valor después de moverlo, que no haya dos referencias mutables simultáneas, y que ninguna referencia sobreviva al dato que apunta. Si el programa compila, esas familias enteras de bugs no pueden ocurrir.

El objetivo hondo es ver el movimiento y el préstamo no como sintaxis exótica, sino como una respuesta de ingeniería a una pregunta vieja: ¿quién libera esta memoria y cuándo? C responde «tú, a mano, y reza». Java responde «un recolector, cuando le parezca». Rust responde «el dueño, al final de su ámbito, y lo garantizo en compilación».

## 🧩 Situación

Tienes una cadena de texto y quieres dos cosas: medir su longitud y luego mostrarla. En un lenguaje con recolector no lo piensas dos veces: usas la variable las veces que quieras y el GC limpiará después. En C tendrías que decidir tú cuándo hacer `free`, con el riesgo de liberarla dos veces o de usarla ya liberada. En Rust el compilador te obliga a ser explícito sobre la intención: medir la longitud solo necesita *leer*, así que la **prestas** (`&s`) y la conservas; mostrarla en una función que se vuelve dueña de ella la **mueve**, y a partir de ahí el compilador no te dejará volver a usar `s` porque ya no es tuya. Esa disciplina, que al principio incomoda, es exactamente la que impide que uses por accidente un recurso que ya cediste. La situación de esta clase —prestar para leer, mover para consumir— es el «hola mundo» de la propiedad en Rust.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII)
- **Salida** (stdout): `movido=<palabra> longitud=<len>`
- **Regla:** longitud por préstamo; el texto se muestra tras moverse

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `movido=Ada longitud=3` |
| `Bo` | `movido=Bo longitud=2` |
| `hola` | `movido=hola longitud=4` |

## 📖 Definiciones y características

- **Propiedad (ownership)** — la regla de que cada valor tiene un único dueño, y que al terminar el ámbito del dueño el valor se libera automáticamente (Rust llama a eso *drop*). Klabnik y Nichols la resumen en tres reglas: cada valor tiene un dueño; solo puede haber un dueño a la vez; cuando el dueño sale de ámbito, el valor se descarta. Es la base de que Rust no necesite recolector.
- **Movimiento (move)** — pasar un valor «pesado» (como un `String`, que posee memoria en el heap) transfiere la propiedad: la variable de origen queda **invalidada** y el compilador prohíbe seguir usándola. No es una copia; es un traspaso de la responsabilidad de liberar. Evita que dos variables crean ser dueñas del mismo dato y lo liberen dos veces.
- **Préstamo (borrow)** — crear una referencia con `&` para usar un valor **sin** tomar su propiedad. El dueño sigue siendo el original; el préstamo es un acceso temporal. Un préstamo compartido `&T` permite leer; un préstamo mutable `&mut T` permite escribir, con la regla de que no pueden coexistir dos préstamos mutables (ni uno mutable con otros compartidos) al mismo tiempo.
- **`Copy` vs. `Clone`** — no todo se mueve. Los tipos simples que caben en la pila (enteros, `bool`, `char`) implementan el rasgo `Copy`: al pasarlos se **copian** en vez de moverse, así que el original sigue válido (como viste en la clase 079). Los tipos que poseen recursos del heap (`String`, `Vec`) se **mueven** por defecto; para duplicarlos de verdad hay que pedirlo explícitamente con `.clone()`, que copia también el contenido del heap.
- **Verificador de préstamos (borrow checker)** — la parte del compilador que comprueba estas reglas en tiempo de compilación: que no uses un valor movido, que las referencias no sobrevivan al dato, que el aliasing mutable sea único. Si algo viola las reglas, el programa **no compila**; no hay coste en tiempo de ejecución.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; len <- longitud(prestar w)
mostrar(mover w)
ESCRIBIR "movido=" w " longitud=" len
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

s = sys.stdin.readline().strip()
longitud = len(s)  # Python comparte la referencia (GC), no hay 'move'.
print(f"movido={s} longitud={longitud}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const s = readFileSync(0, "utf8").trim();
const longitud = s.length; // JS usa GC: la cadena sigue disponible.
console.log(`movido=${s} longitud=${longitud}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const s: string = readFileSync(0, "utf8").trim();
const longitud: number = s.length;
console.log(`movido=${s} longitud=${longitud}`);
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
        String s = br.readLine().trim();
        int longitud = s.length(); // GC: sin propiedad ni move.
        System.out.println("movido=" + s + " longitud=" + longitud);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string s = Console.In.ReadToEnd().Trim();
int longitud = s.Length; // GC: la cadena permanece.
Console.WriteLine($"movido={s} longitud={longitud}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

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
	s := strings.TrimSpace(line)
	longitud := len(s) // GC: sin propiedad explícita.
	fmt.Printf("movido=%s longitud=%d\n", s, longitud)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn longitud(s: &str) -> usize {
    s.len() // préstamo: se lee sin tomar la propiedad
}

fn mostrar(s: String) {
    // move: 'mostrar' se vuelve dueña de la cadena
    let len = s.len();
    println!("movido={s} longitud={len}");
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).unwrap();
    let s = buf.trim().to_string();
    let _ = longitud(&s); // se presta
    mostrar(s); // se mueve
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[256];
    if (scanf("%255s", s) != 1) return 1;
    /* C: gestión manual; aquí no se copia ni se mueve, se usa directamente. */
    int longitud = (int) strlen(s);
    printf("movido=%s longitud=%d\n", s, longitud);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene propiedad de memoria: opera sobre datos.
WITH palabras(s) AS (VALUES ('Ada'), ('Bo'), ('hola'))
SELECT printf('movido=%s longitud=%d', s, length(s)) AS resultado FROM palabras;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$s = trim(fgets(STDIN));
$longitud = strlen($s); // PHP usa GC por conteo de referencias.
echo "movido=$s longitud=$longitud\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "Ada"`, `esperado = "movido=Ada longitud=3"`), primero en Rust —donde el concepto es protagonista— y luego en dos lenguajes que lo resuelven sin propiedad.

**Rust — préstamo y luego movimiento.** En `main`, tras leer la entrada, `let s = buf.trim().to_string()` crea un `String` cuyo dueño es `s`; ese `String` posee memoria en el heap con los bytes `A`, `d`, `a`. La línea `let _ = longitud(&s)` **presta** la cadena: `&s` construye una referencia `&str` que la función `longitud` recibe como `s: &str`. Como es un préstamo y no un movimiento, `longitud` puede leer `s.len()` —que devuelve `3`— pero al terminar **no** libera nada ni se queda con la propiedad; `s` en `main` sigue siendo el dueño, plenamente válido. Justo después, `mostrar(s)` **mueve** la cadena: la firma `mostrar(s: String)` toma un `String` por valor, así que la propiedad se transfiere de `main` a `mostrar`. A partir de esa línea, la variable `s` de `main` queda invalidada —si intentaras usarla, el compilador lo rechazaría—. Dentro de `mostrar`, la función es ahora la dueña: calcula `len = 3`, imprime `movido=Ada longitud=3`, y al terminar su ámbito libera la cadena automáticamente (*drop*). Fíjate en el orden que impone la lógica: se **presta primero** (para medir) y se **mueve al final** (para consumir), porque después del movimiento ya no habría cadena que prestar.

**Python — sin propiedad, con recolector.** `s = sys.stdin.readline().strip()` deja `s` apuntando a la cadena `"Ada"`. No hay préstamo ni movimiento: `len(s)` lee la longitud (`3`) y `s` sigue disponible sin ceremonia alguna. El f-string `f"movido={s} longitud={3}"` produce `movido=Ada longitud=3`. La memoria de la cadena vive mientras haya referencias a ella, y el recolector de Python (conteo de referencias más un detector de ciclos) la liberará cuando ya nadie la use. El programador nunca decide *cuándo*; ese es precisamente el coste y la comodidad del GC que Rust evita.

**C — gestión manual, sin ninguno de los dos conceptos.** `scanf("%255s", s)` llena el arreglo `char s[256]` con `Ada\0`. No hay `String` con dueño ni referencia prestada: `s` es un buffer en la pila, y `strlen(s)` recorre los bytes hasta el `\0` para devolver `3`. La salida es `movido=Ada longitud=3`. Como el buffer está en la pila (no en el heap con `malloc`), aquí ni siquiera hay que liberar nada; pero si lo hubiéramos reservado dinámicamente, sería responsabilidad del programador hacer `free` en el momento correcto —ni antes (uso tras liberar) ni dos veces (doble liberación)—, exactamente los errores que el modelo de Rust vuelve imposibles. El tercer caso, `hola`, recorre lo mismo en los tres: cuatro bytes, `longitud=4`, salida `movido=hola longitud=4`. Mismo resultado, tres filosofías de memoria: propiedad comprobada (Rust), recolección automática (Python), gestión manual (C).

## 🔬 Comparación

| Lenguaje | Cómo gestiona la memoria del texto |
|---|---|
| Python | Recolector por conteo de referencias; sin propiedad ni movimiento, la cadena vive mientras se use. |
| JavaScript | Recolector traza-y-marca; la cadena permanece disponible sin gestión explícita. |
| TypeScript | Igual que JS en runtime; los tipos no cambian la gestión de memoria. |
| Java | Recolector de la JVM; las cadenas son objetos, sin propiedad ni `move`. |
| C# | Recolector del CLR; la cadena es un objeto gestionado que sobrevive mientras haya referencias. |
| Go | Recolector concurrente; sin propiedad explícita, el runtime libera lo inalcanzable. |
| Rust | **Propiedad + préstamo + movimiento**, comprobados por el *borrow checker*; sin recolector. |
| C | Gestión **manual** (`malloc`/`free`); ni copia ni movimiento automáticos, control y riesgo totales. |
| SQL | No hay propiedad de memoria del usuario; el motor opera sobre datos de las filas. |
| PHP | Recolector por conteo de referencias con detección de ciclos; sin `move`. |

La síntesis, siguiendo a Klabnik y Nichols, es que estos tres conceptos son la respuesta de Rust a un compromiso que los demás lenguajes resuelven en extremos opuestos. Los lenguajes con recolector (Python, JS, Java, C#, Go, PHP) regalan comodidad —usa el valor las veces que quieras— a cambio de un coste en tiempo de ejecución y pausas de latencia impredecibles. C regala control total a cambio de poner sobre el programador toda la responsabilidad, con el *use-after-free* y la doble liberación siempre acechando. Rust rechaza el dilema: consigue seguridad de memoria *sin* recolector moviendo la comprobación al compilador. El precio no es rendimiento en ejecución, sino una curva de aprendizaje: convencer al *borrow checker* de que tu programa es correcto.

## 🧬 El concepto en la familia

**C++** es el pariente más cercano: tiene semántica de movimiento explícita con `std::move` y *move constructors* desde C++11, además de referencias `&` y punteros inteligentes (`unique_ptr`, `shared_ptr`) que modelan propiedad. La diferencia crucial con Rust es que C++ **no** comprueba en compilación que no uses un objeto tras moverlo: hacerlo es *undefined behavior*, un bug silencioso, mientras que en Rust es un error de compilación. **Swift** gestiona la memoria con conteo automático de referencias (ARC), a medio camino entre el GC y la propiedad de Rust. **Java, Go y Python** se apoyan por completo en recolectores y no exponen el concepto de propiedad al programador. Reconocer dónde cae cada lenguaje —comprobación estática de propiedad, movimiento sin comprobar, o recolección— explica de un vistazo qué garantías te da y qué errores te deja cometer.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 081
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor tras moverlo (Rust)** → causa: pasar un `String` a una función (que lo mueve) y luego intentar usarlo de nuevo; el compilador responde con «value borrowed here after move» → solución: si necesitas seguir usándolo, **préstalo** con `&` en vez de moverlo, o clónalo con `.clone()` si de verdad necesitas dos dueños.
- **Clonar por miedo al borrow checker** → causa: sembrar `.clone()` por todas partes para evitar los errores de propiedad, pagando copias caras del heap innecesariamente → solución: preferir préstamos `&`; reservar `.clone()` para cuando realmente necesites una copia independiente.
- **Asumir movimiento en lenguajes con GC** → causa: creer que pasar una cadena a una función en Java o Python «consume» la variable → solución: recordar que allí no hay propiedad ni move; el recolector mantiene el valor vivo mientras exista cualquier referencia.
- **Confundir préstamo con copia** → causa: pensar que `&s` duplica la cadena → solución: un préstamo es solo una referencia, un puntero con reglas; no copia el dato, por eso es barato y por eso el dueño no cambia.

## ❓ Preguntas frecuentes

- **¿Por qué Rust mueve en vez de copiar?** Para garantizar un único dueño responsable de liberar el recurso, y así descartar memoria de forma determinista sin recolector y sin el riesgo de doble liberación o *use-after-free*. Copiar un `String` grande sería caro; mover solo transfiere la propiedad del puntero al heap.
- **¿Un préstamo copia el dato?** No. Un préstamo (`&s`) es una referencia: un puntero con reglas de seguridad verificadas por el compilador. No duplica el contenido; da acceso temporal mientras el dueño conserva la propiedad.
- **¿Los enteros también se mueven en Rust?** No: los tipos simples que implementan `Copy` (enteros, `bool`, `char`, `f64`...) se **copian** al pasarse, así que la variable original sigue válida. El movimiento aplica a los tipos que poseen recursos del heap, como `String` o `Vec`, que no son `Copy` por defecto.
- **¿Rust es más lento por todas estas comprobaciones?** No en ejecución: el *borrow checker* trabaja solo en tiempo de compilación y no deja ningún rastro en el binario. La seguridad de memoria de Rust es de coste cero en runtime; lo que cuesta es el tiempo del programador aprendiendo a satisfacer al compilador.

## 🔗 Referencias

**Libros de la parte:**

- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/), cap. 4 «Understanding Ownership» (4.1 Ownership, 4.2 References and Borrowing).
- R. W. Sebesta — *Concepts of Programming Languages* (11ª ed., Pearson), cap. 6 sobre gestión de memoria y tipos, cap. 9 sobre paso de parámetros.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. sobre gestión de recursos.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre gestión de memoria y recolección.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley); ítems sobre el recolector y liberación de recursos.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley); recolección de basura.
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), §7.8.5 sobre `malloc`/`free`.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 080](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 082 ⏭️](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md)
