# Clase 132 — RAII, propiedad y préstamos (Rust/C++)

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Las dos clases anteriores dejaron un dilema aparentemente cerrado: o gestionas la memoria a mano y te expones a fugas y *use-after-free*, o delegas en un recolector y aceptas pausas que no controlas. Esta clase presenta la tercera vía —la que hace que **Rust no necesite recolector**— y que consiste en un cambio de estrategia radical: en lugar de resolver el problema *en tiempo de ejecución*, se resuelve *en tiempo de compilación* codificando la propiedad en el sistema de tipos. El ejercicio es deliberadamente mínimo —prestar `n` a una función que devuelve `2n`— porque lo interesante no es lo que el código hace, sino lo que el compilador **demuestra** sobre él antes de generar una sola instrucción. El *porqué* de estudiarlo es que este modelo se ha convertido en una de las ideas más influyentes del diseño de lenguajes de la última década, y porque entenderlo cambia cómo lees también el C++ moderno: `unique_ptr`, `shared_ptr` y los destructores son la misma idea, con menos comprobación. Klabnik y Nichols dedican a esto el núcleo entero de *The Rust Programming Language*, y con razón: es el concepto sin el cual Rust no se entiende.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Enunciar las tres reglas de propiedad de Rust y explicar por qué garantizan que no haya doble liberación.
2. Distinguir un **movimiento** de una **copia** y de un **préstamo**, y predecir cuál ocurre en una asignación.
3. Explicar la regla del *borrow checker* —muchos lectores o un escritor, nunca ambos— y qué error de la clase 130 elimina cada mitad.
4. Relacionar RAII con la liberación determinista y con la gestión de recursos que no son memoria.
5. Explicar qué es un *lifetime* y por qué el compilador puede rechazar una referencia colgante sin ejecutar el programa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | RAII | Ata la vida del recurso a un ámbito, no a una línea de código |
| 2 | Propiedad y movimiento | Un solo dueño en todo momento: la doble liberación se vuelve inexpresable |
| 3 | Préstamo (`&T`, `&mut T`) | Permite usar sin poseer, que es el 90 % de lo que un programa hace |
| 4 | Reglas del *borrow checker* | Aliasing y mutación no pueden coexistir: elimina también las carreras de datos |
| 5 | *Lifetimes* | El compilador comprueba que ninguna referencia sobreviva a su dato |

## 📖 Definiciones y características

**RAII** —*Resource Acquisition Is Initialization*, el nombre que le dio Bjarne Stroustrup en C++— invierte el planteamiento de la clase 130. En lugar de escribir la liberación como una *instrucción* que hay que recordar colocar en todos los caminos de salida, se escribe como una *propiedad del tipo*: el objeto que posee el recurso lo suelta en su destructor, y el compilador garantiza que el destructor se ejecuta cuando el objeto sale de ámbito. Sea cual sea la salida —un `return` temprano, una excepción, un `break`—, el destructor corre. Ese es el detalle que resuelve la fuga por ruta de error de la clase anterior, y por qué es una idea sobre *recursos* en general y no solo sobre memoria: un candado, un archivo, una transacción, una conexión.

La **propiedad** en Rust se rige por tres reglas: cada valor tiene una variable que es su dueña; solo puede haber un dueño a la vez; cuando el dueño sale de ámbito, el valor se destruye. La segunda regla es la clave. Cuando escribes `let b = a;` con un tipo que posee memoria, Rust no copia el bloque: **mueve** la propiedad a `b` e invalida `a`. Si intentas usar `a` después, el compilador rechaza el programa. El efecto es que la doble liberación deja de ser un bug para convertirse en algo que el lenguaje no te deja escribir: nunca hay dos dueños que pudieran liberar el mismo bloque. Los tipos simples que caben en registros (`i64`, `bool`, `char`) implementan el rasgo `Copy` y se copian en lugar de moverse, porque copiarlos es trivial y no hay nada que liberar.

Pero mover en cada llamada sería insoportable: la mayor parte del tiempo solo quieres *leer* un dato. Para eso está el **préstamo**. `&n` crea una referencia: la función accede al valor sin adquirir la propiedad, y al volver, `n` sigue siendo válida y sigue perteneciendo a quien la tenía. Hay dos sabores: `&T` es un préstamo compartido de solo lectura, y `&mut T` un préstamo exclusivo que permite mutar. La regla del **borrow checker** que los gobierna es una sola frase con consecuencias enormes: *en cualquier momento puedes tener o bien cualquier número de referencias `&T`, o bien exactamente una `&mut T`, pero nunca ambas cosas*. Aliasing y mutabilidad, separados por construcción.

Esa regla no es una restricción arbitraria. Elimina de un golpe varias familias de errores. Impide que se invalide un iterador mientras se recorre —no puedes tener una referencia a un elemento del vector y a la vez mutar el vector, porque `push` podría reasignar el buffer entero—. E impide las **carreras de datos**: una carrera requiere que dos hilos accedan al mismo dato, que al menos uno escriba y que no haya sincronización; si escribir exige un préstamo exclusivo, la primera condición y la segunda no pueden darse juntas. Rust obtiene la seguridad de concurrencia como corolario de las reglas de memoria, no como un mecanismo aparte —el famoso «*fearless concurrency*», tema que reaparece en la clase 136—.

El tercer ingrediente son los **lifetimes**. Cada referencia lleva, en el sistema de tipos, una anotación —normalmente inferida y por tanto invisible— que indica durante qué región del código es válida. El compilador comprueba que ninguna referencia sobreviva al dato al que apunta, y por eso puede rechazar una función que devuelve una referencia a una variable local: sería una referencia colgante, exactamente el *use-after-free* de la clase 130, detectado sin ejecutar nada. Todo esto sucede en compilación y **desaparece** del binario: en tiempo de ejecución no queda contador, ni bit de marcado, ni comprobación. Ese es el sentido de *zero-cost abstraction*: el código generado es el mismo que escribiría un programador de C que no cometiera errores.

## 🧩 Situación

Un equipo migra un componente crítico de C++ a Rust tras una auditoría que encontró tres *use-after-free* explotables. Lo que buscan no es velocidad —el C++ ya era rápido— sino que la categoría de error deje de ser posible. Al portarlo, el compilador rechaza media docena de construcciones que en C++ compilaban sin una advertencia: una referencia guardada en una estructura que sobrevivía al dato, un puntero compartido entre dos hilos sin sincronización. Cada rechazo es un fallo de producción que no llegó a existir. Prestar `n` a `doble(&n)` es el caso más simple de ese mismo mecanismo: el compilador verifica que el préstamo termina antes que el dato, y por eso el programa es correcto por construcción, no por revisión.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** prestar n a una función que devuelve 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
prestar n (referencia) a doble(&n) ; ESCRIBIR resultado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def doble(x):
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + doble(n));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long Doble(long x) => x * 2;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
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

func doble(x int64) int64 { return x * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: &i64) -> i64 {
    *x * 2 // préstamo: se lee sin tomar la propiedad
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(&n));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(const long *x) {
    return *x * 2; /* se accede por referencia sin copiar */
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(&n));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone propiedad de memoria; se calcula el resultado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function doble($x) {
    return $x * 2;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Solo dos de las diez implementaciones escriben el `&`, y por razones opuestas.

En **Rust**, la firma `fn doble(x: &i64) -> i64` es una declaración de intenciones legible por el compilador: «recibo prestado un `i64`, no me hago dueño, solo leo». El `*x` en el cuerpo es la desreferencia explícita. En la llamada, `doble(&n)` crea el préstamo y lo termina en cuanto la función retorna, de modo que `n` sigue disponible después. Merece la pena notar que para un `i64` este préstamo es *innecesario*: `i64` es `Copy` y pasarlo por valor sería más idiomático y probablemente más rápido, porque una referencia a 8 bytes ocupa 8 bytes. Se escribe así aquí para hacer visible el mecanismo. La otra observación importante es que el binario generado por `rustc` no contiene rastro del préstamo: no hay comprobación en ejecución, no hay contador. El *borrow checker* trabajó y se fue.

En **C**, `long doble(const long *x)` parece lo mismo y no lo es. El `const` documenta la intención de no modificar, pero nada impide que otra parte del programa tenga *otro* puntero al mismo `long` y lo modifique mientras `doble` lo lee; nada impide tampoco que `x` apunte a memoria ya liberada. La sintaxis es casi idéntica a la de Rust; la garantía es inexistente. Esta pareja de líneas es el mejor resumen posible de la diferencia entre los dos lenguajes: no está en cómo se escribe, sino en qué se puede demostrar.

En **Python**, **JavaScript**, **TypeScript**, **Java**, **C#**, **Go** y **PHP** no hay nada que decidir: `doble(n)` pasa el valor y punto. Los tres modelos de memoria de esta parte del curso convergen aquí porque el dato es un entero primitivo. Si en vez de un `i64` pasáramos una lista, la diferencia reaparecería con toda su fuerza: Python y Java pasarían una referencia al mismo objeto —mutable desde dentro de la función—, Go copiaría la cabecera del *slice* pero compartiría el array subyacente, y Rust exigiría elegir explícitamente entre mover, prestar (`&`) o clonar (`.clone()`). En **SQL** la noción de propiedad de memoria no existe: el motor decide cómo materializar cada fila.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Quién decide la liberación | El compilador, en el punto de salida de ámbito (Rust, C++); un recolector (Java, C#, Go, JS); un contador de referencias (Python, PHP); el programador (C). |
| Semántica de `b = a` | Mueve e invalida `a` para tipos no `Copy` (Rust); copia superficial de la referencia (Java, C#, Python, JS, PHP); copia del valor para tipos simples y estructuras (Go, C). |
| Aliasing mutable | Prohibido por el compilador (Rust); permitido y frecuente fuente de bugs (todos los demás). |
| Coste en ejecución | Cero (Rust, C, C++ con `unique_ptr`); recolector en segundo plano (Java, C#, Go, JS); incremento/decremento de contador en cada asignación (Python, PHP). |
| Recursos no-memoria | Cerrados por el destructor automáticamente (Rust `Drop`, C++); requieren `try-with-resources`, `using`, `defer` o `with` (Java, C#, Go, Python); manual (C, PHP). |
| Coste de aprendizaje | Alto y anticipado — el compilador rechaza y hay que entender por qué (Rust); bajo al principio, con los fallos apareciendo en producción (los demás). |

## 🧬 El concepto en la familia

RAII nace en C++, donde Stroustrup ató la liberación al destructor para que las excepciones no dejaran recursos huérfanos; el C++ moderno lo lleva a su forma madura con `unique_ptr` (un único dueño, movible pero no copiable — exactamente el modelo de Rust, pero verificado solo parcialmente) y `shared_ptr` (propiedad compartida por conteo de referencias, con `weak_ptr` para romper ciclos). Rust toma esa idea y la hace obligatoria y verificable: lo que en C++ es una convención disciplinada, en Rust es un rechazo de compilación. Swift ocupa un punto intermedio con ARC, conteo de referencias insertado por el compilador, determinista pero con coste en ejecución y con ciclos que el programador debe romper a mano con `weak`. En la familia de sistemas, Zig prescinde de todo esto y apuesta por `defer` y por asignadores explícitos: liberación determinista, sin verificación. Y en el otro extremo del espectro, la familia funcional tipada —OCaml, Haskell— resuelve el aliasing mutable por la vía opuesta, eliminando la mutación en lugar de restringirla; los *linear types* y *uniqueness types* de Clean e Idris son parientes teóricos directos de la propiedad de Rust. Conviene ver estos modelos como puntos de una misma curva: cuánto trabajo mueves del tiempo de ejecución al compilador, y cuánta carga cognitiva estás dispuesto a poner sobre quien escribe.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 132
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor después de moverlo** → causa: pasar un `String` o un `Vec` por valor a una función y volver a usarlo después; la propiedad se transfirió → solución: prestarlo con `&` si solo hay que leerlo, o clonarlo explícitamente si de verdad hacen falta dos copias. El mensaje `value borrowed here after move` señala exactamente esto.
- **Prestar mutable mientras hay un préstamo compartido vivo** → causa: pedir `&mut v` mientras existe una `&v` que aún se usará más adelante → solución: reordenar el código para que los préstamos no se solapen; desde la introducción de los *non-lexical lifetimes* el compilador acepta bastante más de lo que la gente supone, porque el préstamo termina en su último uso, no al final del bloque.
- **Pelear con el *borrow checker* llenando el código de `.clone()`** → causa: usar la clonación como escape ante cada rechazo → solución: casi siempre el rechazo indica un problema real de diseño (una estructura de datos que quiere dos dueños). Replantear la propiedad, o usar deliberadamente `Rc<RefCell<T>>` cuando la propiedad compartida es lo correcto.
- **Anotar *lifetimes* a ciegas hasta que compile** → causa: tratar `'a` como ruido sintáctico → solución: leer `fn f<'a>(x: &'a T) -> &'a U` como «la referencia devuelta no vive más que la recibida». Casi siempre la anotación es una afirmación sobre el diseño, y forzarla sin entenderla esconde el error.
- **Esperar RAII donde no lo hay** → causa: suponer que un objeto en Java o Python libera su recurso al perder la referencia → solución: en esos lenguajes la liberación de memoria es diferida y la de otros recursos, manual; usar el constructo de ámbito del lenguaje (`try-with-resources`, `with`, `defer`).
- **Crear un ciclo con `Rc`** → causa: dos `Rc<T>` que se apuntan mutuamente mantienen su contador en 1 para siempre → solución: `Weak<T>` en una de las dos direcciones. Rust garantiza la ausencia de *use-after-free*, no la ausencia de fugas: filtrar memoria es seguro, y por eso `Box::leak` existe y no es `unsafe`.

## ❓ Preguntas frecuentes

- **¿RAII o GC?** No es una cuestión de cuál es mejor sino de dónde pagas. RAII y ownership pagan en compilación —tiempo de compilación largo y una curva de aprendizaje real— y no pagan nada en ejecución. El GC paga poco al escribir y paga en ejecución: pausas, memoria adicional y menos control. Para un servicio web con SLA de 200 ms, el GC es la elección obvia; para un motor de audio, un kernel o un navegador, no lo es.
- **¿Prestar copia el dato?** No: `&n` es una dirección. Para un `i64` la referencia ocupa lo mismo que el valor, así que prestar no ahorra nada; para un `Vec` de un millón de elementos, prestar cuesta 8 bytes y clonar cuesta ocho megabytes. Ese es el caso en el que el préstamo importa.
- **¿Rust es entonces incapaz de compartir datos mutables?** Puede, con mecanismos explícitos que trasladan la comprobación a ejecución: `RefCell<T>` verifica la regla de préstamos en tiempo de ejecución y entra en pánico si se viola; `Rc<T>` da propiedad compartida en un solo hilo, y `Arc<Mutex<T>>` entre hilos. Lo relevante es que compartir mutabilidad es *visible* en el tipo: quien lee la firma sabe que ahí hay algo que vigilar.
- **¿Y `unsafe`?** Existe y es necesario: alguien tiene que escribir `Vec`, y por dentro hay aritmética de punteros. `unsafe` no apaga el *borrow checker*; solo habilita unas pocas operaciones concretas —desreferenciar punteros crudos, llamar funciones `unsafe`, acceder a estáticas mutables— y traslada la obligación de la prueba del compilador al programador, dentro de un bloque acotado y auditable. El objetivo del diseño es que ese bloque sea diminuto y esté envuelto en una API segura.
- **¿Por qué C++ no da las mismas garantías si también tiene RAII?** Porque en C++ RAII es opcional y el lenguaje conserva todo lo anterior: punteros crudos, referencias que sobreviven a su objeto, copias implícitas. `unique_ptr` codifica la propiedad, pero nada impide obtener un puntero crudo con `.get()` y guardarlo más tiempo del debido. Rust no tiene esa puerta trasera fuera de `unsafe`.

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

> [⏮️ Clase 131](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 133 ⏭️](../../parte-8-como-funcionan-los-lenguajes/133-concurrencia-procesos-hilos-y-memoria-compartida/README.md)
